import __main__

def get_filename():
    return __main__.__file__.replace(".py", ".txt")

def load():
    return open(get_filename(), 'r').read()

def file_to_lines(a):
    return a.splitlines()

def file_to_ints(a):
    return [int(l) for l in a.splitlines()]