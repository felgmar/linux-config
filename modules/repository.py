#!/bin/env python3

import subprocess
import os

class RepositoryManager():
    def __init__(self, repo_url: str, repo_dir: str):
        self.repo_url: str = repo_url
        self.repo_dir: str = repo_dir
        self.repositories_dir = os.path.join(os.getcwd(), "modules/repositories")

    def update_repo(self):
        previous_dir: str = os.getcwd()
        repo_to_update: str = os.path.join(self.repositories_dir, self.repo_dir)
        command: str = "git pull"

        assert os.path.isdir(repo_to_update)

        try:
            os.chdir(repo_to_update)
            subprocess.run(command, shell=True, check=True)
        except Exception as e:
            raise e

        os.chdir(previous_dir)

    def clone_repo(self):
        repo_to_clone: str = os.path.join(self.repositories_dir, self.repo_dir)
        command: str = f"git clone {self.repo_url}"

        if not os.path.exists(self.repositories_dir):
            os.mkdir(self.repositories_dir)

        try:
            os.chdir(self.repositories_dir)
        except Exception as e:
            raise e

        if not os.path.exists(repo_to_clone):
            try:
                subprocess.run(command, shell=True, check=True)
            except Exception as e:
                raise e
        else:
            print(repo_to_clone, "is already cloned")

        os.chdir(self.repositories_dir)
