# memory.py

previous_objects = set()

def update_memory(new_objects):
    global previous_objects
    previous_objects = new_objects

def get_previous_objects():
    return previous_objects
