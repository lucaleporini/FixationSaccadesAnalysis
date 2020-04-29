"""
QUESTO SCRIPT PYTHON PERMETTE DI TRASFORMARE I RAW DATA OTTENUTI DA EYE TRACKER
VENGONO PULITI DA VALORI DI BLINK (0,0) E DA VALORI NON AMMESSI O FUORI DALLO SCHERMO
VENGONO CALCOLATE DISTRIBUZIONI SULLA BASE DELLA MEDIA DEGLI UTENTI --> SOMMA DELLE FREQUENZE / N° DI UTENTI
"""

# OBIETTIVO: individuare statistiche dell'utente medio che osserva il video

# stats_raw_data_cleaned.pkl --> file che presente le statistiche dei singoli utenti per ogni video
# sotto forma di dizionario
# Ogni file.pkl rappresenta un determinato video. In ogni file.pkl è presente il seguente formato:
# {
#       "video_1": {
#                      "user_1": {
#                                   "raw_data_sublists": ...
#                                   "blink": ...
#                                   "time_fixations": ...
#                                   "width_saccades": ...
#                                   "saccades_directions": ...
#                       },
#                       "user_N": { ... }
#       },
#       "video_N": { ... }
# }
#
#
# "mean_user_time_fixations" rappresenta i tempi di fissazione dell'utente medio. Presenta il seguente formato:
# { K0: V0, ... , Kn: Vn} dove:
# -> Ki rappresenta i tempi di fissazione in secondi (0.04, 0.08, ....)
# -> Vi rappresenta la frequenza di fissazioni con tempo Ki dell'utente medio
#
#
# "mean_user_saccades_width" rappresenta le ampiezze delle saccadi dell'utente medio. Presenta il seguente formato:
# { K0: V0, ... , Kn: Vn} dove:
# -> Ki rappresenta l'intervallo di distanze (Ki-1, Ki]. K0 rappresenta un intervallo (0, K0]
# -> Vi rappresenta la frequenza di ampiezze delle saccade che ricando nell'intervallo definito da Ki


# parametri per l'esecuzione delle statistiche
# list_users (dict) --> lista di utenti sulla quale effettuare le statistiche
# step_sw (int) --> bins per la creazione della distribuzione delle ampiezze delle saccadi --> distanza euclidea
# step_sd (int) --> bins per la creazione della distribuzione delle direzioni delle saccadi --> gradi
import pprint


def run(stats_video, list_users, step_sw, step_sd):
    # print("compute RG_average_user.py")
    # fattore di normalizzazione per le statistiche
    n_users = len(list_users)

    # statistche per l'utente medio
    mean_users_stats = {}

    # fissazioni dell'utente MEDIO rispetto al singolo video
    mean_user_time_fixations = {}
    mean_user_blink = {}
    mean_user_saccades_width = {}
    mean_user_saccades_directions = {}

    for k_user in list(list_users.keys()):
        # caricamento di "mean_user_time_fixations"
        # somma cumultate delle frequenze dei tempi di fissazione (espressi in secondi)
        for k_fixation in stats_video[k_user]["time_fixations"].keys():
            if mean_user_time_fixations.get(k_fixation) is None:
                mean_user_time_fixations[k_fixation] = stats_video[k_user]["time_fixations"][k_fixation]
            else:
                mean_user_time_fixations[k_fixation] += stats_video[k_user]["time_fixations"][k_fixation]

        """ caricamento di "mean_user_blink"
        # somma cumultate delle frequenze dei tempi di blink (espressi in secondi)
        for k_blink in stats_video[k_user]["blink"].keys():
            if mean_user_blink.get(k_blink) is None:
                mean_user_blink[k_blink] = stats_video[k_user]["blink"][k_blink]
            else:
                mean_user_blink[k_blink] += stats_video[k_user]["blink"][k_blink]"""

        # popolamento delle ampiezze delle saccadi di tutti gli utenti --> CUMULATA
        for k in list(stats_video[k_user]["saccades_width"].keys()):
            if mean_user_saccades_width.get(k) is None:
                mean_user_saccades_width[k] = stats_video[k_user]["saccades_width"][k]
            else:
                mean_user_saccades_width[k] += stats_video[k_user]["saccades_width"][k]

        # popolamento delle direzioni delle saccadi --> CUMULATA

        for k in stats_video[k_user]["saccades_directions"].keys():
            if mean_user_saccades_directions.get(k) is None:
                mean_user_saccades_directions[k] = stats_video[k_user]["saccades_directions"][k]
            else:
                mean_user_saccades_directions[k] += stats_video[k_user]["saccades_directions"][k]

    # ---------------------------------------------------------------------------------------------------

    # TIME FIXATION
    # normalizzo per il numero di utenti
    mean_user_time_fixations = {k: v / n_users for k, v in mean_user_time_fixations.items()}
    # ordino il dizionario per chiave
    mean_user_time_fixations = dict(sorted(mean_user_time_fixations.items(), key=lambda k: k[0]))
    # aggiungo al dict risultante
    mean_users_stats["mean_user_time_fixations"] = mean_user_time_fixations

    # ---------------------------------------------------------------------------------------------------
    """
    # BLINK
    # normalizzo per il numero di utenti
    mean_user_blink = {k: v / n_users for k, v in mean_user_blink.items()}
    # ordino il dizionario per chiave
    mean_user_blink = dict(sorted(mean_user_blink.items(), key=lambda k: k[0]))
    # aggiungo al dict risultante
    mean_users_stats["mean_user_blink"] = mean_user_blink
"""
    # ---------------------------------------------------------------------------------------------------

    # SACCADES AMPLITUDES
    # normalizzo per il numero di utenti
    mean_user_saccades_width = {k: v / n_users for k, v in mean_user_saccades_width.items()}
    # ordino il dizionario per chiave
    mean_user_saccades_width = dict(sorted(mean_user_saccades_width.items(), key=lambda k: k[0][0]))
    # aggiungo al dict risultante
    mean_users_stats["mean_user_saccades_width"] = mean_user_saccades_width

    # ---------------------------------------------------------------------------------------------------

    # SACCADES DIRECTIONS
    # normalizzo per il numero di utenti
    mean_user_saccades_directions = {k: v / n_users for k, v in mean_user_saccades_directions.items()}
    # ordino il dizionario per chiave
    mean_user_saccades_directions = dict(sorted(mean_user_saccades_directions.items(), key=lambda k: k[0][0]))
    # aggiungo al dict risultante
    mean_users_stats["mean_user_saccades_directions"] = mean_user_saccades_directions

    # ---------------------------------------------------------------------------------------------------

    return mean_users_stats




