"""
BLG517E - Spring 2019 Term Project
User Influence Analysis for GitHub Developer Social Networks
Sefa Eren Sahin
504171526
"""

import pandas as pd
import networkx as nx
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from user_influence_analysis.utils import logger


class NetworkAnalysis:
    def __init__(self):
        self.user_followers_path = self.output_dir = os.path.join(
            os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))),
            "output",
            "user_followers.csv"
        )
        self.user_followers_df = self.read_user_followers()

    def read_user_followers(self):
        user_followers_df = pd.read_csv(self.user_followers_path)
        return user_followers_df.drop_duplicates()

    def build_graph(self):
        G = nx.from_pandas_edgelist(self.user_followers_df, "follower", "user",
                                    create_using=nx.DiGraph())
        return G

    def in_degree(self, G):
        logger.info("In degree start")
        df = pd.DataFrame(G.in_degree())
        df.set_index(0, inplace=True)
        df.columns = ["followers"]
        logger.info("In degree end")

        return df

    def pagerank(self, G):
        logger.info("PageRank start")
        pr = nx.pagerank_scipy(G)
        logger.info("PageRank end")

        df = pd.DataFrame.from_dict(pr, orient="index")
        df.columns = ["pagerank"]
        return df

    def hits(self, G):
        logger.info("HITS start")
        hits = nx.hits_scipy(G)
        logger.info("HITS end")

        df = pd.DataFrame(hits).T
        df.columns = ["hub", "authority"]
        return df.drop("hub", axis=1)

    def eigenvector_centrality(self, G):
        logger.info("Eigenvector start")
        eig = nx.eigenvector_centrality_numpy(G)
        logger.info("Eigenvector end")

        df = pd.DataFrame.from_dict(eig, orient="index")
        df.columns = ["eigenvector_centrality"]
        return df

    def katz_cetrality(self, G):
        logger.info("Katz start")
        katz = nx.katz_centrality_numpy(G)
        logger.info("Katz end")

        df = pd.DataFrame.from_dict(katz, orient="index")
        df.columns = ["katz_centrality"]
        return df

    def get_network_metrics(self):
        G = self.build_graph()
        pr = self.pagerank(G)
        in_degree = self.in_degree(G)
        hits = self.hits(G)
        eig = self.eigenvector_centrality(G)
        # katz = self.katz_cetrality(G)

        network_metrics = pr.join([in_degree, hits, eig])
        return network_metrics
