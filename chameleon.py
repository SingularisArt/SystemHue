#!/bin/python3

import argparse
import yaml
import os
import subprocess
from os.path import expanduser
from shutil import copyfile
from bs4 import BeautifulSoup
from whichcraft import which
from shutil import which

#  _   _ _   _ _ _ _   _           
# | | | | |_(_) (_) |_(_) ___  ___ 
# | | | | __| | | | __| |/ _ \/ __|
# | |_| | |_| | | | |_| |  __/\__ \
#  \___/ \__|_|_|_|\__|_|\___||___/

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_status(status, program):
    if(status == 0):
        print(bcolors.OKGREEN + "⚡"+bcolors.ENDC+bcolors.OKBLUE+" Themed "+program + bcolors.ENDC)
    elif(status == 1):
        print(bcolors.FAIL + "X"+bcolors.ENDC+bcolors.WARNING+" Failed to theme "+program + bcolors.ENDC)
    elif(status == 2):
        print(bcolors.FAIL + "X"+bcolors.ENDC+bcolors.WARNING+" User hook "+program + " failed"+bcolors.ENDC)
    elif(status == 3):
        print(bcolors.OKGREEN + "⚡"+bcolors.ENDC+bcolors.OKBLUE+" User hook "+program + " succeeded"+bcolors.ENDC)

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    return which(name) is not None

#   ____             __ _       
#  / ___|___  _ __  / _(_) __ _ 
# | |   / _ \| '_ \| |_| |/ _` |
# | |__| (_) | | | |  _| | (_| |
#  \____\___/|_| |_|_| |_|\__, |
#                         |___/ 

# get home directory
home = expanduser("~")

# get config path
config_dir = home + '/.config/chameleon'
config_path = home + '/.config/chameleon/config.yaml'

# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Chameleon Arguments')
    parser.add_argument('--theme', '-t', metavar='theme', type=str, nargs='?', help='a color scheme name to use as a theme')
    parser.add_argument('--image', '-i', metavar='image', type=str, nargs='?', help='an image file to use as a theme')
    args = parser.parse_args()
    return args

# Parse user config file
def parse_yaml():
    with open(config_path, mode='r') as file:
        file_dict = yaml.full_load(file)
        file.close()
    return file_dict

# Print keys from a dictionary
def print_keys(dictionary):
    for key in dictionary:
        print(key)
        if isinstance(dictionary[key], dict):
            print_keys(dictionary[key])


#  _____ _                    _             
# |_   _| |__   ___ _ __ ___ (_)_ __   __ _ 
#   | | | '_ \ / _ \ '_ ` _ \| | '_ \ / _` |
#   | | | | | |  __/ | | | | | | | | | (_| |
#   |_| |_| |_|\___|_| |_| |_|_|_| |_|\__, |
#                                     |___/ 

# Detects and runs hooks set by user
def user_hooks(config):
    # if the user has defined hooks
    if("hooks" in config):
        # iterate through the hooks
        for value in config["hooks"].items():
            # If the user has a simple command to run
            if(type(value[1]) == str):
                #  print("single command found")
                try:
                    arglist = value[1].split(' ')
                    p = subprocess.Popen(arglist)
                    p.wait()
                except:
                    print_status(2, value[0])
                    return
            # User has specified options for the hook
            elif(type(value[1]) == dict):
                path = value[1].get('directory', './')
                arglist = value[1].get('command').split(' ')
                try:
                    p = subprocess.Popen(arglist, cwd=path)
                    p.wait()
                except:
                    print_status(2, value[0])
                    return
            print_status(3, value[0])

def call_wal(args):
    # if we are calling wal on an image
    if(args.image):
        imagepath = os.path.abspath(args.image[0])
        commandstring = "wal -i "+imagepath
        print(commandstring)
        os.system(commandstring)
    # if we are using a prebuilt or custom colorscheme
    if(args.theme):
        commandstring = "wal --theme "+args.theme[0]
        os.system(commandstring)
    else:
        print("Error, missing required argument")


def call_slickpywal(config):
    # Check to see if the user defined a custom path
    if("slickpywal" in config):
        try:
            p = subprocess.Popen(["slick-pywal"], cwd=config["slickpywal"]["path"])
            p.wait()
        except:
            print_status(1, "SlickGreeter Pywal")
            return
    # Check to see if it exists somewhere in the path
    elif(is_tool("slick-pywal")):
        try:
            p = subprocess.Popen(["slick-pywal"])
            p.wait()
        except:
            print_status(1, "SlickGreeter Pywal")
            return
    else:
        return
    print_status(0, "SlickGreeter Pywal")
    return

def call_pywalneopixels(config):
    # Check to see if the user defined a custom path
    if("pywalneopixels" in config):
        try:
            commandstring = config["pywalneopixels"]["path"]+"startLEDs"
            os.system(commandstring)
        except:
            print_status(1, "Pywal NeoPixel")
    # Check to see if it exists somewhere in the path
    elif(is_tool("startLEDs")):
        try:
            os.system("startLEDs")
        except:
            print_status(1, "Pywal NeoPixel")
            return
    # it is not detected it all
    else:
        return
    print_status(0, "Pywal NeoPixel")


def call_wal_discord(config):
    # Check to see if the user defined a custom path
    if("waldiscord" in config):
        try:
            m = subprocess.Popen(["wal-discord", "-t"], cwd=config["waldiscord"]["path"])
            m.wait()
        except:
            print_status(1, "Discord")
            return
        print_status(0, "Discord")
    # Check to see if it exists somewhere in the path
    elif(is_tool("wal-discord")):
        try:
            n = subprocess.Popen(["wal-discord", "-t"])
            n.wait()
        except:
            print_status(1, "Discord")
            return
        print_status(0, "Discord")
    else:
        return

def call_xmenu(config):
    # Check to see if the user defined a custom path
    if("xmenu" in config):
        try:
            # make xmenu
            m = subprocess.Popen(["make"], cwd=config["xmenu"]["path"])
            m.wait()
            retval = m.returncode
            # if making failed
            if(retval != 0):
                print_status(1, "Xmenu")
                return
            # Install the new files
            i = subprocess.Popen(["sudo", "make", "install"], cwd=config["xmenu"]["path"])
            i.wait()
            retval = m.returncode
            # if installation failed
            if(retval != 0):
                print_status(1, "Xmenu")
                return
        # If we found a config but something went wrong
        except:
            print_status(1, "Xmenu")
            return
        print_status(0, "Xmenu")
    # no config for xmenu, just return
    else:
        return

def theme(config, args):
    #  call_wal(args)
    #  call_slickpywal(config)
    call_pywalneopixels(config)
    #  call_wal_discord(config)
    #  call_xmenu(config)
    #  user_hooks(config)

def main():
    config = parse_yaml()
    args = parse_args()
    theme(config, args)

if __name__ == '__main__':
    main()
