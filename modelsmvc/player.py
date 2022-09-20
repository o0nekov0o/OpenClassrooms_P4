class Joueur:
    def __init__(self, nom_de_famille, prenom, date_de_naissance,
                 sexe, classement, score=0, hasard=0):
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

    def ajouter_joueur():
        globals()[f"tournoi_{settings.num}"] = tournament.Tournoi.ajouter_tournoi()  # ajout tournoi avant joueur
        # utilisation contournee afin d'obtenir la valeur de retour pour le reste de la fonction
        for m in range(8):
            globals()[f"joueur_{m}"] = Joueur("nom_de_famille", "prenom", "date_de_naissance",
                                              "sexe", "classement")
            globals()[f"joueur_{m}"].nom_de_famille = ""
            while not globals()[f"joueur_{m}"].nom_de_famille.isalpha():
                globals()[f"joueur_{m}"].nom_de_famille = input(f"Entrez le nom de famille du joueur {m}: ")
            globals()[f"joueur_{m}"].prenom = ""
            while not globals()[f"joueur_{m}"].prenom.isalpha():
                globals()[f"joueur_{m}"].prenom = input(f"Entrez le prenom du joueur {m}: ")
            globals()[f"joueur_{m}"].date_de_naissance = "99-99-9999"
            while not settings.validate(globals()[f"joueur_{m}"].date_de_naissance):
                globals()[f"joueur_{m}"].date_de_naissance = input(f"Entrez la date de naissance du joueur {m}, "
                                                                   f"JJ-MM-AAAA: ")
            globals()[f"joueur_{m}"].sexe = "homme"
            while globals()[f"joueur_{m}"].sexe.lower() not in {"m", "f"}:
                globals()[f"joueur_{m}"].sexe = input(f"Entrez le sexe du joueur {m}, masculin (m) ou feminin (f): ")
            globals()[f"joueur_{m}"].classement = m
            globals()[f"tournoi_{settings.num}"].joueurs.append(globals()[f"joueur_{m}"])
        return globals()[f"tournoi_{settings.num}"]  # pour utilisation module round
