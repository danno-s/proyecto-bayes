#!/usr/bin/python

from datetime import datetime

import json
from src.utils.dataParsingUtils import *
from src.utils.loadConfig import Config

def dataParse():
    sqlPD = sqlWrapper(db='PD')
    sqlPD = sqlWrapper(db='PD')