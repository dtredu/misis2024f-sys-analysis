from pathlib import Path
import json,sys

script_dir = Path(__file__).parent.resolve()

path_to_temp = script_dir / "temp.json"
path_to_heat = script_dir / "heat.json"
path_to_ctrl = script_dir / "ctrl.json"


def run(real_temp: float):
    with open(path_to_temp) as temperature:
        with open(path_to_heat) as heating:
            with open(path_to_ctrl) as control:
                result = main(temperature.read(), heating.read(), control.read(), real_temp)
    print(result)

def membership_function(x, points):
    for (x0, y0), (x1, y1) in zip(points[:-1], points[1:]):
        if x0 <= x <= x1:
            if y0 == y1:
                return y0
            else:
                return y0 + (y1 - y0) * ((x - x0) / (x1 - x0))
    return 0.0


def compute_fuzzy_value(value, fuzzy_sets):
    fuzzy_values = {}
    for term, params in fuzzy_sets.items():
        fuzzy_values[term] = membership_function(value, params)
    return fuzzy_values


def main(temperature_json: str, heating_json: str, control_json: str, t: float):
    temp_sets = json.loads(temperature_json)
    heat_sets = json.loads(heating_json)
    rules = json.loads(control_json)

    temp_fuzzy_values = compute_fuzzy_value(t, temp_sets)

    heat_fuzzy_values = {}
    for rule in rules:
        temp_term, heat_term = rule
        membership_degree = temp_fuzzy_values.get(temp_term)
        if heat_term in heat_fuzzy_values:
            heat_fuzzy_values[heat_term] += membership_degree
        else:
            heat_fuzzy_values[heat_term] = membership_degree

    max_degree = max(heat_fuzzy_values.values(), default=0)
    first_max_term = next((term for term, degree in heat_fuzzy_values.items() if degree == max_degree), None)

    first_max_points = heat_sets[first_max_term]
    xs = [x for x, y in first_max_points if y > 0]
    centroid_value = sum(xs) / len(xs) if xs else 0
    return f"Set to {first_max_term}, value = {centroid_value}"

def print_help():
    print("help: python3 task.py <real_temperature:float>")

temp = 20.0 # default
if __name__ == "__main__":
    if len(sys.argv) > 1 and (set(sys.argv) & set(("-h","--help"))):
        print_help()
        exit(0)
    if len(sys.argv) > 1:
        temp = float(sys.argv[1])
    run(temp)

# python3 task.py run -t temperature.json -h heating.json -c control.json -r 21
