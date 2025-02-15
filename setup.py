from setuptools import setup, find_packages

setup(
    name="markdown-to-diagrams",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    install_requires=[
        "click",  # for CLI interface
        "markdown",  # for markdown parsing
        "openai",  # for LLM interaction
        "graphviz",  # for diagram generation
    ],
    entry_points={
        "console_scripts": [
            "md2diagram=markdown_to_diagrams.cli:main",
        ],
    },
    author="xiaowenz",
    description="A CLI tool to generate diagrams from markdown files using LLM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
)