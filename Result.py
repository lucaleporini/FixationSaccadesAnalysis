import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import pprint
features = ['time_fixations', 'saccades_width', 'saccades_directions']
mod_CAM_names = {
    1: "squeezenet",
    2: "resnet",
    3: "densenet"
}
plot_titles = {
    "time_fixations": "TIME FIXATIONS",
    "saccades_width": "SACADES AMPLITUDES",
    "saccades_directions": "SACADES DIRECTIONS"
}

result_test = pkl.load(open("result/test_all_videos/result_test_pearson_all_videos.pkl", "rb"))
def run(result_test):
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
            result_lls.append((k, np.mean([v for v in list(lls_tf.values()) if not np.isnan(v)])))

            # print("CAM1: ", np.mean([v for v in list(cam1_tf.values()) if not np.isnan(v)]))
            result_cam1.append((k, np.mean([v for v in list(cam1_tf.values()) if not np.isnan(v)])))

            # print("CAM2: ", np.mean([v for v in list(cam2_tf.values()) if not np.isnan(v)]))
            result_cam2.append((k, np.mean([v for v in list(cam2_tf.values()) if not np.isnan(v)])))

            # print("CAM3: ", np.mean([v for v in list(cam3_tf.values()) if not np.isnan(v)]))
            result_cam3.append((k, np.mean([v for v in list(cam3_tf.values()) if not np.isnan(v)])))
        # print(result_lls)
        for i in [0, 6, 7, 13, 14, 20, 21, 27]:
        # for i in [-0.5, 6.5, 13.5, 20.5, 27.5]:
            plt.axvline(x=i, linewidth=0.8, color='black', ls="--")
        plt.plot(range(len(result_lls)), [x[1] for x in result_lls], label="LLS", marker=".", linestyle="-", markersize=10)
        plt.plot(range(len(result_cam1)), [x[1] for x in result_cam1], label="Squeezenet", marker=".", linestyle="-", markersize=10)
        plt.plot(range(len(result_cam2)), [x[1] for x in result_cam2], label="Resnet", marker=".", linestyle="-", markersize=10)
        plt.plot(range(len(result_cam3)), [x[1] for x in result_cam3], label="Densenet", marker=".", linestyle="-", markersize=10)
        plt.title(plot_titles[feature], fontsize=25)
        plt.xlabel("Iteration of I-DT algorithm params", fontsize=25)
        plt.xticks(range(len(result_lls)), [x[0] for x in result_lls], fontsize=18, rotation=45)
        plt.ylabel("Average CCP of videos in exam", fontsize=25)
        plt.yticks(fontsize=18)
        plt.legend(fontsize=20)
        plt.grid(True, lw=0.3)
        plt.show()

        #for i in [0.3, 0.7, 1]:
        # for i in [-0.5, 6.5, 13.5, 20.5, 27.5]:
        if feature == "time_fixations": plt.hlines([0.7], 0, 27, linestyle="--")
        elif feature == "saccades_width": plt.hlines([0.3, 0.7], 0, 27, linestyle="--")
        else: plt.hlines([0.3], 0, 27, linestyle="--")
        plt.plot(range(len(result_lls)), sorted([x[1] for x in result_lls]), label="LLS", marker=".", linestyle="-", markersize=10)
        plt.plot(range(len(result_cam1)), sorted([x[1] for x in result_cam1]), label="Squeezenet", marker=".", linestyle="-", markersize=10)
        plt.plot(range(len(result_cam2)), sorted([x[1] for x in result_cam2]), label="Resnet", marker=".", linestyle="-", markersize=10)
        plt.plot(range(len(result_cam3)), sorted([x[1] for x in result_cam3]), label="Densenet", marker=".", linestyle="-", markersize=10)
        plt.title(plot_titles[feature]+" (SORTED)", fontsize=25)
        plt.xlabel("Iteration of I-DT algorithm params", fontsize=25)
        plt.xticks(fontsize=18)
        plt.ylabel("Average CCP of videos in exam", fontsize=25)
        plt.yticks(fontsize=18)
        plt.legend(fontsize=20)
        plt.grid(True, lw=0.3)
        plt.show()


run(result_test)