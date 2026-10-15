# Team Organization

## Main responsibilities

### Adrien / `asavidan`

Main focus: gameplay and rendering.

Work included:
- maze rendering and visual wall improvements;
- player movement and buffered direction changes;
- pacgums and super-pacgums;
- collision handling;
- ghost movement, pathfinding and behaviours;
- frightened/respawn gameplay;
- cheat effects;
- level progression support;
- sprites and menu visual polish;
- packaging/testing support.

### Tom / 'todubois'

Main focus: application infrastructure and UI.

Work included:
- configuration loading and validation;
- application/state-machine structure;
- menu, pause, instructions, end and highscore screens;
- highscore persistence and validation;
- shared session/state integration;
- UI flow and application-level error handling.

## Shared work

The following areas were handled together or reviewed by both of us:
- integration of gameplay into the `Playing` state;
- maze-generator integration;
- timer and level progression;
- Makefile and dependency setup;
- packaging with PyInstaller;
- code review, lint fixes and final subject-compliance checks.

## Working method

The team split large features to reduce overlap, then integrated them through the shared state/session interfaces. Important architecture decisions, bugs and deviations from the initial plan were recorded in `ROADMAP.md` and `ARCHITECTURE.md`.

When a blocking issue appeared, the team first reproduced it in isolation, fixed the smallest responsible module, then retested the complete game flow.
