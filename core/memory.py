import json
import os

MEM_PATH = "memory.json"


def load_memory():
    if os.path.exists(MEM_PATH):
        return json.load(open(MEM_PATH))
    return []


def save_memory(entry):
    mem = load_memory()
    mem.append(entry)

    json.dump(mem, open(MEM_PATH, "w"), indent=4)
