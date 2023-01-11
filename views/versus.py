from models.rounds import Tour
from controller import rounds
from z__mvc__z import settings

class VersusView:
    def get_new_score(self, match_to_modify):
        """
        param match_to_modify: match to modify
        :return: None
        """
        choix_score = int(input(f"Quel est le score du match (0 si "
                                f"{match_to_modify.liste_de_joueurs[0].prenom} a gagné, "
                                f"1 si nul, 2 si {match_to_modify.liste_de_joueurs[1].prenom}) ? "))
        print("-" * 163)
        return choix_score
    
    def confirm_modify_existing_match(self):
        choix = "oui"
        while choix not in {"o", "n"}:
            choix = input("Match déjà saisi, voulez-vous le modifier, oui (o) ou non (n) ? ")
            print("-" * 163)
        return choix
    
    def get_match_to_modify(self, main_tournoi, bdd):
        try:
            if not main_tournoi.tournees:
                print("Round non créé, créez-en un nouveau")
                rounds.RoundController().ajouter_tour(main_tournoi, bdd)
            round_to_modify = main_tournoi.tournees[-1]
            if Tour(f"tour_{len(main_tournoi.tournees) + 1}", "liste_de_matchs").completed(main_tournoi):
                print("Round terminé, créez-en un nouveau")
                settings.modify_round(round_to_modify, main_tournoi, bdd)
            for i, match in enumerate(round_to_modify.liste_de_matches):
                print(f"{i}/ {match.liste_de_joueurs[0].prenom} vs {match.liste_de_joueurs[1].prenom}")
            choix = int(input("Quel match voulez vous saisir ? "))
            print("-" * 163)
            match_to_modify = round_to_modify.liste_de_matches[choix]
            return match_to_modify

        except (ValueError, IndexError):
            print("Je n'ai pas compris votre choix")
            print("-" * 163)
            self.get_match_to_modify(main_tournoi, bdd)
        except KeyboardInterrupt:
            print(" ==> Modification du tour annulée")
            print("-" * 163)
            self.get_match_to_modify(main_tournoi, bdd)
