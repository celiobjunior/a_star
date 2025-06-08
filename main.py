from typing import Tuple

from src.implementation import GridWithWeights, a_star_search, reconstruct_path, draw_grid, validate_positions
from data.walls import WALLS
from data.scenarios import get_scenario_by_index, list_scenarios

GridLocation = Tuple[int, int]

if __name__ == "__main__":
    GRID_WIDTH = 50
    GRID_HEIGHT = 50

    # --- Configurações ---
    SCENARIO_INDEX = 4
    ENABLE_VERBOSE = True
    
    print("********** ALGORITMO A* PARA BUSCA DE CAMINHO **********\n")
    
    # --- Listar cenários disponíveis ---
    #list_scenarios()
    
    # --- Selecionar cenário ---
    try:
        scenario = get_scenario_by_index(SCENARIO_INDEX)
        print(f"Cenário selecionado: {scenario.name}")
        print(f"Descrição: {scenario.description}")
        print(f"Start: {scenario.start} → Goal: {scenario.goal}")
        print()
    except IndexError as e:
        print(f"Erro: {e}")
        exit(1)

    g = GridWithWeights(GRID_WIDTH, GRID_HEIGHT)

    # --- Definir Áreas de Custo ---
    # Área 1
    g.add_cost_area(0, GRID_HEIGHT // 2 - 2, GRID_WIDTH - 1, GRID_HEIGHT // 2 + 2, 1.0)

    # Área 2
    g.add_cost_area(GRID_WIDTH // 2, 0, GRID_WIDTH - 1, GRID_HEIGHT // 2 - 1, 1.0)

    # Área 3
    g.add_cost_area(0, GRID_HEIGHT // 2 + 3, GRID_WIDTH // 2 - 1, GRID_HEIGHT - 15, 1.0)

    # Área 4
    g.add_cost_area(10, 10, 15, 15, 1.0)

    # --- Usar coordenadas do cenário ---
    start: GridLocation = scenario.start
    goal: GridLocation = scenario.goal

    # --- Carregar paredes do arquivo separado ---
    g.walls = WALLS
    print(f"{len(g.walls)} paredes carregadas do arquivo de dados.")
    print()

    # --- Executar A* ---
    print(f"Procurando caminho de {start} para {goal}...")
    print(f"Log detalhado: {'Ativado' if ENABLE_VERBOSE else 'Desativado'}")
    print()
    
    try:
        came_from, cost_so_far = a_star_search(g, start, goal, verbose=ENABLE_VERBOSE)
        path = reconstruct_path(came_from, start=start, goal=goal)
    except ValueError as e:
        print(e)
        print("\nVerifique se as coordenadas do cenário não coincidem com obstáculos.")
        exit(1)

    # --- Resultados ---
    if not path:
        print(f"Nenhum caminho encontrado de {start} para {goal}.")
        draw_grid(g, start=start, goal=goal)
    else:
        print(f"Caminho encontrado com {len(path)} passos.")
        print(f"Custo total do caminho: {cost_so_far.get(goal, float('inf'))}")
        print()
        
        if ENABLE_VERBOSE:
            style_args = {
                'point_to': came_from,
                'path': path,
                'start': start,
                'goal': goal,
            }
            draw_grid(g, **style_args)