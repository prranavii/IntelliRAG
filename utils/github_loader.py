import time
from pathlib import Path
from git import Repo


class GitHubLoader:

    def __init__(self, repo_dir="data/repos"):
        self.repo_dir = Path(repo_dir)
        self.repo_dir.mkdir(parents=True, exist_ok=True)

    def _delete_path_recursive(self, path):
        path = Path(path)
        if not path.exists():
            return
        for item in list(path.iterdir()):
            if item.is_file():
                try:
                    item.unlink()
                except Exception:
                    pass
            elif item.is_dir():
                self._delete_path_recursive(item)
        try:
            path.rmdir()
        except Exception:
            pass

    def _cleanup_dir(self, path):
        path = Path(path)
        if not path.exists():
            return
        # Move locked directory out of the way on Windows by renaming it to a trash path
        trash_path = path.parent / f"{path.name}_trash_{int(time.time() * 1000)}"
        try:
            path.rename(trash_path)
            self._delete_path_recursive(trash_path)
        except Exception:
            # Fallback to in-place recursive deletion if rename is blocked
            self._delete_path_recursive(path)

    def clone_repo(self, github_url: str):
        repo_name = github_url.rstrip("/").split("/")[-1]
        destination = self.repo_dir / repo_name

        # If already cloned, attempt clean update
        if destination.exists():
            try:
                print(f"Repository '{repo_name}' already exists. Updating...")
                with Repo(destination) as repo:
                    repo.git.reset('--hard')
                    repo.remotes.origin.pull()
                print("Update completed!")
                return destination
            except Exception as e:
                print(f"Update failed: {e}. Re-cloning...")
                self._cleanup_dir(destination)

        print(f"Cloning {repo_name}...")
        repo = Repo.clone_from(github_url, destination)
        repo.close()
        print("Clone completed!")

        return destination