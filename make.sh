#!/bin/sh
rm -rf .eggs dist build
python3 setup.py py2app
