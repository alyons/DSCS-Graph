from digimon import Digimon

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

    for digi_name in graph:
        results = [d for d in graph.keys() if digi_name in graph[d].digivolutions]
        print(digi_name, "digivolves from", results)
        graph[digi_name].dedigivolutions = results

    print("Digimon found:", count)

def print_digimon():
    line = ""
    for i in range(0, 32):
        line += '-'

    for digimon in graph:
        print(digimon)
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
        else:
            print("Please enter a recognized command")

    print("Thanks for using the program")


if __name__ == "__main__":
    # load_digimon("digimon.txt")
    load_digimon_ex("digimon_story_cyber_sleuth_evo_guide.txt")
    # print_digimon()
    main_app()


