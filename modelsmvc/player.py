from modelsmvc import settings


class Joueur:
    def __init__(self, id, nom_de_famille, prenom, date_de_naissance,
                 sexe, classement, score=0, hasard=0):
        self.id = id
        self.nom_de_famille = nom_de_famille
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.sexe = sexe
        self.classement = classement
        self.score = score
        self.hasard = hasard

    def __lt__(self, other):
        if len(settings.deja_fait) >= 36:
            return self.hasard < other.hasard
        elif self.score != other.score:
            return self.score < other.score
        elif self.score == other.score:
            return self.classement < other.classement

    def ajouter_joueur(self, main_tournoi, bdd):
        """
        creates player instances, from the class specified above, whose name is 'Joueur'
        :param main_tournoi: from main.py, player_controller, to append players list of tournament being managed
        :param bdd: from main.py, to create serialized player instances in json file
        :return:
        """
        try:
            for i in range(8):
                if len(main_tournoi.joueurs) < 8:
                    new_player = Joueur(f"joueur_{len(main_tournoi.joueurs)}", "nom_de_famille", "prenom",
                                        "date_de_naissance", "sexe", "classement")
                    new_player.nom_de_famille = ""
                    while not new_player.nom_de_famille.isalpha():
                        new_player.nom_de_famille = input(
                            f"Entrez le nom de famille du joueur {len(main_tournoi.joueurs)}: ")
                    new_player.prenom = ""
                    while not new_player.prenom.isalpha():
                        new_player.prenom = input(f"Entrez le prenom du joueur {len(main_tournoi.joueurs)}: ")
                    new_player.date_de_naissance = "99-99-9999"
                    while not settings.validate(new_player.date_de_naissance):
                        new_player.date_de_naissance = input(
                            f"Entrez la date de naissance du joueur {len(main_tournoi.joueurs)}, "
                            f"JJ-MM-AAAA: ")
                    new_player.sexe = "homme"
                    while new_player.sexe.lower() not in {"m", "f"}:
                        new_player.sexe = input(f"Entrez le sexe du joueur {len(main_tournoi.joueurs)}, "
                                                f"masculin (m) ou feminin (f): ")
                    new_player.classement = len(main_tournoi.joueurs)
                    main_tournoi.joueurs.append(new_player)
                    settings.player_encode(main_tournoi, bdd, new_player)
                elif len(main_tournoi.joueurs) >= 8:
                    print("Le tournoi a déjà son nombre maximal de joueurs")
                    break
        except KeyboardInterrupt:
            print(" ==> Ajout du joueur annulé")
            return None

    def editer_joueur(self, main_tournoi, bdd):
        """
        edit created player instances
        :param main_tournoi: from main.py, player_controller, to edit players list of tournament being managed
        :param bdd: from main.py, to update serialized player instances in json file
        :return:
        """
        if len(main_tournoi.joueurs) > 0:
            try:
                for i, joueur in enumerate(main_tournoi.joueurs):
                    print(f"{i}/ {joueur.prenom}")
                index = int(input("Quel joueur voulez-vous modifier ? "))
                player_to_modify = main_tournoi.joueurs[index]
                print(f"0/ Nom: {player_to_modify.nom_de_famille}")
                print(f"1/ Prénom: {player_to_modify.prenom}")
                print(f"2/ Date: {player_to_modify.date_de_naissance}")
                print(f"3/ Sexe: {player_to_modify.sexe}")
                print("4/ Annulation et retour")
                choix = input("Que voulez-vous modifier ? ")
                if choix == '0':
                    new_name = ""
                    while not new_name.isalpha():
                        new_name = input("Entrer le nouveau nom de famille du joueur: ")
                    player_to_modify.nom_de_famille = new_name
                    print("Le joueur a été modifié")
                elif choix == '1':
                    new_firstname = ""
                    while not new_firstname.isalpha():
                        new_firstname = input("Entrer le nouveau prénom du joueur: ")
                    player_to_modify.prenom = new_firstname
                    print("Le joueur a été modifié")
                elif choix == '2':
                    new_date = "99-99-9999"
                    while not settings.validate(new_date):
                        new_date = input("Entrer la nouvelle date de naissance du joueur: ")
                    player_to_modify.date_de_naissance = new_date
                    print("Le joueur a été modifié")
                elif choix == '3':
                    new_sex = "homme"
                    while new_sex.lower() not in {"m", "f"}:
                        new_sex = input("Entrer le nouveau sexe du joueur: ")
                    player_to_modify.sexe = new_sex
                    print("Le joueur a été modifié")
                elif choix == '4':
                    return None
                else:
                    print("Je n'ai pas compris votre choix")
                    self.editer_joueur(main_tournoi, bdd)
                settings.edit_player_encode(main_tournoi, bdd, player_to_modify)
            except (ValueError, IndexError):
                print("Je n'ai pas compris votre choix")
                self.editer_joueur(main_tournoi, bdd)
            except KeyboardInterrupt:
                print(" ==> Modification du joueur annulée")
                return None
        else:
            print("Aucun joueur n'a déjà été ajouté")
            return None
