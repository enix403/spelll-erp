#!/usr/bin/env python
import sys
from pathlib import Path

if __name__ == '__main__':
    sys.path.append(str(Path(__file__).parent.parent.resolve()))
    from app.bootstrap.configmanager import ConfigManager

    ConfigManager.load_config()
    argc = len(sys.argv)
    if argc == 2:
        print(ConfigManager.get(sys.argv[1]))
    else:
        print("Invalid Usage")
        print("Usage: getconfig.py key")
