# Algoritmo A* 

Este projeto implementa o algoritmo A* (A-star) para busca de caminho em um grid 2D com diferentes custos de terreno e obstáculos.

## Metodologia

### Estrutura do Agente

O agente de busca de caminho é implementado através do algoritmo A*, que é um algoritmo de busca informada que utiliza uma função heurística para guiar a exploração do espaço de estados. O agente opera em um ambiente representado por um grid bidimensional onde cada célula pode ter diferentes custos de movimento.

#### Componentes Principais:

1. **Estado**: Cada posição (x, y) no grid representa um estado
2. **Ações**: Movimento para células adjacentes (Norte, Sul, Leste, Oeste)
3. **Função de Custo**: Custo de mover de uma célula para outra
4. **Função Heurística**: Estimativa do custo restante até o objetivo (Distância de Manhattan)
5. **Função de Avaliação**: f(n) = g(n) + h(n), onde g(n) é o custo acumulado e h(n) é a heurística

### Estruturas de Dados Utilizadas

#### Classes Principais:

1. **`GridLocation`**: `Tuple[int, int]`
   - Representa uma coordenada (x, y) no grid
   - Tipo básico para posições no espaço de estados

2. **`PriorityQueue`**: 
   - Implementada usando `heapq` do Python
   - Armazena elementos como tuplas `(prioridade, item)`
   - Permite recuperação eficiente do elemento com menor prioridade
   - **Complexidade**: O(log n) para inserção e remoção

3. **`SquareGrid`**:
   ```python
   class SquareGrid:
       def __init__(self, width: int, height: int):
           self.width = width
           self.height = height
           self.walls: list[GridLocation] = []
   ```
   - Representa o grid básico com largura, altura e obstáculos
   - Métodos: `in_bounds()`, `passable()`, `neighbors()`

4. **`GridWithWeights(SquareGrid)`**:
   ```python
   class GridWithWeights(SquareGrid):
       def __init__(self, width: int, height: int):
           super().__init__(width, height)
           self.weights: Dict[GridLocation, float] = {}
           self.area_definitions: List[Dict] = []
   ```
   - Estende `SquareGrid` com suporte a custos variáveis
   - `weights`: Custos específicos por célula
   - `area_definitions`: Áreas retangulares com custos uniformes

### Heurística: Admissibilidade vs Não-Admissibilidade

#### Definições Fundamentais

**Heurística Admissível:**
- h(n) ≤ C*(n) para todo nó n
- **NUNCA SUPERESTIMA** o custo real para o objetivo
- **Garante** que o A* encontre o caminho ótimo
- Exemplo: Distância de Manhattan com multiplicador ≤ custo mínimo de movimento

**Heurística Não-Admissível:**
- h(n) > C*(n) para alguns nós n
- **SUPERESTIMA** o custo real em certas situações
- A* pode encontrar caminhos subótimos, mas geralmente executa mais rapidamente
- Exemplo: Distância de Manhattan com multiplicador > custo mínimo de movimento

#### Implementação da Heurística

#### Propriedades da Heurística:

1. **Admissibilidade Condicional**:
   - ✅ **ADMISSÍVEL quando `min_step_cost <= 1.0`**: A heurística nunca superestima o custo real
   - ❌ **NÃO-ADMISSÍVEL quando `min_step_cost > 1.0`**: A heurística pode subestimar o custo real

2. **Consistência**: ✓ (quando admissível)
   - Para qualquer nó n e seu sucessor n':
   - h(n) ≤ c(n, n') + h(n')
   - Verdade quando min_step_cost representa o custo real mínimo de movimento

### Tratamento de Erros e Casos de Falha

O sistema implementa tratamento robusto para:

- **Posições inválidas**: Detecta coordenadas fora do grid ou em obstáculos
- **Objetivos isolados**: Identifica quando não há caminho possível
- **Validação de entrada**: Verifica parâmetros antes da execução

### Estrutura de Dados e Algoritmo

O algoritmo A* utiliza:

- **Fila de prioridade (frontier)**: Para explorar nós em ordem de menor f(n)
- **Lista fechada (closed_set)**: Nós já processados
- **Lista aberta (open_set)**: Nós descobertos mas não processados
- **came_from**: Para reconstruir o caminho final
- **cost_so_far**: Custos acumulados g(n) para cada nó

## Cenários de Teste

O projeto inclui 8 cenários pré-definidos para demonstrar diferentes aspectos:
Cada cenário é definido pela classe `Scenario`:
```python
@dataclass
class Scenario:
    name: str
    description: str
    start: GridLocation
    goal: GridLocation
```

## Funcionalidades Implementadas

### Core do Algoritmo
- ✅ Implementação completa do A*
- ✅ Função heurística configurável (admissível/não-admissível)
- ✅ Validação de posições e conectividade
- ✅ Tratamento de casos de falha

### Visualização e Debugging
- ✅ Grid visual com símbolos intuitivos
- ✅ Exibição do caminho encontrado
- ✅ Logging detalhado das iterações (modo verbose)
- ✅ Estatísticas de desempenho

### Estrutura Modular
- ✅ Separação entre dados (cenários, paredes) e lógica
- ✅ Configurações centralizadas no main.py
- ✅ Tratamento de erros em múltiplas camadas

## Como Usar

### Configuração Básica
```python
# main.py - Configurações principais
SCENARIO_INDEX = 4        # Escolher cenário (0-7)
ENABLE_VERBOSE = True     # Ativar logs detalhados
GRID_WIDTH = 50          # Largura do grid
GRID_HEIGHT = 50         # Altura do grid
```

### Definir Áreas de Custo
```python
# Sintaxe: add_cost_area(x_min, y_min, x_max, y_max, custo)
g.add_cost_area(0, 23, 49, 27, 6.0)    # Área horizontal
g.add_cost_area(25, 0, 49, 24, 10.0)   # Área superior direita
```

### Executar
```bash
python main.py
```

## Saída do Programa

### Informações do Cenário
```
Cenário selecionado: Caminho Complexo
Descrição: Navegação através de múltiplas áreas com custos diferentes
Start: (1, 1) → Goal: (4, 48)
```

### Estatísticas de Execução
```
Caminho encontrado com 109 passos.
Custo total do caminho: 364.0
Total de nós explorados: 1210
Total de nós visitados: 1317
```

### Visualização do Grid
- `A`: Posição inicial (start)
- `Z`: Posição objetivo (goal)  
- `@`: Caminho encontrado
- `#`: Obstáculos/paredes
- `.`: Células livres
- Símbolos direcionais (`^`, `v`, `<`, `>`) mostram o fluxo do algoritmo

## Estrutura do Projeto

```
a_star/
├── main.py                 # Arquivo principal de execução
├── src/
│   └── implementation.py   # Algoritmo A* e classes auxiliares
├── data/
│   ├── scenarios.py        # Cenários de teste predefinidos
│   └── walls.py           # Definições de obstáculos
└── README.md              # Esta documentação
```