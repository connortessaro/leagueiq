# League of Legends Match Autopsy

A rule-based post-game analysis system that transforms raw Riot Games match timeline data into structured insights about player decision-making and in-game impact.

Rather than focusing solely on surface-level statistics, the system evaluates **how and when players contributed** throughout a match by analyzing objective participation, fight presence, and involvement during key moments — across both wins and losses.

---

## Overview

League of Legends Match Autopsy processes match and timeline data from the Riot Games API and converts event-level data into higher-level analytical features.

Instead of relying on metrics such as KDA, damage, or CS alone, the system derives contextual signals from timeline events to evaluate player impact over time. These derived features are then evaluated using explicit rule logic to generate interpretable post-game reports.

The goal is to move beyond raw statistics and toward understanding *decision-making quality* during critical moments of a match.

---

## Features

* Match and timeline ingestion via Riot Games API
* Frame-by-frame event processing
* Derived feature generation from timeline events
* Objective participation analysis (dragons, herald, baron, towers)
* Fight presence and absence detection
* Severity-based issue classification
* Structured post-game impact reports
* Supports analysis for both wins and losses

---

## Example Output

<img width="468" height="433" alt="ss" src="https://github.com/user-attachments/assets/b3f01ede-8408-4495-b757-3f8d58cabdff" />

---

## Why I Built This

Most League analysis tools primarily surface raw post-game metrics — such as KDA, damage dealt, CS, and XP — without interpreting *when* those numbers were accumulated or how players participated during critical moments.

This project was built to explore how raw event streams can be transformed into interpretable signals that reflect player involvement, presence, and decision-making throughout a match.

By analyzing timeline data directly, the system aims to provide insight into *how* a game was played rather than simply summarizing the final scoreboard.

---

## System Architecture

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

## Project Structure

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

## Design Focus

* Transforming raw timeline events into higher-level analytical features
* Separating ingestion, feature generation, and evaluation logic
* Making decision logic explicit and interpretable
* Supporting analysis across both wins and losses

---

## Tech Stack

* Python
* Riot Games API
* SQLite
* Requests

---

## Current Status

Core ingestion, feature generation, and rule evaluation pipelines are complete.

Planned improvements include:

* Champion-specific analysis logic (early-game vs scaling champions)
* Role-aware performance expectations (jungler vs laner vs support)
* Deeper comparisons between the player and their opposing laner
* Database schema refactor to support multiple players per match
* Visualization of objective timelines and match comparisons

---

## How to Run

```bash
python main.py
```

(Requires a Riot Games API key)

---

## Notes

* This project is intended for educational and analytical purposes.
* It is not affiliated with or endorsed by Riot Games.
