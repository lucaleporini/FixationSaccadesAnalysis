import csv
import pprint
import sys
import os
import pickle as pkl
import cv2

import CNN_elaboration
import LLS_elaboration
import RG_average_user
import RG_elaboration
import RG_select_users
import plottingPearsonResultAllParameters
import test_PC
from correlate import RT_reformat
import gaze_detector_IDT

# statistiche
# 1 -> distribuzione dei tempi di fissazione
# 2 -> distribuzione delle ampiezze delle saccadi
# 3 -> distribuzione delle direzioni delle saccadi
import test_KS
step_sw = 20
step_sd = 20
mod_CAM_names = {
    1: "squeezenet",
    2: "resnet",
    3: "densenet"
}
distr_names = {
    "tf": "TIME FIXATIONS",
    "sw": "SACCADES WIDTH",
    "sd": "SACCADES DIRECTIONS"
}

"""
- creo una cartella denominata come il video
- 3 file .pkl per le statistiche 1,2,3
- - stats_CAM_data
- - stats_real_gaze_data
- - stats_low_level_saliency_data
"""
# video_path = ""
# if len(sys.argv) > 1:
#     video_path = sys.argv[1]
#     if not os.path.exists(video_path):
#         print("Missing file video: video path is not correct")
#         exit(0)
# else:
#     print("Missing parameter: path from this to directory to video")
#     exit(0)


def run(video_path):
    video_name = video_path.split('\\')[-1].split(".")[0]
    print("VIDEO:", video_name)
    # features of video
    vidcap = cv2.VideoCapture(video_path)
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    print("-----------------\nFEATURES OF VIDEO\nHEIGHT: "+str(height)+
          "\nWIDTH: "+str(width)+"\nFPS: "+str(fps))

    video_name = video_path.split('\\')[-1].split(".")[0]
    result_path = "result/" + video_name
    if not os.path.exists("result"):
        os.makedirs("result")
    if not os.path.exists(result_path):
        os.makedirs(result_path)


    # COMPUTING DATA -->  RG_data, CNN_data, LLS_data
    print("----------------------------------------------------------")
    print("REAL DATA ELABORATION ...")
    if not os.path.exists(result_path + "/RG_data.pkl"):
        print("RG_data computing")
        # ottengo i valori medi degli utenti che hanno visto i video
        RG_data = RG_elaboration.run(video_path)
        pkl.dump(RG_data, open(result_path + "/RG_data.pkl", "wb"))
    else:
        print("RG_data already computed")
        RG_data = pkl.load(open(result_path + "/RG_data.pkl", "rb"))


    print("----------------------------------------------------------")
    print("LLS ELABORATION ...")
    if not os.path.exists(result_path+"/LLS_data.pkl"):
        print("LLS_data computing")
        LLS_data = LLS_elaboration.run(video_path, result_path)
        pkl.dump(LLS_data, open(result_path+"/LLS_data.pkl", "wb"))
    else:
        print("LLS_data already computed")
        LLS_data = pkl.load(open(result_path + "/LLS_data.pkl", "rb"))

    print("----------------------------------------------------------")
    print("CNN ELABORATION ...")
    # CNN STATS COMPUTING -----------------------------------------------------------------------------------------
    CNN_data = {}
    for model_CAM in mod_CAM_names.keys():
        print("Model CAM: "+str(model_CAM))
        if not os.path.exists(result_path+"/CAM_data_mod_"+str(model_CAM)+".pkl"):
            print("CAM_data computing")
            CNN_data[mod_CAM_names[model_CAM]] = CNN_elaboration.run(video_path, result_path, model_CAM)
            pkl.dump(CNN_data, open(result_path + "/CAM_data_mod_" + str(model_CAM) + ".pkl", "wb"))
        else:
            print("CAM_data already computed")
            CNN_data[mod_CAM_names[model_CAM]] = pkl.load(open(result_path + "/CAM_data_mod_" + str(model_CAM) + ".pkl", "rb"))
    print("----------------------------------------------------------")

    result_test_pearson = {}
    RG_stats_all = {}
    LLS_stats_all = {}
    CNN_stats_all = {}

    print("\nINTERATION ON PARAMTERS OF I-DT ALGORITHM")
    for duration_threshold in range(3, 7):
        for dispersion_threshold in range(10, 45, 5):
            print("DUR_T:", duration_threshold, "DISP_T:", dispersion_threshold)
            key_thresholds = str(duration_threshold) + "_" + str(dispersion_threshold)
            result_test_pearson[key_thresholds] = {}
            RG_stats_all[key_thresholds] = {}
            LLS_stats_all[key_thresholds] = {}
            CNN_stats_all[key_thresholds] = {}

            # RG STATS COMPUTING -----------------------------------------------------------------------------------------
            print("RG stats of all users computing")
            RG_stats_all_users = RG_elaboration.calculate_stats(RG_data, duration_threshold, dispersion_threshold,
                                                          height, width, fps, step_sw, step_sd)

            # creazione lista di utenti su cui calcolare le statisitche dell'utente medio
            # parameters:
            # - utenti con l'errore minore (senza parametri)
            # - utenti con selzione per sesso (sex = "m" o "f")
            # - utenti selezionati per ordine di visione dei video (order = "fwd" o "bwd")
            list_users, f_descr = RG_select_users.createListUsers()
            # statistiche dell'utente medio
            print("RG stats of average user computing")
            RG_av_stats = RG_average_user.run(RG_stats_all_users, list_users, step_sw, step_sd)

            RG_stats_all[key_thresholds] = RG_av_stats

            # LLS STATS COMPUTING -----------------------------------------------------------------------------------------

            print("LLS stats computing")
            LLS_stats = gaze_detector_IDT.run(LLS_data, duration_threshold, dispersion_threshold,
                                                  height, width, fps, step_sw, step_sd)

            result_test_pearson[key_thresholds]["lls"] = {}
            result_test_pearson[key_thresholds]["lls"] = test_PC.run(LLS_stats, RG_av_stats)

            # agggiungo a LLS_stats_all contente tutte le stats calcolate
            LLS_stats_all[key_thresholds] = LLS_stats

            # CNN STATS COMPUTING -----------------------------------------------------------------------------------------
            for model_CAM in mod_CAM_names.keys():
                print(mod_CAM_names[model_CAM]+" stats computing")
                CAM_stats = gaze_detector_IDT.run(CNN_data[mod_CAM_names[model_CAM]], duration_threshold, dispersion_threshold,
                                                  height, width, fps, step_sw, step_sd)

                # print("PLOT DISTRIBUTIONS ...")
                # plotDistributionFixationSaccades.run(CAM_stats, LLS_stats, RG_av_stats,
                # video_path, result_path, step_sw, step_sd)

                result_test_pearson[key_thresholds][mod_CAM_names[model_CAM]] = {}
                result_test_pearson[key_thresholds][mod_CAM_names[model_CAM]] = test_PC.run(CAM_stats, RG_av_stats)

                CNN_stats_all[key_thresholds][mod_CAM_names[model_CAM]] = {}
                CNN_stats_all[key_thresholds][mod_CAM_names[model_CAM]] = CAM_stats

            print("-----------------------------------")

    pkl.dump(RG_stats_all, open(result_path+"/RG_stats.pkl", "wb"))
    pkl.dump(LLS_stats_all, open(result_path+"/LLS_stats.pkl", "wb"))
    pkl.dump(CNN_stats_all, open(result_path+"/CNN_stats.pkl", "wb"))

    if not os.path.exists(result_path+"/test"):
        os.makedirs(result_path+"/test")
    pkl.dump(result_test_pearson, open(result_path+"/test/result_pearson_all_parameters_IDT.pkl", "wb"))


    # plotting results
    plottingPearsonResultAllParameters.run(result_test_pearson)
