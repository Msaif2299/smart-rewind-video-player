"""
CODE SOURCE: "https://stackoverflow.com/questions/73849342/packing-images-together-with-the-main-file-with-pyinstaller-onefile-problem"
"""

from os import path
import sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)) + "/../assets/")
    return path.join(base_path, relative_path)