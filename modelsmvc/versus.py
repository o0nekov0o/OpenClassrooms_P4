from modelsmvc import round
from modelsmvc import settings


class Match:
    def __init__(self, id, resultat, liste_de_joueurs):
        self.id = id
        self.resultat = resultat
        self.liste_de_joueurs = liste_de_joueurs

    def generer_paires(self, matchs_potentiels, main_tournoi):
        """
        generates pairs of players from the managed tournament players list, in order to make the matches happen
        :param matchs_potentiels from ajouter_match, used to configure the matches from the generated pairs
        :param main_tournoi: from ajouter_match, used to determinate match players list from managed tournament
        :return: for tour.py, saisir_score use
        """
        main_tournoi.joueurs.sort()
        paire_0 = {'0': main_tournoi.joueurs[0], '1': main_tournoi.joueurs[4]}
        paire_1 = {'0': main_tournoi.joueurs[1], '1': main_tournoi.joueurs[5]}
        paire_2 = {'0': main_tournoi.joueurs[2], '1': main_tournoi.joueurs[6]}
        paire_3 = {'0': main_tournoi.joueurs[3], '1': main_tournoi.joueurs[7]}
        paire_4 = {'0': paire_0['1'], '1': paire_0['0']}
        paire_5 = {'0': paire_1['1'], '1': paire_1['0']}
        paire_6 = {'0': paire_2['1'], '1': paire_2['0']}
        paire_7 = {'0': paire_3['1'], '1': paire_3['0']}
        matchs_potentiels.liste_de_joueurs = [paire_0, paire_1, paire_2, paire_3,
                                              paire_4, paire_5, paire_6, paire_7]
        return matchs_potentiels  # pour utilisation module round

    def ajouter_match(self, tour_managed, main_tournoi):
        """
        starts the appending of the played matches in round matches list, especially by creating match instances
        :param tour_managed: from tour.py, ajouter_tour, used to pass the instance to round.py, saisir_score
        :param main_tournoi: from tour.py, ajouter_tour, used to pass the instance to saisir_score & generer_paires
        :return: None
        """
        reply = "o-n"
        while reply.lower() not in {"o", "n"}:
            if settings.skip_1 == 0:
                reply = input("Entrez si vous voulez ajouter un match, et saisir son score, oui (o) ou non (n): ")
            elif settings.skip_1 == 1:
                reply = "o"
            while reply == "o":
                global j
                j = 0
                for j in range(4):
                    settings.pwd = j
                    new_match = Match(f"match_{settings.pwd}", {'0': '1', '1': '2'"""results"""}, ["""players"""])
                    matchs_prochains = new_match.generer_paires(new_match, main_tournoi)
                    round.Tour(f"tour_{settings.ref}", "liste_de_matchs") \
                        .saisir_score(matchs_prochains, j, tour_managed, main_tournoi)
                    if settings.skip_1 == 0:
                        reply = "o-n"
                    elif settings.skip_1 == 1:
                        reply = "o"
                    if reply == "o":
                        settings.skip_0 = 1
                    while reply.lower() not in {"o", "n"}:
                        if j != 3:
                            if settings.skip_1 == 0:
                                reply = input("Entrez si vous voulez ajouter un match, et saisir son score, "
                                              "oui (o) ou non (n): ")
                            elif settings.skip_1 == 1:
                                reply = "o"
                            if reply == "o" and j < 3:
                                settings.skip_0 = 0
                                continue
                            elif reply == "n" or j == 3:
                                print("Pas de nouveau match à ajouter pour le tour associé")
                                if reply == "n":
                                    settings.skip_0 = 0
                                else:
                                    settings.skip_0 = 1
                                break
                        elif j == 3:
                            print("Pas de nouveau match à ajouter pour le tour associé")
                            settings.skip_0 = 1
                            break
                    if reply == "n" or j == 3:
                        print("Pas de nouveau match à ajouter pour le tour associé")
                        break
                if reply == "n" or j == 3:
                    break
            if reply == "n" or j == 3:
                break
        return None
