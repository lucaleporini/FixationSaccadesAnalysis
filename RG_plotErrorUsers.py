import matplotlib
import matplotlib.pyplot as plt
import pickle as pkl
import numpy as np
import RG_select_users
import pprint

def createListSingleExperiment(error_users):
    list_users = {}
    last = None

    # se non setto nessun parametro ottengo la lista di utenti selezionando le prove degli utenti con errore minimo
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
    return list_users


def run(error_threshold, error_total_users):
    font = {'family': 'normal',
            'weight': 'bold',
            'size': 21}

    matplotlib.rc('font', **font)

    error_users = createListSingleExperiment(error_total_users)
    print(len(error_users.keys()))
    keys = list(error_users.keys())
    keys = [s.split("_")[0] for s in keys]
    values = list(error_users.values())
    print(np.mean(list(error_users.values())))
    plt.figure(figsize=(14,6), dpi=100)
    plt.xticks(range(0, len(keys)), keys, rotation=270)
    plt.hlines(error_threshold, 0, len(keys), colors='k', linestyles='solid', label='')
    plt.bar(range(0, len(keys)), sorted(values))
    plt.show()


RG_total_users = pkl.load(open("error_total_users.pkl", "rb"))
pprint.pprint(RG_total_users)
run(0.07, RG_total_users)