# Laser Tag

## Description

Multiplayer laser tag game in Python with raycasting.

Host and join LAN parties.

Team up or compete with your friends in different game modes.

Shoot players to score points.

> [!NOTE]
> This is a beta version of the game. Some features may not be fully functional.

## Prerequisites

- [Python](https://www.python.org) (>= 3.10)
- [Pip](https://pypi.org/project/pip)

## Installation

### Python virtual environment (optional)

#### Create

```shell
python -m venv .venv
```

#### Activate

Linux

```shell
source .venv/bin/activate
```

Windows

```shell
.venv\Scripts\activate
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

### Run the standalone server (using Docker)

```shell
docker compose up --build
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
