from setuptools import find_packages
from setuptools import setup

setup(
    name="markdown-mermaid-to-images",
    version="0.1.0 ",
    description="Exports mermaid diagrams in Markdown documents as images.",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    author="hmajid2301",
    author_email="hmajid2301@gmail.com",
    keywords="markdown,mermaid,exporter",
    license="Apache License",
    url="https://gitlab.com/hmajid2301/markdown-mermaid-to-images.git",
    python_requires="~=3.6",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    zip_safe=False,
    include_package_data=True,
    install_requires=["click>=7.0"],
    entry_points={"console_scripts": ["markdown_mermaid_to_images = markdown_mermaid_to_images.cli:cli"]},
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
