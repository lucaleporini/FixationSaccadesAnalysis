import pickle as pkl
import matplotlib.pyplot as plt
import numpy as np
import pprint

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


# result_test = pkl.load(open("result/v01_Hugo_2172_left/test/result_test_pearson.pkl", "rb"))
def run(result_test):
    result_mean_CCP = {}
    for feature in features:
        result_lls = []
        result_cnn1 = []
        result_cnn2 = []
        result_cnn3 = []
        for k in result_test.keys():
            result_lls.append(result_test[k]["lls"][feature][0])
            result_cnn1.append(result_test[k][mod_CAM_names[1]][feature][0])
            result_cnn2.append(result_test[k][mod_CAM_names[2]][feature][0])
            result_cnn3.append(result_test[k][mod_CAM_names[3]][feature][0])

        result_mean_CCP[feature] = sorted([("lls", np.mean(result_lls)),
                                           (mod_CAM_names[1], np.mean(result_cnn1)),
                                           (mod_CAM_names[2], np.mean(result_cnn2)),
                                           (mod_CAM_names[3], np.mean(result_cnn3))],
                                          key=lambda x: x[1], reverse=True)
        plt.plot(range(len(result_lls)), sorted(result_lls), label="LLS")
        plt.plot(range(len(result_cnn1)), sorted(result_cnn1), label="Squeezenet")
        plt.plot(range(len(result_cnn2)), sorted(result_cnn2), label="Resnet")
        plt.plot(range(len(result_cnn3)), sorted(result_cnn3), label="Densenet")
        plt.title(plot_titles[feature], fontsize=25)
        plt.xlabel("Iteration of I-DT algorithm params", fontsize=30)
        plt.xticks(fontsize=18)
        plt.ylabel("CCP", fontsize=30)
        plt.yticks(fontsize=18)
        plt.legend(fontsize=25)
        plt.show()

    print("\nCALCULATING MEAN PEARSON COEFFICIENT ON ITERATION OF PARAMETERS OF I-DT ALGORITHM")
    for feature in features:
        print(plot_titles[feature])
        for method, ccp in result_mean_CCP[feature]:
            print(method, ccp)
        print("---------------------")
