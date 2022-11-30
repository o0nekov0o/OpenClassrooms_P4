from z__project_all__z import settings


class Tournoi:
    def __init__(self, id, nom, lieu, date,
                 nombre_de_tours, tournees, joueurs,
                 controle_du_temps, description):
        self.id = id
        self.nom = nom
        self.lieu = lieu
        self.date = date
        self.nombre_de_tours = nombre_de_tours
        self.tournees = tournees
        self.joueurs = joueurs
        self.controle_du_temps = controle_du_temps
        self.description = description

    def ajouter_tournoi_view(self, tous_les_tournois):
        """
        creates tournament instances, from the class specified above, whose name is 'Tournoi'
        :param tous_les_tournois: from main.py, main_controller, to append all_tournaments list
        :param bdd: from main.py, to create serialized tournament instances in json file
        :return: for main.py, main_controller use, in case of adding or adding canceled
        """
        new_tournament = {
            "id": f"tournoi_{len(tous_les_tournois)}",
            "nom": "",
            "lieu": "",
            "date": "99-99-9999",
            "nombre_de_tours": 4,
            "tournees": [],
            "joueurs": [],
            "controle_du_temps": "quickblitz",
            "description": ""
        }
        try:
            while not new_tournament["nom"].isalpha():
                new_tournament["nom"] = input("Entrez le nom du tournoi: ")
            while not new_tournament["lieu"].isalpha():
                new_tournament["lieu"] = input("Entrez le lieu du tournoi: ")
            while not settings.validate(new_tournament["date"]):
                new_tournament["date"] = input("Entrez la date du tournoi, JJ-MM-AAAA: ")
            while new_tournament["controle_du_temps"].lower() not in {"bullet", "blitz", "quickshot"}:
                new_tournament["controle_du_temps"] = input("Entrez le contrôle du temps du tournoi, "
                                                            "bullet, blitz ou quickshot: ")
            while not new_tournament["description"].isalpha():
                new_tournament["description"] = input("Entrez la description du tournoi: ")
            print("-" * 163)
            return new_tournament
        except KeyboardInterrupt:
            print(" ==> Ajout du tournoi annulé")
            print("-" * 163)

    def ajouter_tournoi_controller(self, tous_les_tournois, bdd):
        """
        creates tournament instances, from the class specified above, whose name is 'Tournoi'
        :param tous_les_tournois: from main.py, main_controller, to append all_tournaments list
        :param bdd: from main.py, to create serialized tournament instances in json file
        :return: for main.py, main_controller use, in case of adding or adding canceled
        """
        try:
            new_tournament_data = self.ajouter_tournoi_view(tous_les_tournois)
            new_tournament = Tournoi(new_tournament_data["id"], new_tournament_data["nom"],
                                     new_tournament_data["lieu"], new_tournament_data["date"],
                                     new_tournament_data["nombre_de_tours"], new_tournament_data["tournees"],
                                     new_tournament_data["joueurs"], new_tournament_data["controle_du_temps"],
                                     new_tournament_data["description"])
            tous_les_tournois.append(new_tournament)
            settings.tournament_encode(new_tournament, bdd)
        except KeyboardInterrupt:
            print(" ==> Ajout du tournoi annulé")
            print("-" * 163)

    def editer_tournoi_view(self, tous_les_tournois):
        """
        edit created tournament instances
        :param tous_les_tournois: from main.py, main_controller, to edit all_tournaments list
        :param bdd: from main.py, to update serialized tournament instances in json file
        :return: None
        """
        new_data_tournament = {
            "nom": "",
            "lieu": "",
            "date": "99-99-9999",
            "controle_du_temps": "quickblitz",
            "description": ""
        }
        try:
            for i, tournament in enumerate(tous_les_tournois):
                print(f"{i}/ {tournament.nom}")
            index = int(input("Quel tournoi voulez-vous modifier ? "))
            tournament_to_modify = tous_les_tournois[index]
            print(f"0/ Nom: {tournament_to_modify.nom}")
            print(f"1/ Lieu: {tournament_to_modify.lieu}")
            print(f"2/ Date: {tournament_to_modify.date}")
            print(f"3/ Temps: {tournament_to_modify.controle_du_temps}")
            print(f"4/ Description: {tournament_to_modify.description}")
            print("5/ Annulation et retour")
            choix = input("Que voulez-vous modifier ? ")
            if choix in {"0", "1", "2", "3", "4", "5"}:
                return new_data_tournament, tournament_to_modify, choix
            else:
                print("Je n'ai pas compris votre choix")
                print("-" * 163)
                self.editer_tournoi_view(tous_les_tournois)
            print("-" * 163)
        except (ValueError, IndexError):
            print("Je n'ai pas compris votre choix")
            print("-" * 163)
            self.editer_tournoi_view(tous_les_tournois)
        except KeyboardInterrupt:
            print(" ==> Modification du tournoi annulée")
            print("-" * 163)
            return None


    def editer_tournoi_controller(self, tous_les_tournois, bdd):
        """
        edit created tournament instances
        :param tous_les_tournois: from main.py, main_controller, to edit all_tournaments list
        :param bdd: from main.py, to update serialized tournament instances in json file
        :return: None
        """
        new_data_tournament, tournament_to_modify, choix = self.editer_tournoi_view(tous_les_tournois)
        if len(tous_les_tournois) > 0:
            try:
                if choix == "0":
                    while not new_data_tournament["nom"].isalpha():
                        new_data_tournament["nom"] = input("Entrer le nouveau nom du tournoi: ")
                    tournament_to_modify.nom = new_data_tournament["nom"]
                    print("Le tournoi a été modifié")
                elif choix == "1":
                    while not new_data_tournament["lieu"].isalpha():
                        new_data_tournament["lieu"] = input("Entrer le nouveau lieu du tournoi: ")
                    tournament_to_modify.lieu = new_data_tournament["lieu"]
                    print("Le tournoi a été modifié")
                elif choix == "2":
                    while not settings.validate(new_data_tournament["date"]):
                        new_data_tournament["date"] = input("Entrer la nouvelle date du tournoi: ")
                    tournament_to_modify.date = new_data_tournament["date"]
                    print("Le tournoi a été modifié")
                elif choix == "3":
                    while new_data_tournament["controle_du_temps"].lower() not in {"bullet", "blitz", "quickshot"}:
                        new_data_tournament["controle_du_temps"] = input("Entrer le nouveau "
                                                                         "contrôle du temps du tournoi: ")
                    tournament_to_modify.controle_du_temps = new_data_tournament["nom"]
                    print("Le tournoi a été modifié")
                elif choix == "4":
                    while not new_data_tournament["description"].isalpha():
                        new_data_tournament["nom"] = input("Entrer la nouvelle description du tournoi: ")
                    tournament_to_modify.description = new_data_tournament["description"]
                    print("Le tournoi a été modifié")
                elif choix == "5":
                    return None
                else:
                    print("Je n'ai pas compris votre choix")
                    print("-" * 163)
                    self.editer_tournoi_controller(tous_les_tournois, bdd)
                print("-" * 163)
                settings.edit_tournament_encode(tournament_to_modify, bdd)
            except (ValueError, IndexError):
                print("Je n'ai pas compris votre choix")
                print("-" * 163)
                self.editer_tournoi_controller(tous_les_tournois, bdd)
            except KeyboardInterrupt:
                print(" ==> Modification du tournoi annulée")
                print("-" * 163)
                return None
        else:
            print("Aucun tournoi n'a déjà été ajouté")
            print("-" * 163)
            return None
