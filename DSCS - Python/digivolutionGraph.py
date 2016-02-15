from digimon import Digimon
from enum import Enum

class LoadingState(Enum):
    none = 0
    name_found = 1
    skills_found = 2
    evos_found = 3
    devos_found = 4


graph = {}

def load_digimon(file_name):
    digimon_file = open(file_name, "r")

    print("Loading Digimon from file:", file_name, "...")

    for line in digimon_file.readlines(-1):
        data = line.split(':')

        if len(data) == 3:
            name = data[0]
            digivolutions = data[1].split(',')
            dedigivolutions = data[2].split(',')
            if "\n" in dedigivolutions:
                dedigivolutions.remove("\n")
            digimon = Digimon(name, digivolutions, dedigivolutions)
            graph.append(digimon)
        else:
            print("Failed to load Digimon:", line)

    print("Finished loading Digimon.")


def load_digimon_ex(file_name):
    digimon_file = open(file_name, "r")

    print("Hyper Loading from file:", file_name, "...")
    count = 0


    for line in digimon_file.readlines(-1):
        if ": " in line: # This is a digimon line
            count += 1
            line = line.replace("\n","")
            data = line.split(": ")

            digimon = Digimon(data[0])
            digivolutions = data[1]
            if "\n" in digivolutions:
                digivolutions.replace("\n","")
            digimon.digivolutions = digivolutions.split(', ')
            graph[data[0]] = digimon

    generate_dedigivolutions()


def load_digimon_hyper(file_name):
    loading_state = LoadingState.none

    digimon_file = open(file_name, "r", encoding="UTF-8")

    lines = digimon_file.readlines(-1)

    name = "Tempmon"
    evos = []
    devos = []

    for l in range(0, len(lines)):

        if loading_state == LoadingState.evos_found:
            if "No. " in lines[l+2]:
                loading_state = LoadingState.none
                # print("End of evos")
            else:
                evo_line = lines[l]
                # print(name, "digivoles into", evo_line)
                evo_name = evo_line.split(' ')[0]
                if evo_name not in evos:
                    evos.append(evo_name)

        if "No. " in lines[l]:

            # Unload previous Digimon
            if name != "Tempmon":
                graph[name] = Digimon(name, evos, devos)
                evos = []
                devos = []

            name_line = lines[l-2]
            name = name_line.split(' ')[0]
            loading_state = LoadingState.name_found
        elif "Digivolves Into" in lines[l]:
            # print("Evos Found!")
            loading_state = LoadingState.evos_found

        if l == len(lines) - 1:
            if name != "Tempmon":
                graph[name] = Digimon(name, evos, devos)

    generate_dedigivolutions()


def generate_dedigivolutions():
    for digi_name in graph:
        results = [d for d in graph.keys() if digi_name in graph[d].digivolutions]
        graph[digi_name].dedigivolutions = results


def print_digimon():
    line = ""
    for i in range(0, 32):
        line += '-'

    for digimon in graph:
        print("Key in Graph:", digimon)
        print(graph[digimon])
        print(line)


def find_path(first, last, path=[]):
    path = path + [first]

    if first == last:
        return path

    if first in graph:
        for node in graph[first].digivolutions:
            if node not in path:
                new_path = find_path(node, last, path)
                if new_path:
                    return new_path

        for node in graph[first].dedigivolutions:
            if node not in path:
                new_path = find_path(node, last, path)
                if new_path:
                    return new_path

    return None


def main_app():
    while True:
        print("What option would you like?")
        print("1. Find Digimon Path")
        print("2. Search for Digimon by name")
        print("3. Print Digimon Info")
        print("4. Print all Digimon")
        print("Enter 'quit' or 'q' to close the program")

        choice = input("Enter a command: ")

        if choice.lower() == 'quit' or choice.lower() == 'q':
            break
        elif choice == '1':
            first = input("Enter the starting Digimon: ")
            second = input("Enter the ending Digimon: ")

            path = find_path(first, second)

            if path is None:
                print("There is no path from %s to %s" % (first, second))
            else:
                output = "This is the path found to the Digimon:\n"

                for i in range(0, len(path)):
                    output += path[i]
                    if i < len(path) - 1:
                        if path[i + 1] in graph[path[i]].digivolutions:
                            output += " ==> "
                        elif path[i + 1] in graph[path[i]].dedigivolutions:
                            output += " --> "

                output += ""

                print(output)
        elif choice == '2':
            search_term = input("Enter the search term: ")
            results = [d for d in graph.keys() if search_term in d]
            output = "The Digimon with that search term in their name are:\n["

            for i in range(0, len(results)):
                output += results[i]
                if i < len(results) - 1:
                    output += ', '

            output += "]"
            print(output)
        elif choice == '3':
            name = input("Enter a Digimon: ")
            if name in graph:
                digimon = graph[name]
                print("Name:", digimon.name)
                print("Digivolves to:", digimon.digivolutions)
                print("Dedigivoles to:", digimon.dedigivolutions)
            else:
                print("Please retry with a valid Digimon in this game.")
        elif choice == '4':
            print_digimon()
        else:
            print("Please enter a recognized command")

    print("Thanks for using the program")


if __name__ == "__main__":
    # load_digimon("digimon.txt")
    # load_digimon_ex("digimon_story_cyber_sleuth_evo_guide.txt")
    load_digimon_hyper("digimon_super_file.txt")
    # print_digimon()
    main_app()


