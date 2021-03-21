"""
BLG517E - Spring 2019 Term Project
User Influence Analysis for GitHub Developer Social Networks
Sefa Eren Sahin
504171526
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from user_influence_analysis.utils import logger
from user_influence_analysis.analysis.network_analysis import NetworkAnalysis
from user_influence_analysis.analysis.h_index import HIndex


class CorrelationAnalysis:
    def __init__(self):
        self.network_analyzer = NetworkAnalysis()
        self.h_index = HIndex()
        self.output_dir = os.path.join(
            os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))),
            "output"
        )
        self.network_metrics = None
        self.h_index_metrics = None

    def get_metrics(self, how="inner"):
        if self.network_metrics is None:
            self.network_metrics = self.network_analyzer.get_network_metrics()

        if self.h_index_metrics is None:
            self.h_index_metrics = self.h_index.h_index_analysis()

        return self.network_metrics.join(self.h_index_metrics, how=how)

    @staticmethod
    def feature_correlation(metrics, top=100):
        metrics.sort_values('followers', ascending=False, inplace=True)
        cols = [c for c in metrics.columns if not c.endswith("_rank")]
        correlations = metrics[cols][:top].corr('spearman')
        return correlations

    @staticmethod
    def borda_score(row, N, rank_cols):
        score = sum([N - row[r] for r in rank_cols])
        return score

    @staticmethod
    def normalize_column(df, col):
        return (df[col] - df[col].min()) / (df[col].max() - df[col].min())

    def borda_count(self, metrics):
        headers = metrics.columns
        n = len(metrics)

        logger.info("Calculating borda count scores start.")
        rank_cols = []
        for h in headers:
            col = "{}_rank".format(h)
            metrics[col] = metrics[h].rank(method="first", ascending=False)
            rank_cols.append(col)

        metrics["borda_score"] = metrics.apply(self.borda_score,
                                               args=(n, rank_cols,),
                                               axis=1)

        metrics["borda_score"] = self.normalize_column(metrics, "borda_score")
        logger.info("Calculating borda count scores end.")

        return metrics

    def export_top_n_metric_users(self, metrics, feature, feature_set, n=20):
        file_path = os.path.join(
            self.output_dir,
            "{}_top_{}_{}.csv".format(feature_set, n, feature)
        )

        metrics.sort_values(feature, ascending=False)[feature][:n].to_csv(
            file_path, index_label="user"
        )

    def analyze_correlation(self, feature_set="all_metrics"):
        metrics = self.get_metrics(how="inner")
        logger.info("Correlation analysis on {} users".format(len(metrics)))

        metrics = self.borda_count(metrics)

        for n in [100, 1000, 10000]:
            corr = self.feature_correlation(metrics, top=n)
            file_path = os.path.join(
                self.output_dir,
                "{}_corr_{}.csv".format(feature_set, n)
            )

            corr.round(4).to_csv(file_path)

        cols = [c for c in metrics if not c.endswith("_rank")]

        for col in cols:
            self.export_top_n_metric_users(metrics, col, feature_set, n=20)

        logger.info("Correlation analysis end.")

    def run_correlation_analysis(self):
        logger.info("Correlation analysis for all metrics")
        self.analyze_correlation()

        logger.info("Correlation analysis for all metrics end")


if __name__ == "__main__":
    corr_analysis = CorrelationAnalysis()
    corr_analysis.run_correlation_analysis()




