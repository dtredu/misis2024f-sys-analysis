from pathlib import Path
import json,sys

script_dir = Path(__file__).parent.resolve()

path_to_data = script_dir / "data.json"

def serialize(value,indent=2):
  st = json.dumps(value,indent=indent)
  return st

def main(json_string):
  j = json.loads(json_string)
  return j

if __name__ == "__main__":
  filepath = path_to_data
  if len(sys.argv) > 1:
    filepath = sys.argv[1]
  file_in = open(filepath,'r')
  text_data = file_in.read()
  file_in.close()
  json_data = main(text_data)['nodes']
  print(json_data)
