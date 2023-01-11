from z__mvc__z import settings_2


class Joueur:
    def __init__(self, id, nom_de_famille, prenom, date_de_naissance,
                 sexe, classement, score=0):
        self.id = id
        self.nom_de_famille = nom_de_famille
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.sexe = sexe
        self.classement = classement
        self.score = score

    def ajouter_joueur_view(self, main_tournoi):
        """
        creates player instances, from the class specified above, whose name is 'Joueur'
        :param main_tournoi: from main.py, player_controller, to append players list of tournament being managed
        :param bdd: from main.py, to create serialized player instances in json file
        :return: None
        """
        new_player = {
            "id": f"joueur_{len(main_tournoi.joueurs)}",
            "nom_de_famille": "",
            "prenom": "",
            "date_de_naissance": "99-99-9999",
            "sexe": "homme",
            "classement": len(main_tournoi.joueurs)

        }
        try:
            while not new_player["nom_de_famille"].isalpha():
                new_player["nom_de_famille"] = input(
                    f"Entrez le nom de famille du joueur {len(main_tournoi.joueurs)}: ")
            while not new_player["prenom"].isalpha():
                new_player["prenom"] = input(f"Entrez le prenom du joueur {len(main_tournoi.joueurs)}: ")
            while not settings_2.validate(new_player["date_de_naissance"]):
                new_player["date_de_naissance"] = input(
                    f"Entrez la date de naissance du joueur {len(main_tournoi.joueurs)}, "
                    f"JJ-MM-AAAA: ")
            while new_player["sexe"].lower() not in {"m", "f"}:
                new_player["sexe"] = input(f"Entrez le sexe du joueur {len(main_tournoi.joueurs)}, "
                                           f"masculin (m) ou feminin (f): ")
            print("-" * 163)
            return new_player
        except KeyboardInterrupt:
            print(" ==> Ajout du joueur annulé")
            print("-" * 163)
            return None

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
                    settings_2.edit_tournament_encode(main_tournoi, bdd)
                elif len(main_tournoi.joueurs) >= 8:
                    print("Le tournoi a déjà son nombre maximal de joueurs")
                    print("-" * 163)
                    break
        except KeyboardInterrupt:
            print(" ==> Ajout du joueur annulé")
            print("-" * 163)
            return None

    def editer_joueur_view(self, main_tournoi):
        """
        edit created player instances
        :param main_tournoi: from main.py, player_controller, to edit players list of tournament being managed
        :param bdd: from main.py, to update serialized player instances in json file
        :return: None
        """
        new_data_player = {
            "nom_de_famille": "",
            "prenom": "",
            "date_de_naissance": "99-99-9999",
            "sexe": "homme",
        }
        try:
            for i, joueur in enumerate(main_tournoi.joueurs):
                print(f"{i}/ {joueur.prenom}")
            index = int(input("Quel joueur voulez-vous modifier ? "))
            print("-" * 163)
            player_to_modify = main_tournoi.joueurs[index]
            print(f"0/ Nom: {player_to_modify.nom_de_famille}")
            print(f"1/ Prénom: {player_to_modify.prenom}")
            print(f"2/ Date: {player_to_modify.date_de_naissance}")
            print(f"3/ Sexe: {player_to_modify.sexe}")
            print("4/ Annulation et retour")
            choix = input("Que voulez-vous modifier ? ")
            print("-" * 163)
            if choix in {"0", "1", "2", "3", "4"}:
                return new_data_player, player_to_modify, choix
            else:
                print("Je n'ai pas compris votre choix")
                print("-" * 163)
                self.editer_joueur_view(main_tournoi)
            print("-" * 163)
        except (ValueError, IndexError):
            print("Je n'ai pas compris votre choix")
            print("-" * 163)
            self.editer_joueur_view(main_tournoi)
        except KeyboardInterrupt:
            print(" ==> Modification du joueur annulée")
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
                    while not settings_2.validate(new_data_player["date_de_naissance"]):
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
                settings_2.edit_tournament_encode(main_tournoi, bdd)
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
