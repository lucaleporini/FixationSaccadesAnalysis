import pickle as pkl
import matplotlib.pyplot as plt
import pprint
import csv


def fromAbsoluteToRelativeFrequency(distribution):
    n = sum(distribution.values())
    if n > 0:
        return [freq / n for freq in list(distribution.values())]
    else:
        return []


def distributionInBins(distribution, step, min, max):
    result = {}
    bins = [(i, i + step) for i in list(range(min, max + step, step))]

    for bin in bins:
        freq = 0
        for w in distribution:
            if bin[0] <= w < bin[1]:
                freq += 1
        if result.get(bin) is None:
            result[bin] = freq
        else:
            result[bin] += freq
    return result


def run(CAM_stats, LLS_stats, RG_av_stats, video_path, result_path, step_sw, step_sd):
    plt.subplots(3, 3)
    plt.suptitle(video_path)

    """CAM DATA"""
    ###################################################################################################################
    # PLOT TEMPI DI FISSAZIONE

    plt.subplot2grid((3, 3), (0, 0))
    CAM_time_fixations = CAM_stats["time_fixations"]
    plt.bar(list(CAM_time_fixations.keys()), list(CAM_time_fixations.values()), width=0.01, bottom=0)
    plt.title("Time fixations")
    plt.ylabel("CAM_DATA")
    # plt.xlabel("Seconds (s)")

    ############################################################
    # PLOT AMPIEZZA SACCADI

    plt.subplot2grid((3, 3), (0, 1))
    CAM_saccades_width = CAM_stats["saccades_width"]
    # etichetta da apporre ad ogni barra del grafico
    bins_keys = []
    for sw_key in list(CAM_saccades_width.keys()):
        bins_keys.append(str(sw_key[0]) + "-" + str(sw_key[1]))

    # grafico delle frequenze delle ampiezze delle saccadi
    sw_xticks = bins_keys
    plt.xticks(range(0, len(bins_keys)), sw_xticks, rotation=90)
    plt.bar(range(0, len(bins_keys)), list(CAM_saccades_width.values()), width=1, bottom=0)
    # plt.plot(range(0, len(bins_keys)), list(mean_user_saccades_width.values()), "-o")
    plt.title("Saccade amplitudes")
    # plt.ylabel("Frequency")
    # plt.xlabel("Euclidean Distance")

    ############################################################
    # PLOT DIREZIONI SACCADI
    plt.subplot2grid((3, 3), (0, 2))
    CAM_directions_saccades = CAM_stats["saccades_directions"]
    # etichetta da apporre ad ogni barra del grafico
    bins_keys = []
    for k in list(CAM_directions_saccades.keys()):
        bins_keys.append(str(k[0]) + " | " + str(k[1]))
    # pprint.pprint(bins_keys)
    # grafico delle frequenze delle ampiezze delle saccadi
    my_xticks = bins_keys
    plt.xticks(range(0, len(bins_keys)), my_xticks, rotation=90)
    plt.bar(range(0, len(bins_keys)), list(CAM_directions_saccades.values()), width=0.8, bottom=0)
    # plt.plot(range(0, len(bins_keys)), list(mean_user_saccades_directions.values()), "-o")
    plt.title("Saccade directions")
    # plt.ylabel("Frequency")
    # plt.xlabel("Degrees")

    """REAL GAZE DATA"""
    ############################################################
    # PLOT TEMPI DI FISSAZIONE

    plt.subplot2grid((3, 3), (1, 0))
    RG_time_fixations = RG_av_stats["mean_user_time_fixations"]

    plt.bar(list(RG_time_fixations.keys()), list(RG_time_fixations.values()), width=0.01, bottom=0)
    # plt.title("Time fixations")
    plt.ylabel("DATI REALI")
    # plt.xlabel("Seconds (s)")

    ############################################################
    # PLOT AMPIEZZA SACCADI

    plt.subplot2grid((3, 3), (1, 1))
    RG_saccades_width = RG_av_stats["mean_user_saccades_width"]
    # etichetta da apporre ad ogni barra del grafico
    bins_keys = []
    for sw_key in list(RG_saccades_width.keys()):
        bins_keys.append(str(sw_key[0]) + "-" + str(sw_key[1]))

    # grafico delle frequenze delle ampiezze delle saccadi
    sw_xticks = bins_keys
    plt.xticks(range(0, len(bins_keys)), sw_xticks, rotation=90)
    plt.bar(range(0, len(bins_keys)), list(RG_saccades_width.values()), width=1, bottom=0)
    # plt.plot(range(0, len(bins_keys)), list(mean_user_saccades_width.values()), "-o")
    # plt.title("Saccade amplitudes")
    # plt.ylabel("Frequency")
    # plt.xlabel("Euclidean Distance")

    ############################################################
    # PLOT DIREZIONI SACCADI
    plt.subplot2grid((3, 3), (1, 2))
    RG_saccades_directions = RG_av_stats["mean_user_saccades_directions"]

    """n_saccades_directions = 0
    for d in mean_user_saccades_width.values():
        n_saccades_directions += d

    mean_user_saccades_directions_relative = []
    if n_saccades_width is not 0:
        mean_user_saccades_directions_relative = [freq / n_saccades_directions for freq in
                                                  list(mean_user_saccades_directions.values())]
    """
    # etichetta da apporre ad ogni barra del grafico
    bins_keys = []
    for k in list(RG_saccades_directions.keys()):
        bins_keys.append(str(k[0]) + " | " + str(k[1]))
    # pprint.pprint(bins_keys)
    # grafico delle frequenze delle ampiezze delle saccadi
    my_xticks = bins_keys
    plt.xticks(range(0, len(bins_keys)), my_xticks, rotation=90)
    plt.bar(range(0, len(bins_keys)), list(RG_saccades_directions.values()), width=0.8, bottom=0)
    # plt.plot(range(0, len(bins_keys)), list(mean_user_saccades_directions.values()), "-o")
    # plt.title("Saccade directions")
    # plt.ylabel("Frequency")
    # plt.xlabel("Degrees")

    """LOW LEVEL SALIENCY"""
    ############################################################
    # PLOT TEMPI DI FISSAZIONE

    plt.subplot2grid((3, 3), (2, 0))
    LLS_time_fixations = LLS_stats["time_fixations"]
    """n_time_fixations = 0
    for f in mean_user_time_fixations.values():
        n_time_fixations += f
    mean_user_time_fixations_relative = [freq / n_time_fixations for freq in list(mean_user_time_fixations.values())]
    """
    plt.bar(list(LLS_time_fixations.keys()), list(LLS_time_fixations.values()), width=0.01, bottom=0)
    # plt.title("Time fixations")
    plt.ylabel("LOW LEVEL")
    # plt.xlabel("Seconds (s)")

    ############################################################
    # PLOT AMPIEZZA SACCADI

    plt.subplot2grid((3, 3), (2, 1))
    LLS_saccades_width = LLS_stats["saccades_width"]
    # etichetta da apporre ad ogni barra del grafico
    """n_saccades_width = 0
    for s in mean_user_saccades_width.values():
        n_saccades_width += s

    mean_user_saccades_width_relative = []
    if n_saccades_width is not 0:
        mean_user_saccades_width_relative = [freq / n_saccades_width for freq in
                                             list(mean_user_saccades_width.values())]
    """
    bins_keys = []
    for sw_key in list(LLS_saccades_width.keys()):
        bins_keys.append(str(sw_key[0]) + "-" + str(sw_key[1]))

    # grafico delle frequenze delle ampiezze delle saccadi
    sw_xticks = bins_keys
    plt.xticks(range(0, len(bins_keys)), sw_xticks, rotation=90)
    plt.bar(range(0, len(bins_keys)), list(LLS_saccades_width.values()), width=1, bottom=0)
    # plt.plot(range(0, len(bins_keys)), list(mean_user_saccades_width.values()), "-o")
    # plt.title("Saccade amplitudes")
    # plt.ylabel("Frequency")
    # plt.xlabel("Euclidean Distance")

    ############################################################
    # PLOT DIREZIONI SACCADI
    plt.subplot2grid((3, 3), (2, 2))
    LLS_saccades_directions = LLS_stats["saccades_directions"]

    """n_saccades_directions = 0
    for d in mean_user_saccades_width.values():
        n_saccades_directions += d

    mean_user_saccades_directions_relative = []
    if n_saccades_width is not 0:
        mean_user_saccades_directions_relative = [freq / n_saccades_directions for freq in
                                                  list(mean_user_saccades_directions.values())]
    """
    # etichetta da apporre ad ogni barra del grafico
    bins_keys = []
    for k in list(LLS_saccades_directions.keys()):
        bins_keys.append(str(k[0]) + " | " + str(k[1]))
    # pprint.pprint(bins_keys)
    # grafico delle frequenze delle ampiezze delle saccadi
    my_xticks = bins_keys
    plt.xticks(range(0, len(bins_keys)), my_xticks, rotation=90)
    plt.bar(range(0, len(bins_keys)), list(LLS_saccades_directions.values()), width=0.8, bottom=0)
    # plt.plot(range(0, len(bins_keys)), list(mean_user_saccades_directions.values()), "-o")
    # plt.title("Saccade directions")
    # plt.ylabel("Frequency")
    # plt.xlabel("Degrees")

    plt.savefig(result_path+'/plotResult.png', dpi=300)
    plt.show()


