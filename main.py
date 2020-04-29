import os
import pickle as pkl
import cv2

import CNN_elaboration
import LLS_elaboration
import RG_average_user
import RG_elaboration
import RG_select_users
import test_PC
import gaze_detector_IDT

step_sw = 20
step_sd = 20

mod_CAM_names = {
    1: "squeezenet",
    2: "resnet",
    3: "densenet"
}
features = ['time_fixations', 'saccades_width', 'saccades_directions']
plot_titles = {
    "time_fixations": "TIME FIXATIONS",
    "saccades_width": "SACCADES WIDTH",
    "saccades_directions": "SACCADES DIRECTIONS"
}


# statistiche
# 1 -> distribuzione dei tempi di fissazione
# 2 -> distribuzione delle ampiezze delle saccadi
# 3 -> distribuzione delle direzioni delle saccadi
import test_KS

"""
- creo una cartella denominata come il video
- 3 file .pkl per le statistiche 1,2,3
- - stats_CAM_data
- - stats_real_gaze_data
- - stats_low_level_saliency_data
"""

# if len(sys.argv) > 1:
#     video_path = sys.argv[1]
#     # numero di frame minimi per una fissazione
#     duration_threshold = int(sys.argv[2])
#     # raggio di dispersione massima per farsi che i punti facciano parte di una fissazione
#     dispersion_threshold = int(sys.argv[3])
#     if not os.path.exists(video_path):
#         print("Missing file video: video path is not correct")
#         exit(0)
# else:
#     print("Missing parameter: path from this to directory to video")
#     exit(0)

def run(video_path, duration_threshold, dispersion_threshold):
    # features of video
    vidcap = cv2.VideoCapture(video_path)
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    print("-----------------\nFEATURES OF VIDEO\nHEIGHT: "+str(height)+
          "\nWIDTH: "+str(width)+"\nFPS: "+str(fps))

    print("\nI-DT ALGORITHM PARAMS")
    print("DURATION THRESHOLD: " +str(duration_threshold) + " (frame)")
    print("DISPERSION THRESHOLD: " +str(dispersion_threshold) + " (pixel)")

    result_path = "result/" + video_path.split('\\')[-1].split(".")[0]
    if not os.path.exists("result"):
        os.makedirs("result")
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    # COMPUTING DATA -->  RG_data, CNN_data, LLS_data
    print("\n--------------------------")
    print("REAL DATA ELABORATION ...")
    if not os.path.exists(result_path + "/RG_data.pkl"):
        print("RG_data computing")
        # ottengo i valori medi degli utenti che hanno visto i video
        RG_data = RG_elaboration.run(video_path)
        pkl.dump(RG_data, open(result_path + "/RG_data.pkl", "wb"))
    else:
        print("RG_data already computed")
        RG_data = pkl.load(open(result_path + "/RG_data.pkl", "rb"))

    print("\nLLS ELABORATION ...")
    if not os.path.exists(result_path+"/LLS_data.pkl"):
        print("LLS_data computing")
        LLS_data = LLS_elaboration.run(video_path, result_path)
        pkl.dump(LLS_data, open(result_path+"/LLS_data.pkl", "wb"))
    else:
        print("LLS_data already computed")
        LLS_data = pkl.load(open(result_path + "/LLS_data.pkl", "rb"))

    print("\nCNN ELABORATION ...")
    CNN_data = {}
    for model_CAM in mod_CAM_names.keys():
        print("Model CNN: "+mod_CAM_names[model_CAM])
        if not os.path.exists(result_path+"/CAM_data_mod_"+str(model_CAM)+".pkl"):
            print("CNN data computing")
            CNN_data[mod_CAM_names[model_CAM]] = CNN_elaboration.run(video_path, result_path, model_CAM)
            pkl.dump(CNN_data, open(result_path + "/CAM_data_mod_" + str(model_CAM) + ".pkl", "wb"))
        else:
            print("CNN data already computed")
            CNN_data[mod_CAM_names[model_CAM]] = pkl.load(open(result_path + "/CAM_data_mod_" + str(model_CAM) + ".pkl", "rb"))



    # -------------------------------------------------
    print("\n----------------------------------------------------------------------")
    print("COMPUTING STATS: TIME FIXATION, SACADES AMPLITUDES, SACADES DIRECTIONS")
    result_test_pearson = {}

    # RG STATS COMPUTING -----------------------------------------------------------------------------------------
    print("RG stats of all users computing")
    RG_stats_all_users = RG_elaboration.calculate_stats(RG_data, duration_threshold, dispersion_threshold,
                                                        height, width, fps, step_sw, step_sd)

    # creazione lista di utenti su cui calcolare le statisitche dell'utente medio
    # parameters:
    # - utenti con l'errore minore (senza parametri)
    list_users, f_descr = RG_select_users.createListUsers()
    # statistiche dell'utente medio
    print("RG stats of average user computing")
    RG_av_stats = RG_average_user.run(RG_stats_all_users, list_users, step_sw, step_sd)

    pkl.dump(RG_av_stats, open(result_path+"/RG_stats_"+str(duration_threshold)+"_"+str(dispersion_threshold)+".pkl", "wb"))

    # LLS STATS COMPUTING -----------------------------------------------------------------------------------------
    print("LLS stats computing")
    LLS_stats = gaze_detector_IDT.run(LLS_data, duration_threshold, dispersion_threshold,
                                          height, width, fps, step_sw, step_sd)

    pkl.dump(LLS_stats, open(result_path+"/LLS_stats_"+str(duration_threshold)+"_"+str(dispersion_threshold)+".pkl", "wb"))
    result_test_pearson["lls"] = {}
    result_test_pearson["lls"] = test_PC.run(LLS_stats, RG_av_stats)

    # CNN STATS COMPUTING -----------------------------------------------------------------------------------------
    for model_CAM in mod_CAM_names.keys():
        print(mod_CAM_names[model_CAM] + " stats computing")
        CAM_stats = gaze_detector_IDT.run(CNN_data[mod_CAM_names[model_CAM]], duration_threshold, dispersion_threshold,
                                          height, width, fps, step_sw, step_sd)
        pkl.dump(CAM_stats,
                 open(result_path + "/CNN_stats_mod_"+str(model_CAM)+ "_" + str(duration_threshold) + "_" +
                      str(dispersion_threshold) + ".pkl", "wb"))
        result_test_pearson[mod_CAM_names[model_CAM]] = {}
        result_test_pearson[mod_CAM_names[model_CAM]] = test_PC.run(CAM_stats, RG_av_stats)

    if not os.path.exists(result_path+"/test"):
        os.makedirs(result_path+"/test")
    pkl.dump(result_test_pearson, open(result_path+"/test/result_pearson_"+str(duration_threshold)+"_"+
                                       str(dispersion_threshold)+".pkl", "wb"))
    print("\n------------------------------")
    print("COMPUTING PEARSON COEFFICIENT")

    for feature in features:
        print("-------------------")
        print(plot_titles[feature])
        for method, ccp in sorted([(method, result_test_pearson[method][feature])for method in result_test_pearson], key=lambda x: x[1], reverse=True):
            # if ccp[1]>0.05:
            #     print("------ NOT SIGNIFICANT", ccp[1])
            print(method.upper(), ccp[0])

