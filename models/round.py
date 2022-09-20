import random
import player
import versus
import settings


class Tour:
    def __init__(self, liste_de_matchs=[]):
        self.liste_de_matchs = liste_de_matchs
        global liste_de_joueurs
        liste_de_joueurs = {'0': player.joueur_0, '1': player.joueur_1, '2': player.joueur_2, '3': player.joueur_3,
                            '4': player.joueur_4, '5': player.joueur_5, '6': player.joueur_6, '7': player.joueur_7}

    def saisir_score():
        global match_0, match_1, match_2, match_3, j, \
            paire_0, paire_1, paire_2, paire_3, paire_4, paire_5, paire_6, paire_7
        paire_0, paire_1, paire_2, paire_3, paire_4, paire_5, paire_6, paire_7 = versus.Match.generer_paires()
        # utilisation contournee afin d'obtenir les valeurs de retour pour le reste de la fonction
        match_0 = match_1 = match_2 = match_3 = {}
        L = versus.j + 4
        if globals()[f"paire_{versus.j}"] and globals()[f"paire_{L}"] not in settings.deja_fait:
            while True:
                try:
                    globals()[f"paire_{versus.j}"]['0'].score += int(
                        input(f"Entrer le score de {globals()[f'paire_{versus.j}']['0'].prenom}"
                              f" (contre {globals()[f'paire_{versus.j}']['1'].prenom}): "))
                    globals()[f"paire_{versus.j}"]['1'].score += int(
                        input(f"Entrer le score de {globals()[f'paire_{versus.j}']['1'].prenom}"
                              f" (contre {globals()[f'paire_{versus.j}']['0'].prenom}): "))
                    globals()[f"paire_{versus.j}"]['0'].hasard += random.randrange(0, 11)
                    globals()[f"paire_{versus.j}"]['1'].hasard += random.randrange(0, 11)
                    settings.deja_fait.append(globals()[f"paire_{versus.j}"])
                    settings.deja_fait.append(globals()[f"paire_{L}"])
                except ValueError:
                    continue
                break
        elif globals()[f"paire_{versus.j}"] and globals()[f"paire_{L}"] in settings.deja_fait:
            globals()[f"paire_{versus.j}"]['0'].score += 0
            globals()[f"paire_{versus.j}"]['1'].score += 0
            globals()[f"paire_{versus.j}"]['0'].hasard += random.randrange(0, 11)
            globals()[f"paire_{versus.j}"]['1'].hasard += random.randrange(0, 11)
            versus.j = 3
        globals()[f"match_{versus.j}"]['0'] = [globals()[f"paire_{versus.j}"]['0'].prenom,
                                               globals()[f"paire_{versus.j}"]['0'].score]
        globals()[f"match_{versus.j}"]['1'] = [globals()[f"paire_{versus.j}"]['1'].prenom,
                                               globals()[f"paire_{versus.j}"]['1'].score]
        globals()[f"match_{versus.j}"] = tuple(globals()[f"match_{versus.j}"].values())
        globals()[f"tour_{settings.ref}"].liste_de_matchs.append(globals()[f"match_{versus.j}"])
        globals()[f"tournoi_{settings.num}"].tournees.append(globals()[f"tour_{settings.ref}"].liste_de_matchs)
        return None

    def demarrer_tour():
        globals()[f"tournoi_{settings.num}"] = player.Joueur.ajouter_joueur()  # ajout joueur avant tour
        # utilisation contournee afin d'obtenir la valeur de retour pour le reste de la fonction
        reponse = "o-n"
        while reponse.lower() not in {"o", "n"}:
            if settings.skip_0 == 0:
                reponse = input("Entrez si vous voulez ajouter un tour, oui (o) ou non (n): ")
            elif settings.skip_0 == 1 or settings.skip_0 == 2:
                reponse = "o"
            while reponse == "o":
                settings.ref += 1
                globals()[f"tour_{settings.ref}"] = Tour("liste_de_matchs")
                globals()[f"tour_{settings.ref}"].nom = f"round {settings.ref}"
                globals()[f"tour_{settings.ref}"].liste_de_matchs = []
                globals()[f"tour_{settings.ref}"].date_heure_de_debut = settings.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                versus.Match.ajouter_match()
                globals()[f"tour_{settings.ref}"].date_heure_de_fin = settings.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if settings.skip_0 == 0:
                    reponse = "o-n"
                elif settings.skip_0 == 1 or settings.skip_0 == 2:
                    reponse = "o"
                    print("Un nouveau tour va être ajouté pour y associer les matchs")
                    settings.skip_1 = 1
                    settings.skip_0 = 2
                while reponse.lower() not in {"o", "n"}:
                    if settings.skip_0 == 0:
                        if settings.skip_0 == 0:
                            reponse = input("Entrez si vous voulez ajouter un tour, oui (o) ou non (n): ")
                        elif settings.skip_0 == 1 or settings.skip_0 == 2:
                            reponse == "o"
                        if reponse == "o" and len(settings.deja_fait) < 56:
                            settings.skip_1 = 0
                            settings.skip_0 = 1
                            continue
                        elif reponse == "n" or len(settings.deja_fait) >= 56:
                            reponse = "n"
                            print("Pas de nouveau tour à ajouter pour le tournoi associé")
                            settings.skip_1 = 0
                            settings.skip_0 = 1
                            break
                    elif settings.skip_0 == 1 or settings.skip_0 == 2:
                        print("Un nouveau tour va être ajouté pour y associer les matchs")
                        settings.skip_1 = 1
                        settings.skip_0 = 2
                        continue
                if reponse == "n" or len(settings.deja_fait) >= 56:
                    print("Pas de nouveau tour à ajouter pour le tournoi associé")
                    break
            if reponse == "n" or len(settings.deja_fait) >= 56:
                break
        return None
