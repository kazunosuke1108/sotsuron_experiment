#! /usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess

def git_auto_push(msg="AutoPush"):
    subprocess.run("git add .", shell=True, check=True)
    subprocess.run(f"git commit -m \"{msg}\"", shell=True, check=True)
    subprocess.run("git pull origin devel/ras", shell=True, check=True)
    subprocess.run("git push origin devel/ras", shell=True, check=True)
