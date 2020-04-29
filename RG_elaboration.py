import os
import csv
import pickle as pkl
import re
import RG_cleaning
import gaze_detector_IDT


def run(video_path):
    video_name = re.search(r'.*_.*_.*_', video_path.split("/")[-1][:-4]).group()
    with open("real_gaze_data/list_video.txt") as file:
        r = csv.reader(file, delimiter=' ')
        list_video = [a + "_" + b + "_" + c + "_" for a, b, c in r]

    with open("real_gaze_data/list_user.txt") as file:
        r = csv.reader(file, delimiter=' ')
        list_user = [a + "_" + b + "_" + c + "_" + d + "_" + e for a, b, c, d, e in r]

    if not os.path.exists("raw_data_cleaned"):
        os.makedirs("raw_data_cleaned")

    if not os.path.exists("raw_data_cleaned/raw_data_cleaned.pkl") or not os.path.exists(
            "raw_data_cleaned/error_users.pkl"):
        print("Cleaning raw data")
        raw_data_cleaned, error_users = RG_cleaning.run(list_video, list_user, 0.06)
        pkl.dump(raw_data_cleaned, open("raw_data_cleaned/raw_data_cleaned.pkl", "wb"))
        pkl.dump(error_users, open("raw_data_cleaned/error_users.pkl", "wb"))
    else:
        raw_data_cleaned = pkl.load(open(str("raw_data_cleaned/raw_data_cleaned.pkl"), 'rb'))

    return raw_data_cleaned[video_name]


def calculate_stats(RG_data, velocity_threshold, dispersion_threshold, height, width, fps, step_sw, step_sd):
    statsOfVideoFromAllUsers = {}
    for user in RG_data.keys():
        statsOfVideoFromAllUsers[user] = \
            gaze_detector_IDT.run(RG_data[user],
                                  velocity_threshold, dispersion_threshold,
                                  height, width, fps, step_sw, step_sd)
    return statsOfVideoFromAllUsers
