from z__mvc__z import settings
from models.player import Joueur
from views.player import PlayerView


class PlayerController:
    def ajouter_joueur_controller(self, main_tournoi, bdd):
        """
        creates player instances, from the class specified above, whose name is 'Joueur'
        :param main_tournoi: from main.py, player_controller, to append players list of tournament being managed
        :param bdd: from main.py, to create serialized player instances in json file
        :return: None
        """
        for i in range(8):
                new_player_data = PlayerView().ajouter_joueur_view(main_tournoi)
                new_player = Joueur(new_player_data["id"], new_player_data["nom_de_famille"],
                                    new_player_data["prenom"], new_player_data["date_de_naissance"],
                                    new_player_data["sexe"], new_player_data["classement"])
                main_tournoi.joueurs.append(new_player)
                settings.edit_tournament_encode(main_tournoi, bdd)

    def editer_joueur_controller(self, main_tournoi, bdd):
        """
        edit created player instances
        :param main_tournoi: from main.py, player_controller, to edit players list of tournament being managed
        :param bdd: from main.py, to update serialized player instances in json file
        :return: None
        """
        new_data_player, player_to_modify, choix = PlayerView().editer_joueur_view(main_tournoi)
        if choix == "0":
            player_to_modify.nom_de_famille = new_data_player["nom_de_famille"]
        elif choix == "1":
            player_to_modify.prenom = new_data_player["prenom"]
        elif choix == "2":
            player_to_modify.date_de_naissance = new_data_player["nom_de_famille"]
        elif choix == "3":
            player_to_modify.sexe = new_data_player["sexe"]
        elif choix == "4":
            return None
        print("Le joueur a été modifié")
        print("-" * 163)
        settings.edit_tournament_encode(main_tournoi, bdd)
        self.editer_joueur_controller(main_tournoi, bdd)
        return None
