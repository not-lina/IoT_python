import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iot_gen_cnt4144",
    version="0.0.1",
    author="Lina Zhukov",
    author_email="pzhuk001@fiu.edu",
    description="assignment 7",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/not-lina/IoT_python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
