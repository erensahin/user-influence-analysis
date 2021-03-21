"""
BLG517E - Spring 2019 Term Project
User Influence Analysis for GitHub Developer Social Networks
Sefa Eren Sahin
504171526
"""

import requests
import pandas as pd
from collections import OrderedDict
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from user_influence_analysis import secret_config
from user_influence_analysis.utils import logger

class UserFetcher:
    def __init__(self):
        self.api_url = "https://api.github.com/graphql"
        token = secret_config["github-api"]["tokens"][0]
        self.headers = {'Authorization': 'token ' + token}
        self.output_dir = os.path.join(
            os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))),
            "output"
        )

        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)

    def __fetch_followers_of_user(self, user_name):
        query = '''
            query($login: String!, $after: String){
              user(login: $login) {
                followers(first: 100, after: $after) {
                  totalCount
                  edges {
                    cursor
                    node {
                      login
                    }
                  }
                  pageInfo {
                    hasNextPage
                    hasPreviousPage
                    endCursor
                    startCursor
                  }
                }
              }
            }
        '''

        variables = {
            "login": user_name,
            "after": None
        }

        user_followers_list = []

        while True:
            r = requests.post(self.api_url,
                              headers=self.headers,
                              json={'query': query, 'variables': variables})
            result_json = r.json()
            field_dict = result_json["data"]["user"]["followers"]

            after_cursor = field_dict["pageInfo"]["endCursor"]
            variables["after"] = after_cursor
            user_followers = [OrderedDict({"user": user_name,
                                           "follower": x["node"]["login"]})
                              for x in field_dict["edges"]]
            user_followers_list.extend(user_followers)

            if not field_dict["pageInfo"]["hasNextPage"]:
                break

        return user_followers_list

    def __fetch_repositories_of_user(self, user_name):
        query = '''
            query($login: String!, $after: String){
              user(login: $login) {
                login
                repositories(first: 100, after: $after, orderBy: {field: STARGAZERS, direction: DESC}) {
                  nodes {
                    name
                    owner {login}
                    isFork
                    stargazers {
                      totalCount
                    }
                    forks {
                      totalCount
                    }
                  }
                  pageInfo {
                    hasNextPage
                    hasPreviousPage
                    endCursor
                    startCursor
                  }
                }
              }
            }
        '''

        variables = {
            "login": user_name,
            "after": None
        }

        user_repos = []

        while True:
            r = requests.post(self.api_url,
                              headers=self.headers,
                              json={'query': query,
                                    'variables': variables})
            result_json = r.json()
            field_dict = result_json["data"]["user"]["repositories"]

            after_cursor = field_dict["pageInfo"]["endCursor"]
            variables["after"] = after_cursor

            repos = [
                OrderedDict({
                    "owner": user_name,
                    "name": x["name"],
                    "stars": x["stargazers"]["totalCount"],
                    "forks": x["forks"]["totalCount"]
                })
                for x in field_dict["nodes"]
                if x["isFork"] is False and x["owner"]["login"] == user_name
            ]

            user_repos.extend(repos)

            if not field_dict["pageInfo"]["hasNextPage"]:
                break

        return user_repos

    def fetch_and_save_followers(self, users, return_followers=False):
        user_followers = []
        logger.info("Fetching user followers... size: {}".format(len(users)))

        try:
            user_followers_df = self.__read_user_followers()
            users_fetched = user_followers_df.user.unique()
        except:
            logger.warning(
                "Unable to read user followers data. "
                "Continue with empty user list")
            users_fetched = []
            user_followers_df = pd.DataFrame()

        try:
            file_path = os.path.join(self.output_dir, "skip_users.csv")
            skipped_users = np.ravel(pd.read_csv(
                file_path, header=None).values).tolist()
        except:
            skipped_users = []

        if len(users) > 0:
            logger.info("First user: {}".format(users[0]))
            user_followers.extend(user_followers_df.to_dict('records'))

        users = set(users) - set(users_fetched) - set(skipped_users)

        for user in users:
            logger.info("Current user: {}".format(user))
            if user in users_fetched:
                logger.info("User {} is already fetched.".format(user))
                current = user_followers_df[user_followers_df.user == user]
                user_followers.extend(current.to_dict('records'))
                continue

            if len(skipped_users) % 10 == 0:
                logger.info("Exporting skipped len: {}".format(
                    len(skipped_users)))
                self.__export_skipped_users(skipped_users)

            followers = self.__fetch_followers_of_user(user)

            if len(followers) < 3:
                logger.info("Skipping {} since followers < 3".format(user))
                skipped_users.append(user)
                continue

            user_followers.extend(followers)

            log_msg = "Fetched {} user followers. Last user {}.".format(
                len(user_followers), user
            )
            logger.info(log_msg)

            self.__export_user_followers(followers)

        if return_followers:
            return pd.DataFrame(user_followers)

    def fetch_and_save_user_repos(self, users):
        try:
            user_repos_df = self.__read_user_repos()
            users_fetched = user_repos_df.owner.unique()
        except:
            users_fetched = []

        _users = set(users) - set(users_fetched)
        logger.info("Fetch repos for {} users".format(len(_users)))
        for user in _users:
            repos = self.__fetch_repositories_of_user(user)
            logger.info("{} repos for {}".format(len(repos), user))

            self.__export_user_repos(repos)

    def __export_user_followers(self, user_followers):
        output_path = os.path.join(self.output_dir, "user_followers.csv")
        header = not os.path.exists(output_path)

        user_followers_df = pd.DataFrame(user_followers)
        user_followers_df.to_csv(output_path, mode="a", index=False,
                                 header=header)

    def __export_user_repos(self, user_repos):
        output_path = os.path.join(self.output_dir, "user_repos.csv")
        header = not os.path.exists(output_path)

        user_repos_df = pd.DataFrame(user_repos)
        user_repos_df.to_csv(output_path, mode="a", index=False,
                             header=header)

    def __export_skipped_users(self, skipped_users):
        output_path = os.path.join(self.output_dir, "skip_users.csv")
        header = not os.path.exists(output_path)

        try:
            current = pd.read_csv(skipped_users, index_col=None)
        except:
            current = pd.DataFrame()

        skipped_df = pd.DataFrame(skipped_users)
        skipped_df = pd.concat([current, skipped_df]).drop_duplicates()

        skipped_df.to_csv(output_path, mode="a", index=False, header=header)

    def __read_user_followers(self):
        file_path = os.path.join(self.output_dir, "user_followers.csv")
        return pd.read_csv(file_path, index_col=None)

    def __read_user_repos(self):
        file_path = os.path.join(self.output_dir, "user_repos.csv")
        return pd.read_csv(file_path, index_col=None)
