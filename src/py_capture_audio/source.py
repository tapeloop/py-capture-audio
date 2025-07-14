""" module for identifying and handling source of audio input """

import enum
import platform

class Source(enum.Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    UNDEFINED = "undefined"


def get_source() -> Source:
    system = platform.system()

    if system == "Windows":
        return Source.WINDOWS
    elif system == "Linux":
        return Source.LINUX
    else:
        return Source.UNDEFINED
