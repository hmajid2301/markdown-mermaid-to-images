.. image:: https://gitlab.com/hmajid2301/markdown-mermaid-to-images/badges/master/pipeline.svg
   :target: https://gitlab.com/hmajid2301/markdown-mermaid-to-images
   :alt: Pipeline Status

.. image:: https://gitlab.com/hmajid2301/markdown-mermaid-to-images/badges/master/coverage.svg
   :target: https://gitlab.com/hmajid2301/markdown-mermaid-to-images
   :alt: Coverage

.. image:: https://img.shields.io/pypi/l/markdown-mermaid-to-images.svg
   :target: https://pypi.org/project/markdown-mermaid-to-images/
   :alt: PyPI Project License

.. image:: https://img.shields.io/pypi/v/markdown-mermaid-to-images.svg
   :target: https://pypi.org/project/markdown-mermaid-to-images/
   :alt: PyPI Project Version

markdown-mermaid-to-images
==========================

A CLI tool for publishing markdown articles to dev.to. The tool will also update articles if they already exist
on dev.to. It matches articles based on title in the frontmatter. 

> Info: You will need to have `pandoc preinstalled <https://pandoc.org/installing.html>_` for this script to work correctly. Or you can use the Docker image instead.

Usage
-----
.. code-block:: bash

  pip install markdown-mermaid-to-images
  markdown_mermaid_to_images --help

Usage: markdown_mermaid_to_images [OPTIONS]

  Exports mermaid diagrams in Markdown documents as images.

Options:
  -m, --file PATH                 Path to markdown file, where the mermaid
                                  code blocks will be converted to images.
  -f, --folder PATH               Path to folder where we will convert all
                                  markdown mermaid code blocks to images.
  -i, --ignore PATH               Path to folder to ignore, markdown files in
                                  this folder will not be converted.
  -o, --output PATH               Path to folder where to save the new
                                  markdown files.  [required]
  -l, --log-level                 [DEBUG|INFO|ERROR]
                                  Log level for the script.
  --help                          Show this message and exit.

.. code-block:: bash

    $ markdown_mermaid_to_images -f tests/data -o tests/data/output/ -i tests/data/another_folder

Docker Image
============

You can also use the Docker image that comes with all the dependencies preinstalled. In this example
you can find the output in `tests/data/output` on your host machine.

.. code-block:: bash

    $ docker run -v ${PWD}/tests/data/another_folder:/data/input -v ${PWD}/tests/data/output:/data/output test

Example Markdown File
---------------------

Where an example markdown file may look something like this. The meramid code blocks
must be surrounded by three ` and have the class ``mermaid``.

.. code-block:: 

  ## Introduction

  Example Document

  ## Heading

  ```mermaid
  %% Image: image_name
  graph LR;
    A --> B;
  ```

  > INFO: Info

  ```mermaid
  graph LR;
    A --> B
    B --> C
    subgraph 1;
    subgraph 2;
    C --> D;
    end
    end;
  ```

This will then get converted into a file that looks like

.. code-block:: 

  Introduction
  ------------

  Example Document

  Heading
  -------

  ![Image](image_name.png)

  > INFO: Info

  ![Image](7d2490309c1c4bf48069dd7399944ff4.png)

GitLab CI
---------

You can use also use this in your CI/CD with the provided Docker image. Below is an example ``.gitlab-ci.yml`` file,
you may wish to use or include. The advantage of this is you can publish your aritcles using CI/CD.

.. code-block:: yaml

  stages:
    - pre-publish

  convert-mermaid:markdown:
    image: registry.gitlab.com/hmajid2301/markdown-mermaid-to-images
    stage: pre-publish
    script:
      - markdown_mermaid_to_images --folder tests/data --ignore tests/data/another_folder --output tests/data/output

Setup Development Environment
-----------------------------

.. code-block:: bash

  git clone git@gitlab.com:hmajid2301/markdown-mermaid-to-images.git
  cd markdown-mermaid-to-images
  pip install tox
  make install-venv
  source .venv/bin/activate
  make install-dev

Changelog
---------

You can find the `changelog here <https://gitlab.com/hmajid2301/markdown-mermaid-to-images/blob/master/CHANGELOG.md>`_.

Appendix
--------

Docker Image `inspired by sc250024 <https://github.com/sc250024/docker-mermaid-cli>`_.
