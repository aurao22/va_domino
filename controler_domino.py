from beans_domino import *
from random import sample


class Partie:
    """
    2 joueurs chacun prend 7 dominos, à 3 et 4 joueurs chacun prend 6 dominos, à 5 et 6 joueurs chacun prend 4 dominos.
    """
    regles = { 2: 7,
               3: 6,
               4: 6,
               5: 4,
               6: 4
              }
    
    def jeux_complet():
        """Génère une boite de domino complète

        Returns:
            [List]: List de dominos
        """
        jeux_complet = []

        for i in range(0, 7):
            j = 0
            for j in range (0, i):
                jeux_complet.append(Domino(j, i))
            jeux_complet.append(Domino(i, i))
        return jeux_complet
    
    def __init__(self, partie_name="", niveau_ia=1):
        self._joueurs = []
        self._pioche = None
        self._plateau = []
        self.partie_name = partie_name
        self._joueur_courant_position = 0
        self._niveau_ia=niveau_ia

    def ajouter_ordinateur(self):
        self.ajouter_joueur(Joueur("Ordinateur", "ordinateur"))

    def ajouter_joueur(self, joueur):
        res = None
        if len(self._joueurs) < 6 :
            if isinstance(joueur, str):
                res=Joueur(joueur)
                self._joueurs.append(res)
            elif isinstance(joueur, Joueur):
                res=joueur
                self._joueurs.append(joueur)
            else : 
                raise Exception ('La création de joueur doit être de type str ou obj !')
        else :
            raise Nombre_Joueurs_Exception()
        return res

    def distribue_dominos(self):
        """
        Distribus les dominos de manière aléatoire aux joueurs
        """
        # Initialisation de la pioche
        self._pioche = Partie.jeux_complet()

        # nombre de joueurs
        nb_joueurs = len(self._joueurs)
        if nb_joueurs < 1:
            raise Exception("Aucun joueur n'a été ajouté")
        elif nb_joueurs == 1:
            self.ajouter_joueur("Ordinateur")
            nb_joueurs = len(self._joueurs)

        # nombre de dominos à distribuer en fonction du nombre de joueurs
        nb_dominos = Partie.regles[nb_joueurs]

        for joueur in self._joueurs:
            # on tire au sort les dominos
            main = sample(self._pioche, nb_dominos)
            # on affecte les dominos au joeur
            joueur.dominos_en_main = main
            # on suprrime les dominos déjà distribués de la pioche
            for domino in main:
                self._pioche.remove(domino)
    
    def pioche_auto(self, joueur):
        """[summary]

        Args:
            partie ([type]): [description]
            joueur ([type]): [description]

        Returns:
            [type]: [description]
        """
        domino = self.pioche(joueur)
        if domino is not None:
            self.deposer_domino_auto(joueur, domino)
        return domino

    def peut_piocher(self, joueur):
        dominos = joueur.dominos_compatibles(self.domino_a_gauche, self.domino_a_droite)
        return len(dominos) == 0

    def pioche(self, joueur):
        """[summary]

        Returns:
            [type]: [description]
        """
         # On vérifie que le joueur n'a pas un domino compatible dans son jeu
        dominos = joueur.dominos_compatibles(self.domino_a_gauche, self.domino_a_droite)
        if len(dominos) > 0:
            raise Pioche_Interdite_Domino_Compatibles()
        domino = None
        print("Pioche:", end="")
        if len(self._pioche) > 0:
            domino = sample(self._pioche, 1)
            if domino is not None:
                domino = domino[0] 
                self._pioche.remove(domino)
        print(domino)
        # On ajoute le domino à la main du joueur
        if domino is not None:
            joueur.ajouter_domino(domino)
        return domino

    def affiche_plateau(self):
        print("------------------------------------")
        print("PLATEAU => ", end="")
        for domino in self._plateau:
            print(domino, end="")
        print("")
        print("------------------------------------")
    
    def affiche_joueurs_mains(self):
        for joueur in self._joueurs:
            print(joueur)

    def affiche_pioche(self):
        print(f"Pioche:{len(self._pioche)}=>{self._pioche}")
    
    def domino_a_gauche(self):
        if len(self._plateau) == 0:
            raise Exception("Aucun domino sur le plateau")
        return self._plateau[0].valeur_a_gauche

    def domino_a_droite(self):
        if len(self._plateau) == 0:
            raise Exception("Aucun domino sur le plateau")
        return self._plateau[-1].valeur_a_droite


    def jouer_domino(self, joueur, domino, cote):
        # On vérifie que ce joueur peut bien jouer
        # if self.joueur_courant().name != joueur.name:
        #     raise Jouer_Domino_Exception(f"Le joueur {joueur} ne peut pas jouer, il s'agit du tour du joueur {self.joueur_courant}")
        if cote is not None and domino is not None:
            cote = cote.lower()
            if "i" in cote :
                domino.inverse()
            if "g" in cote:
                if self.deposer_domino_a_gauche(joueur, domino):
                    return True
                else:
                    raise Jouer_Domino_Exception(f"Impossible de déposer le domino tel que : {domino} <> {self.domino_a_gauche()}")
            elif "d" in cote:
                if self.deposer_domino_a_droite(joueur, domino):
                    return True
                else:
                    raise Jouer_Domino_Exception(f"Impossible de déposer le domino tel que : {self.domino_a_droite()} <> {domino}")
            else:
                raise Jouer_Domino_Exception("Erreur de côté de position (g ou d ou ig ou id)")  
        else:
            if cote is None :
                raise Jouer_Domino_Exception("Erreur de côté de position (g ou d ou ig ou id)")
            else:
                raise Jouer_Domino_Exception("Erreur de sélection du Domino")


    def deposer_domino_auto(self, joueur, domino, inverse=False):
        """Tente de deposer le domino des deux côtés et en inversant le domino

        Args:
            joueur (Joueur): Joueur en cours
            domino (Domino): Domino à déposer
            inverse (bool, optional): [description]. Defaults to False.

        Returns:
            [type]: [description]
        """
        res = self.deposer_domino_a_gauche(joueur, domino)
        if not res:
            res = self.deposer_domino_a_droite(joueur, domino)
            if not res and not inverse:
                domino.inverse()
                res = self.deposer_domino_auto(joueur, domino, inverse=True)
        return res

    def deposer_domino_a_gauche(self, joueur, domino):
        """ Ajoute le domino à la chaine
        Args:
            joueur (Joueur): Joueur en cours
            domino (Domino): le domino à ajouter

        Raises:
            Exception: S'il ne s'agit pas d'un Domino

        Returns:
            Boolean: True si le Domino a été déposé, False si le domino ne pouvait pas être déposé (incompatible)
        """
        ajout_success = self._ajouter_domino(joueur, domino, "gauche")
        return ajout_success
    
    def deposer_domino_a_droite(self, joueur, domino):
        """ Ajoute le domino à la chaine

        Args:
            joueur (Joueur): Joueur en cours
            domino (Domino): le domino à ajouter

        Raises:
            Exception: S'il ne s'agit pas d'un Domino

        Returns:
            Boolean: True si le Domino a été déposé, False si le domino ne pouvait pas être déposé (incompatible)
        """
        ajout_success = self._ajouter_domino(joueur, domino, "droite")
        return ajout_success

    def deposer_premier_domino(self, joueur, domino):
        """ Ajoute le domino à la chaine

        Args:
            joueur (Joueur): Joueur en cours
            domino (Domino): le domino à ajouter

        Raises:
            Exception: S'il ne s'agit pas d'un Domino

        Returns:
            Boolean: True si le Domino a été déposé, False si le domino ne pouvait pas être déposé (incompatible)
        """
        ajout_success = self._ajouter_domino(joueur, domino, "")
        return ajout_success  

    def joueur_courant(self):
        """
        Raises:
            Exception: Si aucun joueur couarnt n'est définit (avant de déterminer le 1er joueur par exemple)

        Returns:
            [Joeur]: Le joueur courant
        """
        if self._joueur_courant_position > -1:
            return self._joueurs[self._joueur_courant_position]
        else :
            raise Exception("Aucun joueur courant définit")
    
    def joueur_suivant(self):
        """
        Raises:
            Exception: Si aucun joueur courant n'est définit, il ne peut pas y avoir de joueur suivant

        Returns:
            [Joueur]: Le joueur suivant
        """
        if self._joueur_courant_position > -1:
            self._joueur_courant_position += 1
            if self._joueur_courant_position >= len(self._joueurs):
                self._joueur_courant_position = 0
            return self._joueurs[self._joueur_courant_position]
        else :
            raise Exception("Aucun joueur courant définit, donc aucun suivant ne peut être définit")

    def premier_joueur(self):
        """Identifie le premier joueur de la partie en suivant les règles suivantes :
            - Le joueur ayant le double le plus élevé commence la partie de dominos et pose son domino au centre de la 
            table (si personne n’a pas le double 6, c’est le double 5 qui commence, etc.… et 
            - si personne n’a de double, c'est le domino 6/5 qui commence ou sinon le 6/4 etc.). 
                  
        Returns:
            [Joueur]: Le joueur qui doit commencer la partie
            [Domino] : Le domino que doit jouer le joueur
        """
        premier_domino = None 
        premier_joueur = None
        pos = 0
        for joueur in self._joueurs:
            # On vérifie la présence de double pour chaque joueurs, en gardant le plus grand
            if premier_domino == None:
                # On défini la valeur de premier_domino par la première valeur trouvé
                premier_domino = joueur.maxi_double()
                if premier_domino is not None:
                    premier_joueur = joueur
                    self._joueur_courant_position = pos
            else :
                # On vérifie maintenant si les nouveaux doubles trouvé sont plus grands que la valeur enregistré
                double_joueur = joueur.maxi_double()
                if double_joueur is not None and double_joueur.score() > premier_domino.score() :
                    premier_domino = double_joueur
                    premier_joueur = joueur
                    self._joueur_courant_position = pos
            pos += 1

        # On applique maintenant la règle dans le cas ou aucun joueurs ne possède de domino double
        # On regarde donc la valeur maximun des dominos présent dans la main de chaque joueurs
        if premier_joueur is None :
            pos = 0
            for joueur in self._joueurs:
                if premier_domino == None:
                    premier_domino = joueur.maxi_domino()
                    premier_joueur = joueur
                    self._joueur_courant_position = pos
                else :
                    joueur_max_dom = joueur.maxi_domino()
                    if  joueur_max_dom is not None and joueur_max_dom.score() > premier_domino.score() :
                        premier_domino = joueur_max_dom
                        premier_joueur = joueur
                        self._joueur_courant_position = pos
                pos += 1
        return premier_joueur, premier_domino
    
    def nb_domino_avec_la_valeur(self, valeur_recherchee):
        """Compte le nombre de domino dans la pioche avec la valeur recherchée.
        Un domino double ne compte qu'une fois

        Args:
            valeur_recherchee (int): valeur à compter

        Returns:
            int: Le nombre de domino avec la valeur reçue (ou 0 si aucune)
        """
        nb = 0
        for dom in self._plateau:
            if dom.valeur_a_droite == valeur_recherchee or dom.valeur_a_gauche == valeur_recherchee:
                nb += 1
        return nb


    def tour_auto(self, joueur):
        """Joue le tour automatiquement ou semi automatiquement

        Args:
            partie (Partie): [description]
            joueur (Joueur): [description]
        """
        # On affiche le plateau
        self.affiche_plateau()
        # on affiche les dominos du joueur courant
        print(joueur)
        # Recupérer les dominos compatibles
        dominos = joueur.dominos_compatibles(self.domino_a_gauche(), self.domino_a_droite())
        if len(dominos)==0:
            self.pioche_auto(joueur)
        else:
            domi = None
            # Ajout d'un peu d'IA, on pose le domino compatible
            # qui a le plus de points au lieu de le sélectionner en aléaoire
            if self._niveau_ia == 1: 
                for dom in dominos:
                    if domi == None:
                        domi = dom
                    else:
                        if dom > domi:
                            domi = dom
            # Domino max qui permettrait de bloquer le jeu
            elif self._niveau_ia == 2:
                domi = self._ia_2(joueur, dominos)
            elif self._niveau_ia == 3:
                domi = self._ia_3(joueur, dominos)
                
            # Echec des IA ou Pas d'IA, tirage aléatoire
            if domi is None:
                domi = sample(dominos, 1)[0]

            self.deposer_domino_auto(joueur, domi)
        # on traite le cas où le cas où il n'y a plus de domino en main
        # on affiche les dominos du joueur courant
        print(joueur)
        return len(joueur.dominos_en_main) > 0
        

    @property
    def joueurs(self):
        return self._joueurs

    @joueurs.setter
    def joueurs(self, joueurs):
         raise Exception("Impossible de modifier les joueurs en cours de partie !")        

    def classement(self):
        """ Calcul le nombre de points dans les mains des joueurs et les ajoute dans un dictionnaire
            Le gagnant est celui qui totalise le moins de points.
        Returns:
            Dict(int, List[Joueur]): (nb points, Liste de joueurs concernés)
        """
        classe = {}
        if self._joueurs is not None:
            for joueur in self._joueurs:
                score = joueur.score()
                liste = classe.get(score, [])
                liste.append(joueur.name)
                classe[score] = liste
        return classe

    def affiche_classement(self):
        """ Affiche le classement trié du 1er au dernier joueur.
            Le gagnant est celui qui totalise le moins de points.
        """
        classe = self.classement()
        if classe is not None:
            nb_points = list(classe.keys())
            nb_points.sort()
            i = 1
            for nb_point in nb_points:
                print(f"{i} - avec {nb_point} pour :{classe[nb_point]}")
                i += 1
        else:
            print("Aucun classement à afficher")

    def __repr__(self):
        return self.str()

    def __str__(self):
        return f"{self.partie_name}:{self.classement()}"

    def _ajouter_domino(self, joueur, domino, position):
        """Ajoute un domino dans la chaine de domino de la partie

        Args:
            joueur (Joueur): Joueur en cours
            domino (Domino): le domino à ajouter
            position (String): emplacement où déposer le domino : 'droite' ou 'gauche'

        Raises:
            Exception: Si l'emplacement indiqué n'existe pas ou s'il ne s'agit pas d'un Domino

        Returns:
            Boolean: True si le Domino a été déposé, False si le domino ne pouvait pas être déposé (incompatible)
        """
        ajout_success = False
        if domino != None and isinstance(domino, Domino):
            # Traitement du cas du premier domino
            if len(self._plateau) == 0 :
                self._plateau = [domino] 
                ajout_success = True
            else :
                # Traitement des autres domino
                if position in "droite":
                    # Vérifier que la valeur de gauche du domino = la valeur de droite du dernier domino du plateau
                    domino_plateau = self.domino_a_droite()
                    if domino.valeur_a_gauche == domino_plateau or domino.valeur_a_gauche == 0 or domino_plateau==0:
                        self._plateau.append(domino)
                        ajout_success = True
                elif position in "gauche":
                    domino_plateau = self.domino_a_gauche()
                    if domino.valeur_a_droite == domino_plateau or domino.valeur_a_droite == 0 or domino_plateau==0:
                        self._plateau.insert(0, domino)
                        ajout_success = True
                else:
                    raise Exception("Position non gérée pour l'instant", position)
        else:
            raise Exception("Domino attendu et non", domino)
        
        if ajout_success:
            # on retire le domino du joueur
            joueur.retirer_domino(domino)
        return ajout_success

    def _ia_2(self, joueur, dominos):
        """Détermine le domino qui a une valeur déjà utilisée plusieurs fois,
        qui a donc le plus de chance de bloquer le jeu et qui a le plus de points

        Args:
            joueur (Joueur): [description]
            dominos (List(Domino)): Liste des Dominos

        Returns:
            Domino: Le domino à jouer ou None
        """
        # dans la liste des dominos compatibles
                # Compter le nombre de domino d'un valeur
        domi = None
        _, valeurs = self._ia_nb_occur_domino(joueur, dominos)
        
        # ensuite nous prenons les dominos qui ont le plus grand nombre
        max_occu = max(list(valeurs.keys()))
        # On sélectionne le domino qui a le plus de point dans la liste des dominos qui est le plus présent
        dominos = valeurs.get(max_occu)
        if dominos is not None:
            for dom in dominos:
                if domi == None:
                    domi = dom
                else:
                    if dom > domi:
                        domi = dom
        return domi  

    def _ia_3(self, joueur, dominos):
        """Détermine le domino qui a une valeur déjà utilisée plusieurs fois et qui n'est pas le côté à placer,
        qui a donc le plus de chance de bloquer le jeu et qui a le plus de points

        Args:
            joueur (Joueur): [description]
            dominos (List(Domino)): Liste des Dominos

        Returns:
            Domino: Le domino à jouer ou None
        """
        # dans la liste des dominos compatibles
                # Compter le nombre de domino d'un valeur
        domi = None
        nb_val_occur_by_val, valeurs = self._ia_nb_occur_domino(joueur, dominos)
        
        keys = sorted(list(valeurs.keys()), reverse=True)

        # on parcours la liste des dominos de ceux qui ont le plus d'occurrence au moins d'occurrence
        for cle in keys:
            list_dom = valeurs.get(cle, [])
            for do in list_dom:
                # on regarde si la face qui a ce nombre d'occurrence est la face à placer
                nb = nb_val_occur_by_val.get(do.valeur_a_gauche)
                # le domino a le nombre d'occurrences attendu
                if nb == cle:
                    # on vérifie qu'il ne s'agit pas de la face à "coller"
                    if do.valeur_a_gauche != self.domino_a_droite and do.valeur_a_gauche != self.domino_a_gauche:
                        domi = do
                if domi is None:
                    # on regarde si la face qui a ce nombre d'occurrence est la face à placer
                    nb = nb_val_occur_by_val.get(do.valeur_a_droite)
                    # le domino a le nombre d'occurrences attendu
                    if nb == cle:
                        # on vérifie qu'il ne s'agit pas de la face à "coller"
                        if do.valeur_a_droite != self.domino_a_droite and do.valeur_a_droite != self.domino_a_gauche:
                            domi = do
                # sinon on passe au domino suivant
        # si aucun résultat à ce niveau d'IA, on passe au niveau précédent
        if domi is None:
            domi = self._ia_2(joueur, dominos)
        return domi
    
    def _ia_nb_occur_domino(self, joueur, dominos):
        """Compte le nombre d'occurrences des dominos de la liste

        Args:
            joueur (Joueur): [description]
            dominos (List(Domino)): Liste des Dominos

        Returns:
            (Dict(int, int), Dict(int, List)): (Dict(valeur du domino, nombre d'occurrence), Dict(nombre d'occurences, List des dominos))
        """
        valeurs = {}
        nb_val_occur_by_val = {}
        for dom in dominos:
            val_droite = dom.valeur_a_droite
            val_gauche = dom.valeur_a_gauche
            # pour ne faire qu'une fois le traitement par valeur
            if nb_val_occur_by_val.get(val_droite, None) is None:
                nb = joueur.nb_domino_avec_la_valeur(val_droite) + self.nb_domino_avec_la_valeur(val_droite)
                ma_liste = valeurs.get(nb, [])
                nb_val_occur_by_val[val_droite] = nb
                ma_liste.append(dom)
                valeurs[nb] = ma_liste
            if nb_val_occur_by_val.get(val_gauche, None) is None:
                nb = joueur.nb_domino_avec_la_valeur(val_gauche) + self.nb_domino_avec_la_valeur(val_gauche)
                ma_liste = valeurs.get(val_gauche, [])
                nb_val_occur_by_val[val_gauche] = nb
                ma_liste.append(dom)
                valeurs[nb] = ma_liste
        return nb_val_occur_by_val, valeurs
            
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                                              TESTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_jeux_complet():
    print("----------------------------------------------")
    print("Partie > jeux_complet")
    print("----------------------------------------------")
    jeux = Partie.jeux_complet()
    print(jeux)
       
   
def test_ajouter_joueur(): 
    print("----------------------------------------------")
    print("Partie > ajouter_joueur")
    print("----------------------------------------------")
    partie1 = Partie()
    partie1.ajouter_joueur("JoueurUn")
    assert partie1.joueurs[0].name ==  "JoueurUn"
    print( "test d'ajout d'un joueur 'JoueurUn' sous forme str : OK")
    print("----------------------------------------------")
    partie1.ajouter_joueur(Joueur("JoueurDeux"))
    assert partie1.joueurs[1].name ==  "JoueurDeux"
    print( "test d'ajout d'un joueur sous forme objet 'JoueuDeux' : OK")
    print(partie1.joueurs)
    print("----------------------------------------------")
    print( "test de la limite maximun de joueurs par partie")
    partie1.ajouter_joueur("JoueurTrois")
    partie1.ajouter_joueur("JoueurQuatre")
    partie1.ajouter_joueur("JoueurCinq")
    partie1.ajouter_joueur("JoueurSix")
    assert len(partie1.joueurs) <= 6
    print("ajout de 4 joueurs ! Taille de la liste de joueurs : ",len(partie1.joueurs))
    print("----------------------------------------------")
    print("ajout d'un 7ème joueurs")
    try:
        partie1.ajouter_joueur("JoueurSept")
        raise AssertionError("Impossible de rajouter un autre joueur à la partie !")
    except:
        print( "test de la limite maximun de 6 joueurs par partie : OK")
        assert True
    print("-------------- TEST REUSSI -------------------")

def test_distribution_dominos():
    print("----------------------------------------------")
    print("Partie > distribue_dominos")
    print("----------------------------------------------")
    print("Test de la répartition lors d'une partie de deux joueurs - résultat attendu : 7")
    partie1 = Partie()
    j1=partie1.ajouter_joueur("JoueurUn")
    j2=partie1.ajouter_joueur("JoueurDeux")
    partie1.distribue_dominos()
    print("j1 :", len(j1.dominos_en_main),",", "j2 :", len(j2.dominos_en_main))
    assert len(j1.dominos_en_main) == 7 & len(j2.dominos_en_main) == 7
    print("----------------------------------------------")
    print("Test de la répartition lors d'une partie de trois joueurs - résultat attendu : 6")
    j3=partie1.ajouter_joueur("JoueurTrois")
    partie1.distribue_dominos()
    print("j1 :", len(j1.dominos_en_main),",", "j2 :", len(j2.dominos_en_main),",", "j3 :", len(j3.dominos_en_main))
    assert len(j1.dominos_en_main) == 6 & len(j2.dominos_en_main) == 6 & len(j3.dominos_en_main) == 6
    print("----------------------------------------------")
    print("Test de la répartition lors d'une partie de quatre joueurs - résultat attendu : 6")
    j4=partie1.ajouter_joueur("JoueurQuatre")
    partie1.distribue_dominos()
    print("j1 :", len(j1.dominos_en_main), "," , "j2 :", len(j2.dominos_en_main), ",",  "j3 :", len(j3.dominos_en_main), "j4 :", len(j4.dominos_en_main))
    assert len(j1.dominos_en_main) == 6 & len(j2.dominos_en_main) == 6 & len(j3.dominos_en_main) == 6 & len(j4.dominos_en_main) == 6
    print("----------------------------------------------")
    print("Test de la répartition lors d'une partie de cinq joueurs - résultat attendu : 4")
    j5=partie1.ajouter_joueur("JoueurCinq")
    partie1.distribue_dominos()
    print("j1 :", len(j1.dominos_en_main), "," , "j2 :", len(j2.dominos_en_main), ",",  "j3 :", len(j3.dominos_en_main), ",",  "j4 :", len(j4.dominos_en_main), "j5 :", len(j5.dominos_en_main))
    assert len(j1.dominos_en_main) == 4 & len(j2.dominos_en_main) == 4 & len(j3.dominos_en_main) == 4 & len(j4.dominos_en_main) == 4 & len(j5.dominos_en_main) == 4
    print("----------------------------------------------")
    print("Test de la répartition lors d'une partie de six joueurs - résultat attendu : 4")
    j6=partie1.ajouter_joueur("JoueurSix")
    partie1.distribue_dominos()
    print("j1 :", len(j1.dominos_en_main), "," , "j2 :", len(j2.dominos_en_main), ",",  "j3 :", len(j3.dominos_en_main), ",",  "j4 :", len(j4.dominos_en_main), "j5 :", len(j5.dominos_en_main), ",","j6 :", len(j6.dominos_en_main))
    assert len(j1.dominos_en_main) == 4 & len(j2.dominos_en_main) == 4 & len(j3.dominos_en_main) == 4 & len(j4.dominos_en_main) == 4 & len(j5.dominos_en_main) == 4 & len(j6.dominos_en_main) == 4
    print("-------------- TEST REUSSI -------------------")

def test_premier_joueur():
    print("----------------------------------------------")
    print("Partie > premier_joueur")
    print("----------------------------------------------")
    partie1 = Partie()
    res= partie1.premier_joueur()
    assert res ==  (None, None)
    print( "test sans joueur : ",partie1.premier_joueur())
    print("----------------------------------------------")
    partie1.ajouter_joueur("JoueurUn")
    assert partie1.premier_joueur()[0] ==  partie1.joueurs[0]
    print( "test avec un joueur : ",partie1.premier_joueur())
    print("----------------------------------------------")
    partie1.ajouter_joueur('JoueurDeux')
    j1 = partie1.joueurs[0]
    j2 = partie1.joueurs[1]
    j1.ajouter_domino(Domino(2, 6))
    j1.ajouter_domino(Domino(3, 2))
    j2.ajouter_domino(Domino(6 ,4))
    j2.ajouter_domino(Domino(1 ,5))
    print("mains des joueurs :")
    partie1.affiche_joueurs_mains()
    print("----------------------------------------------")
    assert partie1.premier_joueur()[0] == j2
    print( "test avec deux joueurs (sans double): ",partie1.premier_joueur())
    print("----------------------------------------------")
    print("Ajout de double dans les mains de chaque joueurs")
    j1.ajouter_domino(Domino(6, 6))
    j2.ajouter_domino(Domino(3 ,3))
    partie1.affiche_joueurs_mains()
    assert partie1.premier_joueur()[0] == j1
    print("----------------------------------------------")
    print( "test avec deux joueurs (avec double): ",partie1.premier_joueur())
    print("-------------- TEST REUSSI -------------------")


def test_ia_nb_occur_domino():
    partie = Partie("my partie", 3)
    # ajouter des dominos sur le plateau
    j1 = Joueur("My Joueur")
    j1.ajouter_domino(Domino(1, 6))
    j1.ajouter_domino(Domino(5 ,3))
    j1.ajouter_domino(Domino(5 ,4))
    j1.ajouter_domino(Domino(2 ,4))
    j1.ajouter_domino(Domino(3 ,4))
    partie._plateau.append(Domino(4, 6))
    partie._plateau.append(Domino(6, 6))
    partie._plateau.append(Domino(6, 5))
    partie.affiche_plateau()
    dominos = j1.dominos_compatibles(partie.domino_a_gauche(), partie.domino_a_droite())
    nb_val_occur_by_val, valeurs = partie._ia_nb_occur_domino(j1, dominos)
    # contrôle du résultat attendu
    expected_keys = [3, 5, 4, 2]
    expected_dic = {3: 2, 5: 3, 4: 4, 2: 1}
    for key, val in nb_val_occur_by_val.items():
        assert key in expected_keys
        assert expected_dic[key] == val

    # contrôle du résultat attendu
    expected_dic = {2: [Domino(5 ,3), Domino(2 ,4)], 3: [Domino(5 ,3)], 4: [Domino(5 ,4)], 1: [Domino(5 ,3), Domino(2 ,4)]}
    expected_keys = [2, 3, 4, 1]
    for key, val in nb_val_occur_by_val.items():
        assert key in expected_keys
        assert expected_dic[key] == val



if __name__ == "__main__":
    test_jeux_complet()
    test_ajouter_joueur()
    test_premier_joueur()
    test_distribution_dominos()
    test_ia_nb_occur_domino()

