from __future__ import annotations
from typing import List, Protocol, Iterator, Tuple, TypeVar, Optional, Dict
import heapq

T = TypeVar('T')
Location = TypeVar('Location')
GridLocation = Tuple[int, int]

class Graph(Protocol):
    def neighbors(self, id: Location) -> list[Location]: pass

class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float: pass

class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, T]] = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) -> T:
        return heapq.heappop(self.elements)[1]

class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: list[GridLocation] = []

    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls

    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors_coords = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        if (x + y) % 2 == 0: neighbors_coords.reverse() # S N W E
        results = filter(self.in_bounds, neighbors_coords)
        results = filter(self.passable, results)
        return results

class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: Dict[GridLocation, float] = {}
        self.area_definitions: List[Dict] = []

    def add_cost_area(self, x_min: int, y_min: int, x_max: int, y_max: int, area_cost: float):
        """
        Define uma área retangular no grid com um custo de movimento específico.

        Args:
            x_min: Coordenada X mínima da área (inclusiva).
            y_min: Coordenada Y mínima da área (inclusiva).
            x_max: Coordenada X máxima da área (inclusiva).
            y_max: Coordenada Y máxima da área (inclusiva).
            area_cost: O custo para entrar em qualquer célula dentro desta área.
        """
        if not (0 <= x_min < self.width and 0 <= y_min < self.height and
                x_min <= x_max < self.width and y_min <= y_max < self.height):
            print(f"Aviso: Área ({x_min},{y_min})-({x_max},{y_max}) com custo {area_cost} "
                  f"está parcial ou totalmente fora dos limites do grid ({self.width}x{self.height}).")
        self.area_definitions.append({'rect': (x_min, y_min, x_max, y_max), 'cost': area_cost})
        print(f"Adicionada área de custo: ({x_min},{y_min})-({x_max},{y_max}), custo={area_cost}")

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        """
        Retorna o custo de se mover PARA 'to_node'.
        Prioridade:
        1. Custo da primeira área definida que contém 'to_node'.
        2. Se não estiver em nenhuma área, custo de self.weights.get(to_node, 1.0).
        """
        node_x, node_y = to_node

        # Verificar se to_node está dentro de alguma área definida
        for area_def in self.area_definitions:
            rect_x_min, rect_y_min, rect_x_max, rect_y_max = area_def['rect']
            area_specific_cost = area_def['cost']

            if rect_x_min <= node_x <= rect_x_max and rect_y_min <= node_y <= rect_y_max:
                return area_specific_cost

        return self.weights.get(to_node, 1.0)

def heuristic(a: GridLocation, b: GridLocation, min_step_cost: float = 1.0) -> float:
    """
    Calcula a distância de Manhattan entre dois pontos no grid, 
    ajustada pelo custo mínimo de movimento.
    
    Args:
        a: Posição atual (x, y)
        b: Posição objetivo (x, y)  
        min_step_cost: Custo mínimo por movimento (default: 1.0)
        
    Returns:
        Estimativa heurística do custo restante
        
    Note:
        - Com min_step_cost >= 1.0: Heurística ADMISSÍVEL (caminho ótimo garantido)
        - Com min_step_cost > 1.0: Heurística NÃO-ADMISSÍVEL (pode superar custo real)
    """
    (x1, y1) = a
    (x2, y2) = b
    return (abs(x1 - x2) + abs(y1 - y2)) * min_step_cost

def validate_positions(graph: SquareGrid, start: Location, goal: Location) -> tuple[bool, str]:
    """
    Valida se as posições de início e objetivo são válidas.
    
    Args:
        graph: Grid para validação
        start: Posição inicial
        goal: Posição objetivo
        
    Returns:
        (is_valid, error_message): Tupla com status de validação e mensagem de erro
    """
    # Verifica se start está dentro dos limites
    if not graph.in_bounds(start):
        return False, f"Posição inicial {start} está fora dos limites do grid ({graph.width}x{graph.height})"
    
    # Verifica se goal está dentro dos limites
    if not graph.in_bounds(goal):
        return False, f"Posição objetivo {goal} está fora dos limites do grid ({graph.width}x{graph.height})"
    
    # Verifica se start não está em uma parede
    if not graph.passable(start):
        return False, f"Posição inicial {start} está bloqueada por uma parede/obstáculo"
    
    # Verifica se goal não está em uma parede
    if not graph.passable(goal):
        return False, f"Posição objetivo {goal} está bloqueada por uma parede/obstáculo"
    
    # Verifica se start e goal são diferentes
    if start == goal:
        return False, f"Posição inicial e objetivo são iguais: {start}"
    
    return True, ""

def a_star_search(graph: WeightedGraph, start: Location, goal: Location, verbose: bool = False):
    """
    Implementação do algoritmo A* para busca de caminho.
    
    Args:
        graph: Grafo com pesos para navegação
        start: Posição inicial
        goal: Posição objetivo
        verbose: Se True, imprime log detalhado das listas Open e Closed
        
    Returns:
        came_from, cost_so_far: Dicionários para reconstrução do caminho e custos
        
    Raises:
        ValueError: Se as posições de start ou goal forem inválidas
    """
    # Validar posições antes de iniciar
    is_valid, error_message = validate_positions(graph, start, goal)
    if not is_valid:
        raise ValueError(f"ERRO DE VALIDAÇÃO: {error_message}")
    
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    closed_set: set[Location] = set()
    open_set: dict[Location, float] = {start: 0} 
    iteration = 0
    
    if verbose:
        print("=== INICIANDO A* ===")
        print(f"Start: {start}, Goal: {goal}")
        print(f"Heurística inicial: {heuristic(start, goal)}")
        print()
    
    while not frontier.empty():
        iteration += 1
        current: Location = frontier.get()
        
        if current in open_set:
            del open_set[current]
        closed_set.add(current)
        
        if verbose:
            print(f"--- Iteração {iteration} ---")
            print(f"Nó atual: {current}")
            print(f"g(n) = {cost_so_far[current]:.1f}, h(n) = {heuristic(current, goal):.1f}, f(n) = {cost_so_far[current] + heuristic(current, goal):.1f}")
            print(f"LISTA FECHADA: {sorted(list(closed_set))}")
            print(f"LISTA ABERTA: {sorted(open_set.keys())}")
        
        if current == goal:
            if verbose:
                print(f"OBJETIVO ENCONTRADO em {iteration} iterações!")
                print(f"Lista fechada final: {sorted(list(closed_set))}")
            break
        
        neighbors_added = 0
        for next in graph.neighbors(current):
            if next in closed_set:
                continue  # Ignora nós já processados
                
            # Calcula o custo total do caminho até o próximo nó
            # g(n) = custo do caminho atual + custo de mover para o próximo nó
            new_cost = cost_so_far[current] + graph.cost(current, next)
            
            # Atualiza o nó se:
            # 1. É a primeira vez que visitamos (next not in cost_so_far)
            # 2. Encontramos um caminho mais barato (new_cost < cost_so_far[next])
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                # Atualiza o custo acumulado até este nó
                cost_so_far[next] = new_cost
                # Calcula f(n) = g(n) + h(n) para determinar prioridade na fila
                priority = new_cost + heuristic(next, goal)
                # Adiciona à fila de prioridade para exploração futura
                frontier.put(next, priority)
                # Registra o nó anterior para reconstruir o caminho depois
                came_from[next] = current
                # Mantém registro dos nós abertos e suas prioridades
                open_set[next] = priority
                neighbors_added += 1
                
                if verbose:
                    print(f"  → Vizinho {next}: g={new_cost:.1f}, h={heuristic(next, goal):.1f}, f={priority:.1f}")
        
        if verbose:
            print(f"Vizinhos adicionados: {neighbors_added}")
            print()
    
    if verbose:
        print("=== A* FINALIZADO ===")
        print(f"Total de nós explorados: {len(closed_set)}")
        print(f"Total de nós visitados: {len(cost_so_far)}")
        print()
    
    return came_from, cost_so_far

def reconstruct_path(came_from: dict[Location, Location],
                     start: Location, goal: Location) -> list[Location]:
    """
    Reconstrói o caminho do objetivo até o início.
    """
    current: Location = goal
    path: list[Location] = []
    if goal not in came_from:
        return []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def draw_tile(graph, id, style):
    """
    Desenha um tile individual do grid com cores ANSI.
    """
    GREEN = "\033[32m"
    RED = "\033[31m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    RESET_COLOR = "\033[0m"

    r = " . "
    if 'number' in style and id in style['number']: 
        r = " %-2d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = " > "
        if x2 == x1 - 1: r = " < "
        if y2 == y1 + 1: r = " v "
        if y2 == y1 - 1: r = " ^ "

    if 'path' in style and id in style['path']:
        r = f" {GREEN}@{RESET_COLOR} "

    if 'start' in style and id == style['start']:
        r = f" {BLUE}A{RESET_COLOR} "

    if 'goal' in style and id == style['goal']:
        r = f" {YELLOW}Z{RESET_COLOR} "

    if id in graph.walls:
        r = f"{RED}###{RESET_COLOR}"

    return r

def draw_grid(graph, **style):
    """
    Desenha o grid completo no terminal.
    """
    print("___" * graph.width)
    for y in range(graph.height):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~~~" * graph.width) 