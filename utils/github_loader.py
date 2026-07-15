from pathlib import Path
from git import Repo


class GitHubLoader:

    def __init__(self, repo_dir="data/repos"):
        self.repo_dir = Path(repo_dir)

    def clone_repo(self, github_url: str):

        repo_name = github_url.rstrip("/").split("/")[-1]

        destination = self.repo_dir / repo_name

        # If already cloned, reuse it
        if destination.exists():
            print(f"✅ Repository '{repo_name}' already exists.")
            return destination

        print(f"📥 Cloning {repo_name}...")

        Repo.clone_from(github_url, destination)

        print("✅ Clone completed!")

        return destination