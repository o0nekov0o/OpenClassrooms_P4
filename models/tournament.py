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
