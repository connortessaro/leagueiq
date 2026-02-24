# 🧬 League of Legends Match Autopsy

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Riot%20Games%20API-powered-red?logo=riotgames&logoColor=white" alt="Riot Games API" />
  <img src="https://img.shields.io/badge/Database-SQLite-lightblue?logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Status" />
</p>

<p align="center">
  A rule-based post-game analysis system that transforms raw Riot Games match timeline data into structured insights about player decision-making and in-game impact.
</p>

<p align="center">
  Rather than focusing solely on surface-level statistics, the system evaluates <strong>how and when players contributed</strong> throughout a match by analyzing objective participation, fight presence, and involvement during key moments — across both wins and losses.
</p>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Example Output](#example-output)
- [Why I Built This](#why-i-built-this)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Current Status](#current-status)
- [How to Run](#how-to-run)
- [Notes](#notes)

---

## 🔍 Overview

League of Legends Match Autopsy processes match and timeline data from the Riot Games API and converts event-level data into higher-level analytical features.

Instead of relying on metrics such as KDA, damage, or CS alone, the system derives contextual signals from timeline events to evaluate player impact over time. These derived features are then evaluated using explicit rule logic to generate interpretable post-game reports.

> The goal is to move beyond raw statistics and toward understanding *decision-making quality* during critical moments of a match.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📥 **Match Ingestion** | Match and timeline ingestion via Riot Games API |
| 🎞️ **Frame Processing** | Frame-by-frame event processing |
| 🧮 **Feature Generation** | Derived feature generation from timeline events |
| 🎯 **Objective Analysis** | Objective participation analysis (dragons, herald, baron, towers) |
| ⚔️ **Fight Detection** | Fight presence and absence detection |
| 🚨 **Issue Classification** | Severity-based issue classification |
| 📊 **Impact Reports** | Structured post-game impact reports |
| 🏆 **Win/Loss Support** | Supports analysis for both wins and losses |

---

## 📸 Example Output

<p align="center">
  <img width="468" height="433" alt="Example match autopsy report output" src="https://github.com/user-attachments/assets/b3f01ede-8408-4495-b757-3f8d58cabdff" />
</p>

---

## 💡 Why I Built This

Most League analysis tools primarily surface raw post-game metrics — such as KDA, damage dealt, CS, and XP — without interpreting *when* those numbers were accumulated or how players participated during critical moments.

This project was built to explore how raw event streams can be transformed into interpretable signals that reflect player involvement, presence, and decision-making throughout a match.

By analyzing timeline data directly, the system aims to provide insight into *how* a game was played rather than simply summarizing the final scoreboard.

---

## 🏗️ System Architecture

High-level pipeline:

```
User Input
  ↓
Riot Games API
  ↓
Local Database (SQLite)
  ↓
Derived Feature Generation
  ↓
Rule-Based Evaluation Engine
  ↓
Post-Game Match Report
```

Each stage is intentionally separated to support clarity, extensibility, and future expansion of analytical logic.

---

## 📁 Project Structure

```
lol_match_autopsy/
│
├── main.py          # CLI entry point
├── ingest/          # Riot API ingestion pipeline
├── storage/         # SQLite persistence layer
├── features/        # Derived feature generation
├── rules/           # Rule-based evaluation logic
└── report/          # Report formatting and output
```

---

## 🛠️ Tech Stack

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Requests-2CA5E0?style=for-the-badge&logo=python&logoColor=white" alt="Requests" />
  <img src="https://img.shields.io/badge/Riot%20Games%20API-D32936?style=for-the-badge&logo=riotgames&logoColor=white" alt="Riot Games API" />
</p>

---

## 📈 Current Status

Core ingestion, feature generation, and rule evaluation pipelines are complete.

**Planned improvements include:**

- [ ] Champion-specific analysis logic (early-game vs scaling champions)
- [ ] Role-aware performance expectations (jungler vs laner vs support)
- [ ] Deeper comparisons between the player and their opposing laner
- [ ] Database schema refactor to support multiple players per match
- [ ] Visualization of objective timelines and match comparisons

---

## 🚀 How to Run

```bash
python main.py
```

> **Note:** Requires a valid Riot Games API key.

---

## 📝 Notes

> This project is intended for educational and analytical purposes. It is not affiliated with or endorsed by Riot Games.
