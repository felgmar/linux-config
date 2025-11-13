#!/bin/env python3

"""
Module containing the RepositoryManager class.
"""

import subprocess
import os

class RepositoryManager():
    """
    Handles tasks such as cloning and updating repositories.
    """
    def __init__(self, repo_url: str, repo_dir: str):
        self.REPO_URL: str = repo_url
        self.REPO_DIR: str = repo_dir
        self.REPOSITORIES_DIR = os.path.join(os.getcwd(), "modules/repositories")

    def stash_repository_changes(self):
        """
        Stash any changes in the repository.
        Args:
            repository_path (str): The path to the repository.
        Raises:
            AssertionError: If the provided path is not a valid git repository.
            Exception: If the git stash command fails.
        """
        GIT_STASH_COMMAND: list[str] = ["git", "stash", "--include-untracked"]
        IS_GIT_INSIDE_WORK_TREE_COMMAND: list[str] = ["git", "rev-parse", "--is-inside-work-tree"]
        IS_REPOSITORY_VALID: bool = subprocess.run(IS_GIT_INSIDE_WORK_TREE_COMMAND,
                                                   capture_output=True) \
                                                    .stdout.decode("utf-8").strip() == "true"
        
        assert IS_REPOSITORY_VALID, "The provided path is not a valid git repository."

        try:
            print("[INFO] Stashing any local changes...")
            exit_code = subprocess.run(GIT_STASH_COMMAND, check=True)

            if exit_code.returncode == 0:
                print("[INFO] Successfully stashed local changes.")
            else:
                print("[INFO] No local changes to stash.")
        except Exception as e:
            raise e

    def restore_repository_changes(self):
        """
        Restores any stashed changes in the repository.
        Args:
            repository_path (str): The path to the repository.
        Raises:
            AssertionError: If the provided path is not a valid git repository.
            Exception: If the git stash command fails.
        """
        GIT_UNSTASH_COMMAND: list[str] = ["git", "restore", "--staged", "."]
        GIT_IS_INSIDE_WORK_TREE_COMMAND: list[str] = ["git", "rev-parse", "--is-inside-work-tree"]
        IS_REPOSITORY_VALID: bool = subprocess.run(GIT_IS_INSIDE_WORK_TREE_COMMAND,
                                                   capture_output=True) \
                                                    .stdout.decode("utf-8").strip() == "true"

        assert IS_REPOSITORY_VALID, "The provided path is not a valid git repository."

        try:
            print("[INFO] Restoring any stashed changes...")
            exit_code = subprocess.run(GIT_UNSTASH_COMMAND, check=True)
            if exit_code.returncode == 0:
                print("[INFO] Successfully restored stashed changes.")
            else:
                print("[INFO] No stashed changes to restore.")
        except Exception as e:
            raise e

    def update_repo(self):
        """
        Pulls the latest changes from the repository, if any.
        """
        PREVIOUS_DIR: str = os.getcwd()
        FULL_REPOSITORY_PATH: str = os.path.join(self.REPOSITORIES_DIR, self.REPO_DIR)
        COMMAND: list[str] = ["git", "pull"]

        assert os.path.isdir(FULL_REPOSITORY_PATH), "Could not find any repository to update."

        os.chdir(FULL_REPOSITORY_PATH)

        self.stash_repository_changes()

        try:
            subprocess.run(COMMAND, check=True)
        except Exception as e:
            raise e

        self.restore_repository_changes()

        os.chdir(PREVIOUS_DIR)

    def clone_repo(self):
        """
        Clone a repository if it does not exist.
        """
        REPOSITORY_TO_CLONE: str = os.path.join(self.REPOSITORIES_DIR, self.REPO_DIR)
        COMMAND: list[str] = ["git", "clone", self.REPO_URL]

        assert not os.path.isdir(REPOSITORY_TO_CLONE), "Repository already exists."

        if not os.path.exists(self.REPOSITORIES_DIR):
            os.mkdir(self.REPOSITORIES_DIR)

        try:
            os.chdir(self.REPOSITORIES_DIR)
        except Exception as e:
            raise e

        try:
            subprocess.run(COMMAND, check=True)
        except Exception as e:
            raise e

        try:
            os.chdir(self.REPOSITORIES_DIR)
        except Exception as e:
            raise e
