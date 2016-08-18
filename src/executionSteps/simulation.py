"""
Paso 6 (OPCIONAL)
Script para ejecución del proceso de simulación de usuarios y nodos.
"""
from src.simulatedData.simulusers import newGenerate as generate
from src.dataParsing.parseSessions import parseSessions


def simulation(generation=False):

    if generation is True:
        print("\n\n...Generating data...\n\n")
        generate()
    parseSessions(simulation=True)


if __name__ == '__main__':
    simulation(1)
