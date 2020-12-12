import md5
import strutils
import sequtils
import sugar

proc sol1(hash: string): int =
    result = 1
    while true:
        let
            concat = hash & intToStr(result)
            value = getMD5(concat)
        if value[0..<5] == "00000":
            break
        else:
            result += 1

proc sol2(hash: string): int =
    result = 1
    while true:
        let
            concat = hash & intToStr(result)
            value = getMD5(concat)
        if value[0..<6] == "000000":
            break
        else:
            result += 1


#assert sol1("abcdef") == 609043
#assert sol1("pqrstuv") == 1048970
dump sol1("yzbqklnj")
dump sol2("yzbqklnj")