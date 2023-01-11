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
