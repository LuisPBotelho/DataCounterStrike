# CS Season Dashboard

Dashboard desktop em **PyQt6** para analisar o desempenho de uma season de
Counter-Strike a partir de uma planilha Excel pessoal: vitórias por mapa,
por amigo, por combinação de amigos (lineup), médias de kills/KDR, e um
histórico completo de partidas — tudo filtrável e atualizado em tempo real.

A interface foi inspirada em um protótipo HTML/CSS/JS (`cs2_season4_dashboard_02.html`)
construído como referência visual, e depois recriada como aplicativo
desktop nativo para Windows (executável standalone, sem precisar instalar Python).

![Visão geral](screenshots/overview.png)
![Filtro de lineup](screenshots/lineup_filter.png)

---

## Sumário

- [Funcionalidades](#funcionalidades)
- [Stack técnica](#stack-técnica)
- [Arquitetura](#arquitetura)
- [Formato esperado da planilha](#formato-esperado-da-planilha)
- [Como rodar](#como-rodar)
- [Paleta de cores](#paleta-de-cores)
- [Histórico de desenvolvimento e raciocínio](#histórico-de-desenvolvimento-e-raciocínio)
- [Bugs encontrados e como foram resolvidos](#bugs-encontrados-e-como-foram-resolvidos)
- [Limitações conhecidas / próximos passos](#limitações-conhecidas--próximos-passos)

---

## Funcionalidades

### Filtros (sidebar, combináveis entre si)

- **Resultado** — pills `Todos / W / L / D`.
- **Mapa** — chips de seleção múltipla (mostra só os mapas presentes na planilha).
- **Lineup** — o foco do projeto. Permite filtrar partidas pela combinação de
  amigos com quem você jogou, em três modos:
  - **Inclui** (`any`): partidas em que **pelo menos um** dos amigos selecionados jogou.
  - **Todos** (`all`): partidas em que **todos** os amigos selecionados jogaram (pode ter mais gente além deles).
  - **Exata** (`exact`): partidas cuja lineup é **exatamente** o conjunto de amigos selecionado — nem a mais, nem a menos.
  - Lista de amigos com contagem de partidas ao lado de cada nome.
  - Checkbox **"Somente solo"** isola partidas jogadas sem nenhum amigo.
- **Busca livre** — filtra por mapa ou placar na tabela.
- **Limpar filtros** — reseta tudo de uma vez.

Qualquer combinação de filtros recalcula instantaneamente KPIs, gráficos e tabela.

### Painel principal

- **KPIs**: total de partidas, win rate, KDR médio, PTS médio, posição (place) média — todos recalculados sobre o conjunto filtrado.
- **Win rate por mapa**: um card por mapa com barra empilhada W/D/L e contagens.
- **Desempenho por amigo**: gráfico de barras horizontal com win rate % por amigo (top 10), colorido por faixa de desempenho.
- **KDR médio por mapa**: gráfico de barras horizontal, cor da barra = cor do mapa, cor do texto = faixa de desempenho (verde/laranja/vermelho).
- **Histórico de partidas**: tabela com #, Mapa, Placar, Resultado, K, D, A, KDR, PTS, Place e os "chips" da lineup daquela partida. Colunas ordenáveis clicando no cabeçalho (com indicador de direção), busca por texto, contador de partidas exibidas.

### Detecção dinâmica de colunas

Os "amigos" não são uma lista fixa no código: o programa lê o cabeçalho da
planilha e trata como amigo qualquer coluna entre `Amigos` e a primeira coluna
vazia/`Unnamed`. **Isso significa que adicionar um amigo novo na planilha não
exige nenhuma alteração no código** — basta criar a coluna com `1`/`0` por
partida que ela aparece automaticamente no próximo carregamento. Validado com
um teste automatizado que injeta uma coluna fictícia e confirma a detecção.

### Auto-atualização ao salvar

O dashboard observa o arquivo carregado (polling de `mtime`/tamanho a cada
~1s) e, quando detecta que ele foi salvo (ex.: você editou no Excel e
adicionou uma partida ou amigo novo), espera o arquivo estabilizar e recarrega
os dados **sozinho**, sem precisar reabrir o diálogo de arquivo — e mantendo
os filtros, busca e ordenação que você tinha ativos no momento. Veja a seção
de bugs abaixo para o porquê de não usar `QFileSystemWatcher`.

---

## Stack técnica

| Camada | Tecnologia | Por quê |
|---|---|---|
| Linguagem | Python 3.14 | já era o ambiente disponível na máquina |
| UI | **PyQt6** (`QtWidgets`, `QtCore`, `QtGui`) | pedido explícito do usuário, no lugar da versão inicial em Tkinter |
| Estilo | QSS (Qt Style Sheets) | replica 1:1 a paleta de cores e os estados (`:checked`, `:hover`) do protótipo HTML/CSS |
| Dados | `pandas` + `openpyxl` | leitura de `.xlsx`, manipulação tabular |
| Empacotamento | `PyInstaller` (`--onefile --windowed`) | gera um `.exe` standalone, sem exigir Python instalado na máquina do usuário |
| Testes | scripts ad-hoc com `QApplication` headless + `QWidget.grab()` | ver seção de testes abaixo |

Não há framework de teste formal (pytest etc.) — os testes foram scripts
Python descartáveis usados durante o desenvolvimento para validar pipeline de
dados, interações de UI e o bug de auto-atualização (mantidos como referência
de processo, não como suíte de testes do repositório).

---

## Arquitetura

```
cs_data.py            # camada de dados, sem nenhuma dependência de UI
├─ fix_mojibake()      # corrige texto corrompido em encoding (defensivo)
├─ load_season_data()  # le o .xlsx, resolve colunas, monta lista de Match
├─ Match                # 1 partida: mapa, placar, K/D/A, KDR, PTS, place, lineup[]
├─ SeasonData           # dataframe limpo + colunas resolvidas + lista de Match
├─ filter_matches()     # aplica os filtros (resultado/mapa/lineup/solo/busca)
└─ winrate_by_map() / winrate_by_friend() / kdr_by_map() / top_lineups()

cs_dashboard_qt.py     # toda a UI (PyQt6), consome cs_data.py
├─ QSS                  # stylesheet com a paleta de cores
├─ make_kpi_card() / make_bar_row() / make_map_wr_card()  # widgets reutilizáveis
└─ MainWindow
   ├─ _build_real_sidebar()   # pills, chips, modos de lineup, lista de amigos
   ├─ _build_real_main()      # KPIs, win rate por mapa, gráficos, tabela
   ├─ get_filtered()          # le o estado atual e delega para cs_data.filter_matches
   ├─ render_*()              # repintam cada seção a partir dos dados filtrados
   └─ auto-atualização: _poll_file_changed() → _reload_current_file() → _apply_loaded_data()
```

A separação entre `cs_data.py` (puro, testável sem abrir uma janela) e
`cs_dashboard_qt.py` (UI) foi deliberada: permitiu testar toda a lógica de
filtro/agregação rodando scripts simples no terminal, sem precisar instanciar
Qt, antes mesmo da interface existir.

---

## Formato esperado da planilha

Uma aba contendo (nomes de coluna, com ou sem o cabeçalho corrompido — veja
"mojibake" abaixo):

| Coluna | Obrigatória | Descrição |
|---|---|---|
| `Mapa` | sim | nome do mapa jogado |
| `Resultado` | sim | `W` / `L` / `D` |
| `K`, `D`, `A` | sim | kills, deaths, assists |
| `Amigos` | sim | quantidade de amigos naquela partida (apenas usada para achar onde o bloco de amigos começa) |
| `Placar`, `KDR`, `PTS`, `Place (PTS)` | opcional | usadas se existirem; o app calcula fallback (ex.: KDR = K/D) quando ausentes |
| *(bloco de colunas após `Amigos`)* | sim, pelo menos uma | uma coluna por amigo, valor `1` se ele jogou aquela partida, `0` (ou vazio) se não |

Linhas sem `Resultado` válido (ex.: uma linha de "Total" no rodapé da
planilha) são ignoradas automaticamente.

---

## Como rodar

### Executável pronto

```
dist\CS_Season_Dashboard.exe
```

Abre pedindo o arquivo `.xlsx`. Pode também passar o caminho como argumento
(`CS_Season_Dashboard.exe "C:\caminho\Season 4 CS.xlsx"`) para pular o diálogo.

### A partir do código-fonte

```powershell
python -m pip install PyQt6 pandas openpyxl
python cs_dashboard_qt.py
```

### Gerar o executável novamente

```powershell
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --name "CS_Season_Dashboard" "cs_dashboard_qt.py"
```

O `.exe` fica em `dist/CS_Season_Dashboard.exe` (~70 MB — ver nota sobre
`matplotlib` em [Limitações](#limitações-conhecidas--próximos-passos)).

---

## Paleta de cores

Extraída do protótipo HTML de referência e aplicada via QSS:

| Token | Cor | Uso |
|---|---|---|
| `bg` | `#0e0f11` | fundo da janela |
| `surface` / `surface2` / `surface3` | `#15171a` / `#1c1f23` / `#22262c` | painéis, cards, inputs, em camadas crescentes de contraste |
| `border` / `border2` | `#2a2e35` / `#343a44` | bordas sutis e bordas de hover |
| `orange` | `#f5a623` | cor de marca: itens ativos/selecionados, botão de carregar planilha |
| `green` | `#4caf82` | vitórias, desempenho bom |
| `red` | `#e05252` | derrotas, desempenho ruim |
| `blue` | `#5ca4e0` | empates |
| `yellow` | `#f5c842` | destaque de 1º lugar (place) |
| `text` / `text_dim` / `text_muted` | `#d6dae2` / `#7a8494` / `#4a5260` | hierarquia de texto |

Cada mapa também tem uma cor decorativa fixa (`MAP_COLORS` em
`cs_dashboard_qt.py`) usada nas barras do gráfico de KDR e na faixa lateral
das células da coluna "Mapa" na tabela.

---

## Histórico de desenvolvimento e raciocínio

### 1. Exploração inicial da planilha

A planilha tem duas abas: `Planilha1` (uma tabela dinâmica/pivot antiga,
resíduo do Excel, sem uso) e `Season 4` (os dados reais — 224 partidas no
momento da análise). As colunas seguem o padrão: `Match nº, Mapa, Placar,
Resultado, K, D, A, PTS, KDR, Place (PTS), Amigos`, seguidas por ~20 colunas
binárias (uma por amigo) e, por fim, colunas `Unnamed` que são lixo deixado
por uma tabela dinâmica anterior do Excel — precisaram ser explicitamente
ignoradas na detecção do bloco de amigos.

Também havia uma linha de "Total" no rodapé (soma de tudo) que é descartada
automaticamente por não ter `Resultado` em `{W, L, D}`.

### 2. Versão 1: Tkinter (descartada)

A primeira versão foi construída em **Tkinter + matplotlib**, com 5 abas
(Visão geral, Mapas, Amigos, Lineups, Kills). Funcionava, mas o usuário pediu
mais interatividade e mostrou um protótipo HTML com sidebar de filtros, modos
de lineup (`any/all/exact`) e tabela ordenável — pedindo a reconstrução em
**PyQt6**. O código Tkinter e seu `.exe` foram removidos do projeto.

### 3. Versão 2: PyQt6 a partir do protótipo HTML

O HTML de referência (`cs2_season4_dashboard_02.html`) já continha toda a
lógica de filtro em JavaScript (pills, chips, modos de lineup, ordenação de
tabela) e as variáveis CSS de cor. Em vez de reinventar a UX, o trabalho foi
**traduzir** essa lógica para Python/Qt:

- O array `RAW` de partidas em JS virou a lista de objetos `Match` em
  `cs_data.py`.
- A função `getFiltered()` do JS virou `cs_data.filter_matches()`.
- Os elementos `.pill`, `.chip`, `.friend-tag` (`<div>` com `onclick`) viraram
  `QPushButton` com `setCheckable(True)` e estilização via seletor QSS
  `:checked` — incluindo seletores por propriedade dinâmica
  (`QPushButton[resultKind="W"]:checked`) para dar a cada pill de resultado
  sua própria cor quando ativa.
- As mini barras de progresso em CSS (`width: %`) viraram `QHBoxLayout` com
  **stretch factors proporcionais ao valor** (ex.: `addWidget(fill, stretch=valor)`
  + `addWidget(spacer, stretch=máximo-valor)`), o que dá barras proporcionais
  sem nenhum cálculo manual de pixel e que se redimensionam corretamente.
- A tabela usa ordenação **manual em Python** (não a ordenação nativa do
  `QTableWidget`), espelhando a função `sortBy()` do JS — necessário porque
  várias colunas usam `QLabel` como cell widget (chips de mapa, badge de
  resultado, chips de lineup), e o sort nativo do Qt ignora widgets de célula.

### 4. Testes sem ambiente gráfico interativo

Como o agente não tem acesso visual direto ao desktop em tempo real, todo o
desenvolvimento foi validado por scripts automatizados:

- **Pipeline de dados**: scripts chamando `cs_data.load_season_data()` e
  comparando contagens/agregados manualmente.
- **Interações de UI**: scripts que instanciam `QApplication` + `MainWindow`,
  chamam métodos como `toggle_friend()`, `set_mode()`, `reset_all()` e
  verificam o texto do contador de partidas (`count_label`) e o estado dos
  botões depois de cada ação.
- **Verificação visual**: inicialmente via screenshot de tela (`System.Drawing`
  + `CopyFromScreen` no PowerShell), mas o ambiente tem **dois monitores** e a
  janela às vezes abria no monitor secundário (coordenadas negativas) ou atrás
  de outras janelas, retornando capturas em branco ou de outra aplicação.
  A solução definitiva foi usar `QWidget.grab()` — que renderiza a árvore de
  widgets diretamente para um `QPixmap`/PNG, **sem depender de captura de
  tela física, foco de janela ou monitor** — muito mais confiável.

### 5. Pedido de auto-atualização

Depois de pronto, o usuário perguntou se o dashboard se atualizava sozinho ao
editar a planilha. Resposta: não — a leitura era feita uma única vez no
carregamento. Implementação subsequente: ver seção de bugs abaixo, porque essa
funcionalidade expôs o bug mais sério do projeto.

---

## Bugs encontrados e como foram resolvidos

### 1. Aparente corrupção de encoding nos cabeçalhos ("mojibake")

**Sintoma**: ao inspecionar a planilha via PowerShell, cabeçalhos como
`Match nº` apareciam como `Match nÂº`, e o nome de um amigo como `JÃO`
aparecia como `JÃƒO`.

**Investigação**: a hipótese inicial foi que o arquivo `.xlsx` continha texto
salvo com encoding trocado (UTF-8 interpretado como CP1252 em algum ponto da
edição). Foi implementada uma função `fix_mojibake()` (`encode('cp1252').decode('utf-8')`)
para reverter esse tipo de corrupção.

**Causa real**: comparando a leitura via `openpyxl` direto (com
`repr()` salvo em arquivo UTF-8) contra a saída do `Get-Content`/`type` do
PowerShell **sem** especificar `-Encoding utf8`, ficou claro que o problema
era **só de exibição no console** — o `Get-Content` padrão do PowerShell usa
o code page do sistema, não UTF-8, e estava desenhando mal os caracteres
acentuados na tela. Os dados reais no `.xlsx` já estavam corretos
(`Match nº`, `JÃO`).

**Decisão**: a função `fix_mojibake()` foi mantida no código como rede de
segurança (ela é um no-op seguro para strings já corretas — o `try/except`
absorve a falha do round-trip), mas o bug em si nunca existiu nos dados.

### 2. `sys.stdout`/`sys.stderr` viram `None` em build `--windowed`

**Sintoma**: o `.exe` gerado com `--windowed` (sem console) abria a janela e
fechava sozinho silenciosamente segundos depois, sem nenhum erro visível.

**Causa**: builds do PyInstaller sem console deixam `sys.stdout` e
`sys.stderr` como `None`. Qualquer biblioteca que tente escrever um aviso
neles (matplotlib, numpy, pandas costumam fazer isso em alguns caminhos de
código) lança `AttributeError: 'NoneType' object has no attribute 'write'`,
não capturado, derrubando o processo.

**Correção**: no topo do script, antes de qualquer outro import:

```python
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")
```

Confirmado comparando uma build de debug (com console, que mostrava o app
funcionando normalmente) contra a build `--windowed` (que morria) — a
diferença era exatamente a presença do console.

### 3. Widgets "fantasmas" ao trocar de filtro

**Sintoma**: em um teste com `grab()`, ao trocar de filtro (ex.: ativar
"Todos" no modo de lineup), uma linha do gráfico anterior (`DUST II`)
continuava parcialmente visível, sobreposta à nova renderização.

**Causa**: a função `clear_layout()` removia os widgets do layout
(`layout.takeAt(0)`) e chamava `widget.deleteLater()` — mas `deleteLater()`
só agenda a destruição do objeto C++ para o **próximo ciclo do event loop**.
Entre a remoção do layout e essa destruição efetiva, o widget continuava
sendo um filho visível da janela, "flutuando" na última posição em que
estava.

**Correção**: chamar `widget.hide()` e `widget.setParent(None)` **antes** de
`deleteLater()`, garantindo remoção visual imediata independentemente de
quando a destruição de fato acontece.

### 4. Cor errada no gráfico "KDR médio por mapa"

**Sintoma**: o texto do valor de KDR em cada barra usava a cor decorativa do
mapa (ex.: vermelho-alaranjado do Inferno) em vez da cor de
performance (verde/laranja/vermelho conforme o valor do KDR), ao contrário do
protótipo HTML original, que usa cores diferentes para a barra e para o texto.

**Causa**: a função reutilizável `make_bar_row()` só aceitava um parâmetro de
cor, usado tanto para a barra quanto para o texto — perdendo a distinção que
o HTML fazia (`mapCol` na barra, `color` baseado no KDR no texto).

**Correção**: `make_bar_row()` ganhou um parâmetro `text_color` opcional,
permitindo cor de barra e cor de texto independentes. Validado amostrando
pixels exatos do PNG gerado por `grab()` (`Bitmap.GetPixel()`) para confirmar
que o RGB do texto batia exatamente com a cor verde esperada (`#4caf82` →
`76,175,130`) nos casos de KDR alto.

### 5. Crash nativo (`STATUS_STACK_BUFFER_OVERRUN`) na auto-atualização

O bug mais difícil de diagnosticar do projeto.

**Sintoma**: ao implementar a auto-atualização com `QFileSystemWatcher`, o
processo morria com `exit code -1073740791` (`0xC0000409`,
`STATUS_STACK_BUFFER_OVERRUN`) assim que o arquivo monitorado era apagado e
recriado — exatamente o padrão de gravação do Excel/OneDrive (apaga o
original, escreve um temporário, renomeia).

**Investigação, passo a passo**:
1. Trocar `QFileSystemWatcher` por **polling manual** (comparando `mtime`/
   tamanho do arquivo a cada segundo) para eliminar a API de watch nativa do
   SO como suspeita — **o crash persistiu**, descartando o
   `QFileSystemWatcher` como causa raiz.
2. Isolar o `os.remove()` do arquivo, chamado de dentro do loop de eventos do
   Qt via `QTimer` — **crashava** mesmo sem nenhum código de "watch" envolvido.
3. Reproduzir a mesma sequência (`load_season_data()` seguido de
   `os.remove()`) **sem Qt**, em um script Python puro — e aí o resultado foi
   um `PermissionError: [WinError 32] O arquivo já está sendo usado por outro
   processo`, **tratável e sem crash**.

Esse contraste (erro limpo sem Qt vs. crash nativo com Qt) revelou a causa
raiz: `pd.ExcelFile(filepath)`, usado dentro de `load_season_data()`, **nunca
era fechado** — o handle do arquivo ficava aberto indefinidamente no
processo. Tentar apagar um arquivo com handle aberto no Windows normalmente
gera só um erro de violação de compartilhamento; mas, combinado com o
gerenciamento de exceções nativo do Qt/PyQt6 rodando em outra thread/contexto
do event loop, esse erro de baixo nível acabava virando um *stack buffer
overrun* não recuperável em vez de uma exceção Python normal.

**Correção**:

```python
# antes
xls = pd.ExcelFile(filepath)
sheet = _find_sheet(xls)
df = pd.read_excel(xls, sheet_name=sheet)

# depois
with pd.ExcelFile(filepath) as xls:
    sheet = _find_sheet(xls)
    df = pd.read_excel(xls, sheet_name=sheet)
```

Com o handle sempre fechado ao final da função, o arquivo pode ser
apagado/sobrescrito livremente por outro processo (Excel, OneDrive) mesmo com
o dashboard aberto. Validado com um teste que simula a gravação do Excel
(`os.remove()` seguido de `shutil.copy()` de uma versão com uma partida a
mais) rodando dentro do loop de eventos do Qt: o app detecta a mudança,
recarrega os dados, atualiza a contagem de partidas e **mantém o filtro que
estava ativo** — sem crash.

**Lição**: um vazamento de recurso (handle de arquivo) que parecia inofensivo
isoladamente (o processo nunca precisava reabrir o arquivo durante o uso
normal) só se tornou um problema visível quando uma nova funcionalidade
(auto-atualização) passou a depender de outro processo conseguir
escrever/apagar o mesmo arquivo — e o sintoma observado (crash nativo) era
enganosamente distante da causa real (um `with` ausente).

---

## Limitações conhecidas / próximos passos

- O `.exe` empacota `matplotlib` mesmo sem nenhum uso direto dele no código —
  o hook do PyInstaller para `pandas` o inclui especulativamente, inflando o
  binário (~70 MB). Pode ser reduzido com `--exclude-module matplotlib` no
  comando de build.
- Não há suíte de testes automatizada no repositório (os scripts usados
  durante o desenvolvimento foram descartáveis, fora da árvore do projeto).
- A auto-atualização usa polling (intervalo de 1s) em vez de notificação
  nativa do SO — escolha deliberada por estabilidade (ver bug #5), com o
  custo de até ~1-2s de atraso para detectar uma gravação.
- Testado apenas no Windows (PyInstaller `--windowed` e os caminhos de
  arquivo assumem esse ambiente).
