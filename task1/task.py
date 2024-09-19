import json

def serialize(value,indent=2):
  st = json.dumps(value,indent=indent)
  return st

def main(st):
  j = json.loads(st)
  return j

if __name__ == "__main__":
  st = input("print the json string:\n")
  j = main(st)
  print(j)
