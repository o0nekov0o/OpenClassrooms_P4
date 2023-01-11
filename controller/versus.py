from views.versus import VersusView


class VersusController:
    def saisir_score(self, main_tournoi, bdd):
        """
        manages the input of the score for the ended matches into the round being managed
        :param matchs_confirmes: from versus.py.py, ajouter_match, for it to be appended in round matches list
        :param boucle: from versus.py.py, ajouter_match, for using of loop in this function
        :param tour_termine: from versus.py.py, ajouter_match, for management of created tour since code in tour.py
        :param main_tournoi: from versus.py.py, ajouter_match, for appending of round in the tournament rounds list
        :return: None
        """
        match_to_modify = VersusView().get_match_to_modify(main_tournoi, bdd)
        if match_to_modify.resultat is not None:
            choix_ter = VersusView().confirm_modify_existing_match()
            if choix_ter == "o":
                if match_to_modify.resultat == 0:
                    match_to_modify.liste_de_joueurs[0].score -= 1
                elif match_to_modify.resultat == 1:
                    match_to_modify.liste_de_joueurs[0].score -= 0.5
                    match_to_modify.liste_de_joueurs[1].score -= 0.5
                elif match_to_modify.resultat == 2:
                    match_to_modify.liste_de_joueurs[1].score -= 1

                choix_score = VersusView().get_new_score(match_to_modify)
                if choix_score == 0:
                    match_to_modify.liste_de_joueurs[0].score += 1
                elif choix_score == 1:
                    match_to_modify.liste_de_joueurs[0].score += 0.5
                    match_to_modify.liste_de_joueurs[1].score += 0.5
                elif choix_score == 2:
                    match_to_modify.liste_de_joueurs[1].score += 1
                match_to_modify.resultat = choix_score
                print("Score du match saisi")

            self.saisir_score(main_tournoi, bdd)
        else:
            choix_score = VersusView().get_new_score(match_to_modify)
            if choix_score == 0:
                match_to_modify.liste_de_joueurs[0].score += 1
            elif choix_score == 1:
                match_to_modify.liste_de_joueurs[0].score += 0.5
                match_to_modify.liste_de_joueurs[1].score += 0.5
            elif choix_score == 2:
                match_to_modify.liste_de_joueurs[1].score += 1
            match_to_modify.resultat = choix_score
            print("Score du match saisi")

        self.saisir_score(main_tournoi, bdd)
