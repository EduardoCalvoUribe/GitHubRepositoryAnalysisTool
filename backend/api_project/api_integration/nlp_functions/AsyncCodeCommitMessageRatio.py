"""
This file contains the functions associated with computing the code/commit message ratio
"""

# Necessary imports for AsyncCodeCommitMessageRatio.py
import aiohttp, asyncio
from django.conf import settings

async def get_pr_files(repo_owner, repo_name, pull_number):
    """
    Gets all files associated with a pull request in JSON format.

    This function is called by compute_code_commit_ratio within this file. The function
    makes an API call to the endpoint associated with the files of the pull request for a given
    repo owner, repo name and a pull number. 

    Parameters:
    repo_owner: The repository owner associated with the pull request
    repo_name: The repository name associated with the pull request
    pull_number: The pull number associated with the pull request

    Returns:
    .json() object: A .json() object containing all files associated with the pull
    request for the abovementioned parameters.    
    """
    # Github API endpoint for files (based on parameters)
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pull_number}/files"
    # Headers required for API authorization
    headers = {"Authorization": f"token {settings.GITHUB_PERSONAL_ACCESS_TOKEN}"}
    
    # Asynchronous API call to files endpoint 
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

async def get_commit(repo_owner, repo_name, commit_sha):
    """
    Gets a commit object in JSON format.

    This function is called by compute_code_commit_ratio within this file. 
    The function makes an API call to the endpoint associated with the commit 
    for a given repo owner, repo name and a commit_sha. By design, 
    the commit_sha is unique for every commit in Github. 
    
    Parameters:
    repo_owner: The repository owner associated with the pull request
    repo_name: The repository name associated with the pull request
    commit_sha: The commit SHA associated with a commit

    Returns:
    .json() object: A .json() object containing the commit associated 
    with the abovementioned parameters.    
    """
    # Github API endpoint for commit object (based on parameters)
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{commit_sha}"
    # Headers required for API authorization
    headers = {"Authorization": f"token {settings.GITHUB_PERSONAL_ACCESS_TOKEN}"}
    
    # Asynchronous API call to commit object endpoint 
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            
            response.raise_for_status()
            return await response.json()
        
async def compute_code_commit_ratio(repo_owner, repo_name, pull_number, commit_sha, commitJSON):
    """
    Computes the code/commit ratio metric which is part of the general 
    semantic score. This function is only part of the general semantic score
    for commit objects! (i.e. not for comments)

    The code/commit ratio is defined as the number of characters in a commit message
    divided by the number of characters in the added/removed lines of code associated
    with a commit. 
    
    Parameters:
    repo_owner: The repository owner associated with the pull request
    repo_name: The repository name associated with the pull request
    pull_number: The pull number associated with the pull request
    commit_sha: The commit SHA associated with a commit

    Returns:
    float: A float representing the code/commit ratio. If no code has been changed,
    the metric value is set to 0. In the case of an error, the metric value is set to -1.
    """
    await asyncio.sleep(0.1)
    try:
        changed_code_char_count = 0
        # Get files associated with pull request
        #files = await get_pr_files(repo_owner, repo_name, pull_number)
        # print(commitJSON["files"])
        # print(type(commitJSON["files"]))
        if "files" in commitJSON:
            # print(commitJSON["files"]["patch"])
            files = commitJSON["files"]["patch"]
            # Get commit object
            # commit_data = await get_commit(repo_owner, repo_name, commit_sha)

            # Retrieve commit message
            commit_message = commitJSON['commit']['message']
            # Init changed_code_char_count

            # Loop over all files associated with pull request
            print(files)
            print(type(files))
            for file in files:
                patch = file.get("patch", "")
                if patch:
                    patch_lines = patch.split('\n')
                    for line in patch_lines:
                        # If line of code starts with + or -, treat as adjusted line of code
                        if line.startswith('+') or line.startswith('-'):
                            changed_code_char_count += len(line)

        # Compute code/commit message ratio        
        ratio = len(commit_message) / changed_code_char_count if changed_code_char_count != 0 else 0
        return ratio
    except Exception as e:
        print(f"Error computing code commit ratio: {e}")
        return -1