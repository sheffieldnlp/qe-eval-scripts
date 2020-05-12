#!/usr/bin/env python
import sys
import os
import argparse
import codecs
import numpy as np
from scipy.stats import pearsonr, spearmanr

"""
Scoring programme for WMT'20 Task 1 DA, Task 2 HTER
"""

def parse_submission(pred_list):
    lp_segments = []

    for line in pred_list:
        pred = line.strip().split('\t')
        assert len(pred) == 4, \
                "Incorrect format, expecting (tab separated): <LP> <METHOD_NAME> <SEGMENT_NUMBER> <SEGMENT_SCORE>."

        lp_str = pred[0].lower()
        lp_segments.append(pred[1:])

    # The following block make sure that the segment_number is used to keep
    # the scores in order
    tmp_lp_segments = {}
    for _, seg_nb, seg_score in lp_segments:
        tmp_lp_segments[seg_nb] = float(seg_score)

    lp_segments = np.array(list(dict(sorted(tmp_lp_segments.items())).values()))

    return lp_str, lp_segments


def computeScores(truth, pred):

    return [pearson, mae, rmse]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('system', help='System file')
    parser.add_argument('gold', help='Gold output file')

    args = parser.parse_args()

    print("Loading goldlabels...")
    with codecs.open(args.gold, 'r', encoding='utf-8') as truth_file:
        lp_str_gold, goldlabels = parse_submission(truth_file.readlines())
    print("done.")

    print("Loading your predictions...")
    with codecs.open(args.system, 'r', encoding='utf-8') as submission_file:
        lp_str_pred, predictions = parse_submission(submission_file.readlines())
    print("done.")

    assert lp_str_pred == lp_str_gold, \
            "Incorrect LP identification, expecting {}, given {}".format(lp_str_gold, lp_str_pred)

    assert len(goldlabels) == len(predictions), \
            "Incorrect number of predicted scores for {}, expecting {}, given {}.".format(
                    lp_str_pred, len(goldlabels), len(predictions)
                   )

    print("Computing scores...")
    pearson = pearsonr(goldlabels, predictions)[0]
    diff = goldlabels - predictions
    mae = np.abs(diff).mean()
    rmse = (diff ** 2).mean() ** 0.5

    print("pearson: {}".format(pearson))
    print("mae: {}".format(mae))
    print("rmse: {}".format(rmse))

