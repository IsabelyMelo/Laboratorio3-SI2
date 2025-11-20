# Laboratório 3 – Problema do Caixeiro Viajante com Algoritmos Genéticos

## Autores

- **Caio Cezar Dias**
- **Isabely Toledo de Melo**


## Descrição do problema

Este projeto implementa uma solução para o Problema do Caixeiro Viajante (TSP) utilizando Algoritmos Genéticos (AG).

O objetivo é encontrar um percurso de custo mínimo que:

1. Visite todas as cidades apenas uma vez;
2. Retorne à cidade de origem.

A instância utilizada contém 8 cidades posicionadas em um plano 2D, com coordenadas geradas aleatoriamente dentro do intervalo \([0, 100] \times [0, 100]\), mantendo uma seed fixa (`random.seed(32)`) para garantir reprodutibilidade.


## Estrutura geral do algoritmo

O algoritmo segue o ciclo padrão de um AG:

1. **Representação**  
   - Cada indivíduo representa uma possível rota do caixeiro viajante.  
   - Exemplo de indivíduo:  
     ```python
     [0, 3, 5, 1, 7, 2, 4, 6]
     ```

2. **Função de avaliação (fitness)**  
   - A aptidão de um indivíduo é calculada como o inverso do comprimento da rota:
     ```python
     fitness(tour) = 1.0 / tour_length(tour)
     ```
   - O comprimento da rota é a soma das distâncias euclidianas entre cidades consecutivas, incluindo o retorno à cidade inicial.

3. **Inicialização da população**  
   - A população inicial é criada embaralhando permutações válidas de todas as cidades:
     ```python
     POP_SIZE = 100
     population = [create_individual() for _ in range(POP_SIZE)]
     ```

4. **Seleção (Torneio)**
   - Utiliza-se seleção por torneio com tamanho:
     ```python
     TOURNAMENT_SIZE = 3
     ```
   - São escolhidos `k` indivíduos aleatórios e o melhor (menor distância) é selecionado como pai.
   - O torneio foi escolhido pois é computacionalmente eficiente e permite controlar a pressão seletiva ajustando o tamanho k. Para populações pequenas/médias (100 indivíduos), o torneio evita problemas de convergência prematura que a roleta pode ter se houver "super indivíduos".


5. **Crossover (Order Crossover – OX)**  
   - Implementa-se um crossover do tipo order crossover, adequado ao TSP, que:
     - Copia um segmento contínuo do primeiro pai para o filho;
     - Preenche as posições restantes mantendo a ordem relativa dos genes do segundo pai e preservando a permutação válida.
   - A taxa de crossover é:
     ```python
     CROSSOVER_RATE = 0.8
     ```

6. **Mutação (Swap Mutation)**  
   - A mutação utilizada é do tipo swap, que troca duas cidades de posição na rota.
   - É garantido que a permutação continue válida.
   - Taxa de mutação:
     ```python
     MUTATION_RATE = 0.02  # 2%
     ```

7. **Elitismo**  
   - Os melhores indivíduos de uma geração são preservados na próxima:
     ```python
     ELITE_SIZE = 2
     ```

8. **Critério de parada**  
   - O algoritmo encerra quando atinge:
     ```python
     NUM_GENERATIONS = 200
     ```
   - Opcionalmente, há um critério de parada por falta de melhoria:
     ```python
     NO_IMPROVEMENT_LIMIT = 50
     ```
     Se a melhor distância não melhorar por 50 gerações consecutivas, o algoritmo é interrompido.

9. **Registro do histórico**  
   - A cada geração, é registrada a melhor distância encontrada, permitindo a plotagem da evolução da aptidão ao longo das gerações.


## Bibliotecas utilizadas

- `random` – geração de números aleatórios e embaralhamento da população;
- `math` – cálculo da distância euclidiana (`math.hypot`);
- `matplotlib.pyplot` – geração dos gráficos:
  - Gráfico da rota final.
  - Gráfico da evolução da melhor distância por geração.
- `networkx` – construção de um grafo simples para representar:
  - As cidades como nós;
  - As conexões da melhor rota como arestas.


## Saídas do programa

Ao executar o código, são geradas as seguintes saídas:

1. **Coordenadas das cidades**  
   Impressão no terminal das coordenadas geradas para cada cidade.

2. **Melhor rota encontrada**  
   - Lista com a ordem das cidades visitadas.
   - Impressão da melhor distância total encontrada.

3. **Gráfico da melhor rota**  
   - Utilizando `networkx` e `matplotlib`:
     - Cidades como nós do grafo;
     - Arestas representando a melhor rota encontrada;
     - Título contendo a distância total da rota.

4. **Gráfico da evolução da melhor distância**  
   - Eixo X: geração;
   - Eixo Y: melhor distância até aquela geração;
   - Permite visualizar a convergência do algoritmo.