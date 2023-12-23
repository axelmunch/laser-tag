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
- [X] Playable laser tag
- [X] Raycasting
- [X] Vectorial map
- [ ] Textures
- [ ] Controller support
- [ ] Menu and settings screen
- [ ] Audio
- [ ] More laser tag game modes

## Prerequisites

- [Python](https://www.python.org/) (>= 3.10)
- [Pip](https://pypi.org/project/pip/)

## Installation

### Python virtual environment (optional)

#### Create

```shell
python3 -m venv .venv
```

#### Activate

Linux

```shell
source .venv/bin/activate
```

Windows

```shell
.\.venv\Scripts\activate
```

### Install the dependencies

```shell
pip install -r requirements.txt
```

## Usage

### Run the game

```shell
python -m laser_tag
```

### Run the standalone server

```shell
python -m laser_tag.network.Server [port] [debug]
```

## Build

Linux

```shell
./build.sh
```

Windows

```shell
build
```
