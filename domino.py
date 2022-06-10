"""
https://www.agoralude.com/blog/la-regle-du-jeu-de-dominos-n33

'un jeu de dominos classique est composé de 28 pièces dont chaque moitié comporte un certain nombre de petits points allant de 0 à 6.

On commence par mélanger tous les dominos, face cachée au milieu de la table et chaque joueur prend ses dominos de départ qu’il place devant lui en prenant soin de les  cacher aux autres joueurs.
Les dominos restants composent la pioche (ou le talon) placer à un endroit accessible à tous.
À 2 joueurs chacun prend 7 dominos, à 3 et 4 joueurs chacun prend 6 dominos, à 5 et 6 joueurs chacun prend 4 dominos.
    """

class Domino:
    """  """
    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b

    def affiche_points(self):
        print(f"face A : {self.a} face B : {self.b}")

    def valeur(self):
        return self.a + self.b


class Plateau:
    def __init__(self):
        pass


class Joueur:
    def __init__(self, name):
        self._dominos = {}
        self._name = name

    def addDomino(self, new_domino):
        pass


class Partie:

    def __init__(self, nb_joueurs=2):
        self._nb_joueurs = nb_joueurs
        # TODO : initialiser la pioche dans la partie ou dans le plateau ?
        self._pioche = None
        self._plateau = Plateau()
        self._joueurs = {}
        # TODO : vérifier si le ça prend bien le dernier élément
        for i in range (1, nb_joueurs+1):
            self._joueurs['Joueur'+i] = Joueur('Joueur'+i)
        # TODO : distribuer les dominos

    def distribue_dominos(self):
        """
        2 joueurs chacun prend 7 dominos, à 3 et 4 joueurs chacun prend 6 dominos, à 5 et 6 joueurs chacun prend 4 dominos.
        """
        pass

    def jeux_complet():
        """Génère une boite de domino complète

        Returns:
            [List]: List de dominos
        """
        jeux_complet = []
        for i in range(0, 6):
            j = 0
            for j in range (0, i):
                jeux_complet.append(Domino(j, i))
        return jeux_complet
