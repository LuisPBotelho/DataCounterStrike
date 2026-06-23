# Season 4 Analysis — Insights and Conclusions

Analysis of the **229 matches** logged in the `Season 4 CS.xlsx` spreadsheet,
generated from data processed by the CS Season Dashboard. The goal here isn't
to repeat numbers (the dashboard already shows those live), but to
**interpret the patterns** in the data and surface actionable conclusions.

> Where the sample size is small (few games with a specific friend or
> lineup), this is flagged explicitly — a small number of matches produces
> unstable percentages that shouldn't be read as statistical fact.

---

## TL;DR — key takeaways

1. **Overall win rate of 50.2%** (115W-105L-9D) — a balanced season, with no
   clear trend of dominance.
2. **Inferno is your worst map by win rate (37%) but your best by KDR
   (1.33)** — you play *well individually* on this map, but the team loses.
   This is the strongest signal of a tactical/team problem, not a mechanical one.
3. **Playing solo (58.8% WR) beats any 1- or 2-friend combination** — the
   performance "dip" sits specifically in duos, not in playing alone.
4. **The HAMMER + LEO duo sits at 35% WR (the worst recurring lineup)**, but
   the HAMMER + LEO + PILOTO WILLY trio climbs to 53%, and LEO + PILOTO
   WILLY (without HAMMER) reaches 60%. The common denominator behind the
   drop in performance is specifically that duo.
5. **Your KDR has been declining over the season (1.49 → ~1.00) while win
   rate has stayed stable (~50-52%)** — you're getting fewer frags per
   death, but winning at the same rate. A possible sign of tougher opponents
   or a shift in playstyle (more support/objective-oriented, fewer frags).
6. **KDR isn't destiny**: 25% of wins happened with KDR < 1.0, and 32% of
   losses happened with KDR ≥ 1.0. Match outcome depends more on the team
   than on your isolated individual performance.

---

## 1. Overview

| Metric | Value |
|---|---|
| Matches | 229 |
| Wins / Losses / Draws | 115 / 105 / 9 |
| Overall win rate | **50.2%** |
| Avg K | 16.5 |
| Avg D | 15.5 |
| Avg A | 4.7 |
| Avg KDR | 1.23 |
| Avg PTS | 43.1 |
| Avg placement | 2.54 |
| % of matches finishing 1st | 29.7% |
| % of matches finishing last | 13.1% |

Almost half of all matches end with you finishing 1st or 2nd on the
scoreboard (combined, that's over 50%) — meaning individually you outperform
your own team in most matches, regardless of the final result.

---

## 2. Map analysis

| Map | Matches | Win Rate | Avg KDR |
|---|---|---|---|
| DUST II | 18 | **61%** | 1.22 |
| ANUBIS | 17 | **59%** | 1.15 |
| NUKE | 33 | 58% | 1.24 |
| MIRAGE | 74 | 53% | 1.15 |
| OVERPASS | 31 | 48% | 1.31 |
| ANCIENT | 13 | 38% | 1.31 |
| **INFERNO** | 43 | **37%** | **1.33** |

### The Inferno paradox

Inferno is the map with the **second-highest volume** after Mirage (43
matches — a large enough sample to not be noise) and has the **best KDR of
the season (1.33)** — yet it's also the **worst map by win rate (37%)**,
with 0 draws across 43 games (you either win or lose outright). This
disconnect between "I played well individually" and "the team lost" is the
single most actionable finding in this analysis: the problem on Inferno
doesn't appear to be aim/mechanics — it's round execution (economy, map
control, takes), because your personal numbers there are strong.

Worth comparing to **Ancient**, the second-worst map by WR (38%) which also
has a high KDR (1.31) — the same pattern repeats at a smaller scale (13
matches, a more limited sample).

### The good maps

Dust II and Anubis lead in win rate (61% and 59%), but with smaller samples
(18 and 17 matches) — a clear positive direction, but worth watching whether
the percentage holds with more games. Nuke (33 matches, 58% WR) is the
"good" map with the more reliable sample size.

---

## 3. Result vs. individual performance (K/D/A/KDR)

| Result | n | Avg K | Avg D | Avg KDR | Avg PTS |
|---|---|---|---|---|---|
| Win (W) | 115 | 17.7 | 13.4 | **1.59** | 46.2 |
| Loss (L) | 105 | 14.4 | 17.2 | **0.84** | 37.7 |
| Draw (D) | 9 | 25.7 | 21.7 | 1.20 | 66.3 |

An expected pattern (wins have nearly double the KDR of losses), but the
standout data point is **draws**: average K and D spike (25.7/21.7, well
above the overall average of 16.5/15.5). Draws in this spreadsheet (scores
like 15x15) are matches that went to *overtime* — longer games, more trades,
more frags on both sides. This confirms that the season's 9 draws were,
statistically, the most "contested/epic" games.

---

## 4. Friend analysis

| Friend | Matches | Win Rate | Avg K | Avg KDR |
|---|---|---|---|---|
| **JÃO** | 19 | **63%** | 16.3 | 1.49 |
| LEO | 127 | 54% | 17.3 | 1.20 |
| PILOTO WILLY | 101 | 53% | 17.0 | 1.17 |
| NOT | 53 | 53% | 15.2 | 1.01 |
| ERROR | 21 | 52% | 16.6 | 1.08 |
| LAKES | 74 | 49% | 15.4 | 1.13 |
| **HAMMER** | 114 | **44%** | 17.1 | 1.30 |

*(Friends with fewer than 10 matches are omitted from this table for
insufficient sample size — GABEN, ARAGON, MANZA, etc. each have 4-7 games
and range from 0% to 67% WR, which is statistically expected with that
little data and shouldn't be read as a real signal.)*

### The HAMMER case

HAMMER is your **second most frequent teammate** (114 matches, behind only
LEO) and has by far the **worst win rate among teammates with a large
sample (44%)** — despite having a solid personal KDR (1.30, the
second-best in the group). In other words: this isn't a case of "HAMMER
plays poorly," it's a case of **team outcome when he's present**. This ties
directly into the lineup findings below.

### JÃO is your best teammate with a meaningful sample

63% WR over 19 matches — a smaller volume than the others at the top, but
consistent enough to not be pure noise, and the KDR alongside him (1.49) is
also the second-highest among all friends. Worth playing more with him to
confirm whether the number holds.

---

## 5. Lineups: it's the combination, not the individual

This is the most important analysis for answering "who should I play with."

| Lineup | Matches | Win Rate |
|---|---|---|
| LEO + PILOTO WILLY | 15 | **60%** |
| HAMMER + LAKES + LEO + PILOTO WILLY (full squad) | 9 | **67%** |
| LAKES + NOT | 8 | 62% |
| Solo (no friends) | 17 | **59%** |
| HAMMER + LEO + PILOTO WILLY + VAQUEIRO | 7 | 57% |
| HAMMER + LEO + PILOTO WILLY (trio) | 19 | 53% |
| LAKES (alone among friends, without the others) | 17 | 47% |
| **HAMMER + LEO (duo)** | 17 | **35%** |
| NOT (alone among friends) | 10 | 30% |

### The HAMMER + LEO duo is the specific weak point

The clearest data point in the entire analysis: **HAMMER + LEO as an
isolated duo sits at 35% WR over 17 matches** — worse than playing solo. But
look at the progression:

- HAMMER + LEO (duo): **35%**
- HAMMER + LEO + PILOTO WILLY (trio): **53%**
- LEO + PILOTO WILLY (without HAMMER): **60%**
- HAMMER + LAKES + LEO + PILOTO WILLY (full squad): **67%**

Adding PILOTO WILLY to the HAMMER+LEO duo recovers almost 20 percentage
points of win rate, and removing HAMMER from the equation entirely (leaving
just LEO + PILOTO WILLY) is even better. This strongly suggests that **the
HAMMER+LEO duo, without a third player, has some composition/communication/
coordination issue** that disappears as soon as the group grows — it's not
"HAMMER is bad" or "LEO is bad" individually (LEO has a 54% overall WR, the
second-best in the group), it's specifically **the combination of the two
alone**.

### Solo beats most small combinations

Playing solo (no friends at all) has a 58.8% WR — trailing only the full
squad and a few successful 3-player combinations. Cross-referencing with the
group-size table (section 6), it's clear the issue isn't "playing with
friends in general," but rather **specific poorly-matched duos** dragging
down the "1-2 friends" average.

---

## 6. Group size (how many friends per match)

| Group size | Matches | Win Rate | Avg KDR |
|---|---|---|---|
| Solo (0 friends) | 17 | **58.8%** | 1.16 |
| 1 friend | 43 | 48.8% | 1.25 |
| 2 friends | 56 | **46.4%** | 1.37 |
| 3 friends | 53 | 52.8% | 1.08 |
| 4+ friends (squad) | 60 | 50.0% | 1.25 |

A "U" shape: win rate **drops** when entering a 1-2 friend duo/trio (46-49%)
and **recovers** from 3 friends onward (52.8%) — but personal KDR follows
the opposite path, peaking exactly when the group is small (2 friends: KDR
1.37, the highest in the table). In groups of 2, you individually play very
well (more frags), but the team loses more — another signal that the
bottleneck is small-squad coordination, not mechanics.

---

## 7. Evolution over the season

| Match block | Win Rate | Avg K | Avg KDR |
|---|---|---|---|
| 1–50 | 52.0% | 17.4 | **1.49** |
| 51–100 | 44.0% | 17.9 | 1.34 |
| 101–150 | 52.0% | 15.8 | 1.08 |
| 151–200 | 52.0% | 16.2 | 1.15 |
| 201–229 | 51.7% | 14.3 | **1.00** |

Two things are happening at once:

- **Win rate**: dropped in the second block (44%) and has since stabilized
  around ~52% — no consistent upward or downward trend in the final result.
- **KDR**: declines almost monotonically, from 1.49 at the start of the
  season to 1.00 in the most recent block — nearly a 33% drop in average
  individual performance.

The combination of these two curves — **stable win rate + declining KDR** —
is the most interesting pattern in the entire dataset: you're proportionally
getting fewer frags per death as the season goes on, but it isn't costing
you wins. The most likely hypotheses (not verifiable from this data alone,
but worth investigating): (a) opponent skill level increased (higher rank =
harder trades), (b) a shift in in-game role (less entry-fragging, more
objective/support play that generates fewer kills but wins more rounds), or
(c) simple regression to the mean after a statistically "hot" start to the
season (a 1.49 KDR is well above the overall average of 1.23).

---

## 8. Streaks

- Longest win streak: **7**
- Longest loss streak: **6**
- 3+ win streaks: 16 occurrences
- 3+ loss streaks: 14 occurrences

A similar volume of good and bad streaks (16 vs. 14) is further evidence of
a balanced season, without prolonged tilt or an extended dominant phase —
the game's inherent variance appears to be the dominant factor, more so than
an extended period of much better or worse form.

---

## 9. KDR doesn't determine the outcome

- **25.2% of wins (29 of 115)** happened with an individual KDR **below
  1.0** — meaning roughly 1 in 4 wins, you died more than you killed, but
  the team won anyway.
- **32.4% of losses (34 of 105)** happened with an individual KDR **at or
  above 1.0** — in nearly 1 in 3 losses, you had a positive kill/death
  differential and the team still lost.

This numerically reinforces what the map and lineup sections already
suggested: **match outcome is more tied to team dynamics than to your
isolated individual performance.** In CS, this typically points to factors
beyond raw K/D — round economy, team positioning, communication, and the
specific "chemistry" of whoever you're playing with (as shown in section 5).

---

## 10. Practical recommendations

1. **Review your Inferno tactics.** Your personal numbers there are the
   best of the season — the problem isn't aim, it's round/team execution.
   Worth reviewing 2-3 Inferno losses specifically.
2. **Avoid the HAMMER+LEO duo in isolation** (or, if playing with both,
   bring in a third — PILOTO WILLY has already demonstrably fixed the
   problem, raising WR from 35% to 53-60%).
3. **Prioritize LEO + PILOTO WILLY** (with or without the full squad) as a
   base pairing — it's the combination with the best consistent return and
   a meaningful sample (15 matches at 60%, rising to 67% with the full
   squad).
4. **Play more with JÃO** — best WR among friends with a reasonable sample
   (63% over 19 matches), though still not quite enough data to be certain.
5. **Keep an eye on the KDR decline** over the next blocks of matches — if
   win rate starts dropping too, it's a sign the dip in individual
   performance is no longer being offset by the team.

---

*Generated from `Season 4 CS.xlsx` data processed by the CS Season Dashboard
(`cs_data.py`). All numbers can be verified interactively by filtering the
dashboard itself for the same maps/friends/lineups referenced here.*
