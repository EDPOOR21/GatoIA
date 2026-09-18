class Gato:
    def __init__(self):
        # 0 = Vacío, 1 = Jugador 1 (X), -1 = IA (O)
        self.tablero = [0] * 9
        self.turno_actual = 1

    def movimientos_disponibles(self):
        return [i for i, casilla in enumerate(self.tablero) if casilla == 0]

    def hacer_movimiento(self, posicion):
        if self.tablero[posicion] == 0:
            self.tablero[posicion] = self.turno_actual
            self.turno_actual *= -1  # Cambia el turno mágicamente (1 a -1, -1 a 1)
            return True
        return False

    def estado_actual(self):
        # Convierte el tablero a un texto para usarlo como llave en el diccionario del bot
        return str(self.tablero)

    def revisar_ganador(self):
        # Combinaciones ganadoras (filas, columnas, diagonales)
        victorias = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for a, b, c in victorias:
            if self.tablero[a] == self.tablero[b] == self.tablero[c] != 0:
                return self.tablero[a]  # Retorna 1 o -1
        
        if 0 not in self.tablero:
            return 0  # Empate
            
        return None  # El juego sigue