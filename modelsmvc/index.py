from modelsmvc import rounds
from modelsmvc import settings
settings.init()

def demarrer_projet():
    answer = "o-n"
    while answer.lower() not in {"o", "n"}:
        answer = input("Entrez si vous voulez ajouter un tournoi, oui (o) ou non (n): ")
        while answer == "o":
            # tournament.Tournoi.ajouter_tournoi() # appel direct via module player
            # player.Joueur.ajouter_joueur() # appel direct via module round
            poule.Tour.demarrer_tour()
            answer = "o-n"
            while answer.lower() not in {"o", "n"}:
                answer = input("Entrez si vous voulez ajouter un tournoi, oui (o) ou non (n): ")
                if answer == "o":
                    settings.deja_fait = []
                    settings.skip_0 = 0
                    settings.skip_1 = 0
                    continue
                elif answer == "n":
                    break
        return None


demarrer_projet()
