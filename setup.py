from setuptools import setup, find_packages

setup(
    name="cipherloom",
    version="0.1.0",
    author="Vihaan Mathur",
    author_email="vihaan.mathur3141@gmail.com",
    url="https://github.com/Vihaan314/Cipherloom",
    description="A collection of classical cipher implementations and utilities",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages = find_packages(),
    python_requires=">=3.9",
    install_requires=["numpy", "Parametrized"],
)
