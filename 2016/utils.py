import __main__

def get_filename():
    return __main__.__file__.replace(".py", ".txt")

def load():
    return open(get_filename(), 'r').read()

def write_to_file(data):
    with open(get_filename(), 'w') as data_file:
        data_file.write(data.strip())

def file_to_lines(a):
    return a.splitlines()

def file_to_ints(a):
    return [int(l) for l in a.splitlines()]

def line_to_ints(a):
    return [int(l.strip()) for l in a.split(",")]

def line_to_str(a):
    return [l.strip() for l in a.split(",")]
