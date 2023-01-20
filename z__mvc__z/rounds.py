from z__mvc__z import versus
from z__mvc__z import settings_2
import os
import pandas


class Tour:
    def __init__(self, id, liste_de_matches):
        self.id = id
        self.liste_de_matches = liste_de_matches

    def completed(self, main_tournoi):
        for match in main_tournoi.tournees[-1].liste_de_matches:
            if match.resultat is None:
                return False
        return True

    def ajouter_tour(self, main_tournoi, bdd):
        """
        creates round instances, from where the associated functions to ensure the round creation will also be called
        :param main_tournoi: from main.py, round_controller, for appending of round in the tournament rounds list
        :return: None
        """
        try:
            rounds_count = len(main_tournoi.tournees)
            if rounds_count and not Tour(f"tour_{rounds_count + 1}", "liste_de_matchs").completed(main_tournoi):
                print("Round en cours, finissez de le saisir")
                Tour(f"tour_{rounds_count + 1}", "liste_de_matchs").saisir_score(main_tournoi, bdd)
            if rounds_count == 7:
                print("Tournoi terminé, ajoutez-en un autre")
                print("Rapport du tournoi généré : rapport.xlsx")
                pandas.read_json("db.json").to_excel("rapport.xlsx")
                os.system('python main.py')
            number_of_rounds = len(main_tournoi.tournees)
            id_round = f"round_{number_of_rounds + 1}"
            new_matches = []
            main_tournoi.joueurs.sort(key=lambda x: (x.score, x.classement), reverse=True)
            if number_of_rounds == 0:
                for i in range(0, 4):
                    id_match = f"{id_round}_match_{i}"
                    new_matches.append(versus.Match(id=id_match, liste_de_joueurs=[main_tournoi.joueurs[i],
                                                                                   main_tournoi.joueurs[i + 4]]))
                new_tour = Tour(id=id_round, liste_de_matches=new_matches)
                print("Nouveau round créé")
                print("-" * 163)
                print("Voici la liste des matches à jouer")
                for i, match in enumerate(new_matches):
                    print(f"{i}/ {match.liste_de_joueurs[0].prenom} vs {match.liste_de_joueurs[1].prenom}")
                print("-" * 163)
                main_tournoi.tournees.append(new_tour)
                Tour(id=id_round, liste_de_matches=new_matches).saisir_score(main_tournoi, bdd)
            else:
                """already_played = {
                    player1: [player2, player5],
                    player2: [player1, player6],
                    ...
                }"""
                already_played = {player: [] for player in main_tournoi.joueurs}
                for tour in main_tournoi.tournees:
                    for match in tour.liste_de_matches:
                        playerA = match.liste_de_joueurs[0]
                        playerB = match.liste_de_joueurs[1]
                        already_played[playerA].append(playerB)
                        already_played[playerB].append(playerA)
                players_added_to_round = []
                i = 1
                for player in main_tournoi.joueurs:
                    if player not in players_added_to_round:
                        for adversaire in main_tournoi.joueurs:
                            if(
                                    adversaire not in players_added_to_round
                                    and player != adversaire
                                    and adversaire not in already_played[player]
                            ):
                                id_match = f"{id_round}_match_{i}"
                                i += 1
                                new_matches.append(
                                    versus.Match(id=id_match, liste_de_joueurs=[player, adversaire]))
                                players_added_to_round.append(adversaire)
                                players_added_to_round.append(player)
                                break
                remaining_players = [player for player in main_tournoi.joueurs if player not in players_added_to_round]
                j = len(remaining_players)
                if j % 2 != 0:
                    raise Exception("uneven remaining players")
                for idx in range(0, j, 2):
                    id_match = f"{id_round}_match_{i}"
                    i += 1
                    new_matches.append(
                        versus.Match(id=id_match, liste_de_joueurs=[remaining_players[idx], remaining_players[idx+1]]))
                new_tour = Tour(id=id_round, liste_de_matches=new_matches)
                print("Nouveau round créé")
                print("-" * 163)
                print("Voici la liste des matches à jouer")
                for i, match in enumerate(new_matches):
                    print(f"{i}/ {match.liste_de_joueurs[0].prenom} vs {match.liste_de_joueurs[1].prenom}")
                print("-" * 163)
                main_tournoi.tournees.append(new_tour)
                Tour(id=id_round, liste_de_matches=new_matches).saisir_score(main_tournoi, bdd)
        except KeyboardInterrupt:
            print(" ==> Ajout du tour annulé")
            print("-" * 163)
            return None

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
                Tour(f"tour_{len(main_tournoi.tournees) + 1}", "liste_de_matchs").ajouter_tour(main_tournoi, bdd)
            round_to_modify = main_tournoi.tournees[-1]
            if Tour(f"tour_{len(main_tournoi.tournees) + 1}", "liste_de_matchs").completed(main_tournoi):
                print("Round terminé, créez-en un nouveau")
                settings_2.modify_round(round_to_modify, main_tournoi, bdd)
            for i, match in enumerate(round_to_modify.liste_de_matches):
                print(f"{i}/ {match.liste_de_joueurs[0].prenom} vs {match.liste_de_joueurs[1].prenom}")
            choix = int(input("Quel match voulez vous saisir ? "))
            print("-" * 163)
            match_to_modify = round_to_modify.liste_de_matches[choix]
            if match_to_modify.resultat is not None:
                choix_ter = "oui"
                while choix_ter not in {"o", "n"}:
                    choix_ter = input("Match déjà saisi, voulez-vous le modifier, oui (o) ou non (n) ? ")
                    print("-" * 163)
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
                        print("-" * 163)
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
                print("-" * 163)
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
            print("-" * 163)
            self.saisir_score(main_tournoi, bdd)
        except KeyboardInterrupt:
            print(" ==> Modification du tour annulée")
            print("-" * 163)
            return None
        self.saisir_score(main_tournoi, bdd)
