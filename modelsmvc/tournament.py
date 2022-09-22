from modelsmvc import settings


class Tournoi:
    def __init__(self, nom, lieu, date,
                 nombre_de_tours, tournees, joueurs,
                 controle_du_temps, description):
        self.nom = nom
        self.lieu = lieu
        self.date = date
        self.nombre_de_tours = nombre_de_tours
        self.tournees = tournees = []
        self.joueurs = joueurs
        self.controle_du_temps = controle_du_temps
        self.description = description

    def ajouter_tournoi():
        settings.num += 1
        globals()[f"tournoi_{settings.num}"] = Tournoi("nom", "lieu", "date",
                                                       "nombre_de_tours", "tournees", "joueurs",
                                                       "controle_du_temps", "description")
        globals()[f"tournoi_{settings.num}"].nom = ""
        while not globals()[f"tournoi_{settings.num}"].nom.isalpha():
            globals()[f"tournoi_{settings.num}"].nom = input("Entrez le nom du tournoi: ")
        globals()[f"tournoi_{settings.num}"].lieu = ""
        while not globals()[f"tournoi_{settings.num}"].lieu.isalpha():
            globals()[f"tournoi_{settings.num}"].lieu = input("Entrez le lieu du tournoi: ")
        globals()[f"tournoi_{settings.num}"].date = "99-99-9999"
        while not settings.validate(globals()[f"tournoi_{settings.num}"].date):
            globals()[f"tournoi_{settings.num}"].date = input("Entrez la date du tournoi, JJ-MM-AAAA: ")
        globals()[f"tournoi_{settings.num}"].nombre_de_tours = 4
        globals()[f"tournoi_{settings.num}"].tournees = []
        globals()[f"tournoi_{settings.num}"].joueurs = []
        globals()[f"tournoi_{settings.num}"].controle_du_temps = "quickblitz"
        while globals()[f"tournoi_{settings.num}"].controle_du_temps.lower() not in {"bullet", "blitz", "quickshot"}:
            globals()[f"tournoi_{settings.num}"].controle_du_temps = input("Entrez le controle du temps du tournoi, "
                                                                           "bullet, blitz ou quickshot: ")
        globals()[f"tournoi_{settings.num}"].description = ""
        while not globals()[f"tournoi_{settings.num}"].description.isalpha():
            globals()[f"tournoi_{settings.num}"].description = input("Entrez la description du tournoi: ")
        return globals()[f"tournoi_{settings.num}"]  # pour utilisation module player
