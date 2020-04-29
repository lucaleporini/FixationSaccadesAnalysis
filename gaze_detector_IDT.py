import math

# crea sotto-liste di raw data per eliminare i dati ruomorosi
# D: Perchè sotto-liste? perchè in questo modo viene mantenuta la consistenza nel rilevamento di fissazioni e saccadi
# (interrompendo di fatto un fissazione e creando una saccade)
def cleanRawData(raw_data, height, width):
    raw_data_sublists = []
    sublist_temp = []
    for i in range(0, len(raw_data)):
        # controllo se le coordinate x e y sono 0 o al di fuori dallo schermo
        if (raw_data[i][1] == 0 and raw_data[i][2] == 0) or (
                raw_data[i][1] < 0 or raw_data[i][1] > width or raw_data[i][2] < 0 or raw_data[i][2] > height):
            if len(sublist_temp) != 0:
                # aggiungo la sotto lista in modo da rimuovere i dati "sporchi"
                raw_data_sublists.append(sublist_temp)
                sublist_temp = []
        else:
            sublist_temp.append(raw_data[i])
    if len(sublist_temp) != 0:
        raw_data_sublists.append(sublist_temp)
    return raw_data_sublists


def calculate_centroid(fixation_window):
    x_centroid = sum([p[1] for p in fixation_window])/len(fixation_window)
    y_centroid = sum([p[2] for p in fixation_window])/len(fixation_window)
    return x_centroid, y_centroid


def calculate_centroid_bb(fixation_window):
    x = [p[1] for p in fixation_window]
    y = [p[2] for p in fixation_window]
    return (max(x)+min(x))/2, (max(y)+min(y))/2


def calculate_distance(centroid, p):
    return math.hypot(centroid[0] - p[1], centroid[1] - p[2])


def calculate_radius(centroid, fixation_window):
    return max([calculate_distance(centroid, p) for p in fixation_window])


def idt(raw_data, duration_threshold, dispersion_threshold):
    fixations = []
    while not len(raw_data) < duration_threshold:
        index = duration_threshold
        fixation_window = raw_data[0:index]
        centroid = calculate_centroid_bb(fixation_window)

        while calculate_radius(centroid, fixation_window) <= dispersion_threshold and len(raw_data) > index:
            index += 1
            fixation_window = raw_data[0:index]
            centroid = calculate_centroid_bb(fixation_window)

        if len(fixation_window) > duration_threshold:
            del raw_data[:len(fixation_window)-1]
            fixations.append(fixation_window[:-1])

        else:
            fixations.append([raw_data.pop(0)])

    # add remaing saccades points
    if not len(raw_data) == 0:
        fixations += [[r] for r in raw_data]
    return fixations


def calculate_distance_saccades(eye_mov1, eye_mov2):
    centroid1 = calculate_centroid_bb(eye_mov1)
    centroid2 = calculate_centroid_bb(eye_mov2)
    return math.hypot(centroid1[0] - centroid2[0], centroid1[1] - centroid2[1])


def calculate_directions_saccades(eye_mov1, eye_mov2):
    centroid1 = calculate_centroid_bb(eye_mov1)
    centroid2 = calculate_centroid_bb(eye_mov2)
    return math.degrees(math.atan2(centroid2[1] - centroid1[1], centroid2[0] - centroid1[0]))


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


def run(raw_data, duration_threshold, dispersion_threshold, height, width, fps, step_sw, step_sd):
    raw_data_sublists = cleanRawData(raw_data, height, width)
    eye_mov = []
    for sublist in raw_data_sublists:
        eye_mov += idt(sublist, duration_threshold, dispersion_threshold)

    # print("IDT: N FISSAZIONI ", len(eye_mov))
    stats = {"time_fixations": {}, "saccades_width": [], "saccades_directions": []}
    for i in range(0, len(eye_mov) - 1):
        # 1 point rappresent saccade point
        if len(eye_mov[i]) > 1:
            if stats["time_fixations"].get(len(eye_mov[i])/fps):
                stats["time_fixations"][len(eye_mov[i])/fps] += 1
            else:
                stats["time_fixations"][len(eye_mov[i])/fps] = 1

        stats["saccades_width"].append(calculate_distance_saccades(eye_mov[i], eye_mov[i + 1]))
        stats["saccades_directions"].append(calculate_directions_saccades(eye_mov[i], eye_mov[i + 1]))

    if len(stats["saccades_width"]) == 0:
        print("saccades_width EMPTY")
    stats["saccades_width"] = distributionInBins(stats["saccades_width"], step_sw, 0,
                                    int(max(stats["saccades_width"])))

    if len(stats["saccades_directions"]) == 0:
        print("saccades_directions EMPTY")
    stats["saccades_directions"] = distributionInBins(stats["saccades_directions"], step_sd, -180, 180)

    return stats


"""raw_data_cleaned = pkl.load(open(str("raw_data_cleaned/raw_data_cleaned.pkl"), 'rb'))
points = raw_data_cleaned["v01_Hugo_2172_"]["u001_m_21_1_bwd"]
points_sublist = cleanRawData(points, height=1080, width=1920)
CAM_data = pkl.load(open("result\\v01_Hugo_2172_left\\CAM_data_mod_1.pkl", 'rb'))
CAM_data_sublist = cleanRawData(CAM_data, height=1080, width=1920)

stats = run(points, 5, 5, 1080, 1920)
pprint.pprint(stats)"""
