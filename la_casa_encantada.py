"""
  Este es un reto especial por Halloween.
  Te encuentras explorando una mansión abandonada llena de habitaciones.
  En cada habitación tendrás que resolver un acertijo para poder avanzar a la siguiente.
  Tu misión es encontrar la habitación de los dulces.
  Se trata de implementar un juego interactivo de preguntas y respuestas por terminal.
  (Tienes total libertad para ser creativo con los textos)
  - 🏰 Casa: La mansión se corresponde con una estructura cuadrada 4 x 4
    que deberás modelar. Las habitaciones de puerta y dulces no tienen enigma.
    (16 habitaciones, siendo una de entrada y otra donde están los dulces)
    Esta podría ser una representación:
    🚪⬜️⬜️⬜️
    ⬜️👻⬜️⬜️
    ⬜️⬜️⬜️👻
    ⬜️⬜️🍭⬜️
  - ❓ Enigmas: Cada habitación propone un enigma aleatorio que deberás responder con texto.
    Si no lo aciertas no podrás desplazarte.
  - 🧭 Movimiento: Si resuelves el enigma se te preguntará a donde quieres desplazarte.
    (Ejemplo: norte/sur/este/oeste. Sólo deben proporcionarse las opciones posibles)
  - 🍭 Salida: Sales de la casa si encuentras la habitación de los dulces.
  - 👻 (Bonus) Fantasmas: Existe un 10% de que en una habitación aparezca un fantasma y
    tengas que responder dos preguntas para salir de ella.
"""
import json
from typing import List, Dict

from random import random, choice, randint
# from deep_translator import GoogleTranslator
# import requests


SIZE = 4
NUM_QUESTION = 10
DOOR = '|'
SWEET = '$'
GHOST = '@'
ROOM = '-'
PLAYER = '#'
GHOST_PROBABILITY = 0.1
# API_KEY = 'aV9MO2XyNGJgzSoAW/Jd9A==xId1jWd0LUUT4293'
# CATEGORY = ['artliterature', 'language', 'sciencenature', 'general',
#             'fooddrink', 'peopleplaces', 'geography', 'historyholidays',
#             'entertainment', 'toysgames', 'music', 'mathematics',
#             'religionmythology', 'sportsleisure']
# CATEGORY = ['general', 'music', 'sciencenature', 'geography', 'entertainment']
CATEGORY = ['arte', 'cultura', 'tecnologia', 'filosofia', 'musica', 'politica',
            'matematica', 'deporte', 'inventos', 'biologia', 'ciencia', 'cine',
            'geografia', 'historia', 'economia', 'entretenimiento', 'religion',
            'gastronomia', 'industria', 'astronomia', 'transporte', 'medicina',
            'genetica', 'guerra', 'clima']


def start_game() -> None:
    """
    Explain to init the game.
    Returns:
        None:
    """
    print('MANSION EMBRUJADA')
    print('Tu misión es encontrar la habitación de los dulces.')
    print('La mansion es un cuadrado de 4x4 con 16 habitaciones')
    print('En cada habitacion hay un enigma, un Fantasma, \
          o la habitacion de dulces')
    print('Se comienza en la puerta del hotel, debes responder la trivia para \
          avanzar a la siguiente habitacion')
    print('El jugador se mueve por la Mansion con las siguientes coordenadas:')
    print('W -> Arriba')
    print('S -> Abajo')
    print('D -> Derecha')
    print('A -> Izquierda')


def match_option(option: int) -> str:
    """
    Switch different difficulties of the game.
    Returns:
        str: Difficult of game
    """
    match option:
        case 1:
            print("Has ingresado el número 1.")
            level = 'facil'
        case 2:
            print("Has ingresado el número 2.")
            level = 'medio'
        case 3:
            print("Has ingresado el número 3.")
            level = 'dificil'
        case 4:
            print("Has ingresado el número 4.")
            level = 'experto'
        case _:
            print("El número ingresado no está en el rango de 1 a 4.")
    return level


def select_level() -> str:
    """
    Select difficult of the game.
    Returns:
        str: Difficult of game
    """
    print('Seleccinar nivel:')
    print("Ingrese un número entre 1 y 4 dependiendo de la dificultad:")
    print('1 -> Facil')
    print('2 -> Medio')
    print('3 -> Dificil')
    print('4 -> Experto')
    try:
        option = int(input())
        return match_option(option)
    except ValueError as ve:
        print(f"Error: {ve}")


def create_sweet() -> (int, int):
    """
    Create coordinates (x and y) to random sweet in the mansion.
    Returns:
        int: Random row position of the object.
        int: Random column position of the object.
    """
    random_row = randint(0, SIZE - 1)
    random_col = randint(0, SIZE - 1)
    return random_row, random_col


def create_ghost(map_mansion: List[List[str]]) -> List[List[str]]:
    """
    Create ghost in the mansion with GHOST PROBABILITY.
    Returns:
        List[List[str]]: Mansion with ghost.
    """
    # create the ghost probability
    for i, row in enumerate(map_mansion):
        for j, cell in enumerate(row):
            if cell not in {DOOR, SWEET}:
                if random() <= GHOST_PROBABILITY:
                    map_mansion[i][j] = GHOST
    # for i in range(len(map_mansion)):
    #     for j in range(len(map_mansion[0])):
    #         if map_mansion[i][j] != DOOR and map_mansion[i][j] != SWEET:
    #             randon_num = random()
    #             if randon_num <= GHOST_PROBABILITY:
    #                 map_mansion[i][j] = GHOST
    return map_mansion


def create_mansion() -> List[List[str]]:
    """
    Create a mansion (and array 4x4) with doors and sweet.
    Returns:
        List: The mansion created.
    """
    sweet_i, sweet_j = 0, 0
    # Create random position of the sweet in the mansion
    while sweet_i == 0 and sweet_j == 0:
        sweet_i, sweet_j = create_sweet()
    map_mansion = [[DOOR if i == 0 and j == 0 else
                   SWEET if i == sweet_i and j == sweet_j else
                   ROOM for i in range(SIZE)] for j in range(SIZE)]
    
    # Create random position of ghost in the mansion
    mansion_with_ghost = create_ghost(map_mansion)
    return mansion_with_ghost


def coord_player(letter: str, i: int, j: int) -> (int, int):
    """
    Create the movility of player with keyboard in the mansion.
    Returns:
        int: coord_y in the mansion.
        int: coord_x in the mansion.
    """
    letter = letter.lower()
    last_i, last_j = i, j
    if letter == 'w':
        i -= 1
    elif letter == 's':
        i += 1
    elif letter == 'd':
        j += 1
    elif letter == 'a':
        j -= 1
    return last_i, last_j, i, j


def ghost_trivia():
    pass


# def create_trivia(trivia) -> str:
#     """
#     Select a random category and send the trivia question and answer
#     in Spanish.
#     Returns:
#         str: The response of the API trivia Question.
#     """
#     # random_category = get_random_category()
#     # trivia = get_trivia_question(random_category, API_KEY)
#     dict_trivia = from_list_to_dict(trivia)
#     question = dict_trivia['question']
#     answer = dict_trivia['answer']
#     spanish_question = translate_text(question)
#     spanish_answer = translate_text(answer)
#     return spanish_question, spanish_answer

def get_trivia_question(random_category: str, level_trivia: str) -> List[Dict]:
    """
    Select a random category and send the trivia question and answer
    in Spanish.
    Returns:
        str: The response of the API trivia Question.
    """
    route = 'preguntas_' + random_category + '.json'
    with open(route, 'r', encoding="utf-8") as file:
        # Código para procesar el archivo JSON
        file_json = json.load(file)
    # Ahora puedes trabajar con datos_json como un diccionario o una lista
    trivias = file_json[random_category][level_trivia]
    return choice(trivias)


def create_trivia(level_trivia: str) -> (str, List[str], str):
    """
    Select a random category and send the trivia question and answer
    in Spanish.
    Returns:
        str: The response of the API trivia Question.
    """
    random_category = get_random_category()
    trivia = get_trivia_question(random_category, level_trivia)
    print(f"SSelecccttttttt --->>> {random_category}")
    question = trivia['pregunta']
    options = trivia['opciones']
    correct_answer = trivia['respuesta_correcta']
    return question, options, correct_answer


def match_user_answer(answer, option) -> str:
    """
    Switch different answer of the trivia.
    Returns:
        str: response by user
    """
    match answer:
        case 'a':
            response = option[0]
        case 'b':
            response = option[1]
        case 'c':
            response = option[2]
        case 'd':
            response = option[3]
    return response


def solution(question: str, options: List[str], correct_answer, points: int):
    """
    Show the trivia options (a, b, c, d) and receipt the answer by user.
    Returns:
        str: Answer given by user ('a', 'b', 'c' or 'd').
        int: Punctuation in this question.
    """
    print(f"a. {options[0]}")
    print(f"b. {options[1]}")
    print(f"c. {options[2]}")
    print(f"d. {options[3]}")
    user_answer = str(input())
    user_answer = user_answer.lower()
    if user_answer == 'a' or user_answer == 'b' or user_answer == 'c' or user_answer == 'd':
        response_user = match_user_answer(user_answer, options)
        points, is_correct = assignment_points(correct_answer, response_user, points)
    else:
        print("Opcion Incorrecta (solo se puede 'a', 'b', 'c' o 'd').")
        print("Ingrese nuevamente la opcion")
        points, is_correct = solution(question, options, correct_answer, points)
    return points, is_correct


def assignment_points(correct_answer: str,
                      answer_user: str,
                      points: int) -> int:
    """
    Compare correct answer with user answer and assign points to user.
    Returns:
        str: Text translated
    """
    is_correct = False
    if answer_user == str(correct_answer):
        points += 10
        is_correct = True
        print('Respuesta correcta')
    else:
        points -= 5
        print('Respuesta INCORRECTA')
    return points, is_correct


def print_solution(answer: str, points: int) -> None:
    """
    Print question, correct answer, user answer and punctuation .
    Returns:
        None
    """
    print(f"Respuesta correcta: {answer}")
    print(f"Puntos: {points}")


def change_position(map_mansion: List[List[str]],
                    level: str) -> None:
    """
    Change the position of the player inside the mansion.
    Returns:
        None
    """
    first_step = True
    row, col = 0, 0
    last_row, last_col = -1, -1
    last_estate, new_estate = DOOR, DOOR
    points = 0
    is_answer = True
    while map_mansion[row][col] != SWEET:
        press_button = str(input())
        last_row, last_col, row, col = coord_player(press_button, row, col)
        if 0 <= row < SIZE and 0 <= col < SIZE:
            if first_step:
                last_estate = DOOR
                new_estate = map_mansion[row][col]
                first_step = False
            elif is_answer:
                new_estate = map_mansion[row][col]
            map_mansion[row][col] = PLAYER
            map_mansion[last_row][last_col] = last_estate
            [print(*fila) for fila in map_mansion]
            last_estate = new_estate
            if new_estate == GHOST:
                for i in range(2):
                    print(f"ingreso {i} vecessssss")
                    question, options, correct_answer = create_trivia(level)
                    print(question)
                    points, is_answer = solution(question, options,
                                                 correct_answer, points)
                    print_solution(correct_answer, points)
            elif new_estate == ROOM:
                question, options, correct_answer = create_trivia(level)
                print(question)
                points, is_answer = solution(question, options,
                                             correct_answer, points)
                print_solution(correct_answer, points)
            elif new_estate == SWEET:
                print("GANASTEEEEEEEEEE")
                break
            else:
                print("ERRORRRRRRRRRRRRRR")
            [print(*fila) for fila in mansion]
        else:
            row = last_row
            col = last_col


def get_random_category() -> str:
    """
    Get a random category from the CATEGORY list.
    Returns:
        str: A random category.
    """
    return choice(CATEGORY)


if __name__ == "__main__":
    start_game()
    level = select_level()
    mansion = create_mansion()
    [print(*fila) for fila in mansion]
    print('Ingrese movimiento: ')
    change_position(mansion, level)


# def translate_text(text_english: str) -> str:
#     """
#     Translate text from English to Spanish .
#     Returns:
#         str: Text translated
#     """
#     # Realizar la traducción a español
#     text_spanish = GoogleTranslator(source='en', target='es'
#                                     ).translate(text_english)
#     return text_spanish

# def from_list_to_dict(data_list: List) -> Dict:
#     """
#     Transform a list in a Dict .
#     Returns:
#         Dict(): A dictionary with data list
#     """
#     data_dict = {}
#     for item in data_list:
#         data_dict.update(item)
#     return data_dict


# def get_trivia_question(category: str, api_key: str) -> str:
#     """
#     Get a trivia question from a specific category using an API.

#     Args:
#         category (str): The desired trivia category.
#         api_key (str): The API key required for the request.

#     Returns:
#         str: The trivia question or an error message in case of issues.
#     """
#     api_url = f'https://api.api-ninjas.com/v1/trivia?category={category}'
#     headers = {'X-Api-Key': api_key}

#     try:
#         response = requests.get(api_url, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#         return data
#         # return response.text

#     except requests.exceptions.RequestException as e:
#         return f"Error: {e}"

#     except Exception as e:
#         return f"Error inesperado: {e}"


# def create_database_trivia():
#     database_trivia = []
#     for _ in range(NUM_QUESTION):
#         new_category = get_random_category()
#         data = get_trivia_question(new_category, API_KEY)
#         database_trivia.append(data)
#     return database_trivia
