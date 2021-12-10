score = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

complete_score = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

compl = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

class Chunk:
    representation = ''
    opened_char = []
    valid = True
    finished = False

    def __init__(self):
        self.opened_char = []

    def open(self, character):
        self.opened_char.append(character)
        self.representation += character
    
    def close(self, character):
        self.valid = False
        if character == ')' and self.opened_char[-1] == '(':
            self.valid = True
        elif character == ']' and self.opened_char[-1] == '[':
            self.valid = True
        elif character == '}' and self.opened_char[-1] == '{':
            self.valid = True
        elif character == '>' and self.opened_char[-1] == '<':
            self.valid = True
        self.representation += character
        self.opened_char.pop()
        if len(self.opened_char) == 0:
            self.finished = True
    
    def completion(self):
        return ''.join([compl[char] for char in self.opened_char[::-1]])

def sol1(data):
    errors = []
    for line in data:
        chunk = Chunk()
        for char in line:
            if char in '([{<':
                if chunk.finished:
                    chunk = Chunk()
                chunk.open(str(char))
            else:
                chunk.close(str(char))
                if not chunk.valid:
                    errors.append(str(char))
                    break
    return sum([score[e] for e in errors])

def sol2(data):
    incomplete = []
    for line in data:
        chunk = Chunk()
        for char in line:
            if char in '([{<':
                if chunk.finished:
                    chunk = Chunk()
                chunk.open(str(char))
            else:
                chunk.close(str(char))
                if not chunk.valid:
                    break
        else:
            if not chunk.finished:
                incomplete.append(chunk)
    scores = []
    for chunk in incomplete:
        score = 0
        for char in chunk.completion():
            score = score * 5 + complete_score[char]
        scores.append(score)
    scores.sort()
    return scores[len(scores)//2]


if __name__ == "__main__":
    data = [e.strip() for e in open('day10.txt').readlines()]
    test = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".split("\n")
    assert sol1(test) == 26397
    print(sol1(data))
    assert sol2(test) == 288957
    print(sol2(data))