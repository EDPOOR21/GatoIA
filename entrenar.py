from entorno import Gato
from agente import AgenteQLearning

def entrenar_por_historial(partidas=100000):
    agente = AgenteQLearning(epsilon=0.2)
    agente.cargar_memoria()
    
    print(f"Entrenando {partidas} partidas de la IA contra sí misma...")
    
    for _ in range(partidas):
        juego = Gato()
        # Aquí aplicamos tu idea: guardamos la historia completa de la partida
        historial_X = []
        historial_O = []
        
        while True:
            estado_actual = juego.estado_actual()
            acciones = juego.movimientos_disponibles()
            
            if juego.turno_actual == 1:
                # Turno X (La IA jugando con X)
                accion = agente.elegir_accion(estado_actual, acciones)
                historial_X.append((estado_actual, accion))
                juego.hacer_movimiento(accion)
            else:
                # Turno O (La IA jugando con O)
                accion = agente.elegir_accion(estado_actual, acciones)
                historial_O.append((estado_actual, accion))
                juego.hacer_movimiento(accion)
            
            resultado = juego.revisar_ganador()
            if resultado is not None:
                # ¡FIN DEL JUEGO! Evaluamos toda la cadena de turnos
                
                # Definimos quién ganó y quién perdió
                recompensa_X = 1 if resultado == 1 else (-1 if resultado == -1 else 0)
                recompensa_O = 1 if resultado == -1 else (-1 if resultado == 1 else 0)
                
                # Propagamos el castigo o premio HACIA ATRÁS en todo el historial de O
                for estado, accion in reversed(historial_O):
                    agente.aprender(estado, accion, recompensa_O, juego.estado_actual(), [])
                    # El impacto se reduce un poco en turnos más antiguos (gamma)
                    recompensa_O *= agente.gamma 
                    
                # Hacemos lo mismo para el historial de X
                for estado, accion in reversed(historial_X):
                    agente.aprender(estado, accion, recompensa_X, juego.estado_actual(), [])
                    recompensa_X *= agente.gamma
                    
                break
                
    agente.guardar_memoria()
    print("¡Entrenamiento Avanzado completado!")

if __name__ == "__main__":
    entrenar_por_historial()