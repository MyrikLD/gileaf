#  GiLeaf
A prototype design tool for Nanoleaf-like modular light panels.

## Overview
LabelTool allows you to create, arrange, and connect different shaped light panels in a virtual space, helping you plan your perfect light installation before purchasing physical panels.

## Installation
```
git clone https://github.com/MyrikLD/gileaf
cd labeltool
python main.py
```

## Features

- Multiple panel shapes: Triangles (standard & large), Hexagons, and Controller
- Intuitive panel manipulation (move, rotate, connect)
- Magnetic snap functionality for easy alignment
- Multi-panel selection and movement

## Usage
### Basic Controls

- Middle-click on empty space: Create a new panel (selected type)
- Middle-click on panel: Delete the panel
- Left-click + drag: Move panel(s)
- Mouse wheel: Rotate panel (30° per step)
- Shift + left-click: Select multiple panels

### Panel Connection
Panels automatically connect when their connectable edges are aligned and close enough to each other. Connected panels will move together when any panel in the group is selected.

### Panel Types

- Standard triangle
- Large triangle
- Hexagon
- Controller unit

## Requirements

- Python 3.x
- Tkinter (usually included with Python)

## Known Limitations

- No save/load functionality in current version
- Panel scales are approximate representations of real panels
