# 🏆 Producing Soccer Insights for a Sports Media Agency

## 📌 Project Context

The **UEFA Champions League** is the pinnacle of European club football. From underdog stories to legendary rivalries, the tournament offers rich analytical opportunities for clubs, fans, and media.

This project explores key performance metrics and patterns from three seasons: **2020, 2021, and 2022**, using match-level data from Snowflake.

---

## 🗃️ Database Information

**Schema Name:** `SOCCER`  
**Tables:** `TBL_UEFA_2020`, `TBL_UEFA_2021`, `TBL_UEFA_2022`  
_All tables share the same structure._

### 📄 Table Columns:

- `$STAGE` – Stage of the match  
- `$DATE` – Match date  
- `$PENS`, `$PENS_HOME_SCORE`, `$PENS_AWAY_SCORE` – Penalty details  
- `$TEAM_NAME_HOME`, `$TEAM_NAME_AWAY` – Teams  
- `$TEAM_HOME_SCORE`, `$TEAM_AWAY_SCORE` – Final scores  
- `$POSSESSION_HOME`, `$POSSESSION_AWAY` – Possession percentage  
- `$TOTAL_SHOTS_HOME`, `$TOTAL_SHOTS_AWAY` – Shot attempts  
- `$SHOTS_ON_TARGET_HOME`, `$SHOTS_ON_TARGET_AWAY` – Shots on target  
- `$DUELS_WON_HOME`, `$DUELS_WON_AWAY` – Duels won  
- `$PREDICTION_TEAM_HOME_WIN`, `$PREDICTION_DRAW`, `$PREDICTION_TEAM_AWAY_WIN` – Win probabilities  
- `$LOCATION` – Stadium name

---

## 📊 Key Analyses and Insights

### 🔥 1. Home Team with Most Goals

**Query Objective:** Sum of `$TEAM_HOME_SCORE` grouped by `$TEAM_NAME_HOME`.

**🧠 Insight:**  
No result was returned – possibly due to data issues or filters excluding all rows.

---

### 🏅 2. Top 10 Teams by Win Percentage (Min 5 Matches)

- `$Bayern Munich$` → **80%**
- `$Manchester City$` → **78.57%**
- `$Chelsea$` → **71.43%**
- `$Liverpool$` → **70%** (20 matches)
- `$Real Madrid$` → **66.67%**

---

### 🏟️ 3. High-Scoring Stadiums (Min 3 Matches)

- `$Nou Camp$` → **5.0 goals/match**
- `$Ibrox Stadium$` → **5.0 goals/match**
- `$Amsterdam Arena$` → **4.67 goals/match**
- `$Stadio San Paolo$` → **4.67 goals/match**
- `$Olimpico$` → **4 matches**, **4.25 avg goals**

---

### 🎯 4. Shot Efficiency (Min 50 Shots)

- `$B. Mönchengladbach$` → **21.33%** conversion  
  - On target: **48.48%**
- `$FC Porto$` → **18.07%**
- `$Bayern Munich$` → **strong performance under both name variations**
- `$Manchester City$` → **198 shots**, **16.16%** conversion

---

### 📅 5. Performance by Competition Stage

- `$Group Matchday 3$` → **3.58 avg goals**
- `$Final$` → **1.0 avg goals**, **75% away wins**
- `$Semi-final 2nd leg$` → **83.33% home wins**
- `$Quarter-final 2nd leg$` → **58.33% draws**

---

### 🔁 6. Comeback Wins (Win Prob < 50%)

- `$Manchester City$` → **87.5%** comeback win rate  
- `$Real Madrid$` → **9 comeback wins (56.25%)**
- `$Liverpool$` → **35.71%** comeback rate

---

### 🏠 vs 🚗 7. Home vs Away Performance

- `$Liverpool Away$` → **2.9 goals/match (29 in 10)**
- `$Man City Home$` → **3.57 goals/match**
- `$Real Madrid$` → **balanced: 26 home, 24 away**
- `$Bayern$` → **4.0 home avg**, limited to 4 matches

---

### ⚽ 8. Scoring by Match Stage

- `$Matchday 6$` → **4.33 avg goals**
- `$Finals$` → **1.0 avg goals**
- `$Quarter/Semi-finals$` → **2.5–3.0 avg goals**
- Variance in group stages:
  - Matchday 3 → **3.58**
  - Matchday 2 → **2.63**

---

## 📈 Overall Insights

- 🇩🇪 **German Power:** Bayern Munich dominates offensive stats  
- 🏴‍♂️ **English Clubs:** Man City & Liverpool excel in goal-scoring and comebacks  
- 🇪🇸 **Spanish Stability:** Real Madrid shows consistent high-level performance  
- ⚔️ **Stage Matters:** Group stages = more goals; finals = tight defenses  
- 🔄 **Comeback Kings:** Man City and Real show elite resilience  
- 🏟️ **Stadium Influence:** Nou Camp, Ibrox, and Olimpico offer goal-heavy games  
- 🎯 **Efficiency vs Volume:** Mönchengladbach = efficient; Man City = relentless
