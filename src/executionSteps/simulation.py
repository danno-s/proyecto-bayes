"""
Paso 6 (OPCIONAL)
Script para ejecucion del proceso de simulacion de usuarios y nodos.
"""
from src.simulatedData.simulusers import generate
from src.dataParsing.parseSessions import parseSessions
from src.executionSteps.main import start,finish

def simulation(generation=False):
    start()
    if generation is True:
        print("\n\n...Generating data...\n\n")
        generate()
    parseSessions(simulation=True)
    finish()

if __name__ == '__main__':
    simulation(1)
