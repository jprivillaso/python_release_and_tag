from github import Github
import queue
import os

GIT_ACCESS_TOKEN = ''

try:
  GIT_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']

  if GIT_ACCESS_TOKEN is None or GIT_ACCESS_TOKEN == '':
    raise Exception
except:
  raise Exception('Please add the GITHUB_ACCESS_TOKEN to your environment variables')

USER = 'REPLACE_WITH_GITHUB_USER'
REPOSITORY = 'REPLACE_WITH_GITHUB_REPO'
BRANCH = 'REPLACE_WITH_GITHUB_BRANCH'

g = Github(GIT_ACCESS_TOKEN)

def get_current_version():
  try:
    release_version = ''
    file = open('./version.txt')

    for line in file:
      if line.strip() != '':
        release_version = line.strip()
        break

    return release_version
  except:
    raise Exception('Error reading release version')

def get_recent_prs():
  closed_prs = g.get_repo(f'{USER}/{REPOSITORY}').get_pulls('closed')
  recent_closed_prs = queue.Queue()

  for pr in closed_prs:
    if not(pr.title.startswith('RELEASE')):
      if pr.merged_at != None:
        recent_closed_prs.put((pr.title, pr.number))
    else:
      break

  return recent_closed_prs

def format_release_items(recent_closed_prs):
  header    = '| PR Name | PR Number | PR URI | \n'
  subheader = '| ------- | --------- | -------| \n'
  body      = ''

  while recent_closed_prs.qsize() != 0:
    title, number = recent_closed_prs.get()
    body += f'| {title} | {number} | https://github.com/${USER}/${REPOSITORY}/pull/{number} | \n'

  return header + subheader + body

def create_release(version, release_summary):
  branch = g.get_repo(f'{USER}/{REPOSITORY}').get_branch(BRANCH)

  g.get_repo(f'{USER}/{REPOSITORY}').create_git_tag_and_release(
    version,
    f'RELEASE {version}',
    version,
    release_summary,
    branch.commit.sha,
    'commit'
  )

def update_version(version):
  try:
    p1, p2, p3 = version[1:].split('.')
    new_version = ''

    if int(p3) + 1 <= 9:
      new_version = f'v{p1}.{p2}.{str(int(p3) + 1)}'
    else:
      new_version = f'v{p1}.{str(int(p2) + 1)}.0'

    file = open('version.txt', 'w')
    file.write(new_version)
  except:
    raise Exception('Error calculating new version')

def __main__():
  closed_prs = get_recent_prs()
  release_summary = format_release_items(closed_prs)
  version = get_current_version()
  create_release(version, release_summary)
  update_version(version)

if __name__ == "__main__":
  __main__()