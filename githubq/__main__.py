# -*- coding: utf-8 eval: (blacken-mode 1) -*-
#
# September 4 2021, Christian Hopps <chopps@gmail.com>
#
# Copyright (c) 2021 by Christian E. Hopps.
# All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; see the file COPYING; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#
import argparse
import logging
import os
import pdb
import requests
from github import Github

gh = None


def get_password_arg(name):
    if name.startswith("file:"):
        return open(os.path.expanduser(name[5:]), "r", encoding="utf-8").read().strip()
    if name.startswith("env:"):
        return os.environ[name[4:]]
    return name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--auth-token", help="file:filename, env:envvarname, token"
    )
    parser.add_argument("-c", "--context", help="context when needed")
    parser.add_argument(
        "-R", "--repo", help="repo can be shortened to owner/project when using github"
    )
    parser.add_argument("-r", "--sha", "--ref", help="git ref (e.g., SHA, tag, ...)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Be verbose")
    commandparser = parser.add_subparsers(dest="command")
    headsparser = commandparser.add_parser("heads")
    prparser = commandparser.add_parser("pr-data")
    headsparser.add_argument("--pr", help="pull request number")
    prparser.add_argument("--pr", type=int, help="pull request number")
    args = parser.parse_args()

    # Setup basic logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level)

    # Get auth token
    if args.auth_token:
        args.auth_token = get_password_arg(args.auth_token)
    elif os.path.exists(os.path.expanduser("~/.github-auth")):
        args.auth_token = get_password_arg("file:~/.github-auth")

    global gh
    gh = Github(args.auth_token)

    if False:
        repos = {}
        for repo in gh.get_user().get_repos():
            repos[repo.full_name] = repo
        for name in sorted(repos):
            logging.info("REPO: %s", name)

    if False:
        repo = gh.get_repo(args.repo)
        # prs = repo.get_pulls()
        pr = repo.get_pull(args.pr)
        evs = [e for e in pr.get_issue_events()]
        heads = [e for e in evs if e.event == "head_ref_force_pushed"]

        logging.info("PR %s: %s", args.pr, pr)
        pdb.set_trace()
        print("DONE")

    # repo = gh.get_repo
    url = 'https://api.github.com/graphql'
    json = { 'query' : '''
{
  repository(owner:"FRRouting", name:"frr") {
    pullRequests(last: 10) {
      edges {
        node {
          number
          mergeable
        }
      }
    }
  }
}
    '''
    }
    api_token = args.auth_token
    headers = {'Authorization': 'token %s' % api_token}
    r = requests.post(url=url, json=json, headers=headers)
    print (r.text)


if __name__ == "__main__":
    main()
