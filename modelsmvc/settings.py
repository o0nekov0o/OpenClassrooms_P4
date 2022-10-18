from modelsmvc import tournament
from modelsmvc import player
from datetime import datetime
import json


def init():
    global deja_fait
    deja_fait = []
    global skip_0
    skip_0 = 0
    global skip_1
    skip_1 = 0
    global pwd
    pwd = -1
    global ref
    ref = -1
    global cancel
    cancel = 0
    global validate

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
                    "classement": o.classement, "score": o.score, "hasard": o.hasard}
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
            hasard = deserialized_player['hasard']
            joueur = player.Joueur(id=id, nom_de_famille=nom_de_famille, prenom=prenom,
                                   date_de_naissance=date_de_naissance, sexe=sexe,
                                   classement=classement, score=score, hasard=hasard)
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
