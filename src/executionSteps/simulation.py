"""
Paso 6 (OPCIONAL)
Script para ejecucion del proceso de simulacion de usuarios y nodos.
"""
from src.simulatedData.simulusers import newGenerate, cleanDB
from src.dataParsing.parseSessions import parseSessions


def simulation(generation=False):
    from src.executionSteps.main import start, finish
    start()
    if generation:
        print("\n\n...Generating data...\n\n")
        cleanDB()
        newGenerate()
    parseSessions(simulation=generation)
    finish()

if __name__ == '__main__':
    simulation(1)
