
# Import's 
import random
import os
import atexit

# Variables globales

playerVariables = {
    "nom": "",
    "niveau": 1,
    "hp": 20,
    "maxhp": 20,
    "attaque": 2,
    "défense": 1,
    "xp": 0,
    "équipment": "couteau",
    "inventaire": ["Potion", "Attaque Boost", "Défense Boost"],
    "emplacement": [1, 0],
    "exploré": [(1, 0)]
}

# Emplacements sur la carte

forestMap = {
}
mapSize = 5
for i in range(mapSize):
    for j in range(mapSize):
        if i+j < 4:
            forestMap[(i, j)] = 0
        elif i+j < 6:
            forestMap[(i, j)] = 1
        else:
            forestMap[(i, j)] = 2

forestMap[(1, mapSize-1)] = 2

# Variables de dessin de texte

tileSymbolSize = 2
tileSize = 6
tiles = {
    "X": [" o",
          " ^",],
    "e": ["  ",
          "  ",],
    "~": ["¿?",
          "¿?",],
    "O": ["  ",
          "->",],
}


mapDescriptions = {
    0: "Vous êtes dans une partie bien éclairée de la forêt. Il y a des arbres et des buissons tout autour de vous.",
    1: "Vous vous trouvez dans une partie de la forêt avec beaucoup d'arbres.",
    2: "Vous vous enfoncez plus profondément dans la forêt. Les arbres se dressent haut et bloquent une grande partie de la lumière du soleil.",
}

enemies = {
    "Goblin": {
        "hp": 5,
        "attaque": 3,
        "défense": 0,
        "xp": 1,
    },
    "Orc": {
        "hp": 10,
        "attaque": 2,
        "défense": 0,
        "xp": 1,
    },
    "Troll": {
        "hp": 7,
        "attaque": 2,
        "défense": 2,
        "xp": 2,
    },
}



def showStats():
    """
    Affiche les statistiques du joueur.
    """
    print("""
Nom: {}
Niveau: {}
HP: {}
Attaque: {}
Défense: {}
XP: {}
Équipment: {}
Inventaire: {}
        """.format(playerVariables["nom"], playerVariables["niveau"], playerVariables["hp"], playerVariables["attaque"], playerVariables["défense"], playerVariables["xp"], playerVariables["équipment"], playerVariables["inventaire"]))
        # .format(playerVariables["name"], playerVariables["niveau"], playerVariables["hp"], playerVariables["attack"], playerVariables["defense"], playerVariables["xp"], playerVariables["equipment"], playerVariables["inventory"]))


def saveGame():
    """
    Enregistre le jeu
    """
    print("Enregistre le jeu...")
    with open("save.txt", "w") as file:
        file.write(str(playerVariables))
    print("Jeu enregistré.")


def loadGame():
    """
    Charge le jeu
    """
    if os.path.isfile("save.txt"):
        global playerVariables
        print("Chargement du jeu...")
        with open("save.txt", "r") as file:
            playerVariables = eval(file.read())
        print("Jeu chargé.")


# Lorsque l'exécution de python se termine, enregistrez le jeu
atexit.register(saveGame)


def createName():
    """Crée un nom pour le joueur.
    """

    print("Veuillez saisir un nom :")
    playerVariables["nom"] = input()


def mainMenu():
    """Affiche le menu principal.
    """
    if os.path.isfile("save.txt"):
        print("""
Menu principal
1. Jouer
2. Charger
3. Quitter
        """)
    else:
        print("""
Menu principal
1. Jouer
3. Quitter
        """)

    selection = input()
    print()
    print("-"*100)
    print()
    if selection == "1":
        createName()
        print()
        print("-"*100)
        print()
        startGame()
    elif selection == "2" and os.path.isfile("save.txt"):
        loadGame()
        print()
        print("-"*100)
        print()
        startGame()
    elif selection == "3":
        print("Au revoir.")
        quit()
    else:
        print("Veuillez entrer un nombre valide.")
        mainMenu()


def startGame():
    """
    Démarre le jeu."""
    print("Vous vous réveillez au milieu d'une forêt avec un sac contenant un seul objet : un couteau. Vous devrez gagner de l'XP et collecter de nouvelles armes pour devenir plus fort et battre le boss pour sortir de la forêt.")
    showStats()
    print("Ceci est une carte de votre environnement, 'o<' marque votre emplacement, '->' les endroits où vous pouvez aller, '¿?' les endroits que vous n'avez pas encore explorés, et les espaces vides sont ceux que vous avez déjà visité.")
    drawMap()
    while True:
        gameOver = selectMovement()
        print()
        print("-"*100)
        print()
        if gameOver:
            break
        else:
            drawMap()
    mainMenu()


def drawMap():
    """Imprime une carte de la forêt en ligne de commande
    """
    bmap = [["~" for _ in range(mapSize)] for _ in range(mapSize)]
    x, y = playerVariables["emplacement"]
    if x < mapSize-1:
        bmap[x+1][y] = "O"
    if x > 0:
        bmap[x-1][y] = "O"
    if y < mapSize-1:
        bmap[x][y+1] = "O"
    if y > 0:
        bmap[x][y-1] = "O"

    for i in range(mapSize):
        for j in range(mapSize):
            if (i, j) in playerVariables["exploré"]:
                bmap[i][j] = "e"
    bmap[x][y] = "X"
    if x == 1 and y == mapSize-1:
        print(" "*7+" "*(tileSymbolSize+7), end="")
        print("__")
        print(" "*7+" "*(tileSymbolSize+7), end="")
        print("°°")
    for i in range(mapSize):
        print()
        for k in range(tileSymbolSize):
            print("       ", end="")
            for j in range(mapSize):
                for l in range(tileSymbolSize):
                    print(tiles[bmap[j][mapSize-i-1]][k][l], end="")
                print("       ", end="")
            print()


def battle(enemyName, enemyLevel, enemyHP, enemyAttack, enemyDefense, enemyXP):
    """
    Fait combattre le joueur contre un ennemi.
    """
    print()
    print("-"*100)
    print()
    print("Vous avez rencontré un {} niveau {}.".format(enemyName, enemyLevel))
    attackBonus = 0
    defenseBonus = 0
    while True:
        print("""
Votre HP: {}/{}
{} Niveau {} HP: {}
        """.format(playerVariables["hp"], playerVariables["maxhp"],enemyName, enemyLevel, enemyHP))
        print("Quelle action voulez-vous effectuer? ((A)ttaque, (I)nventaire, (R)un")
        action = input().lower()
        if action == "a":
            print("Vous attaquez le {}.".format(enemyName))
            damage = 1 + playerVariables["attaque"] + attackBonus - enemyDefense
            if damage < 0:
                damage = 0
            # Ajouter une chance de manquer
            if random.randint(1, 100) <= 3:
                print("Tu as raté ton attaque !")
                damage = 0
            # Ajouter une chance de critiquer
            if random.randint(1, 100) <= 3:
                print("Vous avez fait un coup critique !")
                damage += 1
                damage *= 2
            enemyHP -= damage
            if enemyHP <= 0:
                print("Tu as tué le {}.".format(enemyName))
                playerVariables["xp"] += enemyXP
                print("Tu as gagné{} XP.".format(enemyXP))
                checkLevelUP()
                return False
            else:
                print("Vous avez infligé {} dégâts.".format(damage))
                damage = enemyAttack - playerVariables["défense"] - defenseBonus
                if damage < 0:
                    damage = 0
                playerVariables["hp"] -= damage
                if playerVariables["hp"] <= 0:
                    print("Tu es mort.")
                    return True
                else:
                    print("Le {} infligé {} dégâts.".format(enemyName, damage))
        elif action == "i":
            print("Vous avez {} articles.".format(len(playerVariables["inventaire"])))
            print("Quel élément souhaitez-vous utiliser ?")
            for i in range(len(playerVariables["inventaire"])):
                print("{}: {}".format(i, playerVariables["inventaire"][i]))
            print("(B)ack")
            item = input()
            if item.isdigit() and int(item) < len(playerVariables["inventaire"]):
                print("Vous avez utilisé {}.".format(playerVariables["inventaire"][int(item)]))
                if playerVariables["inventaire"][int(item)] == "Potion":
                    playerVariables["hp"] += 10
                    if playerVariables["hp"] > playerVariables["maxhp"]:
                        playerVariables["hp"] = playerVariables["maxhp"]
                elif playerVariables["inventaire"][int(item)] == "Attaque Boost":
                    attackBonus += 1
                elif playerVariables["inventaire"][int(item)] == "Défense Boost":
                    defenseBonus += 1
                playerVariables["inventaire"].pop(int(item))
                damage = enemyAttack - playerVariables["défense"] - defenseBonus
                if damage < 0:
                    damage = 0
                playerVariables["hp"] -= damage
                if playerVariables["hp"] <= 0:
                    print("Tu es mort.")
                    return True
                else:
                    print("Le {} infligé {} dégâts.".format(enemyName, damage))
            else:
                print("Selection invalide.")
        elif action == "r":
            print("Tu t'enfuies.")
            return True
        else:
            print("Selection invalide.")


def checkLevelUP():
    """
    Vérifie si le joueur est passé au niveau supérieur.
    """
    while playerVariables["xp"] >= (playerVariables["niveau"]+1)**2:
        playerVariables["niveau"] += 1
        playerVariables["maxhp"] += 3
        playerVariables["attaque"] += 1
        playerVariables["défense"] += 1
        playerVariables["hp"] = playerVariables["maxhp"]
        print("Vous êtes passé au niveau supérieur ! Vous êtes maintenant à niveau {}.".format(playerVariables["niveau"]))


def selectMovement():
    """
    Permet au joueur de choisir où il veut aller.
    """
    gameover = False
    moved = False
    print("Dans quelle direction voulez-vous vous déplacer ? ((N)ord, (S)ud, (E)st, (W)ouest)")
    direction = input().lower()
    if direction == "w":
        if playerVariables["emplacement"][0] > 0:
            playerVariables["emplacement"] = (playerVariables["emplacement"][0] - 1, playerVariables["emplacement"][1])
            moved = True
        else:
            print("Sens invalide.")
    elif direction == "e":
        if playerVariables["emplacement"][0] < mapSize-1:
            playerVariables["emplacement"] = (playerVariables["emplacement"][0] + 1, playerVariables["emplacement"][1])
            moved = True
        else:
            print("Sens invalide.")
    elif direction == "n":
        if playerVariables["emplacement"][1] < mapSize-1 or playerVariables["emplacement"][0] == 1:
            playerVariables["emplacement"] = (playerVariables["emplacement"][0], playerVariables["emplacement"][1] + 1)
            moved = True
        else:
            print("Sens invalide.")
    elif direction == "s":
        if playerVariables["emplacement"][1] > 0:
            playerVariables["emplacement"] = (playerVariables["emplacement"][0], playerVariables["emplacement"][1] - 1)
            moved = True
        else:
            print("Sens invalide.")
    else:
        print("Sens invalide.")
        selectMovement()
    if moved:
        if playerVariables["emplacement"][1] >= mapSize:
            gameOver = bossBattle()
            if not gameOver:
                print("Toutes nos félicitations! Vous avez terminé le jeu !")
            return True
        else:
            if tuple(playerVariables["emplacement"]) not in playerVariables["exploré"]:
                locationDescription = mapDescriptions[forestMap[tuple(playerVariables["emplacement"])]]
                print(locationDescription)

            # Chance de rencontrer un monstre
            if random.randint(1, 100) <= 50:
                enemyName = random.choice(list(enemies.keys()))
                enemyLevel = random.randint(1, playerVariables["niveau"])
                enemyHP = enemies[enemyName]["hp"] + 2*(enemyLevel-1)
                enemyAttack = enemies[enemyName]["attaque"] + (enemyLevel-1)
                enemyDefense = enemies[enemyName]["défense"] + (enemyLevel-1)
                enemyXP = enemies[enemyName]["xp"] + (enemyLevel-1)
                gameover = battle(enemyName, enemyLevel, enemyHP, enemyAttack, enemyDefense, enemyXP)

            if tuple(playerVariables["emplacement"]) not in playerVariables["exploré"]:
                # Chance de trouver un objet
                if random.randint(1, 100) <= 20:
                    item = random.choice(["Potion", "Attaque Boost", "Défense Boost"])
                    playerVariables["inventaire"].append(item)
                    print("Vous avez trouvé un {} et l'avez ajouté à votre inventaire.".format(item))

                playerVariables["exploré"].append(tuple(playerVariables["emplacement"]))
    return gameover


def bossBattle():
    """
    Permet au joueur de combattre le boss.
    """
    enemyName = "Dark Forest King"
    enemyLevel = int(playerVariables["niveau"]/2) + 5
    enemyHP = 20 + 3*(enemyLevel-1)
    enemyAttack = 1 + (enemyLevel-1)
    enemyDefense = 3
    enemyXP = 100 + 10*(enemyLevel-1)
    gameover = battle(enemyName, enemyLevel, enemyHP, enemyAttack, enemyDefense, enemyXP)
    return gameover

mainMenu()
'''
@author : Farid BENAMARA 
'''
