"""
BLG517E - Spring 2019 Term Project
User Influence Analysis for GitHub Developer Social Networks
Sefa Eren Sahin
504171526
"""

import argparse
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from user_influence_analysis.utils import logger
from user_influence_analysis.data_collection.user_fetcher import UserFetcher


class UserFollowerCollector:
    def __init__(self):
        self.user_fetcher = UserFetcher()

    @staticmethod
    def get_followers(user_followers):
        return user_followers.follower.unique().tolist()

    def traverse_from_user(self, user):
        logger.info("Start traversing from user " + user)
        user_followers = self.user_fetcher.fetch_and_save_followers(
            [user],
            return_followers=True
        )

        if user_followers.empty:
            logger.info("No follower for user: {}".format(user))
            logger.info("Execution stops...")
            return

        followers = self.get_followers(user_followers)
        fetched_users = [user]

        all_users = followers + fetched_users

        while len(all_users) < 2000000:
            user_followers = self.user_fetcher.fetch_and_save_followers(
                followers,
                return_followers=True
            )

            fetched_users.extend(followers)

            followers = self.get_followers(user_followers) \
                if not user_followers.empty else []
            all_users = followers + fetched_users

            logger.info("Current number of users: {}".format(len(all_users)))

        logger.info("Traversing completed".format(len(all_users)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="mbostock",
                        help='''Enter a username to start traversing for 
                            followers.''')

    args = parser.parse_args()
    user = args.username

    sc = UserFollowerCollector()
    sc.traverse_from_user(user)
