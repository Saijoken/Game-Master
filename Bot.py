from random import *

#  Variables globales
table: list = []
player1: str
player2: str
player1_life: int = 20
player2_life: int = 20
nb_turn: int = 1
choice_player: int = randint(0, 1)


def intro():
    global player1, player2

    print(
        "Bienvenue dans l'arène du combattant !\nPour survivre tu devras te battre de toutes tes forces !\n ")
    print("Vous possédez chacun 20 PV ; celui qui voit sa barre de vie passer au seuil de 0 a perdu la partie.\n ")
    print("Bon courage !")
    print()
    """nb_players = int(input("Entrez le nombre de joueurs : "))
    nb_players = 2"""

    player1 = input("Joueur 1 - entrez votre pseudo : ").upper()
    player2 = input("Joueur 2 - entrez votre pseudo : ").upper()
    table.append(player1)
    table.append(player2)
    print(table)

    print()
    print("Maintenant que tous les joueurs sont inscrits, le jeu peut démarrer !\n")
    print(player1 + " et " + player2 + " s'affronteront.")


def turn():
    global player1_life
    global player2_life
    global nb_turn
    global choice_player

    print("-----------------------------------------------")
    print("- TOUR " + str(nb_turn) + " -")
    print("-----------------------------------------------")
    print("C'est au tour de " + table[choice_player] + " d'attaquer.")
    nb_turn += 1

    attacks = ["CHIDORI", "RASENGAN", "BOULE DE FEU"]
    print()

    while player1_life > 0 and player2_life > 0:
        print("Vous avez le choix entre trois attaques différentes: \n1) " + attacks[0] + "\n2) " + attacks[1] + "\n3) " +
              attacks[2] + "\n ")
        attack: str = input("Quel numéro choisissez-vous ? ")

        while attack != "1" and attack != "2" and attack != "3":
            print("Choisissez une valeur valide !")
            attack = input("Quel numéro choisissez-vous ? \n")

        if attack == "1":
            print(table[choice_player] + " lance " + attacks[0] + ".\n")
            damage = randint(-20, 30)

            if damage <= 0:
                print("Votre attaque a échoué !")

            else:
                if choice_player == 0:
                    player = player2
                    player2_life -= damage
                else:
                    player = player1
                    player1_life -= damage

                print("Vous avez infligé " + str(damage) + " points de dégâts à " + player + ".\n")

        elif attack == "2":
            print(table[choice_player] + " lance " + attacks[1] + ".\n")
            damage = randint(-10, 10)

            if damage <= 0:
                print("Votre attaque a échoué !")

            else:
                if choice_player == 0:
                    player = player2
                    player2_life -= damage
                else:
                    player = player1
                    player1_life -= damage

                print("Vous avez infligé " + str(damage) + " points de dégâts à " + player + ".\n")

        elif attack == "3":
            print(table[choice_player] + " lance " + attacks[2] + ".\n")
            damage = randint(1, 5)

            if damage <= 0:
                print("Votre attaque a échoué !")

            else:
                if choice_player == 0:
                    player = player2
                    player2_life -= damage
                else:
                    player = player1
                    player1_life -= damage

                print("Vous avez infligé " + str(damage) + " points de dégâts à " + player + ".\n")

        if choice_player == 1:
            choice_player -= 1
        else:
            choice_player += 1

        print(player1_life)
        print(player2_life)

    if player1_life <= 0:
        print("Victoire écrasante de " + table[0] + " !")

    else:
        print("Victoire écrasante de " + table[1] + " !")


intro()
turn()
