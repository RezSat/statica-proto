import sys
from pathlib import Path
from . import parser as st_parser
from .runtime import Runtime

def run_file(path):
    text = Path(path).read_text(encoding="utf-8")
    cmds = st_parser.parse_program(text)
    rt = Runtime()
    rt.execute(cmds)

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m statica.cli path/to/script.sta")
        sys.exit(1)
    run_file(sys.argv[1])

if __name__ == "__main__":
    main()
