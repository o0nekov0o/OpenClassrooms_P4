class Tour:
    def __init__(self, id, liste_de_matches):
        self.id = id
        self.liste_de_matches = liste_de_matches

    def completed(self, main_tournoi):
        for match in main_tournoi.tournees[-1].liste_de_matches:
            if match.resultat is None:
                return False
        return True
