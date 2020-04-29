import pprint

from scipy import stats


def run(mod_stats, RG_stats):
    if len(RG_stats["mean_user_time_fixations"].keys()) == 0:
        print("--------------------------------- RG_stats EMPTY")
    key_set_tf = set(list(mod_stats["time_fixations"].keys()) + list(RG_stats["mean_user_time_fixations"]))
    RG_freq_tf = [RG_stats["mean_user_time_fixations"][k] if
               RG_stats["mean_user_time_fixations"].get(k) is not None else 0
               for k in key_set_tf]
    mod_freq_tf = [mod_stats["time_fixations"][k] if
               mod_stats["time_fixations"].get(k) is not None else 0
               for k in key_set_tf]
    """print("time_fixations")
    print(RG_stats["mean_user_time_fixations"])
    print(RG_freq_tf)
    print("-----------------------")
    print(mod_stats["time_fixations"])
    print(mod_freq_tf)
    pprint.pprint(stats.pearsonr(RG_freq_tf, mod_freq_tf))
    pprint.pprint(stats.pearsonr(sorted(RG_freq_tf), sorted(mod_freq_tf)))"""

    key_set_sw = set(list(mod_stats["saccades_width"].keys()) + list(RG_stats["mean_user_saccades_width"]))
    RG_freq_sw = [RG_stats["mean_user_saccades_width"][k] if
                  RG_stats["mean_user_saccades_width"].get(k) is not None else 0
                  for k in key_set_sw]
    mod_freq_sw = [mod_stats["saccades_width"][k] if
                   mod_stats["saccades_width"].get(k) is not None else 0
                   for k in key_set_sw]
    # print("saccades_width")
    # pprint.pprint(stats.pearsonr(RG_freq_sw, mod_freq_sw))

    key_set_sd = set(list(mod_stats["saccades_directions"].keys()) + list(RG_stats["mean_user_saccades_directions"]))
    RG_freq_sd = [RG_stats["mean_user_saccades_directions"][k] if
                  RG_stats["mean_user_saccades_directions"].get(k) is not None else 0
                  for k in key_set_sd]
    mod_freq_sd = [mod_stats["saccades_directions"][k] if
                   mod_stats["saccades_directions"].get(k) is not None else 0
                   for k in key_set_sd]
    # print("saccades_directions")
    # pprint.pprint(stats.pearsonr(RG_freq_sd, mod_freq_sd))

    result = {
        "time_fixations": tuple(stats.pearsonr(RG_freq_tf, mod_freq_tf)),
        "saccades_width": tuple(stats.pearsonr(RG_freq_sw, mod_freq_sw)),
        "saccades_directions": tuple(stats.pearsonr(RG_freq_sd, mod_freq_sd))
    }
    return result

