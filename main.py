from modelsmvc import tournament, \
    player, rounds, settings
from tinydb import TinyDB

db = TinyDB('db.json')
settings.init()
all_tournaments = []
settings.tournament_decode(db, all_tournaments)
settings.player_decode(db, all_tournaments)


def main_view():
    """
    main menu view
    :return: for main controller use
    """
    print("0/ Ajouter un tournoi")
    print("1/ Modifier un tournoi")
    if settings.cancel == 1:
        all_tournaments.pop(-1)
    for i, tournament in enumerate(all_tournaments):
        print(f"{i + 2}/ Gérer le tournoi {tournament.nom}")
        settings.cancel = 0
    choix = int(input("Que voulez vous faire ? "))
    print("-" * 163)
    return choix


def main_controller():
    """
    main menu controller
    :return: None
    """
    try:
        choix = main_view()
        if choix == 0:
            new_tournament = tournament.Tournoi(f"tournoi_{len(all_tournaments)}", "nom", "lieu", "date",
                                                "nombre_de_tours", "tournees", "joueurs", "controle_du_temps",
                                                "description").ajouter_tournoi_controller(all_tournaments, db)
            all_tournaments.append(new_tournament)
            main_controller()
        elif choix == 1:
            tournament.Tournoi(f"tournoi_{len(all_tournaments)}", "nom", "lieu", "date",
                               "nombre_de_tours", "tournees", "joueurs",
                               "controle_du_temps", "description").editer_tournoi_controller(all_tournaments, db)
            main_controller()
        else:
            tournament_to_manage = all_tournaments[choix - 2]
            tournament_controller(tournament_to_manage)
    except (ValueError, IndexError):
        print("Je n'ai pas compris votre choix")
        main_controller()
    except KeyboardInterrupt:
        print(" ==> Ajout du tournoi annulé")
        return None
    except TypeError:
        main_controller()
        return None


def tournament_view():
    """
    tournament menu view
    :return: for tournament controller use
    """
    print("0/ Gérer les joueurs")
    print("1/ Gérer les rounds")
    print("2/ Revenir au menu principal")
    choix = input("Que voulez vous faire ? ")
    print("-" * 163)
    return choix


def tournament_controller(main_tournoi):
    """
    tournament menu controller
    :param main_tournoi: from main_controller, tournament being managed
    :return: None
    """
    try:
        choix = tournament_view()
        if choix == '0':
            player_controller(main_tournoi)
            tournament_controller(main_tournoi)
        elif choix == '1':
            round_controller(main_tournoi)
            tournament_controller(main_tournoi)
        elif choix == '2':
            main_controller()
        else:
            print("Je n'ai pas compris votre choix")
            tournament_controller(main_tournoi)
    except KeyboardInterrupt:
        print(" ==> Gestion du tournoi annulée")
        main_controller()


def player_view():
    """
    player menu view
    :return: for player controller use
    """
    print("0/ Ajouter un joueur")
    print("1/ Modifier un joueur")
    print("2/ Revenir au menu précédent")
    print("3/ Revenir au menu principal")
    choix = input("Que voulez-vous faire ? ")
    print("-" * 163)
    return choix


def player_controller(main_tournoi):
    """
    player menu controller
    :param main_tournoi: from tournament_controller, tournament being managed
    :return: None
    """
    try:
        choix = player_view()
        if choix == '0':
            player.Joueur(f"joueur_{len(main_tournoi.joueurs)}", "nom_de_famille", "prenom", "date_de_naissance",
                          "sexe", "classement").ajouter_joueur_controller(main_tournoi, db)
            player_controller(main_tournoi)
        elif choix == '1':
            player.Joueur(f"joueur_{len(main_tournoi.joueurs)}", "nom_de_famille", "prenom", "date_de_naissance",
                          "sexe", "classement").editer_joueur_controller(main_tournoi, db)
            player_controller(main_tournoi)
        elif choix == '2':
            return None
        elif choix == '3':
            main_controller()
        else:
            print("Je n'ai pas compris votre choix")
            player_controller(main_tournoi)
    except KeyboardInterrupt:
        print(" ==> Gestion des joueurs annulée")
    except TypeError:
        player_controller(main_tournoi)
        return None


def round_view():
    """
    round menu view
    :return: for round controller use
    """
    print("0/ Ajouter des rounds")
    print("1/ Saisir le round en cours")
    print("2/ Revenir au menu précédent")
    print("3/ Revenir au menu principal")
    choix = input("Que voulez-vous faire ? ")
    print("-" * 163)
    return choix


def round_controller(main_tournoi):
    """
    round menu controller
    :param main_tournoi: from tournament_controller, tournament being managed
    :return:
    """
    try:
        choix = round_view()
        if choix == '0':
            rounds.Tour(f"tour_{len(main_tournoi.tournees) + 1}", "liste_de_matchs").ajouter_tour(main_tournoi, db)
        elif choix == '1':
            rounds.Tour(f"tour_{len(main_tournoi.tournees) + 1}", "liste_de_matchs").saisir_score(main_tournoi, db)
        elif choix == '2':
            return None
        elif choix == '3':
            main_controller()
        else:
            print("Je n'ai pas compris votre choix")
            round_controller(main_tournoi)
    except KeyboardInterrupt:
        print(" ==> Gestion des tours annulée")
        return None


main_controller()
