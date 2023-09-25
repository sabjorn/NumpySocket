import setuptools

setuptools.setup(
    name="numpysocket",
    version="1.0.1",
    description="Socket.Socket Subclass for Sending Numpy Arrays",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    author="Steven A. Bjornson",
    author_email="info@sabjorn.net",
    url="https://github.com/sabjorn/numpysocket",
    packages=["numpysocket"],
    install_requires=["numpy"],
    extras_require={
        "dev": [
            "pre-commit",
        ],
    },
    license="MIT License",
    zip_safe=False,
    keywords="",
    classifiers=[""],
)
