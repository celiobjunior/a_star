"""
Arquivo contendo cenários pré-definidos para start e goal.
Cada cenário representa uma situação para testar o algoritmo A*.
"""

from typing import List, Tuple, Dict

GridLocation = Tuple[int, int]

class Scenario:
    def __init__(self, name: str, start: GridLocation, goal: GridLocation, description: str):
        self.name = name
        self.start = start
        self.goal = goal
        self.description = description

SCENARIOS: List[Scenario] = [
    # Cenário 0
    Scenario(
        name="Isolado em uma praia",
        start=(2, 2),
        goal=(47, 47),
        description="O caminho final não pode ser alcançado pois Z está isolado"
    ),
    # Cenário 1
    Scenario(
        name="Vulcão",
        start=(40, 10),
        goal=(10, 41),
        description="Um vulcão no meio do grid - A não consegue chegar ao objetivo"
    ),
    # Cenário 2
    Scenario(
        name="Posição inválida",
        start=(10, 15),
        goal=(40, 30),
        description="Goal é uma posição inválida pois está dentro de uma parede"
    ),
    # Cenário 3
    Scenario(
        name="Usar Atalho",
        start=(5, 12),
        goal=(20, 13),
        description="Caminho que pode usar o atalho rápido"
    ),
    # Cenário 4
    Scenario(
        name="Bordas Opostas",
        start=(44, 0),
        goal=(4, 48),
        description="Tentando encontrar distâncias maiores"
    ),
    # Cenário 5
    Scenario(
        name="Curta Distância",
        start=(26, 26),
        goal=(30, 30), 
        description="Caminho curto para teste rápido"
    ),
    # Cenário 6
    Scenario(
        name="Evitar Montanha",
        start=(45, 5),
        goal=(5, 45),
        description="Caminho que deve contornar terrenos caros"
    ),
    # Cenário 7
    Scenario(
        name="Desafio",
        start=(30, 49),
        goal=(2, 16),
        description="Navegação com muitos obstáculos"
    )
]

def get_scenario_by_index(index: int) -> Scenario:
    """Retorna um cenário pelo índice."""
    if 0 <= index < len(SCENARIOS):
        return SCENARIOS[index]
    else:
        raise IndexError(f"Índice {index} fora do intervalo. Disponíveis: 0-{len(SCENARIOS)-1}")

def list_scenarios() -> None:
    """Lista todos os cenários disponíveis."""
    print("Cenários disponíveis:")
    for i, scenario in enumerate(SCENARIOS):
        print(f"{i}: {scenario.name} - {scenario.description}")
        print(f"   Start: {scenario.start}, Goal: {scenario.goal}")
    print() 