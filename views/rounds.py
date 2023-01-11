class RoundView:
    def ajouter_tour_success_view(self, new_matches):
        print("Nouveau round créé")
        print("-" * 163)
        print("Voici la liste des matches à jouer")
        for j, match in enumerate(new_matches):
            print(f"{j}/ {match.liste_de_joueurs[0].prenom} vs {match.liste_de_joueurs[1].prenom}")
        print("-" * 163)
