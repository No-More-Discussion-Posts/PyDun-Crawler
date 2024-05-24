# PyDun-Crawler
PyGame dungeon crawler for UMGC CMSC-495 capstone project.

## Quicklinks
1. [Project Plan](docs/ProjectPlan.md)
2. [Backlog/Todo list](https://github.com/orgs/No-More-Discussion-Posts/projects/1/views/1)
3. [Roadmap](https://github.com/orgs/No-More-Discussion-Posts/projects/1/views/4)


# Git Setup
The following is the minimum needed to get setup and start contributing with Git. See the [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf) for a convenient reference of git commands.

## Installation and GUIs
#### Windows
[Git For Windows](https://gitforwindows.org/)
#### Linux
See [the official Git web site](https://git-scm.com/download/linux)
#### Any OS
[Git SCM](https://git-scm.com/downloads)

## Github
 If you haven't already, you'll need an account setup at [Github](https://github.com/)

## Setup
In the command line of your choice (On Windows OS I prefer Git Bash that comes with Git For Windows) you'll need to setup your username with the username you chose in GitHub. The push.autoSetupRemote is not necessary but it does simplify pushing code from new branches.

```bash
> git config --global user.name 'username'
> git config --global push.autoSetupRemote true
```
## Clone the repo
```bash
git clone https://github.com/No-More-Discussion-Posts/PyDun-Crawler.git
```

 A window should pop up prompting you to log in to github.


## Contributing
There is one main branch, or line of development called *main*.
```bash
> git branch -v
* main f1c0ef0 Initial commit
```
When developing you should create your own "feature branch" from the dev branch, develop your code, and then merge your branch back into dev. Main will be updated from dev periodically.

For a more information see [Understanding Git Branching](https://medium.com/@jacoblogan98/understanding-git-branching-5d01f3dda541)

### Creating a Branch
Ensure your branches are up to date
```bash
> git fetch
```
Checkout the dev branch
```bash
> git checkout dev
```

If you already had dev open and the latest code wasn't merged:

Pull from remote to get the most up to date changes
```bash
> git pull
```
Create and checkout your new branch.
```bash
> git checkout -b [branch-name] # Does change your working branch
```
See the following for [branch naming best practices](https://graphite.dev/guides/git-branch-naming-conventions)

### Commiting Code
After creating and checking out a branch you can now code in your IDE of choice as normal. For Git to create a "snapshot" of your development, however, you'll have to create a commit.

```bash
> git add . # Add all files to file index
> git commit -m "Commit message" # Message is viewable by all contributors and helps document what has been changed
```

### Push Code to Remote Repo
You'll want to regularly push your commits to the remote repo (uploading to github vs storing on your local machine).
```bash
> git push
```

### Merging
Eventually you'll want your branch to be merged into the main branch so others can see and test based on your input.

The simplest way to do this is in Github itself. Click [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) for the guide.

# Game Setup
From the base directory (pydun-crawler):

1. Install the game in editable mode so that you can test code changes without installing every time.
```bash
> pip install --user -e .
```

2. If you get a PATH error like below:
```bash
  WARNING: The script pydun.exe is installed in 'C:\Users\melke\AppData\Roaming\Python\Python310\Scripts' which is not on PATH.
```
You'll need to copy that path and [add it to your PATH variable](https://www.java.com/en/download/help/path.html)

3. Run the program
```bash
> pydun
```
You should see the game load!
>Note: You do not need to reinstall anything after making edits, just rerun the *pydun* command.