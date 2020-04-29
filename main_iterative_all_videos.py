import os
import pickle as pkl
import cv2
import csv

import CNN_elaboration
import LLS_elaboration
import RG_average_user
import RG_elaboration
import RG_select_users
import gaze_detector_IDT
import plottingPearsonResultAllVideosAllParameters
import test_KS
import test_PC
step_sw = 20
step_sd = 20
mod_CNN_names = {
    1: "squeezenet",
    2: "resnet",
    3: "densenet"
}
# problem with LLS computing
black_list_videos = ["v12", "v35"]
# statistiche
# 1 -> distribuzione dei tempi di fissazione
# 2 -> distribuzione delle ampiezze delle saccadi
# 3 -> distribuzione delle direzioni delle saccadi

"""
- creo una cartella denominata come il video
- 3 file .pkl per le statistiche 1,2,3
- - CNN_stats
- - RG_stats
- - LLS_stats
"""


# raggio di dispersione massima per farsi che i punti facciano parte di una fissazione
def run():
    with open("real_gaze_data/list_video.txt") as f:
        csv_reader = csv.reader(f, delimiter=" ")
        list_path = ["C:/Users/User/interazione_naturale/sources/"+raw[0]+"_"+raw[1]+"_"+raw[2]+"_left.avi"
                     for raw in csv_reader
                     if raw[0] not in black_list_videos]

    if not os.path.exists("result"):
        os.makedirs("result")

    result_test_ks = {}
    result_test_pearson = {}

    min_dt = 3
    max_dt = 7
    min_dispt = 10
    max_dispt = 45
    step_dispt = 5
    for duration_threshold in range(min_dt, max_dt):
        for dispersion_threshold in range(min_dispt, max_dispt, step_dispt):
            print("DUR_T:", duration_threshold, "DISP_T:", dispersion_threshold)

            key_thresholds = str(duration_threshold)+"_"+str(dispersion_threshold)
            result_test_ks[key_thresholds] = {}
            result_test_pearson[key_thresholds] = {}

            for video_path in list_path:
                # features of video
                video_name = video_path.split('/')[-1].split(".")[0]
                print("- - VIDEO:", video_name)
                vidcap = cv2.VideoCapture(video_path)
                height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
                fps = int(vidcap.get(cv2.CAP_PROP_FPS))

                result_path = "result/" + video_name

                if not os.path.exists(result_path):
                    os.makedirs(result_path)

                result_test_ks[key_thresholds][video_name] = {}
                result_test_pearson[key_thresholds][video_name] = {}

                #######################################################################################################
                if not os.path.exists(result_path + "/RG_data.pkl"):
                    print("RG_data computing")
                    # ottengo i valori medi degli utenti che hanno visto i video
                    RG_data = RG_elaboration.run(video_path)
                    pkl.dump(RG_data, open(result_path + "/RG_data.pkl", "wb"))
                else:
                    RG_data = pkl.load(open(result_path + "/RG_data.pkl", "rb"))

                RG_stats = RG_elaboration.calculate_stats(RG_data, duration_threshold, dispersion_threshold,
                                                          height, width, fps, step_sw, step_sd)

                # creazione lista di utenti su cui calcolare le statisitche dell'utente medio
                # parameters:
                # - utenti con l'errore minore (senza parametri)
                # - utenti con selzione per sesso (sex = "m" o "f")
                # - utenti selezionati per ordine di visione dei video (order = "fwd" o "bwd")
                list_users, f_descr = RG_select_users.createListUsers()
                # statistiche dell'utente medio
                RG_av_stats = RG_average_user.run(RG_stats, list_users, step_sw, step_sd)

                #######################################################################################################
                if not os.path.exists(result_path + "/LLS_data.pkl"):
                    print("LLS_data computing")
                    LLS_data = LLS_elaboration.run(video_path, result_path)
                    pkl.dump(LLS_data, open(result_path + "/LLS_data.pkl", "wb"))
                else:
                    LLS_data = pkl.load(open(result_path + "/LLS_data.pkl", "rb"))

                LLS_stats = gaze_detector_IDT.run(LLS_data, duration_threshold, dispersion_threshold, height, width, fps, step_sw, step_sd)

                result_test_ks[key_thresholds][video_name]["lls"] = {}
                result_test_ks[key_thresholds][video_name]["lls"] = test_KS.run(LLS_stats, RG_av_stats)
                result_test_pearson[key_thresholds][video_name]["lls"] = {}
                result_test_pearson[key_thresholds][video_name]["lls"] = test_PC.run(LLS_stats, RG_av_stats)

                # itero sui modelli di CNN
                print("- - - - CNN: ", end="")
                for model_CNN in mod_CNN_names.keys():
                    print(mod_CNN_names[model_CNN], end=" ")
                    if not os.path.exists(result_path +"/CAM_data_mod_" + str(model_CNN) + ".pkl"):
                        print("CNN data computing")
                        CNN_data = CNN_elaboration.run(video_path, result_path, model_CNN)
                        pkl.dump(CNN_data, open(result_path + "/CAM_data_mod_" + str(model_CNN) + ".pkl", "wb"))
                    else:
                        CNN_data = pkl.load(open(result_path + "/CAM_data_mod_" + str(model_CNN) + ".pkl", "rb"))

                    CNN_stats = gaze_detector_IDT.run(CNN_data, duration_threshold, dispersion_threshold, height, width, fps, step_sw, step_sd)

                    result_test_ks[key_thresholds][video_name][mod_CNN_names[model_CNN]] = {}
                    result_test_ks[key_thresholds][video_name][mod_CNN_names[model_CNN]] = test_KS.run(CNN_stats, RG_av_stats)
                    result_test_pearson[key_thresholds][video_name][mod_CNN_names[model_CNN]] = {}
                    result_test_pearson[key_thresholds][video_name][mod_CNN_names[model_CNN]] = test_PC.run(CNN_stats,
                                                                                                            RG_av_stats)
                print()
    if not os.path.exists("result/test_all_videos"):
        os.makedirs("result/test_all_videos")

    pkl.dump(result_test_pearson, open("result/test_all_videos/result_test_pearson_all_videos_"
                                       +str(min_dt)+"-"+str(max_dt)+"_"+str(min_dispt)+"-"+str(max_dispt)+".pkl", "wb"))

    # plot dei risultati dal calcolo del CCP e calcolo del CCP medio rispetto a tutti i video
    # e alle iterazione dei parametri dell'algoritmo I-DT
    plottingPearsonResultAllVideosAllParameters.run(result_test_pearson)
