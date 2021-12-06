import re

def sol1(data, days):
    school = {}
    for fish in data:
        if fish in school:
            school[fish] += 1
        else:
            school[fish] = 1
    for day in range(days):
        school = {
            8: school.get(0, 0),
            7: school.get(8, 0),
            6: school.get(0, 0) + school.get(7, 0),
            5: school.get(6, 0), 
            4: school.get(5, 0),
            3: school.get(4, 0),
            2: school.get(3, 0),
            1: school.get(2, 0),
            0: school.get(1, 0),
        }
    return sum(school.values())

if __name__ == "__main__":
    data = [int(e) for e in open('day06.txt', 'r').readlines()[0].split(",")]
    test = [int(e) for e in "3,4,3,1,2""".split(",")]
    assert sol1(test, 18) == 26
    assert sol1(test, 80) == 5934
    print(sol1(data, 80))
    assert sol1(test, 256) == 26984457539
    print(sol1(data, 256))
