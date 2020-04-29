import pickle as pkl
import matplotlib.pyplot as plt
import numpy as np
"""
PLOT dei risultati ottenuti dal calcolo del coefficiente di correlazione di Pearson (CCP) medio dei video presi in esame
Per ogni feature (tempi di fissazione, ampiezza delle saccadi, direzione delle saccadi), per ogni metodi (CAMs, LLS), 
per ogni iterazione dei parametri dell'algortimo I-DT
"""

features = ['time_fixations', 'saccades_width', 'saccades_directions']
mod_CAM_names = {
    1: "squeezenet",
    2: "resnet",
    3: "densenet"
}
plot_titles = {
    "time_fixations": "TIME FIXATIONS",
    "saccades_width": "SACCADES WIDTH",
    "saccades_directions": "SACCADES DIRECTIONS"
}


# result_test = pkl.load(open("result/test_all_videos/result_test_pearson_all_videos.pkl", "rb"))
def run(result_test):
    print("\n---------------------------------------------------------------------------------")
    print("COMPUTING CCP MEAN RESPECT ALL VIDEOS AND ALL ITERATIONS OF I-DT ALGORITHM PARAMS")
    for feature in features:
        result_lls = []
        result_cam1 = []
        result_cam2 = []
        result_cam3 = []

        for k in result_test.keys():
            lls_tf = {video: result_test[k][video]["lls"][feature][0] for video in
                      list(result_test[k].keys())}
            cam1_tf = {video: result_test[k][video]["squeezenet"][feature][0] for video in
                       list(result_test[k].keys())}
            cam2_tf = {video: result_test[k][video]["resnet"][feature][0] for video in
                       list(result_test[k].keys())}
            cam3_tf = {video: result_test[k][video]["densenet"][feature][0] for video in
                       list(result_test[k].keys())}

            # print(k)
            # print("LLS: ", np.mean([v for v in list(lls_tf.values()) if not np.isnan(v)]))
            result_lls.append(np.mean([v for v in list(lls_tf.values()) if not np.isnan(v)]))

            # print("CAM1: ", np.mean([v for v in list(cam1_tf.values()) if not np.isnan(v)]))
            result_cam1.append(np.mean([v for v in list(cam1_tf.values()) if not np.isnan(v)]))

            # print("CAM2: ", np.mean([v for v in list(cam2_tf.values()) if not np.isnan(v)]))
            result_cam2.append(np.mean([v for v in list(cam2_tf.values()) if not np.isnan(v)]))

            # print("CAM3: ", np.mean([v for v in list(cam3_tf.values()) if not np.isnan(v)]))
            result_cam3.append(np.mean([v for v in list(cam3_tf.values()) if not np.isnan(v)]))

        plt.plot(range(len(result_lls)), sorted(result_lls), label="LLS")
        plt.plot(range(len(result_cam1)), sorted(result_cam1), label="Squeezenet")
        plt.plot(range(len(result_cam2)), sorted(result_cam2), label="Resnet")
        plt.plot(range(len(result_cam3)), sorted(result_cam3), label="Densenet")
        plt.title(plot_titles[feature], fontsize=25)
        plt.xlabel("Iteration of I-DT algorithm params", fontsize=30)
        plt.xticks(fontsize=18)
        plt.ylabel("Average CCP", fontsize=30)
        plt.yticks(fontsize=18)
        plt.legend(fontsize=25)
        plt.show()

        print(plot_titles[feature])
        for method, ccp in sorted([("LLS", np.mean(result_lls)),
         ("Squeezenet", np.mean(result_cam1)),
         ("Resnet", np.mean(result_cam2)),
         ("Densenet", np.mean(result_cam3))], key=lambda x: x[1], reverse=True):
            print(method, ccp)
        print("-------------------")