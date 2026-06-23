# Análise da Season 4 — Insights e Conclusões

Documento de análise sobre os **229 partidas** registradas na planilha `Season
4 CS.xlsx`, gerado a partir dos dados processados pelo CS Season Dashboard.
O objetivo aqui não é repetir números (isso o dashboard já mostra ao vivo),
mas **interpretar os padrões** que aparecem nos dados e apontar conclusões
acionáveis.

> Onde a amostra é pequena (poucos jogos com um amigo ou lineup específico),
> isso é sinalizado explicitamente — número pequeno de partidas gera
> percentuais instáveis e não deve ser lido como verdade estatística.

---

## TL;DR — principais conclusões

1. **Win rate geral de 50.2%** (115W-105L-9D) — uma season equilibrada, sem
   tendência clara de domínio.
2. **Inferno é seu pior mapa em win rate (37%) mas seu melhor em KDR (1.33)**
   — você joga *bem individualmente* nesse mapa, mas o time perde. Isso é o
   sinal mais forte de um problema tático/de equipe, não mecânico.
3. **Jogar sozinho (58.8% WR) supera qualquer combinação de 1 ou 2 amigos** —
   o "vale" de performance está especificamente nas duplas, não na solidão.
4. **A dupla HAMMER + LEO tem 35% WR (pior lineup recorrente)**, mas o trio
   HAMMER + LEO + PILOTO WILLY sobe pra 53% e LEO + PILOTO WILLY (sem HAMMER)
   chega a 60%. O denominador comum de queda de performance é especificamente
   essa dupla.
5. **Seu KDR vem caindo ao longo da season (1.49 → ~1.00) mas o win rate se
   manteve estável (~50-52%)** — você está fazendo menos frags por morte,
   porém ganhando na mesma proporção. Indício de adversários mais fortes ou
   mudança de estilo de jogo (mais suporte/objetivo, menos frags).
6. **KDR não é destino**: 25% das vitórias aconteceram com KDR < 1.0, e 32%
   das derrotas aconteceram com KDR ≥ 1.0. O resultado da partida depende mais
   do time do que do seu desempenho individual isolado.

---

## 1. Visão geral

| Métrica | Valor |
|---|---|
| Partidas | 229 |
| Vitórias / Derrotas / Empates | 115 / 105 / 9 |
| Win rate geral | **50.2%** |
| K médio | 16.5 |
| D médio | 15.5 |
| A médio | 4.7 |
| KDR médio | 1.23 |
| PTS médio | 43.1 |
| Posição (place) média | 2.54 |
| % de partidas em 1º lugar | 29.7% |
| % de partidas em último lugar | 13.1% |

Quase metade das partidas terminam com você no 1º ou 2º lugar do placar
(somando 1º e 2º, isso passa de 50%) — ou seja, individualmente você está
acima da média do próprio time na maioria das partidas, independente do
resultado final.

---

## 2. Análise por mapa

| Mapa | Partidas | Win Rate | KDR médio |
|---|---|---|---|
| DUST II | 18 | **61%** | 1.22 |
| ANUBIS | 17 | **59%** | 1.15 |
| NUKE | 33 | 58% | 1.24 |
| MIRAGE | 74 | 53% | 1.15 |
| OVERPASS | 31 | 48% | 1.31 |
| ANCIENT | 13 | 38% | 1.31 |
| **INFERNO** | 43 | **37%** | **1.33** |

### O paradoxo do Inferno

Inferno é o mapa com **mais volume** depois de Mirage (43 partidas — amostra
grande, não é ruído) e tem o **melhor KDR da season (1.33)** — mas é também o
**pior mapa em win rate (37%)**, com 0 empates em 43 jogos (ou ganha, ou
perde "seco"). Esse descolamento entre "joguei bem individualmente" e "o time
perdeu" é o achado mais acionável da análise: o problema em Inferno não
parece ser mecânica/mira, e sim execução de round (economia, controle de
área, takes), porque seus números pessoais ali são bons.

Vale comparar com **Ancient**, o segundo pior em WR (38%) mas também com KDR
alto (1.31) — o mesmo padrão se repete em menor escala (13 partidas, amostra
mais limitada).

### Os bons mapas

Dust II e Anubis lideram em win rate (61% e 59%), mas têm amostra menor (18 e
17 partidas) — direção positiva clara, mas vale acompanhar se o percentual se
mantém com mais jogos. Nuke (33 partidas, 58% WR) é o mapa "bom" com volume
mais confiável.

---

## 3. Resultado x Desempenho individual (K/D/A/KDR)

| Resultado | n | K médio | D médio | KDR médio | PTS médio |
|---|---|---|---|---|---|
| Vitória (W) | 115 | 17.7 | 13.4 | **1.59** | 46.2 |
| Derrota (L) | 105 | 14.4 | 17.2 | **0.84** | 37.7 |
| Empate (D) | 9 | 25.7 | 21.7 | 1.20 | 66.3 |

Padrão esperado (vitórias têm KDR quase o dobro das derrotas), mas o dado que
chama atenção são os **empates**: K e D médios disparam (25.7/21.7, bem acima
da média geral de 16.5/15.5). Empates nesta planilha (placares como 15x15)
são partidas que foram a *overtime* — jogos mais longos, mais trocas, mais
frags para os dois lados. Confirma que os 9 empates da season foram, em
geral, os jogos mais "disputados/épicos" estatisticamente.

---

## 4. Análise por amigo

| Amigo | Partidas | Win Rate | K médio | KDR médio |
|---|---|---|---|---|
| **JÃO** | 19 | **63%** | 16.3 | 1.49 |
| LEO | 127 | 54% | 17.3 | 1.20 |
| PILOTO WILLY | 101 | 53% | 17.0 | 1.17 |
| NOT | 53 | 53% | 15.2 | 1.01 |
| ERROR | 21 | 52% | 16.6 | 1.08 |
| LAKES | 74 | 49% | 15.4 | 1.13 |
| **HAMMER** | 114 | **44%** | 17.1 | 1.30 |

*(amigos com menos de 10 partidas omitidos da tabela por amostra
insuficiente — GABEN, ARAGON, MANZA etc. têm 4-7 jogos cada e variam de 0% a
67% de WR, o que é esperado estatisticamente com tão poucos dados e não deve
ser interpretado como sinal real.)*

### O caso HAMMER

HAMMER é o **segundo parceiro mais frequente** (114 partidas, atrás só de
LEO) e tem de longe o **pior win rate entre os parceiros com amostra
grande (44%)** — apesar de ter um KDR pessoal dele bom (1.30, segundo melhor
do grupo). Ou seja: não é um problema de "HAMMER joga mal", é um problema de
**resultado de time quando ele está presente**. Isso conecta diretamente com
o achado da seção de lineups abaixo.

### JÃO é seu melhor parceiro com amostra relevante

63% de WR em 19 partidas — menor volume que os outros do topo, mas
consistente o suficiente para não ser só ruído, e o KDR junto dele (1.49)
também é o segundo mais alto entre todos os amigos. Vale jogar mais com ele
para confirmar se o número se mantém.

---

## 5. Lineups: o efeito da combinação, não da pessoa isolada

Esta é a análise mais importante para responder "com quem eu devo jogar".

| Lineup | Partidas | Win Rate |
|---|---|---|
| LEO + PILOTO WILLY | 15 | **60%** |
| HAMMER + LAKES + LEO + PILOTO WILLY (squad completo) | 9 | **67%** |
| LAKES + NOT | 8 | 62% |
| Sozinho (sem amigos) | 17 | **59%** |
| HAMMER + LEO + PILOTO WILLY + VAQUEIRO | 7 | 57% |
| HAMMER + LEO + PILOTO WILLY (trio) | 19 | 53% |
| LAKES (sozinho entre os amigos, sem os outros) | 17 | 47% |
| **HAMMER + LEO (dupla)** | 17 | **35%** |
| NOT (sozinho entre os amigos) | 10 | 30% |

### A dupla HAMMER + LEO é o ponto fraco específico

O dado mais claro de toda a análise: **HAMMER + LEO como dupla isolada tem
35% de WR em 17 partidas** — pior que jogar sozinho. Mas observe a progressão:

- HAMMER + LEO (dupla): **35%**
- HAMMER + LEO + PILOTO WILLY (trio): **53%**
- LEO + PILOTO WILLY (sem HAMMER): **60%**
- HAMMER + LAKES + LEO + PILOTO WILLY (squad completo): **67%**

Adicionar PILOTO WILLY à dupla HAMMER+LEO recupera quase 20 pontos
percentuais de win rate, e tirar HAMMER da equação (ficando só LEO + PILOTO
WILLY) é ainda melhor. Isso sugere fortemente que **a dupla HAMMER+LEO sem um
terceiro elemento tem algum problema de composição/comunicação/coordenação**
que desaparece assim que o grupo cresce — não é "HAMMER é ruim" nem "LEO é
ruim" isoladamente (LEO tem 54% de WR geral, o segundo melhor do grupo), é
especificamente **a combinação dos dois sozinhos**.

### Solo bate a maioria das combinações pequenas

Jogar sozinho (sem nenhum amigo) tem 58.8% de WR — atrás apenas do squad
completo e de combinações de 3 pessoas bem-sucedidas. Cruzando com a tabela
de "número de amigos" (seção 6), fica claro que o problema não é "jogar
acompanhado em geral", e sim **duplas específicas mal combinadas**
arrastando a média de "1-2 amigos" para baixo.

---

## 6. Tamanho do grupo (quantos amigos por partida)

| Tamanho do grupo | Partidas | Win Rate | KDR médio |
|---|---|---|---|
| Solo (0 amigos) | 17 | **58.8%** | 1.16 |
| 1 amigo | 43 | 48.8% | 1.25 |
| 2 amigos | 56 | **46.4%** | 1.37 |
| 3 amigos | 53 | 52.8% | 1.08 |
| 4+ amigos (squad) | 60 | 50.0% | 1.25 |

Formato em "U": o win rate **cai** ao entrar em dupla/trio de amigos (1-2
amigos: 46-49%) e **recupera** a partir de 3 (52.8%) — mas o KDR pessoal
segue o caminho oposto, subindo justamente quando o grupo é pequeno (2
amigos: KDR 1.37, o mais alto da tabela). Em grupos de 2, você
individualmente joga muito bem (mais frags), mas o time perde mais — outro
sinal de que o gargalo está em coordenação de squad pequeno, não em
mecânica.

---

## 7. Evolução ao longo da season

| Bloco de partidas | Win Rate | K médio | KDR médio |
|---|---|---|---|
| 1–50 | 52.0% | 17.4 | **1.49** |
| 51–100 | 44.0% | 17.9 | 1.34 |
| 101–150 | 52.0% | 15.8 | 1.08 |
| 151–200 | 52.0% | 16.2 | 1.15 |
| 201–229 | 51.7% | 14.3 | **1.00** |

Dois movimentos acontecendo ao mesmo tempo:

- **Win rate**: caiu no segundo bloco (44%) e se estabilizou em ~52% desde
  então — não há tendência de queda ou alta consistente no resultado final.
- **KDR**: cai de forma quase monotônica, de 1.49 no começo da season para
  1.00 no bloco mais recente — uma queda de praticamente 33% no desempenho
  individual médio.

A combinação dessas duas curvas — **win rate estável + KDR em queda** — é o
padrão mais interessante do dataset inteiro: você está fazendo
proporcionalmente menos frags por morte ao longo da season, mas isso não está
custando vitórias. As hipóteses mais prováveis (não verificáveis só com estes
dados, mas valem investigar): (a) o nível dos adversários subiu (rank
mais alto = trocas mais difíceis), (b) mudança de papel dentro do time
(menos entry-fragging, mais jogo de objetivo/suporte que gera menos kills mas
mais rounds), ou (c) simples regressão à média depois de um início de season
estatisticamente "quente" (KDR 1.49 é bem acima da média geral de 1.23).

---

## 8. Sequências (streaks)

- Maior sequência de vitórias seguidas: **7**
- Maior sequência de derrotas seguidas: **6**
- Sequências de 3+ vitórias seguidas: 16 ocorrências
- Sequências de 3+ derrotas seguidas: 14 ocorrências

Volume parecido de sequências boas e ruins (16 vs 14) é mais um indício de
season equilibrada, sem "tilt" prolongado nem fase de domínio absoluto — a
variância do jogo em si parece ser o fator dominante, mais do que uma fase
de forma muito melhor ou pior.

---

## 9. KDR não determina o resultado

- **25.2% das vitórias (29 de 115)** aconteceram com KDR individual **abaixo
  de 1.0** — ou seja, em 1 a cada 4 vitórias, você morreu mais do que matou,
  mas o time ganhou mesmo assim.
- **32.4% das derrotas (34 de 105)** aconteceram com KDR individual **acima
  de 1.0** — em quase 1 a cada 3 derrotas, você teve um saldo de
  kills/deaths positivo e ainda assim o time perdeu.

Isso reforça numericamente o que as seções de mapa e lineup já sugeriam:
**o resultado da partida está mais associado à dinâmica do time do que ao seu
desempenho individual isolado.** Em CS, isso normalmente aponta para fatores
fora do K/D puro — economia de round, posicionamento de equipe, comunicação,
e a "química" específica de quem está jogando junto (como mostrado na seção 5).

---

## 10. Recomendações práticas

1. **Revisar a tática em Inferno.** Seus números pessoais lá são os melhores
   da season — o problema não é mira, é round/equipe. Vale assistir replay de
   2-3 derrotas em Inferno especificamente.
2. **Evitar a dupla HAMMER+LEO isolada** (ou, se for jogar com os dois, puxar
   um terceiro — PILOTO WILLY já comprovadamente resolve o problema, subindo
   de 35% para 53-60% de WR).
3. **Priorizar LEO + PILOTO WILLY** (com ou sem o squad completo) como
   parceria-base — é a combinação com melhor retorno consistente e amostra
   relevante (15 partidas a 60%, sobe pra 67% com o squad completo).
4. **JÃO vale mais jogo** — melhor WR entre os amigos com amostra
   razoável (63% em 19 partidas), mas ainda é pouco dado pra ter certeza.
5. **Acompanhar a queda de KDR** nos próximos blocos de partidas — se o win
   rate começar a cair também, é sinal de que a queda de desempenho
   individual deixou de ser compensada pelo time.

---

*Documento gerado a partir dos dados de `Season 4 CS.xlsx` processados pelo
CS Season Dashboard (`cs_data.py`). Os números podem ser conferidos
interativamente filtrando o próprio dashboard pelos mesmos mapas/amigos/lineups
citados aqui.*
