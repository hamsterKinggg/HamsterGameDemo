# HamsterGameDemo

HamsterGameDemo is an MVP prototype of an interactive narrative game built around a virtual pet (hamster), focusing on story-driven gameplay and video-based interactions.

This project is primarily a **technical and gameplay feasibility demo**, rather than a full production-ready game.

---

## Project Overview

- Platform: **Windows 11 (only)**
- Game type: Interactive narrative / virtual pet
- Core interaction: Button-based choices over real-life video content
- Current stage: **MVP / Demo**

The game uses **HTTP-based video fetching** instead of local video storage.  
Video segments are loaded from a remote server and cached on the client side for playback.

---

## MVP Features

- Basic user login and profile management
- Cloud-based save data (simple save slots)
- 5 pet status values (read & update)
- One complete task chain with branching story choices
- HTTP video loading and prefetching (non-streaming protocol)
- One knowledge-based quiz mini-game
- Simple item system (2–3 items affecting pet status)
- One cosmetic system (swap idle animation/video)

> Performance optimization and full streaming protocols are intentionally out of scope for the MVP.

---

## Development Notes

- This repository is under **active development**
- Architecture and APIs may change frequently
- Code quality is focused on clarity and iteration speed rather than long-term stability

---

## Repository Structure (Planned)
