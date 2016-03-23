from src.simulatedData.simulusers import generate
from src.dataParsing.parseSessions import parseSessions

def simulation(generation = False):
    if generation is True:
        print("\n\n...Generating data...\n\n")
        generate()
    parseSessions(simulation=True)


if __name__ == '__main__':
    simulation()