import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="elasticroute",
    version="1.0.0rc1",
    author="Detrack",
    author_email="chester@detack.com",
    description="Free, intelligent routing for your logistics – now on Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/detrack/elasticroute-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
    ]
)
