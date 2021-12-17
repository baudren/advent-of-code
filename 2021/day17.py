

def sol1(data):
    xs, ys = data.split(" ")[2:]
    x_bound = [int(e) for e in xs.split("=")[1].replace(',', '').split("..")]
    y_bound = [int(e) for e in ys.split("=")[1].split("..")]
    y_max = 0
    for x in range(1, x_bound[0]):
        for y in range(1, -y_bound[0]):
            y_top, shot = shoot(x, y, x_bound, y_bound)
            if shot and y_top > y_max:
                y_max = y_top
    return y_max

def shoot(x_vel, y_vel, x_bound, y_bound):
    positions = [(0, 0)]
    y_top = 0
    shot = False
    iteration = 0
    while True:
        iteration += 1
        new_pos = (positions[-1][0]+x_vel, positions[-1][1]+y_vel)
        x_vel = max(0, x_vel-1)
        y_vel -= 1
        positions.append(new_pos)
        if new_pos[1] > y_top:
            y_top = new_pos[1]
        if x_bound[0] <= new_pos[0] <= x_bound[1] and y_bound[0] <= new_pos[1] <= y_bound[1]:
            shot = True
            break
        if new_pos[1] < y_bound[0]:
            break # overshoot

    return y_top, shot

def sol2(data):
    xs, ys = data.split(" ")[2:]
    x_bound = [int(e) for e in xs.split("=")[1].replace(',', '').split("..")]
    y_bound = [int(e) for e in ys.split("=")[1].split("..")]
    count = 0
    for x in range(0, x_bound[1]+2):
        for y in range(y_bound[0]-10, -y_bound[0]+1):
            y_top, shot = shoot(x, y, x_bound, y_bound)
            if shot:
                count += 1
    return count


if __name__ == "__main__":
    data = "target area: x=241..275, y=-75..-49"
    test = "target area: x=20..30, y=-10..-5"
    assert sol1(test) == 45
    print(sol1(data))
    assert sol2(test) == 112
    print(sol2(data))