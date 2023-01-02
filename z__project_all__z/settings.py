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


def player_decode(serialized_players):
    players = []
    for i in range(len(serialized_players)):
        deserialized_player = serialized_players[i]
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
        players.append(joueur)
    return players


def versus_decode(serialized_matches, players):
    matches = []
    for i in range(len(serialized_matches)):
        deserialized_match = serialized_matches[i]
        id = deserialized_match['id']
        liste_de_joueurs = player_decode(deserialized_match['liste_de_joueurs'])
        for j in range(len(liste_de_joueurs)):
            for k in range(len(players)):
                if liste_de_joueurs[j].id == players[k].id:
                    liste_de_joueurs[j] = players[k]
                else:
                    print("erreur de désérialisation")
        resultat = deserialized_match['resultat']
        match = versus.Match(id=id, liste_de_joueurs=liste_de_joueurs, resultat=resultat)
        matches.append(match)
    return matches


def rounds_decode(serialized_rounds, players):
    tournees = []
    for i in range(len(serialized_rounds)):
        deserialized_round = serialized_rounds[i]
        id = deserialized_round['id']
        liste_de_matches = versus_decode(deserialized_round['liste_de_matches'], players)
        tour = rounds.Tour(id=id, liste_de_matches=liste_de_matches)
        tournees.append(tour)
    return tournees


def tournament_decode(bdd, tous_les_tournois):
    serialized_tournament = bdd.table("tournaments").all()
    for i in range(len(serialized_tournament)):
        deserialized_tournament = serialized_tournament[i]
        id = deserialized_tournament['id']
        nom = deserialized_tournament['nom']
        lieu = deserialized_tournament['lieu']
        date = deserialized_tournament['date']
        nombre_de_tours = deserialized_tournament['nombre_de_tours']
        joueurs = player_decode(deserialized_tournament['joueurs'])
        tournees = rounds_decode(deserialized_tournament['tournees'], joueurs)
        controle_du_temps = deserialized_tournament['controle_du_temps']
        description = deserialized_tournament['description']
        tournoi = tournament.Tournoi(id=id, nom=nom, lieu=lieu, date=date, nombre_de_tours=nombre_de_tours,
                                     tournees=tournees, joueurs=joueurs,
                                     controle_du_temps=controle_du_temps, description=description)
        tous_les_tournois.append(tournoi)


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
                edit_tournament_encode(tournament, bdd)
                rounds.Tour(f"tour_{len(tournament.tournees) + 1}", "liste_de_matchs").ajouter_tour(tournament, bdd)
    except KeyboardInterrupt:
        edit_tournament_encode(tournament, bdd)
        print(" ==> Modification du tournoi annulée")
        print("-" * 163)
        return None
