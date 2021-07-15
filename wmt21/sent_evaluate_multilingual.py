#!/usr/bin/env python
import sys
import os
import argparse
import codecs
import numpy as np
from scipy.stats import pearsonr, spearmanr
from collections import defaultdict

"""
Scoring programme for WMT'21 Task 1 DA and Task 2 HTER **multilingual**
"""

language_pairs = ['en-de', 'en-zh', 'ro-en', 'et-en', 'ne-en', 'si-en', 'ru-en', 'en-cs', 'en-ja', 'ps-en', 'km-en']

def parse_submission(pred_list, goldlabel_bool):
    disk_footprint = 0
    model_params = 0
    lp_dict = defaultdict(list)

    if not goldlabel_bool:
        disk_footprint = pred_list[0].rstrip()
        model_params = pred_list[1].rstrip()
        pred_list = pred_list[2:]

    for line in pred_list:
        pred = line.strip().split('\t')
        assert len(pred) == 4, \
                "Incorrect format, expecting (tab separated): <LP> <METHOD_NAME> <SEGMENT_NUMBER> <SEGMENT_SCORE>."

        lp_str = pred[0]
        lp_dict[lp_str.lower()].append(pred[1:])

    lp_dict_keys = list(lp_dict.keys())
    assert set(language_pairs) == set(lp_dict_keys), \
            "Incorrect list of LPs, expecting: {}, given: {}.".format(language_pairs, lp_dict_keys)

    for lp_str in lp_dict_keys:
        lp_segments = lp_dict[lp_str]
        # The following block make sure that the segment_number is used to keep
        # the scores in order
        tmp_lp_segments = {}
        for _, seg_nb, seg_score in lp_segments:
            tmp_lp_segments[seg_nb] = float(seg_score)

        lp_dict[lp_str] = np.array(list(dict(sorted(tmp_lp_segments.items())).values()))

    return disk_footprint, model_params, lp_dict


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('system', help='System file')
    parser.add_argument('gold', help='Gold output file')

    args = parser.parse_args()

    print("Loading goldlabels...")
    with codecs.open(args.gold, 'r', encoding='utf-8') as truth_file:
        _, _, goldlabels = parse_submission(truth_file.readlines(), True)
    print("done.")

    print("Loading your predictions...")
    with codecs.open(args.system, 'r', encoding='utf-8') as submission_file:
        disk_footprint, model_params, predictions = parse_submission(submission_file.readlines(), False)
    print("done.")

    all_scores = []
    print("Computing scores...")
    for lp_str in predictions:
        print("\t for {}...".format(lp_str))
        assert len(predictions[lp_str]) == len(goldlabels[lp_str]), \
                "Incorrect number of predicted scores for {}, expecting {}, given {}.".format(
                        lp_str, len(goldlabels[lp_str]), len(predictions[lp_str])
                       )
        pearson = pearsonr(goldlabels[lp_str], predictions[lp_str])[0]
        diff = goldlabels[lp_str] - predictions[lp_str]
        mae = np.abs(diff).mean()
        rmse = (diff ** 2).mean() ** 0.5
        all_scores.append([pearson, mae, rmse])

    print("\t averaging...")
    average_scores = np.mean(np.array(all_scores), axis=0)
    print("done.")

    print("disk_footprint: {}".format(disk_footprint))
    print("model_params: {}".format(model_params))
    print("pearson: {:.4}".format(average_scores[0]))
    print("mae: {:.4}".format(average_scores[1]))
    print("rmse: {:.4}".format(average_scores[2]))

