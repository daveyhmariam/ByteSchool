#!/usr/bin/env python3
from git import Repo

def get_latest_commit(repo_path: str, file_path: str) -> str:
    """
    Get the latest commit hash for a specific file in the repository.

    :param repo_path: Path to the Git repository.
    :param file_path: Path to the file within the repository.
    :return: Commit hash of the latest commit that touched the file.
    """
    try:
        repo = Repo(repo_path)
        # Ensure we are working with a valid repo
        assert not repo.bare

        # Get the latest commit for the specific file
        commits = list(repo.iter_commits(paths=file_path))
        if commits:
            latest_commit = commits[0]
            return latest_commit.hexsha
        else:
            return "No commits found for the file."

    except Exception as e:
        return str(e)

# Usage example
if __name__ == '__main__':
    repo_path = '/home/falcon/alx_2/ByteSchool'  # Replace with the path to your repository
    file_path = '/home/falcon/alx_2/ByteSchool/README.md'  # Replace with the relative path to the file

    latest_commit = get_latest_commit(repo_path, file_path)
    print(f"Latest commit for the file: {latest_commit}")
