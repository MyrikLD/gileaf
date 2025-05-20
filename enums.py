from enum import auto, IntEnum, IntFlag


class ConnState(IntEnum):
    EMPTY = 0
    CONNECTED = 2
    POWERED = 3


class StateEnum(IntFlag):
    Shift = auto()
    Lock = auto()
    Control = auto()
    Mod1 = auto()
    Mod2 = auto()
    Mod3 = auto()
    Mod4 = auto()
    Mod5 = auto()
    Button1 = auto()
    Button2 = auto()
    Button3 = auto()
    Button4 = auto()
    Button5 = auto()


class MouseButton(IntEnum):
    LEFT = 1
    RIGHT = 2
