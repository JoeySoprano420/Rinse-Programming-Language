from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rinse-programming-language",
    version="0.1.0",
    author="JoeySoprano420",
    author_email="",
    description="The Rinse Programming Language - A philosophically rich language with dodecagrammatic AST",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoeySoprano420/Rinse-Programming-Language",
    packages=["rinse"],
    package_data={
        "rinse": ["*.py"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Compilers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "rinsec=rinse.rinsec:main",
        ],
    },
    include_package_data=True,
)