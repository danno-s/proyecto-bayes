from src.simulatedData.simulusers import generate
from src.dataParsing.parseSessions import parseSessions
import json

def simulation(generation = False):
    if generation is True:
        print("\n\n...Generating data...\n\n")
        with open("simulConfig.json", "r") as f:
            file = f.read()
        generate(json.loads(file))

    parseSessions(simulation=True)


if __name__ == '__main__':
    simulation()