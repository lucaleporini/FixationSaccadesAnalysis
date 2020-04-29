import pickle as pkl
import pprint
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np


def distributionInBins(distribution, step, min, max):
    result = {}
    bins = [(i, i + step) for i in list(range(min, max + step, step))]
    for bin in bins:
        freq = 0
        for w in distribution:
            if bin[0] <= w < bin[1]:
                freq += 1
        result[bin] = freq
    return result


def cdf(pr_distr):
    result = []
    sum = 0
    for i in range(len(pr_distr)):
        sum += pr_distr[i]
        result.append(sum)
    return result


def run(mod_stats, RG_stats):
    mod_sw = mod_stats["saccades_width"]
    RG_sw = RG_stats["mean_user_saccades_width"]

    mod_sd = mod_stats["saccades_directions"]
    RG_sd = RG_stats["mean_user_saccades_directions"]

    # ---------------------------------------------------------------------------------------------------------------

    # time fixations probability distributions

    key_set = set(list(mod_stats["time_fixations"].keys()) + list(RG_stats["mean_user_time_fixations"]))
    RG_ps_time_fix = [
        RG_stats["mean_user_time_fixations"][k] / sum(RG_stats["mean_user_time_fixations"].values()) if
        RG_stats["mean_user_time_fixations"].get(k) is not None else 0
        for k in key_set]
    mod_ps_time_fix = [
        mod_stats["time_fixations"][k] / sum(mod_stats["time_fixations"].values()) if mod_stats["time_fixations"].get(
            k) is not None else 0
        for k in key_set]
    # LLS_ps_time_fix = [
    #    LLS_stats["time_fixations"][k] / sum(LLS_stats["time_fixations"].values()) if LLS_stats["time_fixations"].get(
    #        k) is not None else 0 for k in key_set]

    # saccades width probability distributions

    mod_ps_saccades_width = [v / sum(mod_sw.values()) for v in mod_sw.values()]
    RG_ps_saccades_width = [v / sum(RG_sw.values()) for v in RG_sw.values()]

    # saccades directions probability distributions
    mod_ps_saccades_direct = [v / sum(mod_sd.values()) for v in mod_sd.values()]
    RG_ps_saccades_direct = [v / sum(RG_sd.values()) for v in RG_sd.values()]

    # ---------------------------------------------------------------------------------------------------------------
    # plotting CDF of distributions

    """plt.plot(range(len(CAM_ps_saccades_width)), cdf(CAM_ps_saccades_width), color="red", label="CAM")
    plt.plot(range(len(RG_ps_saccades_width)), cdf(RG_ps_saccades_width), color="green", label="RG")
    plt.plot(range(len(LLS_ps_saccades_width)), cdf(LLS_ps_saccades_width), color="blue", label="LLS")
    plt.title("SACCADES WIDTH")
    plt.legend()
    plt.show()

    plt.plot(range(len(CAM_ps_time_fix)), cdf(CAM_ps_time_fix), color="red", label="CAM")
    plt.plot(range(len(RG_ps_time_fix)), cdf(RG_ps_time_fix), color="green", label="RG")
    plt.plot(range(len(LLS_ps_time_fix)), cdf(LLS_ps_time_fix), color="blue", label="LLS")
    plt.title("TIME FIXATIONS")
    plt.legend()
    plt.show()

    plt.plot(range(len(CAM_ps_saccades_direct)), cdf(CAM_ps_saccades_direct), color="red", label="CAM")
    plt.plot(range(len(RG_ps_saccades_direct)), cdf(RG_ps_saccades_direct), color="green", label="RG")
    plt.plot(range(len(LLS_ps_saccades_direct)), cdf(LLS_ps_saccades_direct), color="blue", label="LLS")
    plt.title("SACCADES DIRECTIONS")
    plt.legend()
    plt.show()"""

    """print("SACCADES WIDTH")
    print("- PS")
    print("CAM TO RG", stats.ks_2samp(CAM_ps_saccades_width, RG_ps_saccades_width))
    print("LLS TO RG", stats.ks_2samp(LLS_ps_saccades_width, RG_ps_saccades_width))
    print("- CDF")
    print("CAM TO RG", stats.ks_2samp(cdf(CAM_ps_saccades_width), cdf(RG_ps_saccades_width)))
    print("LLS TO RG", stats.ks_2samp(cdf(LLS_ps_saccades_width), cdf(RG_ps_saccades_width)))
    print("------------------------")
    print("TIME FIXATIONS")
    print("- PS")
    print("CAM TO RG", stats.ks_2samp(CAM_ps_time_fix, RG_ps_time_fix))
    print("LLS TO RG", stats.ks_2samp(LLS_ps_time_fix, RG_ps_time_fix))
    print("- CDF")
    print("CAM TO RG", stats.ks_2samp(cdf(CAM_ps_time_fix), cdf(RG_ps_time_fix)))
    print("LLS TO RG", stats.ks_2samp(cdf(LLS_ps_time_fix), cdf(RG_ps_time_fix)))
    print("------------------------")
    print("SACCADES DIRECTIONS")
    print("- PS")
    print("CAM TO RG", stats.ks_2samp(CAM_ps_saccades_direct, RG_ps_saccades_direct))
    print("LLS TO RG", stats.ks_2samp(LLS_ps_saccades_direct, RG_ps_saccades_direct))
    print("- CDF")
    print("CAM TO RG", stats.ks_2samp(cdf(CAM_ps_saccades_direct), cdf(RG_ps_saccades_direct)))
    print("LLS TO RG", stats.ks_2samp(cdf(LLS_ps_saccades_direct), cdf(RG_ps_saccades_direct)))
    """
    # ----------------------------------------------------------------------------------------------------------------
    result = {
        "time_fixations": tuple(stats.ks_2samp(cdf(mod_ps_time_fix), cdf(RG_ps_time_fix))),
        "saccades_width": tuple(stats.ks_2samp(cdf(mod_ps_saccades_width), cdf(RG_ps_saccades_width))),
        "saccades_directions": tuple(stats.ks_2samp(cdf(mod_ps_saccades_direct), cdf(RG_ps_saccades_direct)))
    }
    return result


"""CAM_data = pkl.load(open("result/v01_Hugo_2172_left/CAM_data_mod_1.pkl", "rb"))
# pprint.pprint(CAM_data)
CAM_stats = pkl.load(open("result/v01_Hugo_2172_left/CAM_stats_mod_3_3_5.pkl", "rb"))
RG_av_stats = pkl.load(open("result/v01_Hugo_2172_left/RG_av_stats_all_users_min_error_3_5.pkl", "rb"))
LLS_stats = pkl.load(open("result/v01_Hugo_2172_left/LLS_stats_3_5.pkl", "rb"))
run(CAM_stats, RG_av_stats, LLS_stats)"""