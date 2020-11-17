import strutils # split
import sequtils # map on lists
import sugar # lambda syntax + dump macro

# Read data from a text file
let entireFile = readFile("data.txt")
echo entireFile

# Split based on space, and by line
dump entireFile.splitLines()
echo entireFile.splitLines().map(it => it.split())
let values = entireFile.splitLines().map(it => it.split().map(it => parseInt(it)))
echo values

# Filtering on lists
echo values.map(it => it.filter(it => it > 10))

# Using dicts

# Constants (must be known at compile time)

# Procs

# templates