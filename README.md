# Algoritmo A* 

Este projeto implementa o algoritmo A* (A-star) para busca de caminho em um grid 2D com diferentes custos de terreno e obstáculos.

## Metodologia

### Estrutura do Agente

O agente de busca de caminho é implementado através do algoritmo A*, que é um algoritmo de busca informada que utiliza uma função heurística para guiar a exploração do espaço de estados. O agente opera em um ambiente representado por um grid bidimensional onde cada célula pode ter diferentes custos de movimento.

#### Componentes Principais:

1. **Estado**: Cada posição (x, y) no grid representa um estado
2. **Ações**: Movimento para células adjacentes (Norte, Sul, Leste, Oeste)
3. **Função de Custo**: Custo de mover de uma célula para outra
4. **Função Heurística**: Estimativa do custo do estado atual até o objetivo
5. **Função de Avaliação**: f(n) = g(n) + h(n)

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

#### Estruturas de Dados do Algoritmo:

1. **`frontier: PriorityQueue`**
   - Armazena nós a serem explorados ordenados por f(n) = g(n) + h(n)
   - Garante que sempre exploramos o nó mais promissor primeiro

2. **`came_from: Dict[Location, Optional[Location]]`**
   - Mapeia cada nó para seu predecessor no caminho ótimo
   - Permite reconstrução do caminho após encontrar o objetivo

3. **`cost_so_far: Dict[Location, float]`**
   - Armazena g(n): custo real do início até cada nó
   - Usado para detectar caminhos melhores para nós já visitados

### Validação e Tratamento de Erros

O sistema implementa validação robusta de posições através da função `validate_positions()`:

#### Verificações Realizadas:
1. **Limites do Grid**: Posições dentro dos limites (0, 0) até (width-1, height-1)
2. **Obstáculos**: Start e goal não podem estar em paredes
3. **Diferenciação**: Start e goal devem ser posições diferentes
4. **Passabilidade**: Células devem ser transitáveis

#### Tratamento de Erros:
- `ValueError`: Levantado quando posições são inválidas
- Mensagens descritivas para cada tipo de erro
- Validação prévia antes da execução do algoritmo

### Apresentação Matemática da Função Heurística

#### Distância de Manhattan Ajustada

A função heurística implementada é uma **Distância de Manhattan ajustada por custo mínimo**:

```
h(n) = (|x₁ - x₂| + |y₁ - y₂|) × min_step_cost
```

Onde:
- `(x₁, y₁)` são as coordenadas do estado atual
- `(x₂, y₂)` são as coordenadas do estado objetivo
- `|·|` representa o valor absoluto
- `min_step_cost` é o custo mínimo por movimento (padrão: 1.0)

#### Propriedades da Heurística:

1. **Admissibilidade Condicional**:
   - ✅ **ADMISSÍVEL quando `min_step_cost ≥ 1.0`**: A heurística nunca superestima o custo real
   - ❌ **NÃO-ADMISSÍVEL quando `min_step_cost < 1.0`**: A heurística pode subestimar o custo real

2. **Consistência**: ✓ (quando admissível)
   - Para qualquer nó n e seu sucessor n':
   - h(n) ≤ c(n, n') + h(n')
   - Verdade quando min_step_cost representa o custo real mínimo de movimento

#### Demonstração da Admissibilidade:

Seja d_manhattan(n, goal) a distância de Manhattan entre n e goal.

**Teorema**: h(n) = d_manhattan(n, goal) × min_step_cost é admissível quando min_step_cost ≥ custo_mínimo_real.

**Prova (caso admissível)**:
- Seja h*(n) o custo real ótimo de n até goal
- O número mínimo de movimentos necessários é d_manhattan(n, goal)
- Se min_step_cost ≥ custo real mínimo por movimento:
  - h*(n) ≥ d_manhattan(n, goal) × custo_mínimo_real ≥ d_manhattan(n, goal) × min_step_cost = h(n)
- Portanto, h(n) ≤ h*(n) ∀n ∈ Estados

**Caso não-admissível (min_step_cost < 1.0)**:
- Se min_step_cost = 0.5 e custos reais são ≥ 1.0:
- h(n) = d_manhattan(n, goal) × 0.5 < d_manhattan(n, goal) × 1.0 ≤ h*(n)
- A heurística subestima, violando a admissibilidade
- **Consequência**: O A* pode retornar soluções subótimas

#### Função de Avaliação:

```
f(n) = g(n) + h(n)
```

Onde:
- `g(n)`: Custo real acumulado do início até n
- `h(n)`: Estimativa heurística de n até o objetivo
- `f(n)`: Estimativa do custo total do caminho através de n

## Uso

### Executando o Programa:

```bash
python3 main.py
```

### Estrutura dos Arquivos:

```
├── main.py                 # Arquivo principal de execução
├── src/
│   └── implementation.py   # Classes e algoritmos principais
├── data/
│   ├── walls.py           # Coordenadas dos obstáculos
│   └── scenarios.py       # Cenários pré-definidos
└── README.md              # Este arquivo
```

### Funcionalidades Principais:

#### 1. **Cenários Pré-definidos**
O programa inclui 8 cenários pré-definidos para testar diferentes situações:

- **Cenário 0 - "Isolado em uma praia"**: Goal isolado e inacessível
- **Cenário 1 - "Vulcão"**: Obstáculo central impedindo acesso
- **Cenário 2 - "Posição inválida"**: Goal sobre uma parede (erro)
- **Cenário 3 - "Usar Atalho"**: Caminho com aproveitamento de área rápida
- **Cenário 4 - "Bordas Opostas"**: Máxima distância no grid
- **Cenário 5 - "Curta Distância"**: Teste rápido com caminho simples
- **Cenário 6 - "Evitar Montanha"**: Contorno de terrenos caros
- **Cenário 7 - "Desafio"**: Navegação complexa com muitos obstáculos

Para mudar o cenário, altere `SCENARIO_INDEX` em `main.py` (0-7).

#### 2. **Log Detalhado**
Ative `ENABLE_VERBOSE = True` em `main.py` para ver:
- **Listas Open e Closed** a cada iteração
- **Valores de g(n), h(n) e f(n)** para cada nó
- **Número de vizinhos adicionados** por iteração
- **Estatísticas finais** de exploração (nós visitados/explorados)
- **Processo de validação** de posições

#### 3. **Visualização Colorida**
- 🔵 **A (azul)**: Posição inicial
- 🟡 **Z (amarelo)**: Posição objetivo  
- 🟢 **@ (verde)**: Caminho encontrado
- 🔴 **### (vermelho)**: Obstáculos
- **. (branco)**: Células livres
- **>**, **<**, **^**, **v**: Direções exploradas (quando usando point_to)

#### 4. **Tratamento de Casos de Falha**
- **Validação automática** de posições inválidas
- **Detecção de caminhos impossíveis** (goal isolado)
- **Mensagens de erro descritivas** para debugging
- **Verificação de limites do grid**

### Personalização:

1. **Selecionar cenário**: Altere `SCENARIO_INDEX` em `main.py`
2. **Ativar logging**: Configure `ENABLE_VERBOSE = True` em `main.py`
3. **Modificar o grid**: Altere `GRID_WIDTH` e `GRID_HEIGHT` em `main.py`
4. **Adicionar áreas de custo**: Use `g.add_cost_area(x_min, y_min, x_max, y_max, cost)`
5. **Modificar obstáculos**: Edite a lista `WALLS` em `data/walls.py`
6. **Criar novos cenários**: Adicione objetos `Scenario` em `data/scenarios.py`

### Estrutura de Cenários

Cada cenário é definido pela classe `Scenario`:

```python
class Scenario:
    def __init__(self, name: str, start: GridLocation, goal: GridLocation, description: str):
        self.name = name
        self.start = start
        self.goal = goal
        self.description = description
```

## Análise de Complexidade

- **Tempo**: O(b^d) no pior caso, onde b é o fator de ramificação e d é a profundidade
- **Espaço**: O(b^d) para armazenar a fronteira e nós visitados
- **Otimalidade**: Garantida quando a heurística é admissível (como nossa implementação)

### Estatísticas de Desempenho

O programa exibe estatísticas importantes:
- **Número total de nós explorados** (closed list)
- **Número total de nós visitados** (open + closed)
- **Custo total do caminho** encontrado
- **Número de passos** no caminho
- **Número de iterações** do algoritmo

## Visualização

O programa exibe o grid no terminal com:
- `A`: Posição inicial (azul)
- `Z`: Posição objetivo (amarelo)
- `@`: Caminho encontrado (verde)
- `###`: Obstáculos (vermelho)
- `.`: Células livres
- `>`, `<`, `^`, `v`: Direções exploradas 

## Casos de Teste

O sistema foi projetado para lidar com diversos cenários:

### Casos de Sucesso:
- Caminhos simples e diretos
- Navegação em terrenos com custos variados
- Contorno de obstáculos complexos
- Otimização de rotas em áreas de baixo custo

### Casos de Falha Controlada:
- **Posições fora dos limites**: Detectado na validação
- **Posições em obstáculos**: Rejeitado antes da execução
- **Goals isolados**: Caminho não encontrado após exploração completa
- **Start = Goal**: Detectado como entrada inválida

O tratamento robusto de erros garante que o programa forneça feedback claro sobre problemas na configuração dos cenários. 