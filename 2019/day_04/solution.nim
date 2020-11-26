import strutils
import sequtils


const
    bottom: int = 245182
    top: int = 790572

# There must be at least one double (consecutive)
# the numbers should be strictly not decreasing
proc is_valid(password: int): bool =
    let s_password = intToStr(password)
    result = false
    for i in 1..<s_password.len:
        if s_password[i].int < s_password[i-1].int: 
            return false
        if not result: 
            result = s_password[i] == s_password[i-1]

proc is_valid_part2(password: int): bool =
    let s_password = intToStr(password)
    var counts = @[(s_password[0], 1)]
    for i in 1..<s_password.len:
        if s_password[i].int < s_password[i-1].int:
            return false
        if s_password[i] == s_password[i-1]:
            counts[^1][1] += 1
        else:
            counts.add((s_password[i], 1))
    return counts.anyIt(it[1] == 2)


assert is_valid(111111)
assert not is_valid(123450)
assert is_valid(112345)
assert is_valid(123455)
assert not is_valid(123789)

assert 112233.is_valid_part2
assert not 123444.is_valid_part2
assert 111122.is_valid_part2

echo count((bottom..top).mapIt(is_valid(it)), true)
echo count((bottom..top).mapIt(is_valid_part2(it)), true)