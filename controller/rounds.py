from controller.versus import VersusController
from views.rounds import RoundView
from models.rounds import Tour
from models.versus import Match
import os


class RoundController:
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
                VersusController().saisir_score(main_tournoi, bdd)
            if rounds_count == 7:
                print("Tournoi terminé, ajoutez-en un autre")
                os.system('python main.py')
            number_of_rounds = len(main_tournoi.tournees)
            id_round = f"round_{number_of_rounds + 1}"
            new_matches = []
            main_tournoi.joueurs.sort(key=lambda x: (x.score, x.classement), reverse=True)
            if number_of_rounds == 0:
                for i in range(0, 4):
                    id_match = f"{id_round}_match_{i}"
                    new_matches.append(Match(id=id_match, liste_de_joueurs=[main_tournoi.joueurs[i],
                                                                            main_tournoi.joueurs[i + 4]]))
                new_tour = Tour(id=id_round, liste_de_matches=new_matches)
                RoundView().ajouter_tour_success_view(new_matches=new_matches)

                main_tournoi.tournees.append(new_tour)
                VersusController().saisir_score(main_tournoi, bdd)
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
                for j in range(0, 4):
                    for player in main_tournoi.joueurs:
                        if player not in players_added_to_round:
                            for adversaire in main_tournoi.joueurs:
                                if (
                                        adversaire not in players_added_to_round and
                                        player != adversaire and
                                        adversaire not in already_played[player]
                                ):
                                    id_match = f"{id_round}_match_{j}"
                                    new_matches.append(Match(id=id_match, liste_de_joueurs=[player, adversaire]))
                                    players_added_to_round.append(adversaire)
                                    players_added_to_round.append(player)
                                    j += 1
                                    break
                new_tour = Tour(id=id_round, liste_de_matches=new_matches)
                RoundView().ajouter_tour_success_view(new_matches=new_matches)
                main_tournoi.tournees.append(new_tour)
                VersusController().saisir_score(main_tournoi, bdd)
        except KeyboardInterrupt:
            print(" ==> Ajout du tour annulé")
            return None
