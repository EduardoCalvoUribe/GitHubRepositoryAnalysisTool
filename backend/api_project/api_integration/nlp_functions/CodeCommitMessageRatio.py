# Import PyGithub in project. Library should be automatically installed through requirements.txt
# Alternatively install library with !pip install PyGithub
from github import Github
from django.conf import settings

# Returns PyGithub commit object for a provided repository_owner, repository_name, commit_sha, github_token
def getGithubCommitObject(repository_owner, repository_name, commit_sha):
    # Try retrieving the PyGithub commit object
    try:
        # Initialize PyGithub with token
        g = Github(settings.GITHUB_PERSONAL_ACCESS_TOKEN)

        # Get the repository object
        repo = g.get_repo(f"{repository_owner}/{repository_name}")

        # Get the commit object for specified SHA
        commit = repo.get_commit(sha=commit_sha)
        return commit
    
    # Return error message if PytGithub commit object retrieval unsuccessful
    except Exception as e:
        print(f"Error retrieving commit in getGithubCommitObject: {e}")
        return None
        
# Accepts PyGithub commit object and returns commit message/code length ratio
def computeCodeCommitRatio(commit):
    # Get the files changed in the commit
    commit_files = commit.files

    # List of tuples containing data about every file in commit
    # The data is stored in the following order: file name, number of additions, number of deletions, total number of changes,
    # removed code lines, added code lines
    file_data = []

    # Init counter for counting total number of characters in code additions/deletions
    changed_code_char_count = 0

    # Print the details of each changed file
    for file in commit_files:
        # Retrieve data associated with file in commit_files
        file_name = file.filename
        nr_additions = file.additions
        nr_deletions = file.deletions
        nr_changes = file.changes  # equals nr_additions + nr_deletions

        # Retrieve content of patched code
        patch = file.patch

        # Split code on newline symbol
        patch_lines = patch.split('\n') if patch else []

        # Initialise lists which store added and removed code lines in commit file
        added_lines = []
        removed_lines = []

        # Consider every line which starts with + or -, signifying a code line addition or deletion respectively
        for line in patch_lines:
            if line.startswith('+'):
                added_lines.append(line)
                # Add total number of chars in line to changed_code_char_count
                changed_code_char_count += len(line)
            elif line.startswith('-'):
                removed_lines.append(line)
                # Add total number of chars in line to changed_code_char_count
                changed_code_char_count += len(line)

        # Create tuple containing all relevant data from file, append to file_data
        file_data.append((file_name, nr_additions, nr_deletions, nr_changes, added_lines, removed_lines))

    # Retrieve the commit message from commit
    commit_message = commit.commit.message

    # Compute ratio between number of characters in changed code and number of characters in commit message
    ratio = len(commit_message) / changed_code_char_count if changed_code_char_count != 0 else -1

    return ratio
     