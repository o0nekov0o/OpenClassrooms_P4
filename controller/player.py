from z__project_all__z import settings


class PlayerController:
    def ajouter_joueur_controller(self, main_tournoi, bdd):
        """
        creates player instances, from the class specified above, whose name is 'Joueur'
        :param main_tournoi: from main.py, player_controller, to append players list of tournament being managed
        :param bdd: from main.py, to create serialized player instances in json file
        :return: None
        """
        try:
            for i in range(8):
                if len(main_tournoi.joueurs) < 8:
                    new_player_data = self.ajouter_joueur_view(main_tournoi)
                    new_player = Joueur(new_player_data["id"], new_player_data["nom_de_famille"],
                                        new_player_data["prenom"], new_player_data["date_de_naissance"],
                                        new_player_data["sexe"], new_player_data["classement"])
                    main_tournoi.joueurs.append(new_player)
                    settings.player_encode(main_tournoi, bdd, new_player)
                elif len(main_tournoi.joueurs) >= 8:
                    print("Le tournoi a déjà son nombre maximal de joueurs")
                    print("-" * 163)
                    break
        except KeyboardInterrupt:
            print(" ==> Ajout du joueur annulé")
            print("-" * 163)
            return None

    def editer_joueur_controller(self, main_tournoi, bdd):
        """
        edit created player instances
        :param main_tournoi: from main.py, player_controller, to edit players list of tournament being managed
        :param bdd: from main.py, to update serialized player instances in json file
        :return: None
        """
        new_data_player, player_to_modify, choix = self.editer_joueur_view(main_tournoi)
        try:
            if len(main_tournoi.joueurs) > 0:
                if choix == "0":
                    while not new_data_player["nom_de_famille"].isalpha():
                        new_data_player["nom_de_famille"] = input("Entrer le nouveau nom de famille du joueur: ")
                    player_to_modify.nom_de_famille = new_data_player["nom_de_famille"]
                elif choix == "1":
                    while not new_data_player["prenom"].isalpha():
                        new_data_player["prenom"] = input("Entrer le nouveau prénom du joueur: ")
                    player_to_modify.prenom = new_data_player["prenom"]
                    print("Le joueur a été modifié")
                elif choix == "2":
                    while not settings.validate(new_data_player["date_de_naissance"]):
                        new_data_player["date_de_naissance"] = input("Entrer la nouvelle date de naissance du joueur: ")
                    player_to_modify.date_de_naissance = new_data_player["nom_de_famille"]
                    print("Le joueur a été modifié")
                elif choix == "3":
                    while new_data_player["sexe"].lower() not in {"m", "f"}:
                        new_data_player["sexe"] = input("Entrer le nouveau sexe du joueur: ")
                    player_to_modify.sexe = new_data_player["sexe"]
                    print("Le joueur a été modifié")
                elif choix == "4":
                    return None
                print("-" * 163)
                settings.edit_player_encode(main_tournoi, bdd, player_to_modify)
                self.editer_joueur_controller(main_tournoi, bdd)
            else:
                print("Aucun joueur n'a déjà été ajouté")
                print("-" * 163)
                return None
        except (ValueError, IndexError):
            print("Je n'ai pas compris votre choix")
            print("-" * 163)
            self.editer_joueur_view(main_tournoi)
        except KeyboardInterrupt:
            print(" ==> Modification du joueur annulée")
            print("-" * 163)
            return None