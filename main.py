from modelsmvc import tournament, \
    player, round, versus, settings
settings.init()

# main_tournoi = tournament.Tournoi("")

def main_view():
    print("0/ Gérer les tournois")
    print("1/ Gérer les joueurs")
    print("2/ Gérer les matchs")


def main_controller():
    main_view()
    choix = input("Que voulez-vous faire ?")
    if choix == '0':
        pass
    elif choix == '1':
        player_controller()
    elif choix == '2':
        pass
    else:
        print("Je n'ai pas compris votre choix")
        main_controller()

def player_view():
    print("0/ Ajouter un joueur")
    print("1/ Modifier un joueur")
    print("2/ Revenir au menu principal")

def player_controller():
    player_view()
    choix = input("Que voulez-vous faire ?")
    if choix == '0':
        newplayer_controller()
    elif choix == '1':
        # selectionner tournoi, puis joueur
        pass
    elif choix == '2':
        main_controller()
    else:
        print("Je n'ai pas compris votre choix")
        player_controller()


def newplayer_controller():
    nom = input("quel est le nom du joueur ?")
    newjoueur = Joueur(nom=nom)
    main_tournoi.players.append(newjoueur)
    print("joueur ajoute")
    main_controller()


def editplayer_controller():
    for i, player in enumerate(main_tournoi.players):
        print(f"{settings.i}/ {player.nom}")
    index = input("tapez le num du joueur a modif")
    player_to_modify = maintournoi.players[index]
    # new_name = input("quel est le nouveau nom")
    # player_to_modify.nom = new_name
    main_controller()


main_controller()
