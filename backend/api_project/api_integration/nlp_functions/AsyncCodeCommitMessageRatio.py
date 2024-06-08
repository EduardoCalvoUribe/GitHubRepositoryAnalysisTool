import aiohttp
import asyncio
from django.conf import settings

async def get_pr_files(repo_owner, repo_name, pull_number):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pull_number}/files"
    headers = {"Authorization": f"token {settings.GITHUB_PERSONAL_ACCESS_TOKEN}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.json()

async def get_commit(repo_owner, repo_name, commit_sha):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{commit_sha}"
    headers = {"Authorization": f"token {settings.GITHUB_PERSONAL_ACCESS_TOKEN}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.json()
        
async def compute_code_commit_ratio(repo_owner, repo_name, pull_number, commit_sha):
    try:
        files = await get_pr_files(repo_owner, repo_name, pull_number)
        commit_data = await get_commit(repo_owner, repo_name, commit_sha)
        commit_message = commit_data['commit']['message']
        changed_code_char_count = 0

        for file in files:
            patch = file.get("patch", "")
            if patch:
                patch_lines = patch.split('\n')
                for line in patch_lines:
                    if line.startswith('+') or line.startswith('-'):
                        changed_code_char_count += len(line)

        ratio = len(commit_message) / changed_code_char_count if changed_code_char_count != 0 else -1
        return ratio
    except Exception as e:
        print(f"Error computing code commit ratio: {e}")
        return -1
