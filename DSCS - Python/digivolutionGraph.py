from digimon import Digimon
from digimon import Stage
from enum import Enum
from datetime import datetime


class LoadingState(Enum):
    none = 0
    name_found = 1
    skills_found = 2
    evos_found = 3
    devos_found = 4


graph = {}
shortest_paths = {}

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
    skills = []
    stage = Stage.baby

    for l in range(0, len(lines)):
        if "In-Training" == lines[l]:
            loading_state = LoadingState.none
            stage = Stage.in_training
        elif "Rookie" == lines[l]:
            loading_state = LoadingState.none
            stage = Stage.rookie
        elif "Champion" == lines[l]:
            loading_state = LoadingState.none
            stage = Stage.champion
        elif "Ultimate" == lines[l]:
            break
            loading_state = LoadingState.none
            stage = Stage.ultimate
        elif "Mega" == lines[l]:
            loading_state = LoadingState.none
            stage = Stage.mega
        elif "Super Ultimate" == lines[l]:
            loading_state = LoadingState.none
            stage = Stage.super_ultimate
        elif "Armor" == lines[l]:
            loading_state = LoadingState.none
            stage = Stage.armor

        if loading_state == LoadingState.evos_found:
            if (l + 2) < (len(lines) + 2):
                if "No. " in lines[l+2]:
                    loading_state = LoadingState.none
                    # print("End of evos")
                else:
                    evo_line = lines[l]
                    #if name == "Angewomon":
                    #    print(name, "digivoles into", evo_line)
                    evo_name = evo_line.split(' ')[0]
                    if "\t" in evo_name:
                        evo_name = evo_name.split('\t')[0]
                    if evo_name not in evos:
                        evos.append(evo_name)
        elif loading_state == LoadingState.skills_found:
            if "Level 1 Raw Stats" in lines[l]:
                loading_state = LoadingState.none
            else:
                # print(name, "has skill", lines[l])
                skills.append(lines[l].split('\t')[0])

        if "No. " in lines[l]:
            if name != "Tempmon":
                graph[name] = Digimon(name, digivolutions=evos, skills=skills, stage=stage)
                evos = []
                skills = []

            name_line = lines[l-2]
            name = name_line.split(' ')[0]
            loading_state = LoadingState.name_found
        elif "Digivolves Into" in lines[l]:
            # print("Evos Found!")
            loading_state = LoadingState.evos_found
        elif "Skill Name" in lines[l]:
            loading_state = LoadingState.skills_found

    if l == len(lines) - 1:
        if name != "Tempmon":
            graph[name] = Digimon(name, digivolutions=evos, skills=skills, stage=stage)

    generate_dedigivolutions()
    build_quick_paths()
    generate_shortest_paths()


def generate_dedigivolutions():
    for digi_name in graph:
        results = [d for d in graph.keys() if digi_name in graph[d].digivolutions]
        graph[digi_name].dedigivolutions = results


def print_digimon():
    line = ""
    for i in range(0, 32):
        line += '-'

    for digimon in graph:
        print(graph[digimon])
        print(line)


def print_digimon_path(path):
    output = ""

    for i in range(0, len(path)):
        output += path[i]
        if i < len(path) - 1:
            if path[i + 1] in graph[path[i]].digivolutions:
                output += " ==> "
            elif path[i + 1] in graph[path[i]].dedigivolutions:
                output += " --> "

    print(output)


def find_path(first, last, path=[]):
    path = path + [first]

    if first == last:
        return path

    if first in graph and last in graph:
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


def find_all_paths(start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]

    if start not in graph:
        return []

    if end not in graph:
        return []

    paths = []
    for vertex in graph[start].digivolutions:
        # print("Now finding paths between %s and %s" % (vertex, end))
        if vertex not in path:
            extended_paths = find_all_paths(vertex, end, path)
            for p in extended_paths:
                paths.append(p)

    for vertex in graph[start].dedigivolutions:
        # print("Now finding path between %s and %s" % (vertex, end))
        if vertex not in path:
            extended_paths = find_all_paths(vertex, end, path)
            for p in extended_paths:
                paths.append(p)

    return paths


def find_shortest_path(start, end):
    one_key = "%s => %s" % (start, end)
    two_key = "%s => %s" % (end, start)

    if one_key in shortest_paths:
        return shortest_paths[one_key]

    if two_key in shortest_paths:
        return shortest_paths[two_key][::-1]

    potential_chains = find_shortest_path_helper(start, end)

    if len(potential_chains) > 0:
        path = min(potential_chains, key=len)
        path_key = "%s => %s" % (path[0], path[len(path) - 1])
        shortest_paths[path_key] = path
        return path
    else:
        for start_key in [key for key in shortest_paths if key.startswith("%s =>" % start)]:
            for end_key in [key for key in shortest_paths if key.endswith("=> %s" % end)]:
                end_of_start = start_key.split(" => ")[1]
                start_of_end = end_key.split(" => ")[0]
                potential_chains = potential_chains + find_shortest_path_helper(end_of_start, start_of_end)

        if len(potential_chains) > 0:
            path = min(potential_chains, key=len)
            path_key = "%s => %s" % (path[0], path[len(path) - 1])
            shortest_paths[path_key] = path
            return path

    return None


def find_shortest_path_helper(start, end):
    potential_chains = []
    for start_key in [key for key in shortest_paths if key.startswith("%s =>" % start)]:
        for end_key in [key for key in shortest_paths if key.endswith("=> %s" % end)]:
            end_of_start = start_key.split(" => ")[1]
            start_of_end = end_key.split(" => ")[0]
            combo_key = "%s => %s" % (end_of_start, start_of_end)
            #print("%s ?= %s: %s" % (end_of_start, start_of_end, str(end_of_start == start_of_end)))
            if end_of_start == start_of_end:
                potential_chains.append(shortest_paths[start_key] + shortest_paths[end_key][1::])
            elif combo_key in shortest_paths:
                potential_chains.append(shortest_paths[start_key] + shortest_paths[combo_key][1::] + shortest_paths[end_key][1::])

    return potential_chains


def find_shortest_path_mark_2(start, end):
    should_retire = False
    base_paths = []
    child_paths = []

    if start not in graph or end not in graph:
        return None

    if start == end:
        return [start]

    base_paths.append([start])

    count = 0
    while not should_retire:
        leaf_added = False
        for path in base_paths:
            count += 1
            print("\rProcessing path number: %d" % count)

            leaf_added = False
            if path[0] == start and path[len(path) - 1] == end:
                return path

            potential_leaves = graph[path[len(path) - 1]].digivolutions + graph[path[len(path) - 1]].dedigivolutions
            for leaf in potential_leaves:
                if leaf in graph and leaf not in path:
                    child_paths.append(path + [leaf])
                    leaf_added = True

            if leaf_added:
                for child_path in child_paths:
                    if child_path[0] == start and child_path[len(path) - 1] == end:
                        return child_path

        del base_paths[::]
        base_paths = base_paths + child_paths
        del child_paths[::]

        if not leaf_added:
            should_retire = True

    return None


def find_all_digivolution_paths(digimon, path=[]):
    path = path + [digimon]

    if digimon not in graph:
        return []

    if len(graph[digimon].digivolutions) == 0:
        return [path]

    paths = []
    if len(path) > 1:
        paths.append(path)
    for evo in graph[digimon].digivolutions:
        extended_paths = find_all_digivolution_paths(evo, path)
        for p in extended_paths:
            paths.append(p)

    return paths


def find_all_dedigivolution_paths(digimon, path=[]):
    path = path + [digimon]

    if digimon not in graph:
        return []

    if len(graph[digimon].dedigivolutions) == 0:
        return [path]

    paths = []
    if len(path) > 1:
        paths.append(path)
    for evo in graph[digimon].dedigivolutions:
        extended_paths = find_all_dedigivolution_paths(evo, path)
        for p in extended_paths:
            paths.append(p)

    return paths


def generate_shortest_paths():
    print("Generating all shortest paths")
    total_start = datetime.now()
    for start in graph:
        print("Starting", start)
        begin_time = datetime.now()
        created = 0
        existed = 0
        flipped = 0
        for end in graph:
            if start != end:
                one_key = "%s => %s" % (start, end)
                two_key = "%s => %s" % (end, start)

                # print("Finding path for %s: " % (one_key),)

                if one_key not in shortest_paths and two_key not in shortest_paths:
                    shortest_paths[one_key] = find_shortest_path(start, end)
                    shortest_paths[two_key] = shortest_paths[one_key][::-1]
                    created += 1
                elif two_key in shortest_paths:
                    # print("Reversing %s to use with %s" % (two_key, one_key))
                    shortest_paths[one_key] = shortest_paths[two_key][::-1]
                    flipped += 1
                else:
                    existed += 1

                # print("Found path for", one_key)

        end_time = datetime.now()
        print("Finished %s in %s\nCreated: %d Flipped: %d Exists: %d" % (start, (end_time - begin_time), created, flipped, existed))

    total_end = datetime.now()
    print("Whole operation finished in: ", (total_end - total_start))


def build_quick_paths():
    for digimon in graph:
        # Build all Digivolution Paths (That don't exist)
        paths = find_all_digivolution_paths(digimon)
        for path in paths:
            one_key = "%s => %s" % (path[0], path[len(path) - 1])
            two_key = "%s => %s" % (path[len(path) - 1], path[0])

            if one_key not in shortest_paths:
                shortest_paths[one_key] = path
            else:
                if len(path) < len(shortest_paths[one_key]):
                    shortest_paths[one_key] = path

            if two_key not in shortest_paths:
                shortest_paths[two_key] = path[::-1]
            else:
                if len(path) < len(shortest_paths[two_key]):
                    shortest_paths[two_key] = path[::-1]

        # Build Quickswap Paths
        if len(graph[digimon].digivolutions) > 1:
            for evo_0 in graph[digimon].digivolutions:
                for evo_1 in graph[digimon].digivolutions:
                    if evo_0 != evo_1:
                        path = [evo_0, digimon, evo_1]
                        one_key = "%s => %s" % (path[0], path[len(path) - 1])
                        two_key = "%s => %s" % (path[len(path) - 1], path[0])

                        if one_key not in shortest_paths:
                            shortest_paths[one_key] = path
                        else:
                            if len(path) < len(shortest_paths[one_key]):
                                shortest_paths[one_key] = path

                        if two_key not in shortest_paths:
                            shortest_paths[two_key] = path[::-1]
                        else:
                            if len(path) < len(shortest_paths[two_key]):
                                shortest_paths[two_key] = path[::-1]

        if len(graph[digimon].dedigivolutions) > 1:
            for evo_0 in graph[digimon].dedigivolutions:
                for evo_1 in graph[digimon].dedigivolutions:
                    if evo_0 != evo_1:
                        path = [evo_0, digimon, evo_1]
                        one_key = "%s => %s" % (path[0], path[len(path) - 1])
                        two_key = "%s => %s" % (path[len(path) - 1], path[0])

                        if one_key not in shortest_paths:
                            shortest_paths[one_key] = path
                        else:
                            if len(path) < len(shortest_paths[one_key]):
                                shortest_paths[one_key] = path

                        if two_key not in shortest_paths:
                            shortest_paths[two_key] = path[::-1]
                        else:
                            if len(path) < len(shortest_paths[two_key]):
                                shortest_paths[two_key] = path[::-1]


def is_complete_graph():
    for digimon in graph:
        if len(graph[digimon].digivolutions) == 0 and len(graph[digimon].dedigivolutions) == 0:
            print("%s has no digivolutions or dedigivolutions")
            return False



    return True


def main_app():
    while True:
        print("What option would you like? (You can add args using ',' to break things up.)")
        print("1. Find Digimon Path")
        print("2. Find shortest Digimon path")
        print("3. Search for Digimon by name")
        print("4. Print Digimon Info")
        print("5. Print Digimon Full Digivolutions")
        print("6. Print Digimon Full Digivolutions")
        print("7. Print all Digimon")
        print("8. Find Digimon with Skill")
        print("Enter 'quit' or 'q' to close the program")

        choice = input("Enter a command: ")

        args = choice.split(",")

        if args[0].lower() == 'quit' or args[0].lower() == 'q':
            break
        elif args[0] == '1':
            first = input("Enter the starting Digimon: ")
            second = input("Enter the ending Digimon: ")

            path = find_path(first, second)

            if path is None:
                print("There is no path from %s to %s" % (first, second))
                return

            print("This is the path found to the Digimon:")
            print_digimon_path(path)
        elif args[0] == '2':
            if len(args) == 3:
                start = args[1]
                end = args[2]
            else:
                start = input("Enter the starting Digimon: ")
                end = input("Enter the ending Digimon: ")

            if start not in graph:
                print("%s is not a Digimon that I have on record..." % start)
            elif end not in graph:
                print("%s is not a Digimon that I have on record..." % end)
            else:
                search_start = datetime.now()
                print("Search begins at:", search_start, "...",)
                path = find_shortest_path(start, end)
                search_finish = datetime.now()
                print("completed in:", search_finish - search_start)
                if path is None:
                    print("There is no path from %s to %s" % (start, end))
                else:
                    print("This is the path found to the Digimon:")
                    print_digimon_path(path)
        elif choice == '3':
            search_term = input("Enter the search term: ")
            results = [d for d in graph.keys() if search_term in d]
            output = "The Digimon with that search term in their name are:\n["

            for i in range(0, len(results)):
                output += results[i]
                if i < len(results) - 1:
                    output += ', '

            output += "]"
            print(output)
        elif choice == '4':
            name = input("Enter a Digimon: ")
            if name in graph:
                print(graph[name])
            else:
                print("Please retry with a valid Digimon in this game.")
        elif choice == '5':
            name = input("Enter a Digimon: ")
            if name in graph:
                paths = find_all_digivolution_paths(name)
                for path in paths:
                    print_digimon_path(path)

                print("Total Paths: %d" % len(paths))
            else:
                print("Please retry with a valid Digimon in this game.")
        elif choice == '6':
            name = input("Enter a Digimon: ")
            if name in graph:
                paths = find_all_dedigivolution_paths(name)
                for path in paths:
                    print_digimon_path(path)

                print("Total Paths: %d" % len(paths))
            else:
                print("Please retry with a valid Digimon in this game.")
        elif choice == '7':
            print_digimon()
        elif choice == '8':
            name = input("Enter a skill name: ")
            results = [d for d in graph if name in graph[d].skills]
            print(results)
        else:
            print("Please enter a recognized command")

    print("Thanks for using the program")


if __name__ == "__main__":
    # load_digimon("digimon.txt")
    # load_digimon_ex("digimon_story_cyber_sleuth_evo_guide.txt")
    load_digimon_hyper("digimon_super_file.txt")
    # load_digimon_hyper("digimon_test.txt")
    # print_digimon()
    main_app()


