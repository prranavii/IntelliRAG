from utils.github_loader import GitHubLoader

loader = GitHubLoader()

path = loader.clone_repo(
    "httpps://github.com/langchain-ai/langchain"
)

print(path)
