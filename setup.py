import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kooora",
    version="0.1",
    author="Nabil Elqatib",
    author_email="nabilelqatib@gmail.com",
    description="An unofficial Kooora API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marrakchino/kooora-unofficial-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires='>=3.5',
)

