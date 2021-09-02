#!/bin/sh
rm -rf .eggs dist build
python3 setup.py py2app
unzip dist/cuteplayer.app/Contents/Resources/lib/python39.zip -d dist/cuteplayer.app/Contents/Resources/lib/python39
rm dist/cuteplayer.app/Contents/Resources/lib/python39.zip
mv dist/cuteplayer.app/Contents/Resources/lib/python39 dist/cuteplayer.app/Contents/Resources/lib/python39.zip
