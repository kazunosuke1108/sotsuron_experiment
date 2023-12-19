#! /usr/bin/python3
# -*- coding: utf-8 -*-
import time
import subprocess

def git_auto_push(msg="AutoPush"):
    subprocess.run("git add .", shell=True, check=True)
    subprocess.run(f"git commit -m \"{msg}\"", shell=True, check=True)
    subprocess.run("git pull origin devel/ras", shell=True, check=True)
    subprocess.run("git push origin devel/ras", shell=True, check=True)
for i in range(20):
    git_auto_push()
    time.sleep(90*10)
# git_auto_push()
# interval_sec=60*60*1
# num_iter=10
# for i in range(num_iter):
#     git_auto_push(f"AutoPush no.{i}/{num_iter}")
#     time.sleep(interval_sec)