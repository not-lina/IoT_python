from setuptools import find_packages, setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="iot_gen_cnt4144",
    version="0.0.1",
    author="Lina Zhukov",
    author_email="pzhuk001@fiu.edu",
    description="assignment 7",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/not-lina/IoT_python",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'markdown',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
