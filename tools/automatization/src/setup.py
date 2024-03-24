import setuptools


setuptools.setup(
    name="automatization",
    scripts=["python -m oss"],
    version="0.1.0",
    author="iris GmbH",
    author_email="mail@irisgmbh.de",
    description="Scripts related toLicense_Compliance",
    long_description=open('../README.md').read(),
    url="git@github.com:ParianGol/pago-package-analysis.git",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CLOSED",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

