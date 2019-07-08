#!/usr/bin/env python3

import sys
import os
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_PATH)

from flask_app import app as application
