# League of Legends Match Autopsy

**Post-game analysis system that evaluates player participation, objective involvement, and inferred match impact throughout a match.**

---

## Overview

League of Legends Match Autopsy processes match & timeline data from the Riot Games API to generate structured insights about a player’s in-game impact.

Instead of focusing only on match stats, the system evaluates **how and when players contributed**, including objectives, fights, and presence during major moments, across both wins and losses.

---

## Features

* Match timeline ingestion via Riot Games API
* Frame-by-frame event processing
* Objective participation analysis (dragons, herald, baron, towers)
* Fight presence and absence detection
* Severity-based issue classification
* Structured post-game reports
* Supports analysis for wins and losses

---

## Example Output

<img width="468" height="433" alt="ss" src="https://github.com/user-attachments/assets/b3f01ede-8408-4495-b757-3f8d58cabdff" />

---

## Why I Built This

Most League analysis tools surface raw post-game metrics — such as KDA, damage, CS, and XP — but do not apply structured rulesets to classify player impact or evaluate the impact of player actions and participation during key moments.

This project was built to explore decision-making quality by analyzing when players were involved in major moments of a match and how their presence, or absence, influenced the outcome.

The goal is to transform raw match data & timeline events into actionable insights rather than surface-level statistics.

---

## How It Works

High-level pipeline:

```
User Input
  ↓
Riot API
  ↓
Local Database
  ↓
Derived Feature Generation
  ↓
Rules Engine
  ↓
Match Report
```

---

## Tech Stack

* Python
* Riot Games API
* SQLite
* Requests
---

## Project Structure

```
lol_match_autopsy/
│
├── main.py
├── features/
├── ingest/
├── report/
├── rules/
└── storage/
```
---

## Current Status

Status: **Core functionality complete; additional features in progress**

Planned improvements:
* Champion-specific analysis logic (e.g., scaling champions vs early-game champions)
* Deeper comparisons between the player and their opposing laner
* Role-aware performance expectations (jungler vs laner vs support)
* Database schema refactor to support storing and analyzing multiple players per match

---

## How to Run

```
python main.py
```

(Requires a Riot API key)

---

## Notes
* This project is intended for educational and analytical purposes.
* It is not affiliated with or endorsed by Riot Games.
