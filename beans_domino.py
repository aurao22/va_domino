"""
Ce fichier contient toutes les classes utilisées pour ce projet
"""
from random import randint

class Jouer_Domino_Exception(Exception):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class Nombre_Joueurs_Exception(Exception):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self):
        self.message = "Il doit y avoir au moins 1 joueur et moins de 7 joueurs"

class Pioche_Interdite_Domino_Compatibles(Exception):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self):
        self.message = "Vous ne pouvez pas piocher un domino si vous disposez d'au moins un domino compatible."


class Domino:
    """Cette classe représente un Domino
    """
    def __init__(self, valeur_a_gauche=-1, valeur_a_droite=-1):
        """[summary]
            1. On veut pouvoir construire un domino avec des valeurs déterminées
            2. On veut pouvoir construire un domino avec des valeurs tirées au hasard
            3. On veut s'assurer que les valeurs des côtés du domino sont comprises entre 0 et 6
        Args:
            valeur_a_gauche (int, optional): one face value. Defaults to 0.
            b (int, optional): one face value. Defaults to 0.

        Raises:
            Exception: La valeur doit être entre 0 et 6 (inclus)
        """
        if valeur_a_gauche == -1:
            valeur_a_gauche = randint(0, 6)
        if valeur_a_droite == -1:
            valeur_a_droite = randint(0, 6)

        if valeur_a_gauche > 6 or valeur_a_gauche < 0 or valeur_a_droite > 6 or valeur_a_droite < 0:
            raise Exception("La valeur doit être entre 0 et 6 (inclus)")
        self._valeur_a_gauche = valeur_a_gauche
        self._valeur_a_droite = valeur_a_droite

    def score(self):
        """ Valeur du domino (somme des points des 2 faces)"""
        return self.valeur_a_gauche + self._valeur_a_droite
    
    def inverse(self):
        """ Inverse le sens du Domino"""
        temp = self._valeur_a_gauche
        self._valeur_a_gauche = self._valeur_a_droite
        self._valeur_a_droite = temp

    def __repr__(self):
        return str(self)

    def est_compatible(self, valeur):
        """
        Teste si le domino est compatible avec une valeur passée en paramètre
        c'est-à-dire s'il peut être placé à côté de cette valeur.
        La valeur 0 étant compatible avec n'importe quelle valeur
        """
        est_comp = self._valeur_a_droite == valeur or self._valeur_a_gauche == valeur
        est_comp = est_comp or self._valeur_a_droite == 0 or self._valeur_a_gauche == 0 or valeur == 0
        return est_comp

    def est_double(self):
        """vérifie si le domino a 2 faces égales

        Returns:
            Boolean: True si les 2 faces du domino sont égales, False sinon
        """
        return self._valeur_a_droite == self._valeur_a_gauche
    
    @property
    def valeur_a_gauche(self):
        return self._valeur_a_gauche

    @valeur_a_gauche.setter
    def valeur_a_gauche(self, valeur_a_gauche):
        raise Exception("La valeur ne peut pas être modifiée")

    @property
    def valeur_a_droite(self):
        return self._valeur_a_droite

    @valeur_a_droite.setter
    def valeur_a_droite(self, valeur_a_droite):
        raise Exception("La valeur ne peut pas être modifiée")

    def __str__(self):
        return f"[{' ' if self.valeur_a_gauche==0 else self.valeur_a_gauche}:{' ' if self.valeur_a_droite==0 else self.valeur_a_droite}]"
    
    def __eq__(self, other):
        
        if type(other) != type(self):
            return False
        
        # On vérifie l'égalité dans les deux sens
        equa = self.valeur_a_droite == other.valeur_a_droite and self.valeur_a_gauche == other.valeur_a_gauche
        equa = equa or (self.valeur_a_droite == other.valeur_a_gauche and self.valeur_a_gauche == other.valeur_a_droite)
        return equa

    # Less Than
    def __lt__(self, other):
        if isinstance(other, Domino):          
            return self.score() < other.score()
        if isinstance(other, int):
            self.score() < other
        return NotImplemented

    # Less Than or equals
    def __le__(self, other):
        if isinstance(other, Domino):          
            return self.score() <= other.score()
        if isinstance(other, int):
            self.score() <= other
        return NotImplemented

    # Greater Than
    def __gt__(self, other):
        if isinstance(other, Domino):          
            return self.score() > other.score()
        if isinstance(other, int):
            self.score() > other
        return NotImplemented

    # Greater Than or equals
    def __ge__(self, other):
        if isinstance(other, Domino):          
            return self.score() >= other.score()
        if isinstance(other, int):
            self.score() >= other
        return NotImplemented
    
    def __cmp__(self, other):
        # Cas de comparaison avec un autre Domino
        if isinstance(other, Domino):
            if self == other:
                return 0
            elif self < other:
                return -1
            elif self > other:
                return 1
            other = other.score()
        # Cas de comparaison avec un entier
        if isinstance(other, int):
            self_score = self.score()
            if self_score < other:
                return -1 
            elif self_score > other:
                return 1
            else:
                return 0
        return NotImplemented


class Joueur:

    def __init__(self, name, type="humain"):
        self._dominos_en_main = []
        self.name = name
        self._type = type
        
    def ajouter_domino(self, new_domino):
        """Ajoute un domino dans la main du Joueur

        Args:
            new_domino (Domino): Domino à ajouter
        """
        self._dominos_en_main.append(new_domino)

    def retirer_domino(self, domino_a_retirer):
        """Retire un domino de la main du joueur

        Args:
            domino_a_retirer (int or Domino): Domino à retirer (Position du domino dans la main ou le Domino à retirer)
        """
        if domino_a_retirer is not None:
            if isinstance(domino_a_retirer, int):
                self._dominos_en_main.pop(domino_a_retirer)
            elif isinstance(domino_a_retirer, Domino):
                self._dominos_en_main.remove(domino_a_retirer)
        
    def maxi_domino(self):
        """Recherche le domino en main avec la valeur la plus grande

        Returns:
            Domino: le domino qui a la valeur la plus grande
        """
        max_domino = None
        for domino in self.dominos_en_main:
            if max_domino == None:
                max_domino = domino
            elif domino > max_domino :
                max_domino = domino
        return max_domino

    def nb_domino_avec_la_valeur(self, valeur_recherchee):
        """Compte le nombre de domino en main avec la valeur recherchée.
        Un domino double ne compte qu'une fois

        Args:
            valeur_recherchee (int): valeur à compter

        Returns:
            int: Le nombre de domino avec la valeur reçue (ou 0 si aucune)
        """
        nb = 0
        for dom in self._dominos_en_main:
            if dom.valeur_a_droite == valeur_recherchee or dom.valeur_a_gauche == valeur_recherchee:
                nb += 1
        return nb

    def maxi_double(self):
        """Recherche le domino double en main avec la plus grande valeur

        Returns:
            Domino: Domino double le plus grand ou None si aucun domino double
        """
        maxi = None
        for domino in self._dominos_en_main:
            if domino.est_double():
                if maxi is None:
                    maxi = domino
                elif domino > maxi:
                    maxi = domino
        return maxi

    def score(self):
        """Calcule les points dans les mains du joueur (somme des points de domino en main)

        Returns:
            int: Score du joueur
        """
        score = 0
        if self._dominos_en_main is not None:
            for domino in self._dominos_en_main:
                score += domino.score()
        return score

    def str_main(self):
        """Construit une chaine représentant la main du joueur

        Returns:
            str: Chaine représentant la main du joueur
        """
        main = ""
        for domino in self._dominos_en_main:
            main += f"{domino} "
        return main

    def str_position(self):
        """Construit une chaine représentant la position de chaque domino en main du joueur

        Returns:
            str: Chaine représentant la position des domino en  main du joueur
        """
        main = ""
        for i in range(0, len(self._dominos_en_main)):
            main += f"[ {i} ] "
        return main

    def affiche_main_et_positions(self):
        prefix_main = f"{self.name}: {len(self._dominos_en_main)}=>"
        prefix_position = "positions:"
        taille_pos = len(prefix_position)
        # Formatage de la sortie pour que les dominos et leurs positions soient alignés
        if len(prefix_main) < taille_pos:
            prefix_main = prefix_main +" "*(taille_pos - len(prefix_main))
        else:
            prefix_position = prefix_position+" "*(len(prefix_main) - taille_pos)
        print(prefix_main+self.str_main())
        print(prefix_position + self.str_position())
        
    @property
    def dominos_en_main(self):
        # On retourne une copie de la main pour éviter les modifications de la liste
        return self._dominos_en_main.copy()

    @dominos_en_main.setter
    def dominos_en_main(self, dominos_en_main):
        self._dominos_en_main = dominos_en_main

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        raise Exception("Le type de joueur ne peut pas être modifié")

    def dominos_compatibles(self, valeur_gauche, valeur_droite):
        """Recherche les dominos compatibles dans la main du joueur
        Args:
            valeur_gauche (int): valeur à comparer
            valeur_droite (int): valeur à comparer

        Returns:
            List(Domino): Liste de domino compatibles ou liste vide
        """
        dominos = []
        for domi in self.dominos_en_main:
            if domi.est_compatible(valeur_gauche) or domi.est_compatible(valeur_droite):
                dominos.append(domi)
        return dominos

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.name}: {len(self._dominos_en_main)}=>" + self.str_main()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                                              TESTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DOMINO
def test_domino_constructeur():
    print("Domino > constucteur et repr")
    mon_domino = Domino()
    assert mon_domino.valeur_a_gauche in range(0, 7)
    assert mon_domino.valeur_a_droite in range(0, 7)
    mon_domino = Domino(0, 5)
    assert mon_domino.valeur_a_gauche == 0
    assert mon_domino.valeur_a_droite == 5
    mon_autre_domino = Domino(1, 4)
    assert mon_autre_domino.__repr__() == '[1:4]'
    assert mon_domino.__repr__() == '[ :5]'
    print(mon_domino, mon_autre_domino)

def test_domino_constructeur_erreur():
    print("Domino > constucteur > exception")
    # Doit lever une exception
    try:
        mon_faux_domino = Domino(7, 7)
        raise AssertionError(f"Une exception aurait dû être levée:{mon_faux_domino}") 
    except:
        assert True
    try:
        mon_faux_domino = Domino(-1, 0)
        raise AssertionError(f"Une exception aurait dû être levée:{mon_faux_domino}") 
    except:
        assert True
    try:
        mon_faux_domino = Domino(1, 7)
        raise AssertionError(f"Une exception aurait dû être levée:{mon_faux_domino}") 
    except:
        assert True

def test_domino_inverse():
    print("Domino > inverse()")
    mon_domino = Domino(0, 5)
    print(mon_domino)
    mon_domino.inverse()
    assert mon_domino.valeur_a_gauche == 5
    assert mon_domino.valeur_a_droite == 0
    print(mon_domino)

def test_domino_score():
    print("Domino > score()")
    mon_autre_domino = Domino(1, 4)
    assert mon_autre_domino.score() == 5

def test_domino_est_compatible():
    print("Domino > est_compatible()")
    mon_domino = Domino(0, 5)
    assert mon_domino.est_compatible(4) == True
    mon_autre_domino = Domino(1, 4)
    assert mon_autre_domino.est_compatible(4) == True
    assert mon_autre_domino.est_compatible(5) == False
    assert mon_autre_domino.est_compatible(0) == True

def test_domino_equals():
    print("Domino > equals()")
    mon_domino = Domino()
    assert mon_domino == mon_domino
    assert mon_domino != Domino(0, 5)

def test_domino_less_than():
    print("Domino > less than()")
    mon_domino = Domino(5, 4)
    mon_domino2 = Domino(6, 4)
    assert mon_domino < mon_domino2
    assert not mon_domino2 < mon_domino

def test_domino_more_than():
    print("Domino > less than()")
    mon_domino = Domino(5, 4)
    mon_domino2 = Domino(6, 4)
    assert not mon_domino > mon_domino2
    assert mon_domino2 > mon_domino
    

def test_domino():
    print("Domino > START")
    test_domino_constructeur()
    test_domino_constructeur_erreur()
    test_domino_inverse()
    test_domino_score()
    test_domino_est_compatible()
    test_domino_equals()
    test_domino_less_than()
    test_domino_more_than()
    print("Domino > END")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# JOUEURS
def test_joueur_constructeur():
    print("Joueur > constucteur")
    # def __init__(self, name, type="humain"):
    j1 = Joueur("Player1")
    assert j1.type == "humain"
    assert j1.name == "Player1"
    j2 = Joueur("Player2", "ordinateur")
    assert j2.name == "Player2"
    assert j2.type == "ordinateur"

def test_joueur_exception():
    print("Joueur > Exceptions")
    j1 = Joueur("Player1")
    try:
        j1.type = "ordinateur"
        raise AssertionError("La modification du type devrait déclencher une erreur")
    except:
        assert True

def test_joueur_ajouter_domino(no_joueur=1):
    print("Joueur > Ajouter Domino")
    j1 = Joueur("Player"+str(no_joueur))
    for i in range (5):
        j1.ajouter_domino(Domino())
    assert len(j1.dominos_en_main) == (i+1)
    print(j1)
    return j1


def test_joueur_retirer_domino(joueur=None):
    print("Joueur > Ajouter Domino")
    if joueur is None:
        joueur = test_joueur_ajouter_domino()
    
    pos = 0
    for i in range(len(joueur.dominos_en_main)):
        domino = joueur.dominos_en_main[pos]
        joueur.retirer_domino(pos)
        if len(joueur.dominos_en_main)> 0:
            assert joueur.dominos_en_main[pos] != domino
        else:
            # Cas où il n'y a plus de domino
            assert True
    # Tester le retrait d'un domino avec index hors liste
    joueur = test_joueur_ajouter_domino()
    pos = len(joueur.dominos_en_main) + 2
    try:
        joueur.retirer_domino(pos)
        raise AssertionError("Le retrait d'un domino d'un index > à la taille de la liste devrait lever une erreur")
    except:
        assert True

def test_joueur_maxi_double():
    print("Joueur > Maxi Double")
    j1 = Joueur("Player")
    for i in range (6):
        j1.ajouter_domino(Domino(i, i))  
        maxi = j1.maxi_double()
        assert maxi.score() == i*2

    j1 = Joueur("Player")
    maxi = j1.maxi_double()
    assert maxi is None

    j1.ajouter_domino(Domino(1,2))
    j1.ajouter_domino(Domino(2,3))
    j1.ajouter_domino(Domino(3,4))
    maxi = j1.maxi_double()
    assert maxi is None

    j1.ajouter_domino(Domino(4,4))
    maxi = j1.maxi_double()
    assert maxi.score() == 8

def test_joueur_maxi_domino():
    print("Joueur > Maxi Domino")
    j1 = Joueur("Player1")
    maxi = j1.maxi_domino()
    assert maxi is None
    j1.ajouter_domino(Domino(1,2))
    j1.ajouter_domino(Domino(2,3))
    j1.ajouter_domino(Domino(3,4))
    ma = Domino(5,6)
    j1.ajouter_domino(ma)
    maxi = j1.maxi_domino()
    assert maxi == ma



def test_joueur_dominos_compatibles():
    print("Joueur > Dominos compatibles")
    j1 = Joueur("Player1")
    try:
        compatibles = j1.dominos_compatibles()
        raise AssertionError("Exception manquante pour les paramètres manquants")
    except:
        assert True
    compatibles = j1.dominos_compatibles(1,0)
    assert len(compatibles) == 0
    j1.ajouter_domino(Domino(1,2))
    j1.ajouter_domino(Domino(2,3))
    j1.ajouter_domino(Domino(3,4))
    
    compatibles = j1.dominos_compatibles(1,0)
    assert len(compatibles) == 3

    compatibles = j1.dominos_compatibles(1,2)
    assert len(compatibles) == 2
    compatibles = j1.dominos_compatibles(6,4)
    assert len(compatibles) == 1

    compatibles = j1.dominos_compatibles(5,6)
    assert len(compatibles) == 0


def test_joueur():
    print("Joueur > START")
    test_joueur_constructeur()
    test_joueur_exception()
    j1 = test_joueur_ajouter_domino()
    j1.affiche_main_et_positions()
    j1.name="ARA"
    j1.affiche_main_et_positions()
    test_joueur_retirer_domino()
    test_joueur_maxi_double()
    test_joueur_maxi_domino()
    test_joueur_dominos_compatibles()
    print("Joueur > END")



if __name__ == "__main__":
    test_domino()
    test_joueur()