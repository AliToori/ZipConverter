#!usr/bin/env python3
"""
    AMZBot
    Author: Ali Toori
    Website: https://botflocks.com

"""
import os
import time
import pickle

import gspread
import ntplib
import random
import schedule
import pyfiglet
from datetime import datetime, timedelta
import pandas as pd
import logging.config
from time import sleep
from pathlib import Path
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from multiprocessing import freeze_support
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import zipfile
import shutil

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',  # colored output
            # --> %(log_color)s is very important, that's what colors the line
            'format': '[%(asctime)s] %(log_color)s[%(message)s]',
            'log_colors': {
                'DEBUG': 'green',
                'INFO': 'cyan',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
        'simple': {
                'format': '[%(asctime)s] [%(message)s]',
            },
    },
    "handlers": {
        "console": {
            "class": "colorlog.StreamHandler",
            "level": "INFO",
            "formatter": "colored",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": "AliTestingLab_logs.log"
        },
    },
    "root": {"level": "INFO",
             "handlers": ["console", "file"]
             }
})
LOGGER = logging.getLogger()

def enable_cmd_colors():
    # Enables Windows New ANSI Support for Colored Printing on CMD
    from sys import platform
    if platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


freeze_support()
enable_cmd_colors()
# Print ASCII Art
print('************************************************************************\n')
pyfiglet.print_figlet('____________                   AliZipConverter ____________\n', colors='RED')
print('Author: Ali Toori, Bot Developer\n'
      'Website: https://botflocks.com/\nLinkedIn: https://www.linkedin.com/in/alitoori/\n************************************************************************')

PROJECT_FOLDER = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = Path(PROJECT_FOLDER)


# Returns all files in a directory by file .extension
def get_files_by_extension(files_directory, file_extension):
    files = []
    LOGGER.info(f'Listing {file_extension} files in directory: {files_directory}')
    # Lists all the .extension files in directory and sub-directories
    list_of_file_list = [[os.path.join(root, file) for file in files if file.endswith(file_extension)] for root, dirs, files in os.walk(files_directory)]
    [[files.append(f) for f in file_list] for file_list in list_of_file_list if len(file_list) > 0]
    return files


# Delete files in a directory by file .extension
def delete_files_by_extension(files_directory, file_extension):
    LOGGER.info(f'Deleting {file_extension} files in directory: {files_directory}')
    # get all the files in directory and sub-directories
    file_list = get_files_by_extension(files_directory, file_extension)
    [(os.remove(f), LOGGER.info(f'Removing file: {f}')) for f in file_list]
    LOGGER.info(f'All {file_extension} files have been deleted in directory: {files_directory}')


# Edits Python source code files in a directory
def unzip_directory_files(files_directory, directory_to_extract_to):
    PROJECT_FOLDER = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = Path(PROJECT_FOLDER)
    LOGGER.info(f'Unzipping files from the directory: {files_directory}')
    LOGGER.info(f'Unzipping files to the directory: {directory_to_extract_to}')
    # Lists all the files in a directory
    file_list = [str(PROJECT_ROOT / f'AliMehdi/Delivered/{f}') for f in os.listdir(files_directory) if os.path.isfile(str(PROJECT_ROOT / f'AliMehdi/Delivered/{f}'))]
    print(file_list)
    [unzip_file(path_to_zip_file=f, directory_to_extract_to=directory_to_extract_to) for f in file_list]
    LOGGER.info(f'All files have been unzipped')


# Unzips file to a directory
def unzip_file(path_to_zip_file, directory_to_extract_to):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_file:
        zip_file.extractall(directory_to_extract_to)


# Extracts ZipFile to a directory
def zip_directory_files(files_directory):
    LOGGER.info(f'Zipping files from the directory: {files_directory}: to: {files_directory} ')
    # Lists all the sub-directories in directory
    directory_list = [dirs for root, dirs, files in os.walk(files_directory)]
    directory_list = [(str(PROJECT_ROOT / f'AliMehdi/Delivered/{dirs}'), dirs) for dirs in directory_list[0]]
    [shutil.make_archive(directory[0], 'zip', directory[0]) for directory in directory_list]
    LOGGER.info(f'All files have been zipped')


directory_mehdi_milestion = str(PROJECT_ROOT / "AliMehdi/Milestones_Completed_64_URLs/")
directory_mehdi_upcoming = str(PROJECT_ROOT / "AliMehdi/UpComing/")
delete_files_by_extension(files_directory=directory_mehdi_upcoming, file_extension=".log")
