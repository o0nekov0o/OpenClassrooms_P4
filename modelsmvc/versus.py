from modelsmvc import round
from modelsmvc import settings


class Match:
    def __init__(self, paire_0, paire_1, paire_2, paire_3, paire_4, paire_5, paire_6, paire_7):
        self.paire_0 = paire_0
        self.paire_1 = paire_1
        self.paire_2 = paire_2
        self.paire_3 = paire_3
        self.paire_4 = paire_4
        self.paire_5 = paire_5
        self.paire_6 = paire_6
        self.paire_7 = paire_7

    def generer_paires():
        global paire_0, paire_1, paire_2, paire_3, paire_4, paire_5, paire_6, paire_7
        sorted_keys = sorted(round.liste_de_joueurs, key=lambda k: round.liste_de_joueurs[k])
        round.liste_de_joueurs = {k: round.liste_de_joueurs[k] for k in sorted_keys}
        paire_0 = {'0': list(round.liste_de_joueurs.values())[0], '1': list(round.liste_de_joueurs.values())[4]}
        paire_1 = {'0': list(round.liste_de_joueurs.values())[1], '1': list(round.liste_de_joueurs.values())[5]}
        paire_2 = {'0': list(round.liste_de_joueurs.values())[2], '1': list(round.liste_de_joueurs.values())[6]}
        paire_3 = {'0': list(round.liste_de_joueurs.values())[3], '1': list(round.liste_de_joueurs.values())[7]}
        paire_4 = {'0': paire_0['1'], '1': paire_0['0']}
        paire_5 = {'0': paire_1['1'], '1': paire_1['0']}
        paire_6 = {'0': paire_2['1'], '1': paire_2['0']}
        paire_7 = {'0': paire_3['1'], '1': paire_3['0']}
        return paire_0, paire_1, paire_2, paire_3, paire_4, paire_5, paire_6, paire_7 # pour utilisation module round

    def ajouter_match():
        reply = "o-n"
        while reply.lower() not in {"o", "n"}:
            if settings.skip_1 == 0:
                reply = input("Entrez si vous voulez ajouter un match, oui (o) ou non (n): ")
            elif settings.skip_1 == 1:
                reply = "o"
            while reply == "o":
                global j
                j = 0
                for j in range(4):
                    # Match.generer_paires() # appel direct via module round
                    round.Tour.saisir_score()
                    if settings.skip_1 == 0:
                        reply = "o-n"
                    elif settings.skip_1 == 1:
                        reply = "o"
                    if reply == "o":
                        settings.skip_0 = 1
                    while reply.lower() not in {"o", "n"}:
                        if j != 3:
                            if settings.skip_1 == 0:
                                reply = input("Entrez si vous voulez ajouter un match, oui (o) ou non (n): ")
                            elif settings.skip_1 == 1:
                                reply = "o"
                            if reply == "o" and j < 3:
                                settings.skip_0 = 0
                                continue
                            elif reply == "n" or j == 3:
                                print("Pas de nouveau match à ajouter pour le tour associé")
                                if reply == "n":
                                    settings.skip_0 = 0
                                else:
                                    settings.skip_0 = 1
                                break
                        elif j == 3:
                            print("Pas de nouveau match à ajouter pour le tour associé")
                            settings.skip_0 = 1
                            break
                    if reply == "n" or j == 3:
                        print("Pas de nouveau match à ajouter pour le tour associé")
                        break
                if reply == "n" or j == 3:
                    break
            if reply == "n" or j == 3:
                break
        return None