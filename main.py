from z__mvc__z import settings
from controller import tournament, player, rounds, versus
from tinydb import TinyDB

db = TinyDB('db.json')
all_tournaments = []
settings.tournament_decode(db, all_tournaments)


def main_view():
    """
    main menu view
    :return: for main controller use
    """
    print("0/ Ajouter un tournoi")
    print("1/ Modifier un tournoi")
    for i, tournoi in enumerate(all_tournaments):
        print(f"{i + 2}/ Gérer le tournoi {tournoi.nom}")
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
            tournament.TournamentController().ajouter_tournoi_controller(all_tournaments, db)
            main_controller()
        elif choix == 1:
            tournament.TournamentController().editer_tournoi_controller(all_tournaments, db)
            main_controller()
        else:
            tournament_to_manage = all_tournaments[choix - 2]
            tournament_controller(tournament_to_manage)
    except (ValueError, IndexError):
        print("Je n'ai pas compris votre choix")
        print("-" * 163)
        main_controller()
    except (ValueError, IndexError, AttributeError):
        print("Erreur de saisie, veuillez recommencer svp")
        print("-" * 163)
        tournament.TournamentController().editer_tournoi_controller(all_tournaments, db)
    except KeyboardInterrupt:
        print(" ==> Ajout du tournoi annulé")
        print("-" * 163)
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
            print("-" * 163)
            tournament_controller(main_tournoi)
    except (ValueError, IndexError, AttributeError):
        print("Erreur de saisie, veuillez recommencer svp")
        print("-" * 163)
        round_controller(main_tournoi)
    except KeyboardInterrupt:
        print(" ==> Gestion du tournoi annulée")
        print("-" * 163)
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
            player.PlayerController().ajouter_joueur_controller(main_tournoi, db)
            player_controller(main_tournoi)
        elif choix == '1':
            player.PlayerController().editer_joueur_controller(main_tournoi, db)
            player_controller(main_tournoi)
        elif choix == '2':
            return None
        elif choix == '3':
            main_controller()
        else:
            print("Je n'ai pas compris votre choix")
            print("-" * 163)
            player_controller(main_tournoi)
    except KeyboardInterrupt:
        print(" ==> Gestion des joueurs annulée")
        print("-" * 163)
    except (ValueError, IndexError, AttributeError):
        print("Erreur de saisie, veuillez recommencer svp")
        print("-" * 163)
        player.PlayerController().editer_joueur_controller(main_tournoi, db)
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
            rounds.RoundController().ajouter_tour(main_tournoi, db)
        elif choix == '1':
            versus.VersusController().saisir_score(main_tournoi, db)
        elif choix == '2':
            return None
        elif choix == '3':
            main_controller()
        else:
            print("Je n'ai pas compris votre choix")
            print("-" * 163)
            round_controller(main_tournoi)
    except (ValueError, IndexError, AttributeError):
        print("Erreur de saisie, veuillez recommencer svp")
        print("-" * 163)
        versus.VersusController().saisir_score(main_tournoi, db)
    except KeyboardInterrupt:
        print(" ==> Gestion des tours annulée")
        print("-" * 163)
        return None


main_controller()
