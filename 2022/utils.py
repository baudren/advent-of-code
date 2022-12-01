import __main__

def get_filename():
    return __main__.__file__.replace(".py", ".txt")

def load():
    return open(get_filename(), 'r').read().strip()

def file_to_lines(a):
    return [l.strip() for l in a.split("\n")]

def file_to_ints(a):
    return [int(l.strip()) for l in a.split("\n") if l.strip()]