import random
import math
import matplotlib.pyplot as plt
import networkx as nx

# ==============================================================================
# CONFIGURAÇÕES E PARÂMETROS
# ==============================================================================
random.seed(32) # Garante a reprodutibilidade das coordenadas das cidades

# Parâmetros do Algoritmo Genético
N_CIDADES = 8
TAM_POPULACAO = 100        # Entre 40 e 120
N_GERACOES = 200           # Entre 150 e 400
TAXA_CROSSOVER = 0.8       # 80%
TAXA_MUTACAO = 0.02        # 2%
N_ELITISMO = 2             # Preserva os 2 melhores
TAM_TORNEIO = 3            # K para seleção por torneio

# Geração das Cidades (Conforme enunciado)
cidades = {i: (random.uniform(0, 100), random.uniform(0, 100)) for i in range(N_CIDADES)}

# ==============================================================================
# FUNÇÕES AUXILIARES (DISTÂNCIA E FITNESS)
# ==============================================================================

def calcular_distancia_euclidiana(cid1, cid2):
    """Calcula a distância euclidiana entre dois pontos (x, y)."""
    pos1 = cidades[cid1]
    pos2 = cidades[cid2]
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def calcular_fitness(cromossomo):
    """
    Calcula a aptidão do indivíduo.
    O fitness é o inverso da distância total, pois queremos MINIMIZAR a distância.
    """
    distancia_total = 0
    for i in range(len(cromossomo)):
        cidade_atual = cromossomo[i]
        # Conecta com a próxima cidade, e a última volta para a primeira (ciclo)
        proxima_cidade = cromossomo[(i + 1) % len(cromossomo)]
        distancia_total += calcular_distancia_euclidiana(cidade_atual, proxima_cidade)
    
    return 1 / distancia_total, distancia_total

# ==============================================================================
# OPERADORES GENÉTICOS
# ==============================================================================

def criar_individuo():
    """Cria um indivíduo (rota) como uma permutação aleatória das cidades."""
    individuo = list(cidades.keys())
    random.shuffle(individuo)
    return individuo

def criar_populacao(tamanho):
    """Gera a população inicial."""
    return [criar_individuo() for _ in range(tamanho)]

def selecao_torneio(populacao, fitnesses):
    """
    Seleciona um pai via Torneio.
    Escolhe 'k' indivíduos aleatórios e retorna o melhor entre eles.
    """
    selecionados = random.sample(list(zip(populacao, fitnesses)), TAM_TORNEIO)
    # Retorna o indivíduo com o maior fitness (menor distância)
    return max(selecionados, key=lambda item: item[1][0])[0]

def crossover_ox(pai1, pai2):
    """
    Ordered Crossover (OX1) - Adequado para problemas de permutação (TSP).
    Preserva a ordem relativa dos genes e evita duplicatas.
    """
    tamanho = len(pai1)
    filho = [-1] * tamanho
    
    # 1. Selecionar subsegmento do Pai 1
    inicio, fim = sorted(random.sample(range(tamanho), 2))
    
    # Copia o segmento do pai 1 para o filho
    filho[inicio:fim+1] = pai1[inicio:fim+1]
    
    # 2. Preencher o restante com genes do Pai 2 (na ordem original do Pai 2)
    genes_usados = set(filho[inicio:fim+1])
    pos_atual = (fim + 1) % tamanho
    
    for gene in pai2:
        # Se o gene ainda não está no filho, adiciona ele
        if gene not in genes_usados:
            # Encontra a próxima posição vazia
            while filho[pos_atual] != -1:
                pos_atual = (pos_atual + 1) % tamanho
            
            filho[pos_atual] = gene
            genes_usados.add(gene)
            
    return filho

def mutacao_swap(individuo):
    """
    Mutação por Troca (Swap Mutation).
    Troca duas cidades de posição aleatoriamente.
    """
    idx1, idx2 = random.sample(range(len(individuo)), 2)
    individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]
    return individuo

# ==============================================================================
# CICLO EVOLUTIVO (MAIN)
# ==============================================================================

def executar_ag():
    # 1. População Inicial
    populacao = criar_populacao(TAM_POPULACAO)
    melhor_global_rota = None
    melhor_global_distancia = float('inf')
    
    historico_distancia = []

    print(f"Iniciando AG com {TAM_POPULACAO} indivíduos por {N_GERACOES} gerações...")
    print("-" * 50)

    for geracao in range(N_GERACOES):
        # Avaliação
        fitnesses = [calcular_fitness(ind) for ind in populacao]
        
        # Identificar melhor da geração atual
        # fitnesses é uma tupla (score, distancia_real)
        melhor_ind_gen, (melhor_fit_gen, melhor_dist_gen) = max(zip(populacao, fitnesses), key=lambda item: item[1][0])
        
        # Atualizar melhor global
        if melhor_dist_gen < melhor_global_distancia:
            melhor_global_distancia = melhor_dist_gen
            melhor_global_rota = list(melhor_ind_gen)
            print(f"Geração {geracao}: Nova melhor distância = {melhor_global_distancia:.4f}")
        
        historico_distancia.append(melhor_dist_gen)

        # Elitismo: Preservar os N melhores
        populacao_ordenada = sorted(zip(populacao, fitnesses), key=lambda item: item[1][0], reverse=True)
        nova_populacao = [ind for ind, fit in populacao_ordenada[:N_ELITISMO]]

        # Criação da nova geração
        while len(nova_populacao) < TAM_POPULACAO:
            # Seleção
            pai1 = selecao_torneio(populacao, fitnesses)
            pai2 = selecao_torneio(populacao, fitnesses)
            
            # Crossover
            if random.random() < TAXA_CROSSOVER:
                filho = crossover_ox(pai1, pai2)
            else:
                filho = pai1[:] # Cópia se não houver crossover
            
            # Mutação
            if random.random() < TAXA_MUTACAO:
                filho = mutacao_swap(filho)
            
            nova_populacao.append(filho)
        
        populacao = nova_populacao

    return melhor_global_rota, melhor_global_distancia, historico_distancia

# ==============================================================================
# EXECUÇÃO E VISUALIZAÇÃO
# ==============================================================================

if __name__ == "__main__":
    melhor_rota, melhor_distancia, historico = executar_ag()

    print("-" * 50)
    print("RESULTADO FINAL")
    print(f"Melhor Distância Encontrada: {melhor_distancia:.4f}")
    print(f"Melhor Rota: {melhor_rota}")
    
    # Adiciona o ponto inicial ao final da rota para fechar o ciclo no gráfico
    rota_para_plot = melhor_rota + [melhor_rota[0]]

    # --- Plotagem com NetworkX ---
    G = nx.Graph()
    
    # Adicionar nós
    for node, pos in cidades.items():
        G.add_node(node, pos=pos)
    
    # Adicionar arestas baseadas na melhor rota
    arestas = []
    for i in range(len(rota_para_plot)-1):
        arestas.append((rota_para_plot[i], rota_para_plot[i+1]))
    
    G.add_edges_from(arestas)

    # Configuração visual
    plt.figure(figsize=(10, 5))
    
    # Subplot 1: Mapa das Cidades
    plt.subplot(1, 2, 1)
    pos = nx.get_node_attributes(G, 'pos')
    # Desenha nós
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    # Desenha arestas
    nx.draw_networkx_edges(G, pos, edgelist=arestas, edge_color='r', width=2)
    # Desenha labels
    nx.draw_networkx_labels(G, pos)
    plt.title(f"Melhor Rota (Dist: {melhor_distancia:.2f})")

    # Subplot 2: Convergência
    plt.subplot(1, 2, 2)
    plt.plot(historico)
    plt.title("Evolução da Distância (Convergência)")
    plt.xlabel("Geração")
    plt.ylabel("Distância Total")
    plt.grid(True)

    plt.tight_layout()
    plt.show()