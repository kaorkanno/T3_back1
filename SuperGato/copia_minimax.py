import math
import random
from copy import deepcopy


def es_nodo_terminal(tablero):
    """
    Revisa si el juego ha terminado dado un tablero. Devuelve True o False
    Hay dos opciones que devuelven 'True':
    1) 'X' o 'O' ganó
    2) No hay más posiciones válidas para jugar.
    """
    return tablero.revisar_ganador() != 0 or tablero.jugadas_disponibles() == []


def fichaOponente(ficha):
    if ficha == "O":
        return "X"
    else:
        return "O"


def BestMove(posicion, tablero, ficha):
    puntos_mov = 0
    tablero.ejecutar_jugada(posicion, ficha)
    puntos_mov += 1 # daremos un punto solo por hacer movimiento
    subtablero = posicion[2:]
    if ficha == "X":
        jugador = 1
        otro = 2
    else:
        jugador = 2
        otro = 1
    tablero[subtablero].jugar(jugador, posicion[3], posicion[2])
    if tablero[subtablero].ganador == otro:
        puntos_mov -= 10  # quitamos puntaje si el otro gana
    elif tablero[subtablero].ganador == jugador:
        puntos_mov += 10  # daremos un punto si es que se gana
    elif tablero.revisar_ganador() != 0:
        puntos_mov += 100
    else:
        pass
    return posicion, puntos_mov
    # vamos a dar puntaje si es que la jugada nos permite ganar un subtablero
    # y aún más puntaje si la jugada nos permite ganar todo
    # solo 1 punto por una jugada que no nos permita ganar


def minimax(tablero, profundidad, alpha, beta, funcion_puntaje, maximizar, ficha):
    """
    Algotimo Minimax. Dado el estado actual del juego, alpha, beta,
    y la función de puntuación devuelve (posición, puntaje):

    1) posicion = donde jugar
    2) puntaje = puntuación
    """

    # Primero revisamos si estamos en el nodo terminal (o el juego ha terminado en la profundidad actual)
    es_terminal = es_nodo_terminal(tablero)
    ficha_oponente = fichaOponente(ficha)
    if profundidad == 0 or es_terminal:
        if es_terminal:
            if tablero.revisar_ganador() == ficha:  # Ganó el computador
                return (None, math.inf)

            elif tablero.revisar_ganador() == ficha_oponente:  # Ganó el "Humano"
                return (None, -math.inf)

            else:  # La partida se terminó, no hay más moivmientos válidos
                return (None, 0)

        else:  # Profundidad es 0
            if maximizar:
                return (None, funcion_puntaje(tablero, ficha))
            else:
                return (None, -funcion_puntaje(tablero, ficha_oponente))

    if maximizar:  # Turno del computador en la profundidad actual

        posiciones_validas = tablero.jugadas_disponibles()

        # Iniciamos un puntaje muy bajo
        puntaje = -math.inf

        # Elegir un movimiento random si no hay uno mejor
        posicion = random.choice(posiciones_validas)

        # Expandimos los nodos para cada columna válida
        for jugada in posiciones_validas:
            copia_tablero = deepcopy(tablero)
            
            copia_tablero.ejecutar_jugada(jugada, ficha)
            puntos = BestMove(jugada, copia_tablero, ficha)

            jugada_, puntos = minimax(copia_tablero, profundidad - 1, alpha, beta, funcion_puntaje, False, ficha)

            if puntos > puntaje:
                jugada, puntaje = BestMove(jugada, copia_tablero, ficha)
                alpha = max(alpha, puntaje)
                if beta <= alpha:
                    break
        posicion = jugada
        return posicion, puntaje

    else:  # Turno del "Humano" en la profundidad actual
        posiciones_validas = tablero.jugadas_disponibles()

        # Iniciamos un puntaje muy alto
        puntaje = math.inf

        # Elegir un movimiento random si no hay uno mejor
        posicion = random.choice(posiciones_validas)

        # Expandimos los nodos para cada columna válida
        for jugada in posiciones_validas:
            copia_tablero = deepcopy(tablero)

            copia_tablero.ejecutar_jugada(jugada, ficha)

            jugada_, puntos = minimax(copia_tablero, profundidad - 1, alpha, beta, funcion_puntaje, True, ficha)

            puntos = BestMove(jugada, copia_tablero, ficha)

            if puntos < puntaje:
                puntaje = BestMove(jugada, copia_tablero, ficha)
                beta = min(alpha, puntaje)
                if beta <= alpha:
                    break
        posicion = jugada
        return posicion, puntaje

