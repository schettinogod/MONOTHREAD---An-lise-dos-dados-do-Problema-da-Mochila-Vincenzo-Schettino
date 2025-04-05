# -*- coding: utf-8 -*-
"""MONOTHREAD - Análise dos dados do Problema da Mochila.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/194MYLNk_EWDh3RnKPEXvQxBgFTIcNZRz

# Problema da Mochila:

O problema da mochila (em inglês, Knapsack problem) é um problema de optimização combinatória. O nome dá-se devido ao modelo de uma situação em que é necessário preencher uma mochila com objetos de diferentes pesos e valores. O objetivo é que se preencha a mochila com o maior valor possível, não ultrapassando o peso máximo.


O problema da mochila é um dos 21 problemas NP-completos de Richard Karp, exposto em 1972. A formulação do problema é extremamente simples, porém sua solução é mais complexa. Este problema é a base do primeiro algoritmo de chave pública (chaves assimétricas).


Normalmente este problema é resolvido com programação dinâmica, obtendo então a resolução exata do problema, mas também sendo possível usar PSE (procedimento de separação e evolução). Existem também outras técnicas, como usar algoritmo guloso, meta-heurística (algoritmos genéticos) para soluções aproximadas.
"""

# Lendo a base de dados dos Testes
import pandas as pd
teste = pd.read_csv('tempos_de_execucao_1000_mono_1_thread.csv')
print('Tamanho da Amostra: %d' %len(teste))
display(teste.head())

import matplotlib.pyplot as plt
plt.figure(figsize=(10,7))
plt.scatter(teste.index, teste['Tempo'], label='Alg.Serial')
plt.title('Tempo de execução')
plt.xlabel('Tamanho da Lista')
plt.ylabel('Segundos')
plt.legend()
plt.grid()
plt.show()

# Obtenção dos valores centrais
media   = teste['Tempo'].mean()
d_pad   = teste['Tempo'].std()
mediana = teste['Tempo'].median()

print('Media: %.3f' %media)
print('Desvio Padrão: %.3f' %d_pad)
print('Mediana: %.3f' %mediana)

# Aplicando regra de Sturges para obtenção de intervalos de valores
# Cálculo do intervalo de freqûencia: n = Tamanho da Amostra
import numpy as np

n = len(teste)
k = 1 + (10/3)*np.log10(n)
k = int(k.round(0))
print(f'Tamanho da Amostra: {k}')

# Coletando a frequência
tempo_exec_freq = np.histogram(teste['Tempo'], bins= k)
print(tempo_exec_freq)

from matplotlib import pyplot as plt
plt.figure(figsize=(10,7))
plt.hist(teste, bins = k)
plt.title('Histograma do tempo de execução')
plt.xlabel('Segundos')
plt.grid()
plt.show()

# Gráfico BoxPlot
plt.figure(figsize=(10,7))
plt.boxplot(teste['Tempo'], vert = False)
plt.title('Quartis do Tempo de Execução')
plt.xlabel('Segundos')
plt.legend()
plt.grid()
plt.show()

# Aplicando a Regras Chauvenet - Remoção de Outliers
cond1 = teste['Tempo'] < (media + 2 * d_pad)
cond2 = teste['Tempo'] > (media - 2 * d_pad)
teste = teste[cond1 & cond2]
print('Tamanho da Amostra: %d' %(len(teste)))
teste.head()

# Salvando os dados da Amostra
teste.to_csv('amostra_testes_serial_corrigido.csv', index=False)

# Lendo a base de dados dos Testes
import pandas as pd
teste = pd.read_csv('amostra_testes_serial_corrigido.csv')
teste.head()

"""### Apresentação dos dados sem Outliers"""

# Obtenção dos valores centrais
media   = teste['Tempo'].mean()
d_pad   = teste['Tempo'].std()
mediana = teste['Tempo'].median()

print('Media: %.3f' %media)
print('Desvio Padrão: %.3f' %d_pad)
print('Mediana: %.3f' %mediana)

# Aplicando regra de Sturges para obtenção de intervalos de valores
# Cálculo do intervalo de freqûencia: n = Tamanho da Amostra
import numpy as np

n = len(teste)
k = 1 + (10/3)*np.log10(n)
k = int(k.round(0))
print(f'Tamanho da Amostra: {k}')

# Coletando a frequência
tempo_exec_freq = np.histogram(teste['Tempo'], bins= k)
print(tempo_exec_freq)

from matplotlib import pyplot as plt
plt.figure(figsize=(10,7))
plt.hist(teste, bins = k)
plt.title('Histograma do tempo de execução')
plt.xlabel('Segundos')
plt.grid()
plt.show()

# Gráfico BoxPlot
plt.figure(figsize=(10,7))
plt.boxplot(teste['Tempo'], vert = False)
plt.title('Quartis do Tempo de Execução')
plt.xlabel('Segundos')
plt.legend()
plt.grid()
plt.show()

"""### Aplicando o Teorema do Limite Central"""

# Parâmetros para uma media de amostragens
tam_amost = 60
qtd_amost = 1000

# Obtendo a media de amostragens
import pandas as dp
amostra = []
for i in range(qtd_amost):
    amostra.append(teste.sample(n=tam_amost).mean()[0])
amostra = dp.DataFrame(data = amostra, columns=['Tempo'])
amostra.head()

# Valores Centrais da amostragem
amostra_media   = amostra['Tempo'].mean()
amostra_std     = amostra['Tempo'].std()
amostra_mediana = amostra['Tempo'].median()
print('** Valores Centrais da Amostra **')
print('Média da amostra:       %.4f' %amostra_media)
print('Desv.Padrão da amostra: %.4f' %amostra_std)
print('Mediana da amostra:     %.4f' %amostra_mediana)

# Desvio Padrão de inferência calculado
round(d_pad / np.sqrt(tam_amost),4)

# Visualizando a amostra:
plt.figure(figsize=(10,7))
plt.hist(amostra)
plt.title('Histograma do Tempo de Execução')
plt.ylabel('Frequência')
plt.xlabel('Segundos')
plt.legend()
plt.grid()
plt.show()

from scipy.stats import norm
# Considerando a confiança de 99%
intervalo = norm.interval(alpha = 0.99, loc = amostra_media, scale = amostra_std)

# Commented out IPython magic to ensure Python compatibility.
print('Com uma média de execução %.4f segundos, oscilando entre %.4f e %.4f segundos, com a certeza de 99%c'\
#         % (amostra_media, intervalo[0], intervalo[1], '%'))

# Visualizando a disperção de Pontos da Amostra
plt.figure(figsize=(10,7))
plt.scatter([i for i in range(qtd_amost)], amostra, marker='.')
plt.hlines(y=intervalo[0], xmin=0, xmax=qtd_amost, color='red', linestyles='dashed')
plt.hlines(y=intervalo[1], xmin=0, xmax=qtd_amost, color='red', linestyles='dashed')
plt.hlines(y=amostra_media, xmin=0, xmax=qtd_amost, color='black', linestyles='dashed')
plt.title('Gráfico de Disperção de pontos da amostra')
plt.legend()
plt.grid()
plt.show()

