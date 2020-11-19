import strutils # (split method)
import sequtils # map on lists
import sugar # lambda syntax + dump macro

# Read data from a text file
let entireFile = readFile("data.txt")
echo entireFile

# Split based on space, and by line
# dump is like echo, but displays also the variable being printed
dump entireFile.splitLines()
echo entireFile.splitLines().map(it => it.split())
let values = entireFile.splitLines().map(it => it.split().map(it => parseInt(it)))
echo values

# Filtering on lists
echo values.map(it => it.filter(it => it > 10))

# Using dicts
import tables
var
  a = {1: "one", 2: "two"}.toTable  # creates a Table
  b = a

dump (a, b)  # output: {1: one, 2: two}{1: one, 2: two}

b[3] = "three"
dump (a, b)  # output: {1: one, 2: two}{1: one, 2: two, 3: three}
dump a == b  # output: false

# Constants (must be known at compile time)
const
    c = 4

dump c # displays 4 = 4

# Procs
# the noSideEffect enforces at compile time that there are indeed no side effects
proc fibonacci(n: int): int {. noSideEffect .} =
  if n < 2:
    result = n
  else:
    result = fibonacci(n - 1) + (n - 2).fibonacci

dump fibonacci(6)

# Define an operator between ` `
let zero = ""
proc `+`(a, b: string): string =
  a & b

proc `*`[T](a: T, b: int): T =
  result = zero
  for i in 0..b-1:
    result = result + a  # calls `+` from line 3

dump("a" * 10 == "aaaaaaaaaa")
dump(3*4)

# templates?

# types
# appending a "*" makes the object usable from outside the file
type
  Animal* = object
    name*, species*: string
    age: int

proc sleep*(a: var Animal) =
  a.age += 1

proc dead*(a: Animal): bool =
  result = a.age > 20

var carl: Animal
carl = Animal(name : "Carl",
              species : "L. glama",
              age : 12)

dump carl
assert(not carl.dead)
for i in 0..10:
  carl.sleep()
assert carl.dead