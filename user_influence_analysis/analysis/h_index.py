"""
BLG517E - Spring 2019 Term Project
User Influence Analysis for GitHub Developer Social Networks
Sefa Eren Sahin
504171526
"""

import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from user_influence_analysis.utils import logger


class HIndex:
    def __init__(self):
        self.user_followers_path = self.output_dir = os.path.join(
            os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))),
            "output",
            "user_repos.csv"
        )
        self.user_repos_df = pd.read_csv(self.user_followers_path)

    @staticmethod
    def h_index(user_repos, feature):
        user_repos.sort_values(ascending=False, inplace=True)
        user_repos = user_repos.to_frame(name=feature)
        user_repos["rank"] = user_repos[feature].rank(method="first",
                                                      ascending=False)

        return len(user_repos[user_repos[feature] >= user_repos["rank"]])

    def h_feature(self, feature):
        grouped = (self.user_repos_df.groupby("owner", sort=False)
                   [feature].apply(lambda x: self.h_index(x, feature)))
                   #.apply(lambda x: len(self.h_index(x, feature))))

        grouped = grouped.to_frame()
        grouped.columns = ["h_{}".format(feature)]
        return grouped

    def h_star(self):
        return self.h_feature("stars")

    def h_fork(self):
        return self.h_feature("forks")

    def h_index_analysis(self):
        logger.info("H_Star start")
        h_star = self.h_star()
        logger.info("H_Star end")
        logger.info("H_Fork start")
        h_fork = self.h_fork()
        logger.info("H_Fork end")

        return h_star.join(h_fork)

if __name__ == "__main__":
    h_index = HIndex()
    h_result = h_index.h_index_analysis()
    print('aww')
