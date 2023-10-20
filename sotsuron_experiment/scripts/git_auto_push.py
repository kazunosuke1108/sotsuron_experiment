#! /usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess

def git_auto_push():
    subprocess.run("git add .", shell=True, check=True)
    subprocess.run("git commit -m \"AutoPush\"", shell=True, check=True)
    subprocess.run("git pull origin main", shell=True, check=True)
    subprocess.run("git push origin main", shell=True, check=True)
