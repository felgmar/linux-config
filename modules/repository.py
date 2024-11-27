#!/bin/env python3

import subprocess
import os

class RepositoryManager():
    def __init__(self):
        self.repo_url = ""
        self.repo_dir = ""
        self.repositories_dir = os.path.join(os.getcwd(), "modules/repositories")

    def update_repo(self):
        previous_dir: str = os.getcwd()
        command: str = "git pull"

        if os.path.isdir(self.repositories_dir + self.repo_dir):
            os.chdir(self.repositories_dir + self.repo_dir)
            try:
                subprocess.run(command, shell=True, check=True)
            except Exception as e:
                raise e
        os.chdir(previous_dir)

    def clone_repo(self):
        previous_dir: str = self.repositories_dir
        command: str = f"git clone {self.repo_url}" + \
            os.path.join(self.repositories_dir, self.repo_dir)

        if not os.path.exists(self.repositories_dir):
            os.mkdir(self.repositories_dir)

        os.chdir(self.repositories_dir)

        if not os.path.exists(os.path.join(self.repositories_dir, self.repo_dir)):
            try:
                subprocess.run(command, shell=True, check=True)
            except Exception as e:
                raise e

        os.chdir(previous_dir)
