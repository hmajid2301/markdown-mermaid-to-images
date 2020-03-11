# -*- coding: utf-8 -*-
r"""Exports mermaid diagrams in Markdown documents as images.

Example:
    ::

        $ pip install -e .

.. _Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html

"""

import io
import logging
import os
import subprocess
import sys
import uuid
from pathlib import Path
from shutil import which

import click
import panflute
import pypandoc

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--file",
    "-m",
    type=click.Path(exists=True),
    help="Path to markdown file, where the mermaid code blocks will be converted to images.",
)
@click.option(
    "--folder",
    "-f",
    type=click.Path(exists=True),
    help="Path to folder where we will convert all markdown mermaid code blocks to images.",
)
@click.option(
    "--ignore",
    "-i",
    type=click.Path(exists=True),
    multiple=True,
    help="Path to folder to ignore, markdown files in this folder will not be converted.",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(exists=True),
    required=True,
    help="Path to folder where to save the new markdown files.",
)
@click.option(
    "--log-level",
    "-l",
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "ERROR"]),
    help="Log level for the script.",
)
def cli(file, folder, ignore, output, log_level):
    """Exports mermaid diagrams in Markdown documents as images.."""
    logger.setLevel(log_level)
    markdown_files = get_markdown_file_paths(file, folder, ignore)
    install_mermaid_cli()
    convert_markdown(markdown_files, output)


def get_markdown_file_paths(file, folder, ignore_paths):
    """Gets all the paths to the local markdown article. Either file or folder must be set. If the file is in the
    ignore path it will not convert markdown to .

    Args:
        file (str): Path to file.
        folder (str): Path to folder.
        ignore_paths (tuple): A list of paths to ignore markdown files in.

    Returns:
        dict: key is the title of the article and value is details.

    """
    logger.info("Getting markdown files.")
    article_paths = []
    if not file and not folder:
        logger.error("File and folder cannot be both be empty.")
        sys.exit(1)
    elif folder:
        for path in Path(folder).rglob("*.md"):
            ignore = should_file_be_ignored(ignore_paths, path)

            if not ignore:
                article_paths.append(path)
    else:
        article_paths = [file]
    return article_paths


def should_file_be_ignored(ignore_paths, path):
    """Checks if file should be ignored or not, based on what list of files/folders
    the user has passed as input.

    Args:
        ignore_paths (tuple): A list of paths to ignore markdown files in.
        path (str): Path to markdown file.

    Returns:
        bool: True if we should ignore the file and it will not be uploaded.

    """
    ignore = False
    for path_to_ignore in ignore_paths:
        normalised_ignore_path = os.path.normpath(path_to_ignore)
        if os.path.commonpath([path_to_ignore, path]) == normalised_ignore_path:
            ignore = True
            break

    return ignore


def install_mermaid_cli():
    """Checks if mermaid-cli (mmdc) is installed locally, if not tries to install it. Using "npm install".
    If it fails we will throw an error and quit.

    """
    exists = which("mmdc") is not None
    node_mermaid_path = "./node_modules/.bin/mmdc"
    exists = exists or os.path.exists(node_mermaid_path)

    if not exists:
        logger.info("Installing mermaid-cli.")
        try:
            subprocess.check_output(["npm install"], shell=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install mermaid-cli, using 'npm install'. Check 'node and npm' are installed. {e}")
            sys.exit(1)


def convert_markdown(markdown_files, output):
    """Converts markdown file's mermaid code blocks to image blocks. It does this by:

    * Convert the markdown file to JSON, which include various details such as styling
    * Then find all mermaid code blocks
        * Save the code block to `input.mmd`
        * Use mermaid-cli to export `input.mmd` to a png file
    * Finally replace all code blocks with the image blocks referencing the new image
    * Convert JSON to markdown
    * Save new markdown file

    Where a mermaid code block looks something like:
    ..

        ```mermaid
            graph LR
            A --> B
        ```

    Args:
        markdown_files (:obj:`list` of :obj:`str`): List of paths of the markdown files, we will parse/convert.
        output (str): Path to the output folder where the new markdown files will be saved.

    """
    for markdown_file in markdown_files:
        logger.info(f"Exporting {markdown_file} mermaid code blocks to images.")
        doc = convert_markdown_to_json(markdown_file)
        try:
            doc = panflute.run_filter(export_mermaid_blocks, doc=doc, output=output)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to convert mermaid code block to image. Skiping file. {e}")
            sys.exit(1)
        except OSError as e:
            logger.error(f"Failed to open/create `input.mmd`, check file permissions. Skipping file. {e}")
            sys.exit(1)

        file_name = os.path.basename(markdown_file)
        new_file_name = os.path.join(output, file_name)
        replace_mermaid_blocks_with_images(doc)
        save_new_file(doc, new_file_name)


def convert_markdown_to_json(markdown_file):
    """Converts our markdown file into JSON, which becomes a list of elements.
    We also create an empty dict, where we will store all the code blocks
    we will need to replace with images.

    Where the JSON data looks like:

    ..
        data
        '{"blocks":[{"t":"Para","c":[{"t":"Str","c":"title:"},{"t":"Space"},{"t":"Str","c":"Provisioning"},{"t":"Space"},{"t":"Str","c":"API"},{"t":"Space"},{"t":"Str","c":"LLD"}]},{"t":"Header","c":[1,["low-level-design",[],[]],[{"t":"Str","c":"Low"},{"t":"Space"}}}'

    ..
        doc.content.list
            00: Para(Str(title:) Space Str(Provisioning) Space Str(API) Space Str(LLD))
            01: Header(Str(Low) Space Str(Level) Space Str(Design); level=1, identifier='low-level-design')
            ...
            12: CodeBlock(graph LR;\n    A--> B; classes=['mermaid'])

    Args:
        markdown_file (str): List of paths of the markdown files, we will parse/convert.

    Return:
        panflute.Doc: Pandoc document container.

    """
    try:
        data = pypandoc.convert_file(str(markdown_file), "json")
    except OSError as e:
        logger.error(f"Pandoc is not installed on the host machine. {e}")
        sys.exit(1)

    doc = panflute.load(io.StringIO(data))
    doc.mermaid = {}
    return doc


def export_mermaid_blocks(elem, doc, output):
    """This function is called for every element in the content list. For every element we check if it's a mermaid
    code block. If it is a mermaid code block:

    * Save the mermaid code to a `input.mmd`
    * Export `input.mmd` to an randomly named image `npm run export_image -- -i input.mmd -o random_name.png`
    * Store where the index of the mermaid block in the content list so we can later replace it with an image.

    The reason we don't replace the code block with an image here is because panflute expects a "Block" object
    to be returned. Hence we store where the code block is, so we can replace it later.

    Args:
        element (panflute.elements.x): An element in the markdown file, i.e. `panflute.elements.CodeBlock`.
        doc (panflute.Doc): Pandoc document container, has a mermaid attribute, where we store code block \
            index and image path.
        output (str): Path to the output folder where the new markdown files will be saved.

    """
    if isinstance(elem, panflute.CodeBlock) and "mermaid" in elem.classes:
        with open("input.mmd", "w+") as tmp:
            tmp.write(elem.text)

        output_name = f"{uuid.uuid4().hex}.png"
        output_path = os.path.join(output, output_name)

        puppeteer = ""
        if os.path.isfile("/usr/bin/chromium-browser"):
            puppeteer = "-p /data/puppeteer.json"

        mmdc = "mmdc"
        mmdc_path = os.path.join(os.getcwd(), "node_modules", ".bin", "mmdc")
        if os.path.isfile(mmdc_path):
            mmdc = "npm run export_image --"

        command = [f"{mmdc} -i input.mmd -o {output_path} {puppeteer}"]
        mermaid_output = subprocess.check_output(command, shell=True)
        logger.info(mermaid_output)
        os.remove("input.mmd")
        doc.mermaid[elem.index] = output_name


def replace_mermaid_blocks_with_images(doc):
    """Replaces all mermaid code blocks with image blocks. Then saves the markdown content as a new file.

    Args:
        doc (panflute.Doc): Pandoc document container, has a mermaid attribute, where the  code block \
            index and image path are stored.

    """
    logger.info("Replacing mermaid code blocks with image blocks.")
    for mermaid_block_index, image_path in doc.mermaid.items():
        logger.debug(f"Replacing mermaid block {doc.content.list[mermaid_block_index]}.")
        image_element = panflute.Para(panflute.Image(panflute.Str("Image"), url=image_path))
        doc.content.list[mermaid_block_index] = image_element


def save_new_file(doc, new_file_name):
    """Saves the new markdown content to a file.

    Args:
        doc (panflute.Doc): Pandoc document container, has a mermaid attribute, where the  code block \
            index and image path are stored.
        new_file_name (str): Path where to save the new markdown file.

    """
    logger.info(f"Saving new file to {new_file_name}.")
    with io.StringIO() as temp_file:
        panflute.dump(doc, temp_file)
        contents = temp_file.getvalue()

    try:
        pypandoc.convert_text(contents, "markdown", "json", outputfile=new_file_name)
    except OSError as e:
        logger.error(f"Failed to save file, check permissions. {e}.")
        sys.exit(1)


if __name__ == "__main__":
    cli(sys.argv[1:])
