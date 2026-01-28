from setuptools import setup, find_packages

with open("requirements.txt","r") as f:
    requirements=f.read().splitlines()

setup(
    name="mlops_project1",
    version="0.1.0",
    author="Abhay Parekh",
    author_email="",
    description="MLOps Project 1",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.6",
)