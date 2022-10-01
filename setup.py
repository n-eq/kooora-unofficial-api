import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kooora",
    version="1.2",
    author="Nabil Elqatib",
    author_email="nabilelqatib@gmail.com",
    description="An unofficial Kooora API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/n-eq/kooora-unofficial-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
)

