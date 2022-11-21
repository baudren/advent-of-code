import __main__

def get_filename():
    return __main__.__file__.replace(".py", ".txt")


def load_lines():
    return [l.strip() for l in open(get_filename(), 'r').readlines() if l.strip()]

def load_string():
    return open(get_filename(), 'r').read().strip()
