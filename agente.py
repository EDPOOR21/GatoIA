import json
import random

class AgenteQLearning:
    def __init__(self, epsilon=0.1, alpha=0.2, gamma=0.9):
        self.q_table = {}       # La memoria del bot
        self.epsilon = epsilon  # Tasa de exploración (el "defecto" del 10%)
        self.alpha = alpha      # Tasa de aprendizaje (qué tan rápido sobrescribe memoria vieja)
        self.gamma = gamma      # Factor de descuento (qué tanto le importan las recompensas futuras)

    def obtener_q_valor(self, estado, accion):
        # Si nunca ha visto esta jugada, su valor inicial es 0
        return self.q_table.get((estado, accion), 0.0)

    def elegir_accion(self, estado, acciones_disponibles):
        # Exploración: Jugar al azar basado en Epsilon
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(acciones_disponibles)
        
        # Explotación: Jugar el mejor movimiento conocido
        q_valores = [self.obtener_q_valor(estado, a) for a in acciones_disponibles]
        max_q = max(q_valores)
        
        # Si hay empates en los puntajes máximos, elige uno de ellos al azar
        mejores_acciones = [a for a, q in zip(acciones_disponibles, q_valores) if q == max_q]
        return random.choice(mejores_acciones)

    def aprender(self, estado, accion, recompensa, siguiente_estado, siguientes_acciones):
        q_actual = self.obtener_q_valor(estado, accion)
        
        # Calcular el valor máximo posible en el siguiente turno
        if siguientes_acciones:
            max_q_siguiente = max([self.obtener_q_valor(siguiente_estado, a) for a in siguientes_acciones])
        else:
            max_q_siguiente = 0.0  # El juego terminó, no hay futuro
            
        # Actualización usando la Ecuación de Bellman
        nuevo_q = q_actual + self.alpha * (recompensa + self.gamma * max_q_siguiente - q_actual)
        self.q_table[(estado, accion)] = nuevo_q

    def guardar_memoria(self, ruta="q_table.json"):
        # JSON no soporta tuplas como llaves, las pasamos a texto
        q_table_str = {f"{estado}|{accion}": valor for (estado, accion), valor in self.q_table.items()}
        with open(ruta, 'w') as f:
            json.dump(q_table_str, f)

    def cargar_memoria(self, ruta="q_table.json"):
        try:
            with open(ruta, 'r') as f:
                q_table_str = json.load(f)
            self.q_table = {}
            for llave, valor in q_table_str.items():
                estado, accion = llave.split('|')
                self.q_table[(estado, int(accion))] = float(valor)
        except FileNotFoundError:
            pass # Inicia con memoria vacía