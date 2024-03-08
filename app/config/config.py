from pathlib import Path

BASEDIR = Path(__file__).absolute().parent.parent.parent
STATIC = BASEDIR.joinpath("static")

LOGPATH = BASEDIR.joinpath("log")
