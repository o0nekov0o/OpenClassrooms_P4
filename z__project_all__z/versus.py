from z__project_all__z import rounds
from z__project_all__z import settings


class Match:
    def __init__(self, id, liste_de_joueurs, resultat=None):
        self.id = id
        self.liste_de_joueurs = liste_de_joueurs
        self.resultat = resultat

    def saisir_score(self, main_tournoi, bdd):
        """
        manages the input of the score for the ended matches into the round being managed
        :param matchs_confirmes: from versus.py.py, ajouter_match, for it to be appended in round matches list
        :param boucle: from versus.py.py, ajouter_match, for using of loop in this function
        :param tour_termine: from versus.py.py, ajouter_match, for management of created tour since code in tour.py
        :param main_tournoi: from versus.py.py, ajouter_match, for appending of round in the tournament rounds list
        :return: None
        """
        try:
            if not main_tournoi.tournees:
                print("Round non créé, créez-en un nouveau")
                rounds.Tour(f"tour_{len(main_tournoi.tournees) + 1}", "liste_de_matchs").ajouter_tour(main_tournoi, bdd)
            round_to_modify = main_tournoi.tournees[-1]
            if rounds.Tour(f"tour_{len(main_tournoi.tournees) + 1}", "liste_de_matchs").completed(main_tournoi):
                print("Round terminé, créez-en un nouveau")
                settings.modify_round(round_to_modify, main_tournoi, bdd)
            for i, match in enumerate(round_to_modify.liste_de_matches):
                print(f"{i}/ {match.liste_de_joueurs[0].prenom} vs {match.liste_de_joueurs[1].prenom}")
            choix = int(input("Quel match voulez vous saisir ? "))
            match_to_modify = round_to_modify.liste_de_matches[choix]
            if match_to_modify.resultat is not None:
                choix_ter = "oui"
                while choix_ter not in {"o", "n"}:
                    choix_ter = input("Match déjà saisi, voulez-vous le modifier, oui (o) ou non (n) ? ")
                    if choix_ter == "o":
                        if match_to_modify.resultat == 0:
                            match_to_modify.liste_de_joueurs[0].score -= 1
                        elif match_to_modify.resultat == 1:
                            match_to_modify.liste_de_joueurs[0].score -= 0.5
                            match_to_modify.liste_de_joueurs[1].score -= 0.5
                        elif match_to_modify.resultat == 2:
                            match_to_modify.liste_de_joueurs[1].score -= 1
                        choix_quater = int(input(f"Quel est le score du match (0 si "
                                                 f"{match_to_modify.liste_de_joueurs[0].prenom} a gagné, "
                                                 f"1 si nul, 2 si {match_to_modify.liste_de_joueurs[1].prenom}) ? "))
                        if choix_quater == 0:
                            match_to_modify.liste_de_joueurs[0].score += 1
                        elif choix_quater == 1:
                            match_to_modify.liste_de_joueurs[0].score += 0.5
                            match_to_modify.liste_de_joueurs[1].score += 0.5
                        elif choix_quater == 2:
                            match_to_modify.liste_de_joueurs[1].score += 1
                        match_to_modify.resultat = choix_quater
                        print("Score du match saisi")
                    elif choix_ter == "n":
                        continue
                self.saisir_score(main_tournoi, bdd)
            else:
                choix_bis = int(input(f"Quel est le score du match (0 si "
                                      f"{match_to_modify.liste_de_joueurs[0].prenom} a gagné, "
                                      f"1 si nul, 2 si {match_to_modify.liste_de_joueurs[1].prenom}) ? "))
                if choix_bis == 0:
                    match_to_modify.liste_de_joueurs[0].score += 1
                elif choix_bis == 1:
                    match_to_modify.liste_de_joueurs[0].score += 0.5
                    match_to_modify.liste_de_joueurs[1].score += 0.5
                elif choix_bis == 2:
                    match_to_modify.liste_de_joueurs[1].score += 1
                match_to_modify.resultat = choix_bis
                print("Score du match saisi")
        except (ValueError, IndexError):
            print("Je n'ai pas compris votre choix")
            self.saisir_score(main_tournoi, bdd)
        except KeyboardInterrupt:
            print(" ==> Modification du tour annulée")
            return None
        self.saisir_score(main_tournoi, bdd)