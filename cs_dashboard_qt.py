"""
CS Season Dashboard - PyQt6
Interface inspirada em cs2_season4_dashboard_02.html: sidebar de filtros
(resultado, mapa, lineup any/all/exato, solo) + KPIs + win rate por mapa +
graficos de barra + tabela de partidas ordenavel/pesquisavel.
"""

import sys
import os

if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QScrollArea, QFrame, QLineEdit, QCheckBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox, QSizePolicy,
    QButtonGroup, QAbstractItemView,
)

import cs_data as cd

# ==========================================================================
# Paleta (igual ao cs2_season4_dashboard_02.html)
# ==========================================================================
P = {
    "bg": "#0e0f11",
    "surface": "#15171a",
    "surface2": "#1c1f23",
    "surface3": "#22262c",
    "border": "#2a2e35",
    "border2": "#343a44",
    "orange": "#f5a623",
    "orange_d": "#c07d0f",
    "orange_glow": "rgba(245,166,35,40)",
    "green": "#4caf82",
    "red": "#e05252",
    "blue": "#5ca4e0",
    "yellow": "#f5c842",
    "text": "#d6dae2",
    "text_dim": "#7a8494",
    "text_muted": "#4a5260",
}

RESULT_COLOR = {"W": P["green"], "L": P["red"], "D": P["blue"], "ALL": P["orange"]}
MAP_COLORS = {
    "INFERNO": "#e06030", "MIRAGE": "#5ca4e0", "NUKE": "#4caf82",
    "OVERPASS": "#f5a623", "DUST II": "#a07850", "ANUBIS": "#b070d0", "ANCIENT": "#60b0c0",
}

QSS = f"""
QMainWindow, QWidget {{ background: {P['bg']}; color: {P['text']}; font-family: 'Segoe UI'; font-size: 13px; }}

#TopBar {{ background: {P['surface']}; border-bottom: 1px solid {P['border']}; }}
#TopLogo {{ color: {P['orange']}; font-size: 16px; font-weight: 700; letter-spacing: 2px; }}
#TopTitle {{ color: {P['text_dim']}; font-size: 13px; letter-spacing: 1px; }}
#TotalBadge {{ background: {P['surface3']}; border: 1px solid {P['border']}; border-radius: 4px; padding: 4px 10px; color: {P['text_dim']}; font-size: 12px; }}

#Sidebar {{ background: {P['surface']}; border-right: 1px solid {P['border']}; }}
.SectionTitle {{ color: {P['text_muted']}; font-size: 10px; font-weight: 600; letter-spacing: 1.5px; }}

QPushButton#PillBtn {{
    padding: 4px 12px; border-radius: 3px; font-size: 13px; font-weight: 600;
    border: 1px solid {P['border2']}; background: {P['surface2']}; color: {P['text_dim']};
}}
QPushButton#PillBtn:hover {{ border-color: {P['text_dim']}; color: {P['text']}; }}
QPushButton#PillBtn[resultKind="W"]:checked {{ background: rgba(76,175,130,45); border-color: {P['green']}; color: {P['green']}; }}
QPushButton#PillBtn[resultKind="L"]:checked {{ background: rgba(224,82,82,45); border-color: {P['red']}; color: {P['red']}; }}
QPushButton#PillBtn[resultKind="D"]:checked {{ background: rgba(92,164,224,45); border-color: {P['blue']}; color: {P['blue']}; }}
QPushButton#PillBtn[resultKind="ALL"]:checked {{ background: {P['orange_glow']}; border-color: {P['orange']}; color: {P['orange']}; }}

QPushButton#ChipBtn {{
    padding: 3px 9px; border-radius: 3px; font-size: 12px;
    border: 1px solid {P['border2']}; background: {P['surface2']}; color: {P['text_dim']};
}}
QPushButton#ChipBtn:hover {{ border-color: {P['orange']}; color: {P['orange']}; }}
QPushButton#ChipBtn:checked {{ background: {P['orange_glow']}; border-color: {P['orange']}; color: {P['orange']}; }}

QPushButton#ModeBtn {{
    padding: 4px 0; border-radius: 3px; font-size: 11px; font-weight: 600; letter-spacing: 1px;
    border: 1px solid {P['border2']}; background: {P['surface2']}; color: {P['text_dim']};
}}
QPushButton#ModeBtn:checked {{ background: {P['orange_glow']}; border-color: {P['orange']}; color: {P['orange']}; }}

QPushButton#FriendTag {{
    text-align: left; padding: 5px 8px; border-radius: 3px; border: 1px solid transparent;
    background: transparent; color: {P['text_dim']}; font-size: 12px;
}}
QPushButton#FriendTag:hover {{ background: {P['surface2']}; border-color: {P['border']}; }}
QPushButton#FriendTag:checked {{ background: {P['orange_glow']}; border-color: {P['orange']}; color: {P['text']}; font-weight: 600; }}

QPushButton#ResetBtn {{
    padding: 7px 0; border-radius: 3px; border: 1px solid {P['border2']};
    background: {P['surface2']}; color: {P['text_dim']}; font-size: 12px;
}}
QPushButton#ResetBtn:hover {{ border-color: {P['orange']}; color: {P['orange']}; }}

QPushButton#LoadBtn {{
    padding: 7px 16px; border-radius: 4px; border: 1px solid {P['orange']};
    background: {P['orange']}; color: #14110a; font-size: 12px; font-weight: 700;
}}
QPushButton#LoadBtn:hover {{ background: {P['orange_d']}; }}

QCheckBox {{ color: {P['text_dim']}; font-size: 12px; }}

#KpiCard {{ background: {P['surface']}; border: 1px solid {P['border']}; border-radius: 4px; }}
#KpiLabel {{ color: {P['text_muted']}; font-size: 10px; font-weight: 600; letter-spacing: 1px; }}
#KpiValue {{ font-size: 26px; font-weight: 700; }}
#KpiSub {{ color: {P['text_muted']}; font-size: 11px; }}

.SectionHeader {{ color: {P['text_dim']}; font-size: 12px; font-weight: 700; letter-spacing: 1.5px; }}
#HLine {{ background: {P['border']}; max-height: 1px; min-height: 1px; }}

#WrCard {{ background: {P['surface']}; border: 1px solid {P['border']}; border-radius: 4px; }}
#WrTitle {{ color: {P['text_dim']}; font-size: 12px; }}
#WrSub {{ color: {P['text_muted']}; font-size: 11px; }}
#WrLegend {{ color: {P['text_dim']}; font-size: 11px; }}

#ChartCard {{ background: {P['surface']}; border: 1px solid {P['border']}; border-radius: 4px; }}
#ChartTitle {{ color: {P['text_muted']}; font-size: 11px; font-weight: 700; letter-spacing: 1px; }}
#BarLabel {{ color: {P['text_dim']}; font-size: 11px; }}
#BarOutside {{ color: {P['text_muted']}; font-size: 11px; }}
#BarTrack {{ background: {P['surface3']}; border-radius: 2px; }}

#TableWrap {{ background: {P['surface']}; border: 1px solid {P['border']}; border-radius: 4px; }}
#SearchInput {{
    background: {P['surface2']}; border: 1px solid {P['border2']}; border-radius: 3px;
    padding: 5px 10px; font-size: 12px; color: {P['text']};
}}
#SearchInput:focus {{ border-color: {P['orange']}; }}
#TableCount {{ color: {P['text_muted']}; font-size: 12px; }}

QTableWidget {{
    background: {P['surface']}; gridline-color: {P['border']}; border: none;
    selection-background-color: {P['surface2']}; selection-color: {P['text']};
}}
QTableWidget::item {{ padding: 4px 8px; border-bottom: 1px solid {P['border']}; }}
QHeaderView::section {{
    background: {P['surface2']}; color: {P['text_muted']}; padding: 8px;
    border: none; border-bottom: 1px solid {P['border']}; font-size: 10px;
    font-weight: 700; letter-spacing: 1px;
}}
QHeaderView::section:hover {{ color: {P['orange']}; }}

QScrollBar:vertical {{ background: {P['bg']}; width: 10px; }}
QScrollBar::handle:vertical {{ background: {P['border2']}; border-radius: 4px; min-height: 24px; }}
QScrollBar:horizontal {{ background: {P['bg']}; height: 10px; }}
QScrollBar::handle:horizontal {{ background: {P['border2']}; border-radius: 4px; min-width: 24px; }}
"""


def set_checked_silent(btn, value):
    btn.blockSignals(True)
    btn.setChecked(value)
    btn.blockSignals(False)


def chip_html(text, color):
    return (f'<span style="background:{P["surface3"]};border:1px solid {P["border"]};'
            f'border-radius:2px;padding:1px 5px;color:{P["text_dim"]};font-size:10px;">{text}</span>')


# ==========================================================================
# Widgets reutilizaveis
# ==========================================================================

def make_kpi_card(label, value, sub, color=None):
    card = QFrame()
    card.setObjectName("KpiCard")
    lay = QVBoxLayout(card)
    lay.setContentsMargins(16, 14, 16, 12)
    lay.setSpacing(4)
    lbl = QLabel(label)
    lbl.setObjectName("KpiLabel")
    val = QLabel(value)
    val.setObjectName("KpiValue")
    if color:
        val.setStyleSheet(f"color:{color};")
    sub_lbl = QLabel(sub)
    sub_lbl.setObjectName("KpiSub")
    lay.addWidget(lbl)
    lay.addWidget(val)
    lay.addWidget(sub_lbl)
    return card


def make_bar_row(label, value, max_value, value_text, color, outside_text="", text_color=None):
    """Linha de mini grafico de barra horizontal: label | barra proporcional | texto.
    `color` estiliza o preenchimento/borda da barra; `text_color` (se informado)
    estiliza o valor exibido dentro dela (eles podem divergir, ex.: cor do mapa
    na barra vs. cor de performance no texto)."""
    text_color = text_color or color
    row = QWidget()
    h = QHBoxLayout(row)
    h.setContentsMargins(0, 0, 0, 0)
    h.setSpacing(8)

    lbl = QLabel(label)
    lbl.setObjectName("BarLabel")
    lbl.setFixedWidth(108)
    lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    h.addWidget(lbl)

    track = QFrame()
    track.setObjectName("BarTrack")
    track.setFixedHeight(18)
    track_lay = QHBoxLayout(track)
    track_lay.setContentsMargins(0, 0, 0, 0)
    track_lay.setSpacing(0)

    fill_stretch = max(int(round(value)), 0) if max_value > 0 else 0
    remain_stretch = max(int(round(max_value - value)), 0) if max_value > 0 else 1

    fill = QFrame()
    fill.setStyleSheet(f"background: {color}33; border-right: 2px solid {color}; border-radius: 2px;")
    fill_lay = QHBoxLayout(fill)
    fill_lay.setContentsMargins(6, 0, 6, 0)
    val_lbl = QLabel(value_text)
    val_lbl.setStyleSheet(f"color:{text_color}; font-size:10px; font-weight:700; background: transparent; border: none;")
    fill_lay.addWidget(val_lbl, 0, Qt.AlignmentFlag.AlignRight)
    fill.setLayout(fill_lay)

    track_lay.addWidget(fill, fill_stretch if fill_stretch > 0 else 1)
    if remain_stretch > 0:
        spacer = QWidget()
        track_lay.addWidget(spacer, remain_stretch)
    if fill_stretch == 0:
        fill.setMaximumWidth(2)

    h.addWidget(track, 1)

    out_lbl = QLabel(outside_text)
    out_lbl.setObjectName("BarOutside")
    out_lbl.setFixedWidth(34)
    h.addWidget(out_lbl)
    return row


def make_map_wr_card(row):
    """row: dict com map/total/w/d/l/wr (ver cs_data.winrate_by_map)."""
    card = QFrame()
    card.setObjectName("WrCard")
    lay = QVBoxLayout(card)
    lay.setContentsMargins(14, 12, 14, 12)
    lay.setSpacing(8)

    title_row = QHBoxLayout()
    title = QLabel(row["map"])
    title.setObjectName("WrTitle")
    sub = QLabel(f'{row["total"]} partidas')
    sub.setObjectName("WrSub")
    title_row.addWidget(title)
    title_row.addStretch(1)
    title_row.addWidget(sub)
    lay.addLayout(title_row)

    bar = QFrame()
    bar.setObjectName("BarTrack")
    bar.setFixedHeight(6)
    bar_lay = QHBoxLayout(bar)
    bar_lay.setContentsMargins(0, 0, 0, 0)
    bar_lay.setSpacing(1)
    map_col = MAP_COLORS.get(row["map"], "#888888")
    w_seg = QFrame()
    w_seg.setStyleSheet(f"background:{map_col}; border-radius: 2px;")
    d_seg = QFrame()
    d_seg.setStyleSheet(f"background:{P['blue']}; border-radius: 2px;")
    l_seg = QFrame()
    l_seg.setStyleSheet(f"background:{P['red']}; border-radius: 2px;")
    bar_lay.addWidget(w_seg, max(row["w"], 0) or 0)
    bar_lay.addWidget(d_seg, max(row["d"], 0) or 0)
    bar_lay.addWidget(l_seg, max(row["l"], 1))
    lay.addWidget(bar)

    legend = QLabel(
        f'<span style="color:{P["green"]}">● {row["wr"]}% WR</span>&nbsp;&nbsp;'
        f'<span style="color:{P["green"]}">{row["w"]}W</span>&nbsp;&nbsp;'
        f'<span style="color:{P["blue"]}">{row["d"]}D</span>&nbsp;&nbsp;'
        f'<span style="color:{P["red"]}">{row["l"]}L</span>'
    )
    legend.setObjectName("WrLegend")
    lay.addWidget(legend)
    return card


def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        w = item.widget()
        if w is not None:
            # hide + desanexar imediatamente: deleteLater() sozinho so remove
            # o objeto no proximo ciclo do event loop, deixando o widget
            # "fantasma" visivel ate la.
            w.hide()
            w.setParent(None)
            w.deleteLater()
        else:
            sub = item.layout()
            if sub is not None:
                clear_layout(sub)


SORT_COLUMNS = ["num", "map", "score", "result", "k", "d", "a", "kdr", "pts", "place", None]
TABLE_HEADERS = ["#", "Mapa", "Placar", "Res.", "K", "D", "A", "KDR", "PTS", "Place", "Lineup"]


# ==========================================================================
# Janela principal
# ==========================================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CS Season Dashboard")
        self.resize(1440, 900)
        self.setMinimumSize(1100, 700)
        self.setStyleSheet(QSS)

        self.sd = None
        self.filter_result = "ALL"
        self.filter_maps = set()
        self.filter_friends = set()
        self.lineup_mode = "any"
        self.solo_only = False
        self.search = ""
        self.sort_col = "num"
        self.sort_dir = 1

        self.map_chip_buttons = {}
        self.friend_tag_buttons = {}
        self.pill_buttons = {}
        self.mode_buttons = {}

        self.current_path = None
        self._last_mtime = None
        self._last_size = None
        self._pending_stable = None
        # QFileSystemWatcher trava nativamente quando o arquivo monitorado e
        # apagado/recriado (padrao comum de gravacao do Excel/OneDrive), entao
        # usamos polling por mtime/tamanho em vez da API de watch do SO.
        self._poll_timer = QTimer(self)
        self._poll_timer.setInterval(1000)
        self._poll_timer.timeout.connect(self._poll_file_changed)

        self._build_ui()

    # ---------------------------------------------------------------- UI --
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_topbar())

        body = QWidget()
        body_lay = QHBoxLayout(body)
        body_lay.setContentsMargins(0, 0, 0, 0)
        body_lay.setSpacing(0)

        self.sidebar_scroll = QScrollArea()
        self.sidebar_scroll.setWidgetResizable(True)
        self.sidebar_scroll.setFixedWidth(252)
        self.sidebar_scroll.setObjectName("Sidebar")
        self.sidebar_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.sidebar_inner = QWidget()
        self.sidebar_inner.setObjectName("Sidebar")
        self.sidebar_layout = QVBoxLayout(self.sidebar_inner)
        self.sidebar_layout.setContentsMargins(16, 18, 16, 18)
        self.sidebar_layout.setSpacing(20)
        self.sidebar_scroll.setWidget(self.sidebar_inner)
        body_lay.addWidget(self.sidebar_scroll)

        self.main_scroll = QScrollArea()
        self.main_scroll.setWidgetResizable(True)
        self.main_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.main_inner = QWidget()
        self.main_layout = QVBoxLayout(self.main_inner)
        self.main_layout.setContentsMargins(24, 22, 24, 22)
        self.main_layout.setSpacing(22)
        self.main_scroll.setWidget(self.main_inner)
        body_lay.addWidget(self.main_scroll, 1)

        root.addWidget(body, 1)

        self._build_placeholder_sidebar()
        self._build_placeholder_main()

    def _build_topbar(self):
        bar = QFrame()
        bar.setObjectName("TopBar")
        bar.setFixedHeight(56)
        h = QHBoxLayout(bar)
        h.setContentsMargins(26, 0, 26, 0)
        h.setSpacing(16)

        logo = QLabel("CS2")
        logo.setObjectName("TopLogo")
        sep = QFrame()
        sep.setFixedSize(1, 22)
        sep.setStyleSheet(f"background:{P['border2']};")
        title = QLabel("Season Dashboard · Personal Stats")
        title.setObjectName("TopTitle")

        self.total_badge = QLabel("Nenhuma planilha carregada")
        self.total_badge.setObjectName("TotalBadge")

        load_btn = QPushButton("Carregar planilha...")
        load_btn.setObjectName("LoadBtn")
        load_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        load_btn.clicked.connect(self.prompt_load)

        h.addWidget(logo)
        h.addWidget(sep)
        h.addWidget(title)
        h.addStretch(1)
        h.addWidget(self.total_badge)
        h.addWidget(load_btn)
        return bar

    def _build_placeholder_sidebar(self):
        clear_layout(self.sidebar_layout)
        lbl = QLabel("Carregue uma planilha para ver os filtros.")
        lbl.setWordWrap(True)
        lbl.setStyleSheet(f"color:{P['text_muted']}; font-size:12px;")
        self.sidebar_layout.addWidget(lbl)
        self.sidebar_layout.addStretch(1)

    def _build_placeholder_main(self):
        clear_layout(self.main_layout)
        lbl = QLabel("Carregue um arquivo .xlsx para comecar (botao no topo).")
        lbl.setStyleSheet(f"color:{P['text_muted']}; font-size:14px;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(lbl)
        self.main_layout.addStretch(1)

    # ------------------------------------------------------------ Carga --
    def prompt_load(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Selecione a planilha da season (.xlsx)", "",
            "Planilha Excel (*.xlsx);;Todos os arquivos (*.*)",
        )
        if not path:
            return
        self.load_file(path)

    def load_file(self, path):
        """Carga explicita (botao/dialogo/arquivo inicial): reseta os filtros."""
        try:
            sd = cd.load_season_data(path)
        except Exception as exc:
            QMessageBox.critical(self, "Erro ao carregar planilha", str(exc))
            return
        self.current_path = path
        self._apply_loaded_data(sd, reset_filters=True)
        self._start_watching(path)

    # ---------------------------------------------------- Auto-atualizar --
    def _start_watching(self, path):
        self._last_mtime, self._last_size = self._stat(path)
        self._pending_stable = None
        self._poll_timer.start()

    @staticmethod
    def _stat(path):
        try:
            return os.path.getmtime(path), os.path.getsize(path)
        except OSError:
            return None, None

    def _poll_file_changed(self):
        path = self.current_path
        if not path or not os.path.isfile(path):
            return
        mtime, size = self._stat(path)
        if mtime is None:
            return
        if (mtime, size) == (self._last_mtime, self._last_size):
            self._pending_stable = None
            return
        # so recarrega depois que o arquivo ficar estavel por duas leituras
        # seguidas (evita ler no meio de uma gravacao do Excel/OneDrive)
        if self._pending_stable == (mtime, size):
            self._pending_stable = None
            self._reload_current_file()
        else:
            self._pending_stable = (mtime, size)

    def _reload_current_file(self):
        path = self.current_path
        if not path or not os.path.isfile(path):
            return
        try:
            sd = cd.load_season_data(path)
        except Exception:
            # pode ter sido lido no meio de uma gravacao incompleta; tenta de novo em breve
            QTimer.singleShot(500, self._reload_current_file)
            return
        self._last_mtime, self._last_size = self._stat(path)
        self._apply_loaded_data(sd, reset_filters=False)

    def _apply_loaded_data(self, sd, reset_filters):
        """Reconstroi a UI com os dados carregados. Se reset_filters for False,
        tenta preservar os filtros/ordenacao atuais (usado na auto-atualizacao)."""
        if reset_filters or self.sd is None:
            self.filter_result = "ALL"
            self.filter_maps = set()
            self.filter_friends = set()
            self.lineup_mode = "any"
            self.solo_only = False
            self.search = ""
            self.sort_col = "num"
            self.sort_dir = 1
        else:
            valid_maps = set(cd.known_maps(sd))
            valid_friends = set(cd.known_friends(sd)[0])
            self.filter_maps &= valid_maps
            self.filter_friends &= valid_friends

        self.sd = sd
        self.total_badge.setText(
            f"{os.path.basename(self.current_path)}  ·  {len(sd.matches)} partidas  ·  "
            f"{len(cd.known_friends(sd)[0])} amigos"
        )

        self._build_real_sidebar()
        self._build_real_main()
        if self.sort_col in SORT_COLUMNS:
            idx = SORT_COLUMNS.index(self.sort_col)
            order = Qt.SortOrder.AscendingOrder if self.sort_dir == 1 else Qt.SortOrder.DescendingOrder
            self.table.horizontalHeader().setSortIndicator(idx, order)
        self.render_all()

    # --------------------------------------------------------- Sidebar --
    def _build_real_sidebar(self):
        clear_layout(self.sidebar_layout)
        sd = self.sd

        # Resultado
        self.sidebar_layout.addWidget(self._section_title("Resultado"))
        pill_row = QHBoxLayout()
        pill_row.setSpacing(6)
        self.pill_buttons = {}
        for kind, text in [("ALL", "Todos"), ("W", "W"), ("L", "L"), ("D", "D")]:
            btn = QPushButton(text)
            btn.setObjectName("PillBtn")
            btn.setProperty("resultKind", kind)
            btn.setCheckable(True)
            btn.setChecked(kind == self.filter_result)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _checked, k=kind: self.toggle_result(k))
            pill_row.addWidget(btn)
            self.pill_buttons[kind] = btn
        pill_wrap = QWidget()
        pill_wrap.setLayout(pill_row)
        self.sidebar_layout.addWidget(pill_wrap)

        # Mapa
        self.sidebar_layout.addWidget(self._section_title("Mapa"))
        map_grid = QGridLayout()
        map_grid.setSpacing(5)
        self.map_chip_buttons = {}
        maps = cd.known_maps(sd)
        for i, map_name in enumerate(maps):
            btn = QPushButton(map_name)
            btn.setObjectName("ChipBtn")
            btn.setCheckable(True)
            btn.setChecked(map_name in self.filter_maps)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _checked, m=map_name: self.toggle_map(m))
            map_grid.addWidget(btn, i // 2, i % 2)
            self.map_chip_buttons[map_name] = btn
        map_wrap = QWidget()
        map_wrap.setLayout(map_grid)
        self.sidebar_layout.addWidget(map_wrap)

        # Lineup
        self.sidebar_layout.addWidget(self._section_title("Lineup"))
        mode_row = QHBoxLayout()
        mode_row.setSpacing(4)
        self.mode_buttons = {}
        for mode, text in [("any", "Inclui"), ("all", "Todos"), ("exact", "Exata")]:
            btn = QPushButton(text)
            btn.setObjectName("ModeBtn")
            btn.setCheckable(True)
            btn.setChecked(mode == self.lineup_mode)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _checked, m=mode: self.set_mode(m))
            mode_row.addWidget(btn)
            self.mode_buttons[mode] = btn
        mode_wrap = QWidget()
        mode_wrap.setLayout(mode_row)
        self.sidebar_layout.addWidget(mode_wrap)

        self.solo_checkbox = QCheckBox("Somente solo")
        self.solo_checkbox.blockSignals(True)
        self.solo_checkbox.setChecked(self.solo_only)
        self.solo_checkbox.blockSignals(False)
        self.solo_checkbox.stateChanged.connect(self._on_solo_changed)
        self.sidebar_layout.addWidget(self.solo_checkbox)

        friends, counts = cd.known_friends(sd)
        self.friend_tag_buttons = {}
        friend_list_widget = QWidget()
        friend_list_lay = QVBoxLayout(friend_list_widget)
        friend_list_lay.setContentsMargins(0, 4, 0, 0)
        friend_list_lay.setSpacing(2)
        for f in friends:
            btn = QPushButton(f"{f}      {counts[f]}")
            btn.setObjectName("FriendTag")
            btn.setCheckable(True)
            btn.setChecked(f in self.filter_friends)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _checked, fr=f: self.toggle_friend(fr))
            friend_list_lay.addWidget(btn)
            self.friend_tag_buttons[f] = btn
        self.sidebar_layout.addWidget(friend_list_widget)

        reset_btn = QPushButton("↺  Limpar filtros")
        reset_btn.setObjectName("ResetBtn")
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.clicked.connect(self.reset_all)
        self.sidebar_layout.addWidget(reset_btn)
        self.sidebar_layout.addStretch(1)

    def _section_title(self, text):
        lbl = QLabel(text)
        lbl.setProperty("class", "SectionTitle")
        lbl.setStyleSheet(f"color:{P['text_muted']}; font-size:10px; font-weight:700; letter-spacing:1.5px;")
        return lbl

    # ------------------------------------------------------------ Main --
    def _build_real_main(self):
        clear_layout(self.main_layout)

        self.kpi_row = QHBoxLayout()
        self.kpi_row.setSpacing(12)
        kpi_wrap = QWidget()
        kpi_wrap.setLayout(self.kpi_row)
        self.main_layout.addWidget(kpi_wrap)

        self.main_layout.addLayout(self._section_header("Win Rate por Mapa"))
        self.map_wr_grid = QGridLayout()
        self.map_wr_grid.setSpacing(10)
        map_wr_wrap = QWidget()
        map_wr_wrap.setLayout(self.map_wr_grid)
        self.main_layout.addWidget(map_wr_wrap)

        charts_row = QHBoxLayout()
        charts_row.setSpacing(16)

        friend_card = QFrame()
        friend_card.setObjectName("ChartCard")
        friend_card_lay = QVBoxLayout(friend_card)
        friend_title = QLabel("DESEMPENHO POR AMIGO (WR %)")
        friend_title.setObjectName("ChartTitle")
        friend_card_lay.addWidget(friend_title)
        self.friend_chart_layout = QVBoxLayout()
        self.friend_chart_layout.setSpacing(7)
        friend_card_lay.addLayout(self.friend_chart_layout)
        friend_card_lay.addStretch(1)
        charts_row.addWidget(friend_card, 1)

        map_card = QFrame()
        map_card.setObjectName("ChartCard")
        map_card_lay = QVBoxLayout(map_card)
        map_title = QLabel("KDR MEDIO POR MAPA")
        map_title.setObjectName("ChartTitle")
        map_card_lay.addWidget(map_title)
        self.map_chart_layout = QVBoxLayout()
        self.map_chart_layout.setSpacing(7)
        map_card_lay.addLayout(self.map_chart_layout)
        map_card_lay.addStretch(1)
        charts_row.addWidget(map_card, 1)

        charts_wrap = QWidget()
        charts_wrap.setLayout(charts_row)
        self.main_layout.addWidget(charts_wrap)

        self.main_layout.addLayout(self._section_header("Historico de Partidas"))

        table_wrap = QFrame()
        table_wrap.setObjectName("TableWrap")
        table_wrap_lay = QVBoxLayout(table_wrap)
        table_wrap_lay.setContentsMargins(0, 0, 0, 0)
        table_wrap_lay.setSpacing(0)

        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(14, 10, 14, 10)
        self.search_input = QLineEdit()
        self.search_input.setObjectName("SearchInput")
        self.search_input.setPlaceholderText("Buscar mapa, placar...")
        self.search_input.setFixedWidth(220)
        self.search_input.blockSignals(True)
        self.search_input.setText(self.search)
        self.search_input.blockSignals(False)
        self.search_input.textChanged.connect(self._on_search_changed)
        self.count_label = QLabel("Exibindo 0 partidas")
        self.count_label.setObjectName("TableCount")
        toolbar.addWidget(self.search_input)
        toolbar.addStretch(1)
        toolbar.addWidget(self.count_label)
        toolbar_wrap = QWidget()
        toolbar_wrap.setLayout(toolbar)
        toolbar_wrap.setStyleSheet(f"border-bottom: 1px solid {P['border']};")
        table_wrap_lay.addWidget(toolbar_wrap)

        self.table = QTableWidget(0, len(TABLE_HEADERS))
        self.table.setHorizontalHeaderLabels(TABLE_HEADERS)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(10, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
        self.table.horizontalHeader().setSortIndicatorShown(True)
        self.table.setMinimumHeight(420)
        self.table.setMaximumHeight(560)
        table_wrap_lay.addWidget(self.table)

        self.main_layout.addWidget(table_wrap)

    def _section_header(self, text):
        lay = QHBoxLayout()
        lay.setSpacing(10)
        lbl = QLabel(text.upper())
        lbl.setStyleSheet(f"color:{P['text_dim']}; font-size:12px; font-weight:700; letter-spacing:1.5px;")
        line = QFrame()
        line.setObjectName("HLine")
        line.setFixedHeight(1)
        lay.addWidget(lbl)
        lay.addWidget(line, 1)
        return lay

    # --------------------------------------------------------- Toggles --
    def toggle_result(self, kind):
        self.filter_result = kind
        for k, btn in self.pill_buttons.items():
            set_checked_silent(btn, k == kind)
        self.render_all()

    def toggle_map(self, map_name):
        if map_name in self.filter_maps:
            self.filter_maps.discard(map_name)
        else:
            self.filter_maps.add(map_name)
        self.render_all()

    def toggle_friend(self, friend):
        if friend in self.filter_friends:
            self.filter_friends.discard(friend)
        else:
            self.filter_friends.add(friend)
        self.render_all()

    def set_mode(self, mode):
        self.lineup_mode = mode
        for m, btn in self.mode_buttons.items():
            set_checked_silent(btn, m == mode)
        self.render_all()

    def _on_solo_changed(self, _state):
        self.solo_only = self.solo_checkbox.isChecked()
        self.render_all()

    def _on_search_changed(self, text):
        self.search = text
        self.render_all()

    def reset_all(self):
        self.filter_result = "ALL"
        self.filter_maps.clear()
        self.filter_friends.clear()
        self.lineup_mode = "any"
        self.solo_only = False
        self.search = ""

        for k, btn in self.pill_buttons.items():
            set_checked_silent(btn, k == "ALL")
        for btn in self.map_chip_buttons.values():
            set_checked_silent(btn, False)
        for btn in self.friend_tag_buttons.values():
            set_checked_silent(btn, False)
        for m, btn in self.mode_buttons.items():
            set_checked_silent(btn, m == "any")
        self.solo_checkbox.blockSignals(True)
        self.solo_checkbox.setChecked(False)
        self.solo_checkbox.blockSignals(False)
        self.search_input.blockSignals(True)
        self.search_input.clear()
        self.search_input.blockSignals(False)

        self.render_all()

    def _on_header_clicked(self, index):
        col = SORT_COLUMNS[index]
        if col is None:
            return
        if self.sort_col == col:
            self.sort_dir *= -1
        else:
            self.sort_col = col
            self.sort_dir = 1
        self.table.horizontalHeader().setSortIndicator(
            index, Qt.SortOrder.AscendingOrder if self.sort_dir == 1 else Qt.SortOrder.DescendingOrder
        )
        self.render_table(self.get_filtered())

    # ------------------------------------------------------------ Dados --
    def get_filtered(self):
        if not self.sd:
            return []
        return cd.filter_matches(
            self.sd.matches, result=self.filter_result, maps=self.filter_maps,
            friends=self.filter_friends, lineup_mode=self.lineup_mode,
            solo_only=self.solo_only, search=self.search,
        )

    # ----------------------------------------------------------- Render --
    def render_all(self):
        data = self.get_filtered()
        self.render_kpis(data)
        self.render_map_wr(data)
        self.render_friend_chart(data)
        self.render_map_kdr_chart(data)
        self.render_table(data)

    def render_kpis(self, data):
        clear_layout(self.kpi_row)
        total = len(data)
        wins = sum(1 for m in data if m.result == "W")
        losses = sum(1 for m in data if m.result == "L")
        draws = sum(1 for m in data if m.result == "D")
        wr = round(wins / total * 100) if total else 0
        avg_kdr = cd.avg(m.kdr for m in data)
        avg_k = cd.avg(m.k for m in data)
        avg_d = cd.avg(m.d for m in data)
        avg_pts = cd.avg(m.pts for m in data)
        placed = [m.place for m in data if m.place > 0]
        avg_place = cd.avg(placed)
        p1 = sum(1 for m in data if m.place == 1)

        cards = [
            ("PARTIDAS", str(total), f"{wins}W · {draws}D · {losses}L", P["orange"]),
            ("WIN RATE", f"{wr}%", f"{wins} vitorias", P["green"] if wr >= 50 else P["red"]),
            ("KDR MEDIO", f"{avg_kdr:.2f}", f"{avg_k:.1f} K / {avg_d:.1f} D",
             P["green"] if avg_kdr >= 1 else P["red"]),
            ("PTS MEDIO", f"{avg_pts:.0f}", "avg/partida", P["text"]),
            ("PLACE MEDIO", f"{avg_place:.1f}" if placed else "—", f"#1: {p1}x", P["text"]),
        ]
        for label, value, sub, color in cards:
            self.kpi_row.addWidget(make_kpi_card(label, value, sub, color), 1)

    def render_map_wr(self, data):
        clear_layout(self.map_wr_grid)
        maps = [m for m in cd.known_maps(self.sd) if not self.filter_maps or m in self.filter_maps]
        rows = cd.winrate_by_map(data, maps)
        if not rows:
            empty = QLabel("Sem dados para os filtros atuais.")
            empty.setStyleSheet(f"color:{P['text_muted']}; font-size:13px;")
            self.map_wr_grid.addWidget(empty, 0, 0)
            return
        cols = 4
        for i, row in enumerate(rows):
            self.map_wr_grid.addWidget(make_map_wr_card(row), i // cols, i % cols)

    def render_friend_chart(self, data):
        clear_layout(self.friend_chart_layout)
        friends = cd.known_friends(self.sd)[0]
        rows = cd.winrate_by_friend(data, friends, top_n=10)
        if not rows:
            empty = QLabel("Sem dados")
            empty.setStyleSheet(f"color:{P['text_muted']}; font-size:12px;")
            self.friend_chart_layout.addWidget(empty)
            return
        max_wr = max((r["wr"] for r in rows), default=1) or 1
        for r in rows:
            color = P["green"] if r["wr"] >= 55 else (P["orange"] if r["wr"] >= 45 else P["red"])
            self.friend_chart_layout.addWidget(
                make_bar_row(r["friend"], r["wr"], max_wr, f'{r["wr"]}%', color, f'{r["total"]}p')
            )

    def render_map_kdr_chart(self, data):
        clear_layout(self.map_chart_layout)
        maps = cd.known_maps(self.sd)
        rows = cd.kdr_by_map(data, maps)
        if not rows:
            empty = QLabel("Sem dados")
            empty.setStyleSheet(f"color:{P['text_muted']}; font-size:12px;")
            self.map_chart_layout.addWidget(empty)
            return
        max_kdr = max((r["kdr"] for r in rows), default=1) or 1
        for r in rows:
            perf_color = P["green"] if r["kdr"] >= 1.2 else (P["orange"] if r["kdr"] >= 0.9 else P["red"])
            map_col = MAP_COLORS.get(r["map"], P["orange"])
            self.map_chart_layout.addWidget(
                make_bar_row(r["map"], r["kdr"], max_kdr, f'{r["kdr"]:.2f}', map_col, f'{r["total"]}p',
                              text_color=perf_color)
            )

    def render_table(self, data):
        sorted_data = sorted(
            data, key=lambda m: getattr(m, self.sort_col), reverse=(self.sort_dir == -1)
        )
        self.count_label.setText(f"Exibindo {len(sorted_data)} partidas")
        self.table.setRowCount(len(sorted_data))

        for row_i, m in enumerate(sorted_data):
            num_item = QTableWidgetItem(str(m.num))
            num_item.setForeground(QColor(P["text_muted"]))
            num_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_i, 0, num_item)

            map_lbl = QLabel(m.map)
            map_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            map_col = MAP_COLORS.get(m.map, P["text_dim"])
            map_lbl.setStyleSheet(
                f"background:{P['surface3']}; color:{P['text_dim']}; border-left: 2px solid {map_col};"
                f"font-weight:700; font-size:12px; padding: 3px 6px;"
            )
            self.table.setCellWidget(row_i, 1, map_lbl)

            score_item = QTableWidgetItem(m.score)
            score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_i, 2, score_item)

            res_color = RESULT_COLOR.get(m.result, P["text"])
            res_lbl = QLabel(m.result)
            res_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            res_lbl.setStyleSheet(
                f"background: {res_color}29; color:{res_color}; font-weight:700; "
                f"border-radius:2px; padding: 2px 4px;"
            )
            self.table.setCellWidget(row_i, 3, res_lbl)

            for col_i, val in [(4, m.k), (5, m.d), (6, m.a)]:
                item = QTableWidgetItem(f"{val:.0f}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_i, col_i, item)

            kdr_str = f"{m.kdr:.1f}" if m.kdr >= 10 else f"{m.kdr:.2f}"
            kdr_item = QTableWidgetItem(kdr_str)
            kdr_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            kdr_color = P["green"] if m.kdr >= 1.2 else (P["red"] if m.kdr < 0.85 else P["text"])
            kdr_item.setForeground(QColor(kdr_color))
            self.table.setItem(row_i, 7, kdr_item)

            pts_item = QTableWidgetItem(f"{m.pts:.0f}")
            pts_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_i, 8, pts_item)

            place_str = f"#{int(m.place)}" if m.place > 0 else "—"
            place_item = QTableWidgetItem(place_str)
            place_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            place_color = P["yellow"] if m.place == 1 else (P["text"] if m.place == 2 else P["text_muted"])
            place_item.setForeground(QColor(place_color))
            self.table.setItem(row_i, 9, place_item)

            if m.lineup:
                lineup_html = " ".join(chip_html(f, None) for f in m.lineup)
            else:
                lineup_html = f'<i style="color:{P["text_muted"]}; font-size:11px;">solo</i>'
            lineup_lbl = QLabel(lineup_html)
            lineup_lbl.setTextFormat(Qt.TextFormat.RichText)
            lineup_lbl.setStyleSheet("padding: 2px 6px;")
            self.table.setCellWidget(row_i, 10, lineup_lbl)

            self.table.setRowHeight(row_i, 30)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    win = MainWindow()
    win.show()

    initial_path = sys.argv[1] if len(sys.argv) > 1 else None
    if initial_path and os.path.isfile(initial_path):
        win.load_file(initial_path)
    else:
        win.prompt_load()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
