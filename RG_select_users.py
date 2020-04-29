import csv
import pickle as pkl


###################################################################################################################
# creazione della lista di utenti considerando le prove con il minimo errore
# per ogni utente, considero le prove svolte, scelgo la prova con il minimo errore
def createListUsers(sex=None, order=None, age=None):
    # error_users: dict contenente l'errore nelle diverse prove effettuate dagli utenti
    error_users = pkl.load(open("raw_data_cleaned/error_users.pkl", 'rb'))
    list_users = {}
    if sex is None and order is None:
        return error_users, "all_users_min_error"

    # seleziono gli utenti in base al sesso (m o f)
    # se un utente selezionato ha fatto più prove, individuo la prova con l'erroe minimo
    if not sex is None:
        for user_key, error in error_users.items():
            if user_key.split("_")[1] == sex:
                list_users[user_key] = error
        return list_users, "all_users_" + sex

    # seleziono gli utenti in base all'ordine di visione dei video (fwd o bwd)
    # se un utente selezionato ha fatto più prove, individuo la prova con l'erroe minimo
    if order is not None:
        for user_key, error in error_users.items():
            if user_key.split("_")[4] == order:
                list_users[user_key] = error
        return list_users, "all_users_" + order
