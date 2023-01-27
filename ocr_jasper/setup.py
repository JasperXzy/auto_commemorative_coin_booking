#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/1/17
# @Author  : JasperXzy
# @Site    :
# @File    : setup.py
# @Software: PyCharm
# @Description:

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as description:
    long_description = description.read()

setup(
    name="ocr_jasper",
    version='1.0',
    author="JasperXzy",
    description="Jasper_OCR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where='.', exclude=(), include=('*',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy', 'onnxruntime', 'Pillow', 'opencv-python-headless'],
    python_requires='<3.11',
    include_package_data=True,
    install_package_data=True,
)
