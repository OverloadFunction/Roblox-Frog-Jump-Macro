# Frog Jump Script for Roblox

---

## Overview

This Python script automates a "frog jump" movement sequence in Roblox using keyboard and mouse input simulation. It is designed to demonstrate programmatic input control and automation techniques primarily for educational purposes.

The script performs the following steps when triggered:

- Simulates pressing the **S** key to crouch briefly.
- Holds the **Space** key to jump.
- Simulates pressing **W** to move forward mid-jump.
- Performs a rapid 180-degree flick using mouse movement.
- Holds the jump key during the entire sequence for smooth action.

---

## Features

- Custom mouse movement simulation using Windows API (`ctypes`) for smooth directional flicks.
- Keyboard input simulation via the `keyboard` Python package.
- Hotkeys for easy triggering (`F` for frog jump, `Esc` to exit).
- Cross-platform terminal clearing on startup.
- Checks for required Python packages and gracefully exits if dependencies are missing.
- Console output with ASCII banner and user prompts.

---

## Requirements

- **Python 3.6+**
- Windows OS (uses Windows API calls for mouse input simulation)
- Python package: [`keyboard`](https://pypi.org/project/keyboard/)

---

## Installation

1. Ensure Python 3.6 or newer is installed on your system.
2. Install the required package:
   ```bash
   pip install keyboard
