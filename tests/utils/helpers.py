import glob
import io
import os

import panflute
import pypandoc


class Helpers:
    @classmethod
    def compare_and_remove_files_in_output(cls):
        files = glob.glob("tests/data/output/*")
        for file_name in files:
            if file_name != ".gitkeep":
                if ".md" in file_name:
                    expected_file = os.path.join("tests/data/expected", os.path.basename(file_name))
                    cls.compare_markdown_files(current=file_name, expected=expected_file)
                os.remove(file_name)

    @classmethod
    def compare_markdown_files(cls, current, expected):
        data = pypandoc.convert_file(current, "json")
        current_doc = panflute.load(io.StringIO(data))
        data = pypandoc.convert_file(expected, "json")
        expected_doc = panflute.load(io.StringIO(data))
        panflute.run_filter(cls._compared_markdown_elements, doc=current_doc, expected=expected_doc)

    @staticmethod
    def _compared_markdown_elements(elem, doc, expected):
        if elem.index:
            current_elem = doc.content.list[elem.index]
            expected_elem = expected.content.list[elem.index]
            if isinstance(current_elem, panflute.CodeBlock) and "mermaid" in elem.classes:
                assert isinstance(expected_elem, panflute.Image)
            else:
                assert type(current_elem) == type(expected_elem)
