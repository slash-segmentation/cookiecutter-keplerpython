#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Repackage files in src as kar file
"""
import sys
import os
from zipfile import ZipFile
package_dir = '{{cookiecutter.repo_name}}'

xmlfile = package_dir + '.urn.lsid.kepler-project.org.ns..70097.362.157.xml'

manifest = os.path.join('META-INF', 'MANIFEST.MF')

myzip = ZipFile(os.path.join('src',package_dir+'.kar'),'w')
myzip.write(os.path.join('src', xmlfile), xmlfile)
myzip.write(os.path.join('src', manifest), manifest)
myzip.close()

os.remove(os.path.join('src', xmlfile))

os.remove(os.path.join('src', manifest))

os.rmdir(os.path.join('src', 'META-INF'))

