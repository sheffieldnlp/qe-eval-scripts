#!/usr/bin/env python
import sys
import os
import argparse
import codecs
import numpy as np
from sklearn.metrics import f1_score

"""
Scoring programme for WMT'21 Task 3 Critical Error Detection
"""

tag_map = {'GOOD': 0, 'good': 0, 'OK': 0, 'ok': 0, 'NOT': 0, 'not': 0, 'BAD': 1, 'bad': 1, 'ERR': 1, 'err': 1}


def computeScores(gold_tags, pred_tags):
    try:
        assert len(pred_tags) == len(gold_tags)
    except:
        print("The prediction file doesn't match the length of the test file.")
        print("Length prediction: ",len(pred_tags))
        print("Length test: ",len(gold_tags))

    f1_all_scores = f1_score(gold_tags, pred_tags, average=None, pos_label=None)

    # Matthews correlation coefficient (MCC)
    # true/false positives/negatives
    tp = tn = fp = fn = 0
    for pred_tag, gold_tag in zip(pred_tags, gold_tags):
        if pred_tag == 1:
            if pred_tag == gold_tag:
                tp += 1
            else:
                fp += 1
        else:
            if pred_tag == gold_tag:
                tn += 1
            else:
                fn += 1

    mcc_numerator = (tp * tn) - (fp * fn)
    mcc_denominator = ((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)) ** 0.5
    mcc = mcc_numerator / mcc_denominator

    return np.append(f1_all_scores, mcc)


def parse_submission(pred_list, goldlabel_bool):
    disk_footprint = 0
    model_params = 0
    lp_segments = []

    if not goldlabel_bool:
        disk_footprint = pred_list[0].rstrip()
        model_params = pred_list[1].rstrip()
        pred_list = pred_list[2:]

    for line in pred_list:
        pred = line.strip().split('\t')
        assert len(pred) == 4, \
                "Incorrect format, expecting (tab separated): <LP> <METHOD_NAME> <SEGMENT_NUMBER> <SEGMENT_SCORE>."

        lp_str = pred[0].lower()
        lp_segments.append(pred[1:])

    # The following block make sure that the segment_number is used to keep
    # the scores in order
    tmp_lp_segments = {}
    for _, seg_nb, seg_label in lp_segments:
        tmp_lp_segments[seg_nb] = float(tag_map[seg_label.lower()])

    lp_segments = np.array(list(dict(sorted(tmp_lp_segments.items())).values()))

    return disk_footprint, model_params, lp_str, lp_segments


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('system', help='System file')
    parser.add_argument('gold', help='Gold output file')

    args = parser.parse_args()

    print("Loading goldlabels...")
    with codecs.open(args.gold, 'r', encoding='utf-8') as truth_file:
        _, _, lp_str_gold, goldlabels = parse_submission(truth_file.readlines(), True)
    print("done.")

    print("Loading your predictions...")
    with codecs.open(args.system, 'r', encoding='utf-8') as submission_file:
        disk_footprint, model_params, lp_str_pred, predictions = parse_submission(submission_file.readlines(), False)
    print("done.")

    assert lp_str_pred == lp_str_gold, \
            "Incorrect LP identification, expecting {}, given {}".format(lp_str_gold, lp_str_pred)

    assert len(goldlabels) == len(predictions), \
            "Incorrect number of predicted scores for {}, expecting {}, given {}.".format(
                    lp_str_pred, len(goldlabels), len(predictions)
                   )

    print("Computing scores...")
    f1_bad, f1_good, mcc = computeScores(goldlabels, predictions)

    print("MCC: {:.4}".format(mcc))
    print("F1_bad: {:.4}".format(f1_bad))
    print("F1_good: {:.4}".format(f1_good))
    print("F1_multi: {:.4}".format(f1_bad * f1_good))
    print("disk_footprint: {}".format(disk_footprint))
    print("model_params: {}".format(model_params))

