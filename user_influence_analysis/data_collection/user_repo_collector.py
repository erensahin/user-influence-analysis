"""
BLG517E - Spring 2019 Term Project
User Influence Analysis for GitHub Developer Social Networks
Sefa Eren Sahin
504171526
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import argparse
import pandas as pd

from user_influence_analysis.data_collection.user_fetcher import UserFetcher
from user_influence_analysis.utils import logger


class UserRepoCollector:
    def __init__(self):
        self.user_fetcher = UserFetcher()

    def get_users(self, file_name="user_followers.csv"):
        output_path = os.path.join(self.user_fetcher.output_dir, file_name)

        df = pd.read_csv(output_path)
        return set(df.user.unique().tolist() + df.follower.unique().tolist())

    def collect_user_repos(self, file_name):
        users = self.get_users(file_name)
        logger.info("Repo collection starts with {} users.".format(len(users)))
        self.user_fetcher.fetch_and_save_user_repos(users)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--follower_file", default="user_followers.csv",
                        help='''Enter user follower csv file name. 
                        Default: user_followers.csv''')

    args = parser.parse_args()
    follower_file = args.follower_file

    urc = UserRepoCollector()
    urc.collect_user_repos(follower_file)
