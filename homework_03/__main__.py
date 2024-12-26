import sys
import os

PACKAGE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.dirname(PACKAGE_DIR))

from homework_03.view import menu

file_path = PACKAGE_DIR + '/users.json'

menu(file_path)