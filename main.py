from modelsmvc import tournament, \
    player, round, versus, settings

settings.init()

main_tournoi = tournament.Tournoi.ajouter_tournoi()


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


global ref
ref = -1  # a mettre dans settings


def newplayer_controller():
    global ref
    ref += 1
    nom_de_famille = input("quel est le nom du joueur ?")
    prenom = input("quel est le prenom du joueur ?")
    date_de_naissance = input("quel est la date de naissance du joueur ?")
    sexe = input("quel est le sexe du joueur ?")
    classement = ref
    locals()[f"joueur_{ref}"] = player.Joueur(nom_de_famille=nom_de_famille, prenom=prenom,
                                              date_de_naissance=date_de_naissance, sexe=sexe, classement=classement)
    main_tournoi.joueurs.append(locals()[f"joueur_{ref}"])
    print("joueur ajoute")
    player_controller()


def editplayer_controller():
    for i, joueur in enumerate(main_tournoi.joueurs):
        print(f"{i}/ {joueur.nom_de_famille}")
    index = input("tapez le nom du joueur a modif")
    player_to_modify = main_tournoi.joueurs(index)
    new_name = input("quel est le nouveau nom")
    player_to_modify.nom_de_famille = new_name
    main_controller()


main_controller()
