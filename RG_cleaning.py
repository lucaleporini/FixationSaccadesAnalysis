import csv
import matplotlib.pyplot as plt
import pickle as pkl


def selectUserWithMinimumError(raw_data, error_users):
    list_users = {}
    last = None
    for user_key, error in error_users.items():
        if last is not None:
            user = user_key.split("_")[0]
            last_user = last[0].split("_")[0]
            if last_user == user:
                if last[1] > error:
                    list_users.pop(last[0])
                    list_users[user_key] = error
            else:
                last = (user_key, error)
                list_users[user_key] = error
        else:
            last = (user_key, error)
            list_users[user_key] = error

    raw_data_cleaned = {k: raw_data[k] for k in list(list_users.keys())}
    return raw_data_cleaned, list_users


# CREAZIONE raw_data_cleaned.pkl, error_users.pkl ####################################################################
def reverseUserVideoToVideoUser(raw_data):
    raw_data_cleaned_reverse = {}
    for user in raw_data.keys():
        for video in raw_data[user].keys():
            if video not in raw_data_cleaned_reverse.keys():
                raw_data_cleaned_reverse[video] = {}
                raw_data_cleaned_reverse[video][user] = raw_data[user][video]
            else:
                raw_data_cleaned_reverse[video][user] = raw_data[user][video]
    return raw_data_cleaned_reverse


def run(list_video, list_user, error_threshold):
    print("- - - - preProcessingRawData() ")
    raw_data = {}
    error_users = {}
    for user in list_user:
        print("- - - - - - USER --> "+user)
        count_error_user = 0
        data_user = {}

        for video in list_video:
            # Eye movement from eye tracker
            with open("real_gaze_data/raw_gaze_data/" + video + user + ".txt") as file:
                reader = csv.reader(file, delimiter="\t")

                # controllo che i dati di un occhio non siano tutti a (0,0)
                # se l'occhio SX presenta almeno un valore diverso da zero, condidero i dati dall'occhio SX
                # altrimenti considero i dati presi dall'occhio DX dell'osservatore

                # all_zerosL --> controlla i valori dell'occhio sx
                # all_zerosR --> controlla i valori per l'occhio dx

                all_zerosL = True
                data = []
                for point in reader:
                    data.append((float(point[0]), float(point[1]), float(point[2])))
                    if float(point[1]) != 0 or float(point[2]) != 0:
                        all_zerosL = False

                if all_zerosL:
                    print("ALL ZEROS LEFT EYE:", video, " ---- ", user)
                    data = []
                    all_zerosR = True
                    for point in reader:
                        data.append((float(point[0]), float(point[3]), float(point[4])))
                        if float(point[3]) != 0 or float(point[4]) != 0:
                            all_zerosR = False
                    if all_zerosR:
                        print("ALL ZEROS RIGHT EYE:", video, " ---- ", user)

                    # se tutti i valori (sia dell'occhio dx sia dell'occhio sx) sono nulli
                    # allore il dataset non è utilizzabile
                    if all_zerosL and all_zerosR:
                        print("FILE NOT ALLOWED: " + video + " ---- " + user)

            # Selezione di un punto ogni 20 in modo da avere una rilevazione per frame
            real_gaze_data = [data[i] for i in range(9, len(data), 20)]
            real_gaze_data_frame = [(i, real_gaze_data[i][1], real_gaze_data[i][2]) for i in
                                    range(0, len(real_gaze_data))]
            data_user[video] = real_gaze_data_frame

            # contatore degli errori (frame) commessi da un utente relativo a un singolo video
            count_error_video = 0
            for i in range(0, len(real_gaze_data_frame)):
                # controllo se:
                # - le coordinate x e y sono 0
                # - le coordinate x e y si trovano al di fuori del piano immagine
                if (real_gaze_data_frame[i][1] == 0 and real_gaze_data_frame[i][2] == 0) or (
                        real_gaze_data_frame[i][1] < 0 or real_gaze_data_frame[i][1] > 1920
                        or real_gaze_data_frame[i][2] < 0 or real_gaze_data_frame[i][2] > 1080):
                    count_error_video += 1

            # normalizzazione degli errori (frame) sui frame totali del video (valori cumulati)
            if not len(real_gaze_data_frame) == 0:
                count_error_user += count_error_video/len(real_gaze_data_frame)
            else:
                count_error_user += 1

        # normalizzazione degli errori commessi dall'utente, dividendo per il numero di frame di un video
        error_user = count_error_user/len(list_video)

        # controllo se il l'errore dell'utente è minore di una soglia
        if error_user <= error_threshold:
            raw_data[user] = {}
            raw_data[user] = data_user
            error_users[user] = error_user

        print("- - - - - - - ERROR:", error_user)

    raw_data_cleaned, error_users_updated = selectUserWithMinimumError(raw_data, error_users)

    return reverseUserVideoToVideoUser(raw_data_cleaned), error_users_updated


#######################################################################################################################
