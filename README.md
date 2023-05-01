# Laser Tag

## Description

Laser tag is a game in which players shoot lasers at each other to earn points for themselves or their team. There are several game modes such as: team, solo, elimination...

This game is a multiplayer laser tag game that uses raycasting to simulate a 3D environment.

> **Note**
> The game is currently under development and some of its features may not be completely working nor implemented yet.

## Roadmap

- [X] Entity movement
- [X] Standalone server
- [X] Multiplayer
- [X] Authoritative Server
- [ ] Playable laser tag
- [ ] Raycasting
- [ ] Vectorial map
- [ ] Textures
- [ ] Controller support
- [ ] Menu and settings screen
- [ ] Audio
- [ ] More laser tag game modes

## Prerequisites

- [Python](https://www.python.org/) (>= 3.10)
- [Pip](https://pypi.org/project/pip/)

## Installation

### Create a virtual environment

```bash
python3 -m venv .venv
```

### Activate the virtual environment

Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.\.venv\Scripts\activate
```

### Install the dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Run the game

```bash
python -m laser_tag
```

### Run the standalone server

```bash
python -m laser_tag.network.Server [port] [debug]
```

## Build

```bash
sh build.sh
```
