#!/usr/bin/python
# -*- coding: utf-8 -*-

from src.dataParsing.DataParser import DataParser

def dataParse():
    """Extrae datos desde capture_table y los guarda en nodes en un formato adecuado

    Returns
    -------

    """
    dp = DataParser()

    dp.parseData()


if __name__ == '__main__':
    dataParse()
