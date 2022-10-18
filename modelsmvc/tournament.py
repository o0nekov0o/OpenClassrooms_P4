from modelsmvc import settings


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

    def ajouter_tournoi(self, tous_les_tournois, bdd):
        """
        creates tournament instances, from the class specified above, whose name is 'Tournoi'
        :param tous_les_tournois: from main.py, main_controller, to append all_tournaments list
        :param bdd: from main.py, to create serialized tournament instances in json file
        :return: for main.py, main_controller use, in case of adding or adding canceled
        """
        try:
            new_tournament = Tournoi(f"tournoi_{len(tous_les_tournois)}", "nom", "lieu",
                                     "date", "nombre_de_tours", "tournees", "joueurs",
                                     "controle_du_temps", "description")
            new_tournament.nom = ""
            while not new_tournament.nom.isalpha():
                new_tournament.nom = input("Entrez le nom du tournoi: ")
            new_tournament.lieu = ""
            while not new_tournament.lieu.isalpha():
                new_tournament.lieu = input("Entrez le lieu du tournoi: ")
            new_tournament.date = "99-99-9999"
            while not settings.validate(new_tournament.date):
                new_tournament.date = input("Entrez la date du tournoi, JJ-MM-AAAA: ")
            new_tournament.nombre_de_tours = 4
            new_tournament.tournees = []
            new_tournament.joueurs = []
            new_tournament.controle_du_temps = "quickblitz"
            while new_tournament.controle_du_temps.lower() not in {"bullet", "blitz", "quickshot"}:
                new_tournament.controle_du_temps = input("Entrez le contrôle du temps du tournoi, "
                                                         "bullet, blitz ou quickshot: ")
            new_tournament.description = ""
            while not new_tournament.description.isalpha():
                new_tournament.description = input("Entrez la description du tournoi: ")
            settings.tournament_encode(new_tournament, bdd)
            return new_tournament  # pour utilisation module main
        except KeyboardInterrupt:
            print(" ==> Ajout du tournoi annulé")
            settings.cancel = 1
            return tous_les_tournois[-1]

    def editer_tournoi(self, tous_les_tournois, bdd):
        """
        edit created tournament instances
        :param tous_les_tournois: from main.py, main_controller, to edit all_tournaments list
        :param bdd: from main.py, to update serialized tournament instances in json file
        :return: None
        """
        if len(tous_les_tournois) > 0:
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
                if choix == '0':
                    new_name = ""
                    while not new_name.isalpha():
                        new_name = input("Entrer le nouveau nom du tournoi: ")
                    tournament_to_modify.nom = new_name
                    print("Le tournoi a été modifié")
                elif choix == '1':
                    new_localisation = ""
                    while not new_localisation.isalpha():
                        new_localisation = input("Entrer le nouveau lieu du tournoi: ")
                    tournament_to_modify.lieu = new_localisation
                    print("Le tournoi a été modifié")
                elif choix == '2':
                    new_date = "99-99-9999"
                    while not settings.validate(new_date):
                        new_date = input("Entrer la nouvelle date du tournoi: ")
                    tournament_to_modify.date = new_date
                    print("Le tournoi a été modifié")
                elif choix == '3':
                    new_time = "quickblitz"
                    while new_time.lower() not in {"bullet", "blitz", "quickshot"}:
                        new_time = input("Entrer le nouveau contrôle du temps du tournoi: ")
                    tournament_to_modify.controle_du_temps = new_time
                    print("Le tournoi a été modifié")
                elif choix == '4':
                    new_description = ""
                    while not new_description.isalpha():
                        new_description = input("Entrer la nouvelle description du tournoi: ")
                    tournament_to_modify.description = new_description
                    print("Le tournoi a été modifié")
                elif choix == '5':
                    return None
                else:
                    print("Je n'ai pas compris votre choix")
                    self.editer_tournoi(tous_les_tournois, bdd)
                settings.edit_tournament_encode(tournament_to_modify, bdd)
            except (ValueError, IndexError):
                print("Je n'ai pas compris votre choix")
                self.editer_tournoi(tous_les_tournois, bdd)
            except KeyboardInterrupt:
                print(" ==> Modification du tournoi annulée")
                return None
        else:
            print("Aucun tournoi n'a déjà été ajouté")
            return None
