import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="keywordextraction", 
    version="0.1",
    author="Klaus Lippert",
    author_email="",
    description="keyword extraction using a simple dictionary lookup approach",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/klauslippert/keyword_extraction",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas >= 1",
        ]
)
