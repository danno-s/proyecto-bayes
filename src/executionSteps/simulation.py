"""
Paso 6 (OPCIONAL)
Script para ejecucion del proceso de simulacion de usuarios y nodos.
"""
from src.simulatedData.simulusers import newGenerate
from src.dataParsing.parseSessions import parseSessions


def simulation(generation=False):
    from src.executionSteps.main import start, finish
    start()
    if generation is True:
        print("\n\n...Generating data...\n\n")
        newGenerate()
    #parseSessions(simulation=True)
    finish()

if __name__ == '__main__':
    simulation(1)
