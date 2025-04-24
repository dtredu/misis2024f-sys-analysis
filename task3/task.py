from pathlib import Path
import json,sys,csv,math

script_dir = Path(__file__).parent.resolve()

path_to_data = script_dir / "data.csv"


def run():
    with open(path_to_data, newline='') as raw_file:
        result = main(raw_file.read())
    print(result)


def read_matrix(raw_string: str):
    reader = csv.reader(raw_string.split('\n'))
    matrix = []
    for row in reader:
        matrix.append([int(value) for value in row])
    return matrix


def task(raw_string: str):
    matrix = read_matrix(raw_string)
    entropy = 0
    number = len(matrix)
    for j in range(number):
        for i in range(len(matrix[j])):
            value = matrix[j][i]
            if value > 0:
                # calc H_j_i
                probability = value / (number - 1)
                entropy -= probability * math.log2(probability)
    return entropy


def main(raw_string: str):
    return task(raw_string)


def print_help():
    print("help: python3 task.py")

if __name__ == "__main__":
    if len(sys.argv) > 1 and (set(sys.argv) & set(("-h","--help"))):
        print_help()
        exit(0)
    run()
