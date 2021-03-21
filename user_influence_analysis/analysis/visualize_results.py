"""
BLG517E - Spring 2019 Term Project
User Influence Analysis for GitHub Developer Social Networks
Sefa Eren Sahin
504171526
"""

import pandas as pd
import os
import matplotlib.pyplot as plt


class ResultVisualizer:
    def __init__(self):
        self.output_dir = os.path.join(
            os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))),
            "output"
        )

    def plot_borda_correlations(self):
        for n in [100, 1000, 10000]:
            file_path = os.path.join(self.output_dir,
                                     "all_metrics_corr_{}.csv".format(n))
            df = pd.read_csv(file_path, index_col=0)
            df.drop("borda_score", inplace=True, axis=1)
            df.loc["borda_score"].plot(figsize=(12, 8), style='-o',
                                       label="Top {}".format(n))

        plt.legend()
        plt.title("Correlation of Borda Count to Other Metrics")
        plt.savefig(self.output_dir + "all_metrics.png")

        plt.show()

rv = ResultVisualizer()
rv.plot_borda_correlations()
