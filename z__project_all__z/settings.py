from z__project_all__z import tournament
from z__project_all__z import player
from z__project_all__z import rounds
from z__project_all__z import versus
from datetime import datetime
import json


def validate(date_text):
    try:
        datetime.strptime(date_text, '%d-%m-%Y')
        return True
    except ValueError:
        return False


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, tournament.Tournoi):
            return {"id": o.id, "nom": o.nom, "lieu": o.lieu, "date": o.date,
                    "nombre_de_tours": o.nombre_de_tours, "tournees": o.tournees, "joueurs": o.joueurs,
                    "controle_du_temps": o.controle_du_temps, "description": o.description}
        elif isinstance(o, player.Joueur):
            return {"id": o.id, "nom_de_famille": o.nom_de_famille, "prenom": o.prenom,
                    "date_de_naissance": o.date_de_naissance, "sexe": o.sexe,
                    "classement": o.classement, "score": o.score}
        elif isinstance(o, rounds.Tour):
            return {"id": o.id, "liste_de_matches": o.liste_de_matches}
        elif isinstance(o, versus.Match):
            return {"id": o.id, "liste_de_joueurs": o.liste_de_joueurs, "resultat": o.resultat}
        return super().default(o)


def tournament_encode(tournoi, bdd):
    encoded_tournament = json.dumps(tournoi, cls=Encoder, indent=4)
    tournaments_table = bdd.table("tournaments")
    tournaments_table.insert(eval(encoded_tournament))


def edit_tournament_encode(tournoi, bdd):
    serialized_tournament = bdd.table("tournaments").all()
    encoded_tournament = json.dumps(tournoi, cls=Encoder, indent=4)
    for i in range(len(serialized_tournament)):
        if tournoi.id == f"tournoi_{i}":
            serialized_tournament[i] = eval(encoded_tournament)
            with open("db.json", "r") as jsonFile:
                data = json.load(jsonFile)
            data["tournaments"][f"{i + 1}"] = eval(encoded_tournament)
            with open("db.json", "w") as jsonFile:
                json.dump(data, jsonFile)


def edit_player_encode(tournoi, bdd, joueur):
    serialized_tournament = bdd.table("tournaments").all()
    encoded_player = json.dumps(joueur, cls=Encoder, indent=4)
    for i in range(len(serialized_tournament)):
        if tournoi.id == f"tournoi_{i}":
            serialized_player = bdd.table(f"players_{tournoi.id}").all()
            for j in range(len(serialized_player)):
                if joueur.id == f"joueur_{j}":
                    serialized_player[j] = eval(encoded_player)
                    with open("db.json", "r") as jsonFile:
                        data = json.load(jsonFile)
                    data[f"players_{tournoi.id}"][f"{j + 1}"] = eval(encoded_player)
                    with open("db.json", "w") as jsonFile:
                        json.dump(data, jsonFile)


def player_encode(tournoi, bdd, joueur):
    serialized_tournament = bdd.table("tournaments").all()
    for i in range(len(serialized_tournament)):
        if tournoi.id == f"tournoi_{i}":
            encoded_player = json.dumps(joueur, cls=Encoder, indent=4)
            players_table = bdd.table(f"players_{tournoi.id}")
            players_table.insert(eval(encoded_player))


def player_decode(bdd, tous_les_tournois):
    for tournoi in tous_les_tournois:
        serialized_player = bdd.table(f"players_{tournoi.id}").all()
        tournoi.joueurs = []
        for i in range(len(serialized_player)):
            deserialized_player = serialized_player[i]
            id = deserialized_player['id']
            nom_de_famille = deserialized_player['nom_de_famille']
            prenom = deserialized_player['prenom']
            date_de_naissance = deserialized_player['date_de_naissance']
            sexe = deserialized_player['sexe']
            classement = deserialized_player['classement']
            score = deserialized_player['score']
            joueur = player.Joueur(id=id, nom_de_famille=nom_de_famille, prenom=prenom,
                                   date_de_naissance=date_de_naissance, sexe=sexe,
                                   classement=classement, score=score)
            tournoi.joueurs.append(joueur)


def tournament_decode(bdd, tous_les_tournois):
    serialized_tournament = bdd.table("tournaments").all()
    for i in range(len(serialized_tournament)):
        deserialized_tournament = serialized_tournament[i]
        id = deserialized_tournament['id']
        nom = deserialized_tournament['nom']
        lieu = deserialized_tournament['lieu']
        date = deserialized_tournament['date']
        nombre_de_tours = deserialized_tournament['nombre_de_tours']
        tournees = deserialized_tournament['tournees']
        joueurs = deserialized_tournament['joueurs']
        controle_du_temps = deserialized_tournament['controle_du_temps']
        description = deserialized_tournament['description']
        tournoi = tournament.Tournoi(id=id, nom=nom, lieu=lieu, date=date, nombre_de_tours=nombre_de_tours,
                                     tournees=tournees, joueurs=joueurs,
                                     controle_du_temps=controle_du_temps, description=description)
        tous_les_tournois.append(tournoi)


def rounds_encode(tournoi, bdd, tour):
    serialized_tournament = bdd.table("tournaments").all()
    for i in range(len(serialized_tournament)):
        if tournoi.id == f"tournoi_{i}":
            encoded_round = json.dumps(tour, cls=Encoder, indent=4)
            rounds_table = bdd.table(f"rounds_{tournoi.id}")
            rounds_table.insert(eval(encoded_round))


def versus_encode(tournoi, bdd, match):
    serialized_tournament = bdd.table("tournaments").all()
    for i in range(len(serialized_tournament)):
        if tournoi.id == f"tournoi_{i}":
            encoded_match = json.dumps(match, cls=Encoder, indent=4)
            matches_table = bdd.table(f"matches_{tournoi.id}")
            matches_table.insert(eval(encoded_match))
            for j in range(len(match.liste_de_joueurs)):
                encoded_pairs = json.dumps(match.liste_de_joueurs[j], cls=Encoder, indent=4)
                pairs_table = bdd.table(f"pairs_{match.id}_{tournoi.id}")
                pairs_table.insert(eval(encoded_pairs))


def modify_round(round_being_edited, tournament, bdd):
    try:
        choix_quinquies = "oui"
        while choix_quinquies not in {"o", "n"}:
            choix_quinquies = input("Souhaitez-vous modifier un dernier match, oui (o) ou non (n) ? ")
            if choix_quinquies == "o":
                for i, match in enumerate(round_being_edited.liste_de_matches):
                    print(f"{i}/ {match.liste_de_joueurs[0].prenom} vs {match.liste_de_joueurs[1].prenom}")
                choix_sexties = int(input("Quel match voulez vous saisir ? "))
                match_to_modify = round_being_edited.liste_de_matches[choix_sexties]
                if match_to_modify.resultat is not None:
                    choix_septies = "oui"
                    while choix_septies not in {"o", "n"}:
                        choix_septies = input("Match déjà saisi, voulez-vous le modifier, "
                                              "oui (o) ou non (n) ? ")
                        if choix_septies == "o":
                            if match_to_modify.resultat == 0:
                                match_to_modify.liste_de_joueurs[0].score -= 1
                            elif match_to_modify.resultat == 1:
                                match_to_modify.liste_de_joueurs[0].score -= 0.5
                                match_to_modify.liste_de_joueurs[1].score -= 0.5
                            elif match_to_modify.resultat == 2:
                                match_to_modify.liste_de_joueurs[1].score -= 1
                            choix_octies = int(input(f"Quel est le score du match (0 si "
                                                     f"{match_to_modify.liste_de_joueurs[0].prenom} "
                                                     f"a gagné, 1 si nul, 2 si "
                                                     f"{match_to_modify.liste_de_joueurs[1].prenom}) ? "))
                            if choix_octies == 0:
                                match_to_modify.liste_de_joueurs[0].score += 1
                            elif choix_octies == 1:
                                match_to_modify.liste_de_joueurs[0].score += 0.5
                                match_to_modify.liste_de_joueurs[1].score += 0.5
                            elif choix_octies == 2:
                                match_to_modify.liste_de_joueurs[1].score += 1
                            match_to_modify.resultat = choix_octies
                            print("Score du match saisi")
                        elif choix_septies == "n":
                            rounds.Tour(f"tour_{len(tournament.tournees) + 1}",
                                        "liste_de_matchs").saisir_score(tournament, bdd)
            elif choix_quinquies == "n":
                rounds_encode(tournament, bdd, round_being_edited)
                for matches_played in round_being_edited.liste_de_matches:
                    versus_encode(tournament, bdd, matches_played)
                rounds.Tour(f"tour_{len(tournament.tournees) + 1}", "liste_de_matchs").ajouter_tour(tournament, bdd)
    except KeyboardInterrupt:
        rounds_encode(tournament, bdd, round_being_edited)
        for matches_played in round_being_edited.liste_de_matches:
            versus_encode(tournament, bdd, matches_played)
        print(" ==> Modification du tournoi annulée")
        print("-" * 163)
        return None


def rounds_decode(bdd, tous_les_tournois):
    for tournoi in tous_les_tournois:
        serialized_round = bdd.table(f"rounds_{tournoi.id}").all()
        tournoi.tournees = []
        for i in range(len(serialized_round)):
            deserialized_round = serialized_round[i]
            id = deserialized_round['id']
            liste_de_matches = deserialized_round['liste_de_matches']
            tour = rounds.Tour(id=id, liste_de_matches=liste_de_matches)
            tournoi.tournees.append(tour)


def versus_decode(bdd, tous_les_tournois):
    for tournoi in tous_les_tournois:
        serialized_match = bdd.table(f"matches_{tournoi.id}").all()
        for tour in tournoi.tournees:
            tour.liste_de_matches = []
            for i in range(len(serialized_match)):
                deserialized_match = serialized_match[i]
                id = deserialized_match['id']
                liste_de_joueurs = ['liste_de_joueurs']
                resultat = deserialized_match['resultat']
                match = versus.Match(id=id, liste_de_joueurs=liste_de_joueurs, resultat=resultat)
                tour.liste_de_matches.append(match)
    for tournoi in tous_les_tournois:
        for tour in tournoi.tournees:
            for match in tour.liste_de_matches:
                match.liste_de_joueurs = []
                serialized_pairs = bdd.table(f"pairs_{match.id}_{tournoi.id}").all()
                for j in range(len(serialized_pairs)):
                    deserialized_pairs = serialized_pairs[j]
                    num = deserialized_pairs['id']
                    nom_de_famille = deserialized_pairs['nom_de_famille']
                    prenom = deserialized_pairs['prenom']
                    date_de_naissance = deserialized_pairs['date_de_naissance']
                    sexe = deserialized_pairs['sexe']
                    classement = deserialized_pairs['classement']
                    score = deserialized_pairs['score']
                    joueur = player.Joueur(id=num, nom_de_famille=nom_de_famille, prenom=prenom,
                                           date_de_naissance=date_de_naissance, sexe=sexe,
                                           classement=classement, score=score)
                    match.liste_de_joueurs.append(joueur)
                print(match.id)
                print(match.liste_de_joueurs)
