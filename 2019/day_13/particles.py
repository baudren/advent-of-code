import tcod
import random
import time

screen_width = 80
screen_height = 50
window_title = "A Particle System"
max_particle_moves = 6
particles_per_update = 2

red_lt = tcod.Color(255,215,0) #gold

class Particle:
    def __init__(self, x, y, vx, vy, colour):
        self.p_x = x
        self.p_y = y
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.colour = colour
        self.moves = 0

    def is_dead(self):
        if self.moves > max_particle_moves:
            return True
        else:
            return False

    def move(self):
        self.p_x = self.x
        self.p_y = self.y
        self.x += self.vx
        self.y += self.vy
        self.moves += 1

    def clear(self):
        tcod.console_set_char_background(
            0,
            self.p_x,
            self.p_y,
            tcod.Color(0, 0, 0),
            tcod.BKGND_SET
        )
        tcod.console_set_char_background(
            0,
            self.x,
            self.y,
            tcod.Color(0, 0, 0),
            tcod.BKGND_SET
        )

    def draw(self):
        tcod.console_set_char_background(
            0,
            self.p_x,
            self.p_y,
            tcod.Color(0, 0, 0),
            tcod.BKGND_SET
        )
        tcod.console_set_char_background(
            0,
            self.x,
            self.y,
            self.colour,
            tcod.BKGND_SET
        )


class ParticleSystem:
    max_age = 12
    def __init__(self, x, y):
        self.origin = x, y
        self.particles = []
        self.age = 0

    def update(self):
        self.age += 1
        x, y = self.origin

        for p in self.particles:
            p.move()
            if p.is_dead():
                p.clear()
                self.particles.remove(p)

    def clear(self):
        for p in self.particles:
            p.clear()

    def add_particles(self, number):
        for i in range(0, number):
            vx = random.randint(-2, 2)
            vy = random.randint(-2, 2)
            p = Particle(self.origin[0], self.origin[1], vx, vy, red_lt)
            self.particles.append(p)


    def draw(self):
        for p in self.particles:
            p.draw()


def main():

    tcod.console_set_custom_font(
        "arial10x10.png", tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
    )

    tcod.console_init_root(
        screen_width,
        screen_height,
        window_title,
        False,
    )

    ps = ParticleSystem(20, 20)

    while not tcod.console_is_window_closed():
        tcod.console_clear(0)
        ps.draw()
        ps.update()
        ps.add_particles(particles_per_update)
        time.sleep(.1)
        tcod.console_flush()
        key = tcod.console_check_for_keypress()
        if key.vk == tcod.KEY_ESCAPE: break


if __name__ == "__main__":
    main()
