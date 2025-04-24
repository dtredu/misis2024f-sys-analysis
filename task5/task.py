from pathlib import Path
import json,sys
from itertools import product

script_dir = Path(__file__).parent.resolve()

path_to_a = script_dir / "a.json"
path_to_b = script_dir / "b.json"
path_to_c = script_dir / "c.json"

def run(path_to_a: str | Path, path_to_b: str | Path):
    with open(path_to_a) as a_file:
        with open(path_to_b) as b_file:
            result = main(a_file.read(), b_file.read())
    print(result)

def build_index(ranking):
    index = {}
    for pos, cluster in enumerate(ranking):
        if isinstance(cluster, list):
            for item in cluster:
                index[item] = pos
        else:
            index[cluster] = pos
    return index

def main(ranking1_json, ranking2_json):
    ranking1 = json.loads(ranking1_json)
    ranking2 = json.loads(ranking2_json)

    index1 = build_index(ranking1)
    index2 = build_index(ranking2)

    contradictions = []

    all_items = set(index1.keys()).union(set(index2.keys()))

    for item1, item2 in product(all_items, repeat=2):
        if item1 != item2:
            pos1_first = index1.get(item1, float('inf'))
            pos2_first = index1.get(item2, float('inf'))
            pos1_second = index2.get(item1, float('inf'))
            pos2_second = index2.get(item2, float('inf'))

            if (pos1_first < pos2_first and pos1_second > pos2_second) or (
                pos1_first > pos2_first and pos1_second < pos2_second
            ):
                contradictions.append(tuple(sorted((item1, item2))))

    contradictions = sorted(set(contradictions))
    return json.dumps(contradictions)

def print_help():
    print('''   help: python3 task.py <path_to_a> <path_to_b>
example: python3 task.py a.json b.json''')

if __name__ == "__main__":
    argc = len(sys.argv)
    if (argc != 1) and (argc < 3 or (set(sys.argv) & set(("-h","--help")))):
        print_help()
        exit(0)
    if len(sys.argv) >= 3:
        path_to_a = sys.argv[1]
        path_to_b = sys.argv[2]
    run(path_to_a,path_to_b)
