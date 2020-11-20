import strutils
import sequtils
import sugar

let modules = readFile("data.txt").splitLines().filter(it => it != "").map(it => parseInt(it))

proc mass(module_mass: int): int =
    return (module_mass div 3) - 2

proc full_mass(module_mass: int): int =
    var module_mass = module_mass
    var fuel_mass = 0
    while true:
        let new_mass = mass(module_mass)
        if new_mass < 0:
            return fuel_mass
        else:
            fuel_mass += new_mass
            module_mass = new_mass

let
    sol1 = modules.map(module_mass => mass(module_mass)).foldl(a + b)
    sol2 = modules.map(module_mass => full_mass(module_mass)).foldl(a + b)

dump sol1
dump sol2