from pathlib import Path
import json,sys,csv,math,io

script_dir = Path(__file__).parent.resolve()

path_to_data = script_dir / "data.csv"



def run():
    with open(path_to_data, newline='') as raw_file:
        result = main(raw_file.read())
    print(result)

def graph_read(raw_string: str):
    reader = csv.reader(raw_string.split('\n'))
    edges = []
    for row in reader:
        edges.append((int(row[0]) - 1, int(row[1]) - 1))

    graph = [[] for i in range(len(edges) + 1)]
    rev_graph = [[] for i in range(len(edges) + 1)]
    for u, v in edges:
        graph[u].append(v)
        rev_graph[v].append(u)
    return graph, rev_graph, len(graph)


def dfs_size_and_parent(graph, size, parent, v, p=-1):
    # size[v] != 0 --> used
    if size[v] != 0:
        return

    size[v] = 1
    parent[v] = p
    for u in graph[v]:
        dfs_size_and_parent(graph, size, parent, u, v)
        size[v] += size[u]


def dfs_depth(graph, depth, v, d=0):
    depth[v] = d
    for u in graph[v]:
        dfs_depth(graph, depth, u, d + 1)


def build_subtrees_size_and_parent(graph, n):
    size = [0] * n
    parent = [-1] * n
    for i in range(n):
        dfs_size_and_parent(graph, size, parent, i)
    return size, parent


def build_depth(graph, root, n):
    depth = [0] * n
    dfs_depth(graph, depth, root)
    return depth


def main(raw_string: str):
    graph, rev_graph, number = graph_read(raw_string)
    print("Result graph: ", graph)

    size, parent = build_subtrees_size_and_parent(graph, number)

    root = parent.index(-1)
    print(f"root = {root+1:d}")

    depth = build_depth(graph, root, number)

    result = []
    for v in range(number):
        # direct sons
        l1 = len(graph[v])

        # only root has no parent
        l2 = 0 if v == root else 1

        # all sons except direct
        l3 = size[v] - len(graph[v]) - 1

        # depth in graph except root
        l4 = max(depth[v] - 1, 0)

        # number of parethingnt sons except root
        l5 = 0 if v == root else len(graph[parent[v]]) - 1

        result.append([l1, l2, l3, l4, l5])

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(result)

    return output.getvalue()


def print_help():
    print("help: python3 task.py")

if __name__ == "__main__":
    if len(sys.argv) > 1 and (set(sys.argv) & set(("-h","--help"))):
        print_help()
        exit(0)
    run()
