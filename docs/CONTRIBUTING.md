How to contribute to Escape The Werehouse
=========================================

Thank you for considering contributing to Escape The Werehouse!

Reporting issues
----------------

- Describe what you expected to happen.
- If possible, include a [minimal reproducible example](https://stackoverflow.com/help/minimal-reproducible-example) to help me
  identify the issue. This also helps check that the issue is not with
  your own code.
- Describe what actually happened. Include the full traceback if there was an
  exception.
- List your Python, and Pygame versions. If possible, check if this
  issue is already fixed in the repository.

Submitting patches
------------------

- Include tests if your patch is supposed to solve a bug, and explain
  clearly under which circumstances the bug happens. Make sure the test fails
  without your patch.
- Include a string like "Fixes #123" in your commit message
  (where 123 is the issue you fixed).
  See [Closing issues using keyword](https://help.github.com/en/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword)

First time setup
----------------

- Download and install the [latest version of git](https://git-scm.com/downloads)
- Configure git with your [username](https://help.github.com/en/github/using-git/setting-your-username-in-git) and [email](https://help.github.com/en/github/setting-up-and-managing-your-github-user-account/setting-your-commit-email-address):

        git config --global user.name 'your name'
        git config --global user.email 'your email'

- Make sure you have a [GitHub account](https://github.com/join)
- Fork Escape The Weerehouse to your GitHub account by clicking the [Fork](https://github.com/CrowStudio/Escape-The-Werehouse-/fork) button.
- [Clone](https://help.github.com/en/github/getting-started-with-github/fork-a-repo#step-2-create-a-local-clone-of-your-fork) your GitHub fork locally:

        git clone https://github.com/{username}/Escape-The-Werehouse-
        cd Escape-The-Werehouse-

- Add the main repository as a remote to update later:

        git remote add escape_game https://github.com/{username}/Escape-The-Werehouse-
        git fetch 

- Install Pygame ([for troubleshooting](https://www.pygame.org/wiki/GettingStarted#Further%20information%20on%20installation)):

        python3 -m pip install -U pygame --user
        

Start coding
------------

-   If you're submitting a bug or documentation fix, create a branch to 
    identify the issue you would like to work on:

        git checkout -b branch-name-of-the-issue escape_game/master

    If you're submitting a feature addition or change, create a branch to 
    identify the feature you would like to work on:

        git checkout -b branch-name-your-feature escape_game/master

- Using your favorite editor, make your changes, [committing as you go](https://dont-be-afraid-to-commit.readthedocs.io/en/latest/git/commandlinegit.html#commit-your-changes)
- Push your commits to GitHub:

        git push --set-upstream escape_game your-branch-name

  and [create a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)
  
- Celebrate 🎉

<br>
<br>
<br>

_This document was inspired by Flasks_ [_CONTRIBUTING.md_](https://github.com/pallets/flask/blob/master/CONTRIBUTING.rst)
