import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airflow-grpc",
    version="0.0.4",
    author="Joseph Yin",
    author_email="josephyin@outlook.com",
    description="airflow grpc operator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/josephyin/airflow_grpc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)