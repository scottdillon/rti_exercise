"""
This file taken from https://github.com/icecreammatt/flask-empty
and modified for this project.
"""

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TESTING = True

ADMINS = frozenset(['scott.dillon@gmail.com'])
SECRET_KEY = 'WillWorkForJob'

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = "supercalifragilistic98765"
