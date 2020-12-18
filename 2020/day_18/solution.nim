import strutils
import sugar
import tables
import sequtils
import re
import strformat

var data = readFile("data.txt").split("\n")
let parens = re".*?\((.*?)\).*?"
let sub = re"\(([^())]*?)\)"

let pluses = re".*?(\d+ \+ \d+).*?"
let sub_pluses = re"(\d+ \+ \d+)"

proc evaluate(line: string): int =
    # evaluate nested expressions
    var expression = line
    while expression =~ parens:
        let (min, max) = findBounds(expression, sub, matches, 0, 1000)
        if (min, max) != (-1, 0):
            expression = expression[0..<min] & evaluate(matches[0]).intToStr & expression[max+1..^1]
    var operation = ""
    var number: int
    for elem in expression.split(" "):
        case elem:
            of "*":
                operation = "*"
            of "+":
                operation = "+"
            else:
                number = elem.strip.parseInt
                if result != 0:
                    if operation == "+":
                        result += number
                    else:
                        result *= number
                else:
                    result = number


proc evaluate2(line: string): int =
    # evaluate nested expressions
    var expression = line
    while expression =~ parens:
        let (min, max) = findBounds(expression, sub, matches, 0, 1000)
        if (min, max) != (-1, 0):
            expression = expression[0..<min] & evaluate2(matches[0]).intToStr & expression[max+1..^1]
    # evaluate all + and replace by result
    while expression =~ pluses:
        let (min, max) = findBounds(expression, sub_pluses, matches, 0, 1000)
        if (min, max) != (-1, 0):
            expression = expression[0..<min] & evaluate(matches[0]).intToStr & expression[max+1..^1]
    evaluate(expression)


assert evaluate("1 + 2 * 3 + 4 * 5 + 6") == 71
assert evaluate("1 + (2 * 3) + (4 * (5 + 6))") == 51
echo foldl(data.map(evaluate), a+b)
assert evaluate2("2 * 3 + (4 * 5)") == 46
assert evaluate2("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
assert evaluate2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
assert evaluate2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340
assert evaluate2("1 + (2 * 3) + (4 * (5 + 6))") == 51

echo foldl(data.map(evaluate2), a+b)