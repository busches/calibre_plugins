#!/usr/bin/python
# -*- coding: utf-8 -*-

__license__   = 'GPL v3'
__copyright__ = '2022, Grant Drake based on code from JimmXinu'

'''
Creates an uncompressed zip file for the plugin.
Plugin zips are uncompressed so to not negatively impact calibre load times.

All subfolders of the plugin folder will be included, unless prefixed with '.'
i.e. .build and .tx will not be included in the zip.

Command line usage (from plugin subfolder):
    python ..\common\build.py <plugin zip name>
e.g. 
    python ..\common\build.py "My Plugin.zip"
'''

import os, zipfile, sys
from glob import glob
from six import text_type as unicode

def addFolderToZip(myZipFile,folder,exclude=[]):
    folder = unicode(folder) #convert path to ascii for ZipFile Method
    excludelist=[]
    for ex in exclude:
        excludelist.extend(glob(folder+"/"+ex))
    for file in glob(folder+"/*"):
        if file in excludelist:
            continue
        if os.path.isfile(file):
            myZipFile.write(file, file)
        elif os.path.isdir(file):
            addFolderToZip(myZipFile,file,exclude=exclude)

def createZipFile(filename,mode,files,exclude=[]):
    myZipFile = zipfile.ZipFile( filename, mode, zipfile.ZIP_STORED ) # Open the zip file for writing
    excludelist=[]
    for ex in exclude:
        excludelist.extend(glob(ex))
    for file in files:
        if file in excludelist:
            continue
        file = unicode(file) #convert path to ascii for ZipFile Method
        if os.path.isfile(file):
            (filepath, filename) = os.path.split(file)
            myZipFile.write(file, filename)
        if os.path.isdir(file):
            addFolderToZip(myZipFile,file,exclude=exclude)
    myZipFile.close()
    return (1,filename)

def adjustImportsIfExists(filename, pluginName):
    '''
    Replace this:
        from common_menus import xxx
    with this:
        from calibre_plugins.<pluginName>.common_menus import xxx
    '''
    if not os.path.exists(filename):
        return
    with open(filename, 'r') as file:
        content = file.read()
        newContent = content.replace('from common_', 'from calibre_plugins.'+pluginName+'.common_')
    with open(filename, 'w') as file:
        file.write(newContent)

def adjustCommonImports():
    # Get the name of the current directory as the plugin name
    pluginName = os.path.split(os.getcwd())[1]
    # Add to this list if additional common files are added with interdependencies between them
    adjustImportsIfExists('common_dialogs.py', pluginName)
    adjustImportsIfExists('common_menus.py', pluginName)
    adjustImportsIfExists('common_widgets.py', pluginName)

def getPluginSubfolders():
    cwd = os.getcwd()
    folders = []
    for subfolder in os.listdir(cwd):
        subfolderPath = os.path.join(cwd, subfolder)
        if os.path.isdir(subfolderPath):
            # Filter out our special development folders like .build and .tx
            if not subfolder.startswith('.'):
                folders.append(subfolder)
    return folders

if __name__=="__main__":
    
    filename=sys.argv[1]

    files=getPluginSubfolders()
    
    exclude=['*.pyc','*~','*.xcf','build.py','*.po','*.pot']
    files.extend(glob('*.py'))
    files.extend(glob('*.md'))
    files.extend(glob('*.html'))
    files.extend(glob('*.cmd'))
    files.extend(glob('plugin-import-name-*.txt'))
    adjustCommonImports()
    createZipFile(filename, "w", files, exclude=exclude)
