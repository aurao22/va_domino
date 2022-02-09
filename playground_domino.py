from controler_domino import *
from beans_domino import *

# Gérer la création des joueurs
# Affichage plateau avant jeu
# Gérer les toursV

def tour_joueur(partie, joueur):
     # On vérifie si le joueur peut piocher ou non
    pioche = not partie.peut_piocher(joueur)
    continuer_a_jouer = True
    continuer_tour = True
    nb_erreurs = 3
    
    # Boucle des tours pour 1 joueur (erreur de saisie et pioche)
    while continuer_tour:
        error = False
        # On affiche le plateau
        partie.affiche_plateau()
        # on affiche les dominos du joueur courant
        joueur.affiche_main_et_positions()
        pioche_str = "OU pioche "
        if pioche:
            pioche_str = ""
        jeu = input(f"{joueur.name} quel domino voulez-vous déposer ? position OU auto {pioche_str}OU pass OU exit:")
        if jeu is None or len(jeu) == 0:
            error = True
        else:
            jeu = jeu.lower()
            if jeu == "exit":
                continuer_tour = False
                continuer_a_jouer = False
                break
            elif "auto" in jeu:
                return partie.tour_auto(joueur)
            elif "pioche" in jeu and pioche:
                print("Vous avez en main un domino compatible ou vous avez déjà pioché.")
                error = True
            elif "pass" in jeu:
                continuer_tour = False
                break
            elif "pioche" in jeu and not pioche:
                try:
                    # on pioche automatiquement
                    domino = partie.pioche(joueur)
                    pioche = True
                except Pioche_Interdite_Domino_Compatibles as err:
                    print(f"{err.message}")
                    error = True
            else:
                try:
                    pos = int(jeu)
                    if pos < len(joueur.dominos_en_main):
                        domino = joueur.dominos_en_main[pos]
                        # il faut vérifier que le domino est compatible
                        cote = input(f"{joueur.name} de quel côté voulez-vous déposer votre domino (g ou d ou ig ou id) :")
                        try:
                            partie.jouer_domino(joueur, domino, cote)
                            # Si le joueur n'a plus de domino, il a gagné
                            return len(joueur.dominos_en_main) > 0
                        except Jouer_Domino_Exception as erreur :
                            print(erreur.message)
                            error = True
                    else:
                        error = True
                except:
                    error = True
        if error : 
            nb_erreurs -= 1
            print(f"Merci de saisir une position entre 0 et {len(joueur.dominos_en_main)}, il vous reste {nb_erreurs} essais")
            if nb_erreurs == 0:
                print(f"Vous avez épuisé vos 3 essais, passez votre tour.")
                return len(joueur.dominos_en_main) > 0
    return continuer_a_jouer


def play():

    reponse = " "
    i = 0
    while reponse not in "exit":
        i += 1
        print("##########################################################################")
        print("#                 Bienvenue dans le jeu de dominos                       #")
        print("##########################################################################")
        print("Nouvelle partie !                               'exit' pour sortir du jeu")
        niveau_ia = input("Niveau d'IA souhaité (0, 1, 2, 3):")
        if "0" in niveau_ia or "1" in niveau_ia or "2" in niveau_ia or "3" in niveau_ia:
            niveau_ia = int(niveau_ia)
        else:
            niveau_ia = 0
        partie = Partie("Partie "+str(i), niveau_ia=niveau_ia)
        # Ajout des joueurs
        joueur_name = "Player"
        while joueur_name not in "stop" and joueur_name not in "exit":
            joueur_name = input("Nom du joueur (ou exit ou stop):")
            if joueur_name not in "stop" and joueur_name not in "exit":
                try:
                    partie.ajouter_joueur(joueur_name)
                except Nombre_Joueurs_Exception as err:
                    print(f"{err.message}")
                    joueur_name = "stop"
            else:
                break
        
        if joueur_name in "exit":
            reponse = "exit"
            break
        elif len(partie.joueurs) == 1:
            partie.ajouter_ordinateur()
        
        if len(partie.joueurs)>1:
            # Initilialisation de la partie
            print(partie.partie_name, ": distribution des dominos")
            partie.distribue_dominos()
            print(partie.partie_name, ": le premier joueur est ", end="")
            # Il faut poser le premier domino
            # il faut récupérer l'indice du premier joueur pour initier les tours
            joueur, premier_domino = partie.premier_joueur()
            print(joueur.name)
            # on affiche les dominos du 1er joueur
            print(joueur)
            if partie.deposer_premier_domino(joueur, premier_domino):
                # La partie est initialisée
                continuer_a_jouer = True
                # Boucle des tours joueurs
                while continuer_a_jouer:
                    # Boucle des tours pour 1 joueur (erreur de saisie et pioche)
                    joueur = partie.joueur_suivant()
                    if "ordinateur" in joueur.type:
                        continuer_a_jouer = partie.tour_auto(joueur)
                    else:
                        continuer_a_jouer = tour_joueur(partie, joueur)
                
                print(f"---------------------- {partie.partie_name} IS OVER ----------------------")
                partie.affiche_classement()
                print("--------------------------------------------------------------------------")
                reponse = input("Souhaitez-vous jouer une nouvelle partie ?(o/n):")
                if "n" in reponse.lower():
                    reponse = "exit"
            else:
                print("Erreur lors de l'ajout du premier Domino, reinitialisation de la partie")
        else:
            reponse = input("Vous n'avez saisis aucun joueur, souhaitez-vous quitter le jeux ? o/n\n")
            if "o" in reponse:
                reponse = "exit"
                break
    

play()
# Si un joueur n’a pas de domino qu’il puisse poser, 
# il pioche un domino (sans le montrer aux autres joueurs). 
# S’il peut le poser, il le fait immédiatement, sinon il l’ajoute à ces dominos. 
# Si la pioche est épuisée, le joueur passe son tour.

# TODO :
# - Traiter le cas du jeux bloqué => aucun joueur ne peut poser de domino et pioche vide