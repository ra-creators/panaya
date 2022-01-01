import sys, os

INTERP = "/home/panaya/repositories/panaya/venv/bin/python3"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

from panaya.wsgi import application
