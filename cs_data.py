"""
Camada de dados do CS Season Dashboard (sem dependencia de UI).
Le a planilha .xlsx, limpa/normaliza e expõe uma lista de partidas
(prontas para filtrar) mais funcoes de metricas agregadas.
"""

import pandas as pd


def fix_mojibake(value):
    """Conserta texto corrompido (UTF-8 lido como CP1252)."""
    if not isinstance(value, str):
        return value
    try:
        fixed = value.encode("cp1252").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        return value
    return fixed


def _normalize(text):
    text = fix_mojibake(str(text)).strip().lower()
    replacements = {
        "á": "a", "â": "a", "ã": "a", "à": "a",
        "é": "e", "ê": "e",
        "í": "i",
        "ó": "o", "ô": "o", "õ": "o",
        "ú": "u",
        "ç": "c",
        "º": "o", "ª": "a",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


class Match:
    __slots__ = ("num", "map", "score", "result", "k", "d", "a", "pts",
                 "kdr", "place", "lineup", "num_friends")

    def __init__(self, num, map_, score, result, k, d, a, pts, kdr, place, lineup):
        self.num = num
        self.map = map_
        self.score = score
        self.result = result
        self.k = k
        self.d = d
        self.a = a
        self.pts = pts
        self.kdr = kdr
        self.place = place
        self.lineup = lineup
        self.num_friends = len(lineup)


class SeasonData:
    """Planilha carregada: dataframe limpo + colunas resolvidas + partidas."""

    def __init__(self, df, columns, friend_cols, matches, source_path):
        self.df = df
        self.columns = columns
        self.friend_cols = friend_cols
        self.matches = matches
        self.source_path = source_path

    @property
    def col_mapa(self):
        return self.columns["mapa"]

    @property
    def col_resultado(self):
        return self.columns["resultado"]

    @property
    def col_k(self):
        return self.columns["k"]

    @property
    def col_d(self):
        return self.columns["d"]

    @property
    def col_a(self):
        return self.columns["a"]


def _find_sheet(xls):
    for name in xls.sheet_names:
        try:
            sample = pd.read_excel(xls, sheet_name=name, nrows=3)
        except Exception:
            continue
        norm_cols = [_normalize(c) for c in sample.columns]
        if any("mapa" in c for c in norm_cols) and any("resultado" in c for c in norm_cols):
            return name
    return xls.sheet_names[0]


def _safe_float(value, default=0.0):
    try:
        f = float(value)
        if f != f:  # NaN
            return default
        return f
    except (TypeError, ValueError):
        return default


def load_season_data(filepath):
    # pd.ExcelFile mantem o arquivo aberto ate ser fechado explicitamente; sem
    # isso, o handle vaza e impede o arquivo de ser sobrescrito/apagado
    # externamente (Excel/OneDrive salvando) enquanto o app esta rodando.
    with pd.ExcelFile(filepath) as xls:
        sheet = _find_sheet(xls)
        df = pd.read_excel(xls, sheet_name=sheet)

    df.columns = [fix_mojibake(str(c)) for c in df.columns]
    norm_cols = [_normalize(c) for c in df.columns]

    def find_exact(*names):
        for i, nc in enumerate(norm_cols):
            if nc in names:
                return df.columns[i]
        return None

    col_mapa = find_exact("mapa")
    col_resultado = find_exact("resultado")
    col_k = find_exact("k")
    col_d = find_exact("d")
    col_a = find_exact("a")
    col_amigos = find_exact("amigos")
    # opcionais (degradam graciosamente se nao existirem)
    col_placar = find_exact("placar")
    col_kdr = find_exact("kdr")
    col_pts = find_exact("pts")
    col_place = find_exact("place (pts)", "place")
    col_match_num = find_exact("match no", "match n")

    missing = [n for n, c in [("Mapa", col_mapa), ("Resultado", col_resultado),
                               ("K", col_k), ("D", col_d), ("A", col_a),
                               ("Amigos", col_amigos)] if c is None]
    if missing:
        raise ValueError(
            "Nao foi possivel encontrar as colunas obrigatorias: " + ", ".join(missing) +
            ".\nVerifique se a planilha segue o modelo original (aba com colunas "
            "Mapa, Resultado, K, D, A, Amigos)."
        )

    # Bloco de colunas de amigos: tudo apos "Amigos" ate a primeira coluna
    # sem nome / "Unnamed" / vazia -> detecta automaticamente amigos novos.
    idx_amigos = list(df.columns).index(col_amigos)
    friend_cols = []
    for col in df.columns[idx_amigos + 1:]:
        col_str = str(col)
        if col_str.startswith("Unnamed") or col_str.strip() == "" or col_str.lower() == "nan":
            break
        friend_cols.append(col)

    df[col_resultado] = df[col_resultado].astype(str).str.strip().str.upper()
    df = df[df[col_resultado].isin(["W", "L", "D"])].copy()

    for col in [col_k, col_d, col_a, col_amigos] + friend_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if col_kdr:
        df[col_kdr] = pd.to_numeric(df[col_kdr], errors="coerce")
    if col_pts:
        df[col_pts] = pd.to_numeric(df[col_pts], errors="coerce")
    if col_place:
        df[col_place] = pd.to_numeric(df[col_place], errors="coerce")

    df[col_mapa] = df[col_mapa].apply(fix_mojibake).astype(str).str.strip()

    if df.empty:
        raise ValueError("A planilha nao contem nenhuma partida valida (coluna Resultado vazia).")

    matches = []
    for seq, (_, row) in enumerate(df.iterrows(), start=1):
        lineup = [fc for fc in friend_cols if (row[fc] or 0) > 0]
        num = int(row[col_match_num]) if col_match_num and row[col_match_num] == row[col_match_num] else seq
        k = _safe_float(row[col_k])
        d = _safe_float(row[col_d])
        a = _safe_float(row[col_a])
        pts = _safe_float(row[col_pts]) if col_pts else 0.0
        kdr = _safe_float(row[col_kdr]) if col_kdr else (k / d if d else k)
        place = _safe_float(row[col_place]) if col_place else 0.0
        score = str(row[col_placar]).strip() if col_placar and row[col_placar] == row[col_placar] else ""
        matches.append(Match(num, row[col_mapa], score, row[col_resultado], k, d, a,
                              pts, kdr, place, lineup))

    columns = {
        "mapa": col_mapa, "resultado": col_resultado, "k": col_k, "d": col_d,
        "a": col_a, "amigos": col_amigos, "placar": col_placar, "kdr": col_kdr,
        "pts": col_pts, "place": col_place,
    }
    return SeasonData(df, columns, friend_cols, matches, filepath)


# ==========================================================================
# Metricas e filtragem (operam sobre listas de Match)
# ==========================================================================

ALL_MAPS_ORDER = ["MIRAGE", "INFERNO", "NUKE", "OVERPASS", "DUST II", "ANUBIS", "ANCIENT", "TRAIN", "VERTIGO"]


def known_maps(sd: SeasonData):
    present = {m.map for m in sd.matches}
    ordered = [m for m in ALL_MAPS_ORDER if m in present]
    extra = sorted(present - set(ordered))
    return ordered + extra


def known_friends(sd: SeasonData):
    counts = {fc: 0 for fc in sd.friend_cols}
    for m in sd.matches:
        for f in m.lineup:
            counts[f] = counts.get(f, 0) + 1
    return [f for f in sd.friend_cols if counts.get(f, 0) > 0], counts


def filter_matches(matches, result="ALL", maps=None, friends=None, lineup_mode="any",
                    solo_only=False, search=""):
    maps = maps or set()
    friends = friends or set()
    search = search.strip().lower()
    out = []
    for m in matches:
        if result != "ALL" and m.result != result:
            continue
        if maps and m.map not in maps:
            continue
        if solo_only and m.num_friends > 0:
            continue
        if friends:
            lineup_set = set(m.lineup)
            if lineup_mode == "any":
                if not (friends & lineup_set):
                    continue
            elif lineup_mode == "all":
                if not friends.issubset(lineup_set):
                    continue
            else:  # exact
                if lineup_set != friends:
                    continue
        if search:
            if search not in m.map.lower() and search not in m.score.lower():
                continue
        out.append(m)
    return out


def avg(values):
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def winrate_by_map(matches, maps_order):
    out = []
    for map_ in maps_order:
        ms = [m for m in matches if m.map == map_]
        if not ms:
            continue
        w = sum(1 for m in ms if m.result == "W")
        d = sum(1 for m in ms if m.result == "D")
        l = sum(1 for m in ms if m.result == "L")
        out.append({"map": map_, "total": len(ms), "w": w, "d": d, "l": l,
                     "wr": round(w / len(ms) * 100)})
    return out


def winrate_by_friend(matches, friends_order, top_n=None):
    out = []
    for f in friends_order:
        ms = [m for m in matches if f in m.lineup]
        if not ms:
            continue
        w = sum(1 for m in ms if m.result == "W")
        out.append({"friend": f, "total": len(ms), "wr": round(w / len(ms) * 100)})
    out.sort(key=lambda r: r["wr"], reverse=True)
    return out[:top_n] if top_n else out


def kdr_by_map(matches, maps_order):
    out = []
    for map_ in maps_order:
        ms = [m for m in matches if m.map == map_]
        if not ms:
            continue
        out.append({"map": map_, "total": len(ms), "kdr": avg(m.kdr for m in ms)})
    out.sort(key=lambda r: r["kdr"], reverse=True)
    return out


def lineup_label(lineup):
    if not lineup:
        return "Sozinho (sem amigos)"
    return " + ".join(sorted(lineup))


def top_lineups(matches, top_n=15):
    groups = {}
    for m in matches:
        key = tuple(sorted(m.lineup))
        groups.setdefault(key, []).append(m)
    rows = []
    for key, ms in groups.items():
        w = sum(1 for m in ms if m.result == "W")
        l = sum(1 for m in ms if m.result == "L")
        d = sum(1 for m in ms if m.result == "D")
        rows.append({
            "lineup": lineup_label(list(key)), "total": len(ms), "w": w, "l": l, "d": d,
            "wr": round(w / len(ms) * 100),
        })
    rows.sort(key=lambda r: r["total"], reverse=True)
    return rows[:top_n]
