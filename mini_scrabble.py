
import random
print ("               BIENVENUE AU MINI SCRABBLE !","😁")


START_LIST = ["nuit", "jour", "lune", "haut",
              "petit","photoshop","python","mordre",
              "aimer","gentil","partir","revenir",
              "dormir","manger","table","fleurs","robe" ]  # Liste contenant les mots à choisir


N_SELECTED_WORDS = 3  # Nombre de solutions possibles pour chaque tour
N_ROUNDS = 3 # Nombre de tours à jouer

START_LIST = [word.upper() for word in START_LIST]  # Transformer tous les mots en majuscules
print(f"Le nombre de tours est {N_ROUNDS}")


def select_answers(start_words: list, n_selection: int = N_SELECTED_WORDS) -> list:
    """
    Given a list of accepted words, sample them to a limited amount and return the selection.

    :param start_words:Liste des premiers mots.
    :param n_selection: Nombre de mots à sélectionner
    :return: liste de réponses sélectionnées.
    """
    return random.sample(start_words, n_selection)


def answers_to_characters(selected_answers: list) -> list:
    """
    Given the list of selected answers, produces the list of allowed characters for a solution.
    :param selected_answers: Liste des réponses sélectionnées.
    :return: Liste des caractères acceptés.
    """
    unique_characters = []
    for word in selected_answers:
        for char in word:
            if char not in unique_characters:
                unique_characters.append(char) 
    random.shuffle(unique_characters)
    return unique_characters


def play_scrabble(n_rounds: int) -> int:
    """
    Lancez une nouvelle partie de scrabble.

    :param n_rounds: Nombre de tours à jouer.
    :return: Le nombre de points marqués par le joueur.
    """
    points = 0  # Compteur de points marqués par l'utilisateur

    for rnd in range(n_rounds):  # Pour chaque tour
        print("="*10, f"Tour {rnd}", "="*10)   # le f avant d'ouvrir nos guillemets pour utiliser des expressions formatées like {rnd}
        answers = select_answers(START_LIST)  # Sélectionnez 3 réponses dans la liste de départ
        characters = answers_to_characters(answers)  # Convertir les réponses de ce tour en une liste de caractères
        found_answers = []
        print(f"Tes caracteres: {characters}")
        ans = None
        while ans is None:  # Continuer à demander au joueur de nouvelles réponses
            ans = input("S'il vous plaît, insérez une réponse: ").upper().strip()  # Convertir la réponse saisie en majuscule et supprimer les espaces
            if ans == "QUIT":  # Aller au prochain tour
                break
            elif ans in answers:  # La réponse est valide
                if ans in found_answers:  #Déjà trouvé
                    print(f"Vous avez déjà trouvé la réponse'{ans}!")
                    ans = None
                else:  # Bonne réponse
                    points += 1
                    found_answers.append(ans)
                    print("Tres bien,felicitation !")
                    if len(found_answers) == len(answers):  # Toutes les réponses ont été trouvées (passer au tour suivant)
                        print(" Vous avez trouvé avec succès toutes les réponses possibles ! Passons au tour suivant.")
                    else:   # Demandez une nouvelle réponse
                        ans = None
            else:  # Mauvaise reponse 
                ans = None
                print(f"Non! {ans} est une mauvaise reponse ")
    return points


print(f"Votre score est de {play_scrabble(N_ROUNDS)} points.")

print    ("             Au revoir 🙂            ")
'''
@author : Farid BENAMARA 
'''
