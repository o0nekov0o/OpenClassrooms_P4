import random
from modelsmvc import versus
from modelsmvc import settings


class Tour:
    def __init__(self, id, liste_de_matchs):
        self.id = id
        self.matchs = liste_de_matchs

    def saisir_score(self, matchs_confirmes, boucle, tour_termine, main_tournoi):
        """
        manages the input of the score for the ended matches into the round being managed
        :param matchs_confirmes: from versus.py, ajouter_match, for it to be appended in round matches list
        :param boucle: from versus.py, ajouter_match, for using of loop in this function
        :param tour_termine: from versus.py, ajouter_match, for management of created tour since code in tour.py
        :param main_tournoi: from versus.py, ajouter_match, for appending of round in the tournament rounds list
        :return: None
        """
        clone = boucle + 4
        paire_0, paire_1, paire_2, paire_3, paire_4, paire_5, paire_6, paire_7 = matchs_confirmes.liste_de_joueurs
        if locals()[f"paire_{boucle}"] and locals()[f"paire_{clone}"] not in settings.deja_fait:
            while True:
                try:
                    choix = "3"
                    while choix.lower() not in {"0", "1", "2"}:
                        choix = input(f"Entrer le score de {locals()[f'paire_{boucle}']['0'].prenom} "
                                      f"contre {locals()[f'paire_{boucle}']['1'].prenom}, "
                                      f"0 si {locals()[f'paire_{boucle}']['0'].prenom} a gagné, "
                                      f"1 si match nul, 2 si {locals()[f'paire_{boucle}']['1'].prenom} a gagné: ")
                    if choix == "0":
                        locals()[f'paire_{boucle}']['0'].score += 1
                    elif choix == "1":
                        locals()[f'paire_{boucle}']['0'].score += 0.5
                        locals()[f'paire_{boucle}']['1'].score += 0.5
                    elif choix == "2":
                        locals()[f'paire_{boucle}']['1'].score += 1
                    locals()[f"paire_{boucle}"]['0'].hasard += random.randrange(0, 11)
                    locals()[f"paire_{boucle}"]['1'].hasard += random.randrange(0, 11)
                    settings.deja_fait.append(locals()[f"paire_{boucle}"])
                    settings.deja_fait.append(locals()[f"paire_{clone}"])
                except ValueError:
                    continue
                break
        elif locals()[f"paire_{boucle}"] and locals()[f"paire_{clone}"] in settings.deja_fait:
            locals()[f"paire_{boucle}"]['0'].score += 0
            locals()[f"paire_{boucle}"]['1'].score += 0
            locals()[f"paire_{boucle}"]['0'].hasard += random.randrange(0, 11)
            locals()[f"paire_{boucle}"]['1'].hasard += random.randrange(0, 11)
            boucle = 3
        matchs_confirmes.resultat['0'] = [locals()[f"paire_{boucle}"]['0'].prenom,
                                          locals()[f"paire_{boucle}"]['0'].score]
        matchs_confirmes.resultat['1'] = [locals()[f"paire_{boucle}"]['1'].prenom,
                                          locals()[f"paire_{boucle}"]['1'].score]
        matchs_confirmes.resultat = tuple(matchs_confirmes.resultat.values())
        tour_termine.liste_de_matchs.append(matchs_confirmes.resultat)
        main_tournoi.tournees.append(tour_termine.liste_de_matchs)
        rounds_list = []
        for i in main_tournoi.tournees:
            if i not in rounds_list:
                rounds_list.append(i)
                main_tournoi.tournees = rounds_list
        return None

    def ajouter_tour(self, main_tournoi):
        """
        creates round instances, from where the associated functions to ensure the round creation will also be called
        :param main_tournoi: from main.py, round_controller, for appending of round in the tournament rounds list
        :return: None
        """
        if len(main_tournoi.joueurs) >= 8:
            try:
                reponse = "o-n"
                while reponse.lower() not in {"o", "n"}:
                    if settings.skip_0 == 0:
                        reponse = input("Entrez si vous voulez ajouter un tour, et ses matchs déroulés, "
                                        "oui (o) ou non (n): ")
                    elif settings.skip_0 == 1 or settings.skip_0 == 2:
                        reponse = "o"
                    while reponse == "o":
                        settings.ref += 1
                        new_tour = Tour(f"tour_{settings.ref}", "liste_de_matchs")
                        new_tour.nom = f"round_{settings.ref}"
                        new_tour.liste_de_matchs = []
                        new_tour.date_heure_de_debut = settings.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        versus.Match(f"match_{settings.pwd}", {'0': '1', '1': '2'"""results"""}, ["""players"""]) \
                            .ajouter_match(new_tour, main_tournoi)
                        new_tour.date_heure_de_fin = settings.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        if settings.skip_0 == 0:
                            reponse = "o-n"
                        elif settings.skip_0 == 1 or settings.skip_0 == 2:
                            reponse = "o"
                            print("Un nouveau tour va être ajouté pour y associer les matchs")
                            settings.skip_1 = 1
                            settings.skip_0 = 2
                        while reponse.lower() not in {"o", "n"}:
                            if settings.skip_0 == 0:
                                if settings.skip_0 == 0:
                                    reponse = input("Entrez si vous voulez ajouter un tour, et ses matchs déroulés, "
                                                    "oui (o) ou non (n): ")
                                elif settings.skip_0 == 1 or settings.skip_0 == 2:
                                    reponse = "o"
                                if reponse == "o" and len(settings.deja_fait) < 56:
                                    settings.skip_1 = 0
                                    settings.skip_0 = 1
                                    continue
                                elif reponse == "n" or len(settings.deja_fait) >= 56:
                                    reponse = "n"
                                    print("Pas de nouveau tour à ajouter pour le tournoi associé")
                                    settings.skip_1 = 0
                                    settings.skip_0 = 1
                                    break
                            elif settings.skip_0 == 1 or settings.skip_0 == 2:
                                print("Un nouveau tour va être ajouté pour y associer les matchs")
                                settings.skip_1 = 1
                                settings.skip_0 = 2
                                continue
                        if reponse == "n" or len(settings.deja_fait) >= 56:
                            print("Pas de nouveau tour à ajouter pour le tournoi associé")
                            break
                    if reponse == "n" or len(settings.deja_fait) >= 56:
                        break
            except KeyboardInterrupt:
                print(" ==> Ajout du tour annulé")
                return None
        else:
            print("Le tournoi n'a pas encore atteint 8 jours")
        return None

    def afficher_tours(self, main_tournoi):
        """
        displays ended rounds of managed tournament, with its matches list and the associated appointed players
        :param main_tournoi: from main.py, round_controller, for displaying of round in the tournament rounds list
        :return: None
        """
        if len(main_tournoi.tournees) > 0:
            for i, tour in enumerate(main_tournoi.tournees):
                print(f"{i}/ {tour}")
            print("Voici les derniers tours")
        else:
            print("Aucun tour n'a déjà été ajouté")
            return None
