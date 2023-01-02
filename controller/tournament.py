from z__project_all__z import settings
from models.tournament import Tournoi
from views.tournament import TournamentView


class TournamentController:
    def ajouter_tournoi_controller(self, tous_les_tournois, bdd):
        """
        creates tournament instances, from the class specified above, whose name is 'Tournoi'
        :param tous_les_tournois: from main.py, main_controller, to append all_tournaments list
        :param bdd: from main.py, to create serialized tournament instances in json file
        :return: for main.py, main_controller use, in case of adding or adding canceled
        """
        new_tournament_data = TournamentView.ajouter_tournoi_view(tous_les_tournois)
        new_tournament = Tournoi(new_tournament_data["id"], new_tournament_data["nom"],
                                    new_tournament_data["lieu"], new_tournament_data["date"],
                                    new_tournament_data["nombre_de_tours"], new_tournament_data["tournees"],
                                    new_tournament_data["joueurs"], new_tournament_data["controle_du_temps"],
                                    new_tournament_data["description"])
        tous_les_tournois.append(new_tournament)
        settings.tournament_encode(new_tournament, bdd)

    def editer_tournoi_controller(self, tous_les_tournois, bdd):
        """
        edit created tournament instances
        :param tous_les_tournois: from main.py, main_controller, to edit all_tournaments list
        :param bdd: from main.py, to update serialized tournament instances in json file
        :return: None
        """
        new_data_tournament, tournament_to_modify, choix = TournamentView.editer_tournoi_view(tous_les_tournois)
        if choix == "0":
            tournament_to_modify.nom = new_data_tournament["nom"]
        elif choix == "1":
            tournament_to_modify.lieu = new_data_tournament["lieu"]
        elif choix == "2":
            tournament_to_modify.date = new_data_tournament["date"]
        elif choix == "3":
            tournament_to_modify.controle_du_temps = new_data_tournament["nom"]
        elif choix == "4":
            tournament_to_modify.description = new_data_tournament["description"]
        elif choix == "5":
            return None
        else:
            self.editer_tournoi_controller(tous_les_tournois, bdd)
        print("Le tournoi a été modifié")
        settings.edit_tournament_encode(tournament_to_modify, bdd)