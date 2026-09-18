from entorno import Gato
from agente import AgenteQLearning

def imprimir_tablero(tablero):
    simbolos = {0: " ", 1: "X", -1: "O"}
    print("\n")
    for i in range(0, 9, 3):
        print(f" {simbolos[tablero[i]]} | {simbolos[tablero[i+1]]} | {simbolos[tablero[i+2]]} ")
        if i < 6:
            print("---+---+---")
    print("\n")

def jugar_y_aprender():
    # Iniciamos al agente. Cargará q_table.json si existe, o empezará en blanco.
    agente = AgenteQLearning(epsilon=0.1)
    agente.cargar_memoria()
    
    while True:
        juego = Gato()
        estado_previo_ia = None
        accion_previa_ia = None
        
        print("\n=== NUEVA PARTIDA ===")
        imprimir_tablero(juego.tablero)
        
        while True:
            # 1. TURNO DEL HUMANO (Juega con X = 1)
            movimientos_validos = juego.movimientos_disponibles()
            try:
                humano_pos = int(input("Elige tu casilla (0-8): "))
                if humano_pos not in movimientos_validos:
                    print("Casilla ocupada o inválida. Intenta de nuevo.")
                    continue
            except ValueError:
                print("Ingresa un número válido del 0 al 8.")
                continue
                
            juego.hacer_movimiento(humano_pos)
            resultado = juego.revisar_ganador()
            
            # Si el humano gana, la IA castiga su error anterior
            if resultado is not None:
                imprimir_tablero(juego.tablero)
                if estado_previo_ia is not None:
                    recompensa = -1 if resultado == 1 else 0
                    agente.aprender(estado_previo_ia, accion_previa_ia, recompensa, juego.estado_actual(), [])
                break
            
            # 2. TURNO DE LA IA (Juega con O = -1)
            estado_actual = juego.estado_actual()
            acciones_disponibles = juego.movimientos_disponibles()
            
            # La IA sobrevive un turno más. Aprende que su movimiento anterior fue seguro (Recompensa = 0)
            if estado_previo_ia is not None:
                agente.aprender(estado_previo_ia, accion_previa_ia, 0, estado_actual, acciones_disponibles)
            
            # Elige su siguiente jugada
            accion_ia = agente.elegir_accion(estado_actual, acciones_disponibles)
            juego.hacer_movimiento(accion_ia)
            
            # Guarda qué hizo para evaluarlo en el siguiente turno
            estado_previo_ia = estado_actual
            accion_previa_ia = accion_ia
            
            imprimir_tablero(juego.tablero)
            resultado = juego.revisar_ganador()
            
            # Si la IA gana o empata, se premia a sí misma
            if resultado is not None:
                recompensa = 1 if resultado == -1 else 0
                agente.aprender(estado_previo_ia, accion_previa_ia, recompensa, juego.estado_actual(), [])
                break

        # FIN DE LA PARTIDA: Mostrar resultados y guardar en el JSON
        if resultado == 1:
            print("¡Ganaste! La IA acaba de registrar su error con un puntaje negativo.")
        elif resultado == -1:
            print("¡La IA te ganó!")
        else:
            print("¡Empate!")
            
        agente.guardar_memoria()
        print("-> q_table.json actualizado en tiempo real.")
        
        jugar_otra = input("¿Jugar otra vez? (s/n): ")
        if jugar_otra.lower() != 's':
            print("Saliendo de la arena...")
            break

if __name__ == "__main__":
    jugar_y_aprender()