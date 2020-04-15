# Python Release and Tag

The script contained in this repository is used to automate the RELEASE process at any software whose code is stored in Github.

I define a process or RELEASE that consists in the following steps:

1. Every developer creates features and pull requests at the `dev` branch.

2. Before every release, you will have multiple pull requests created. Each one fixing a bug or adding a new feature.

3. When you are ready to create the RELEASE, first create a pull request with source `dev` and target `master`.

4. After merging the code in master, you can run the ./generate_release.py script.

## Pre-Requisites

1. Create an environment variable named `GITHUB_ACCESS_TOKEN` that must contain the access token, to allow this script to make requests to the Github API and gather your pull requests information. [Here](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) you can find the instructions for generating this token, in case you don't have it.

2. Replace the variables inside the script:

- USER: Your github user's name
- REPOSITORY: The repository that you will use to generate the Release
- BRANCH: Normally this may be filled with `dev`, but feel free to use the branch that contains the pull requests

3. Update the initial version of your software, by replacing the number of the version at the `version.txt` file. It must start with `v.`, so please don't remove it.

4. You're ready to run the script

```bash
  python3 ./generate_release.py
```

## Verify the output

1. Verify the latest tag created

```bash
  git tag | sort -V | tail -1
```

2. Go to your repository and verify the latest release and tags created. Also see the contents that were auto-generated using your pull requests information.

Go to this URL. Replace with your repo information:

`https://github.com/${user}/${repository}/releases`

3. Have fun! You have just saved some minutes of life :)