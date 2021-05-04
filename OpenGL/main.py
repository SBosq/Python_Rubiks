import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import thorpy


def my_choices_1():
    # Rubik's 2x2x2:
    vertices = (
        (1, -1, -1), (1, 1, -1), (-1, 1, -1),
        (-1, -1, -1), (1, -1, 1), (1, 1, 1),
        (-1, -1, 1), (-1, 1, 1)
    )

    edges = (
        (0, 1), (0, 3), (0, 4),
        (2, 1), (2, 3), (2, 7),
        (6, 3), (6, 4), (6, 7),
        (5, 1), (5, 4), (5, 7)
    )

    surfaces = (
        (0, 1, 2, 3), (3, 2, 7, 6),
        (6, 7, 5, 4), (4, 5, 1, 0),
        (1, 5, 7, 2), (4, 0, 3, 6)
    )

    colors = (
        (1, 0, 0), (0, 1, 0),
        (1, 0.5, 0), (1, 1, 0),
        (1, 1, 1), (0, 0, 1)
    )

    class Cube():
        def __init__(self, id, N, scale):
            self.N = 2
            self.scale = scale
            self.init_i = [*id]
            self.current_i = [*id]
            self.rot = [[1 if i == j else 0 for i in range(3)] for j in range(3)]

        def isAffected(self, axis, slice, dir):
            return self.current_i[axis] == slice

        def update(self, axis, slice, dir):

            if not self.isAffected(axis, slice, dir):
                return

            i, j = (axis + 1) % 3, (axis + 2) % 3
            for k in range(3):
                self.rot[k][i], self.rot[k][j] = -self.rot[k][j] * dir, self.rot[k][i] * dir

            self.current_i[i], self.current_i[j] = (
                self.current_i[j] if dir < 0 else self.N - 1 - self.current_i[j],
                self.current_i[i] if dir > 0 else self.N - 1 - self.current_i[i])

        def transformMat(self):
            scaleA = [[s * self.scale for s in a] for a in self.rot]
            scaleT = [(p - (self.N - 1) / 2) * 2.1 * self.scale for p in self.current_i]
            return [*scaleA[0], 0, *scaleA[1], 0, *scaleA[2], 0, *scaleT, 1]

        def draw(self, col, surf, vert, animate, angle, axis, slice, dir):

            glPushMatrix()
            if animate and self.isAffected(axis, slice, dir):
                glRotatef(angle * dir, *[1 if i == axis else 0 for i in range(3)])
            glMultMatrixf(self.transformMat())

            glBegin(GL_QUADS)
            for i in range(len(surf)):
                glColor3fv(colors[i])
                for j in surf[i]:
                    glVertex3fv(vertices[j])
            glEnd()

            glPopMatrix()

    class EntireCube():
        def __init__(self, N, scale):
            self.N = 2
            cr = range(2)
            self.cubes = [Cube((x, y, z), self.N, scale) for x in cr for y in cr for z in cr]

        def mainloop(self):

            rot_cube_map = {K_UP: (-1, 0), K_DOWN: (1, 0), K_LEFT: (0, -1), K_RIGHT: (0, 1)}
            rot_slice_map = {
                K_1: (0, 0, 1), K_2: (0, 1, 1),
                K_3: (1, 0, 1), K_4: (1, 1, 1),
                K_5: (2, 0, 1), K_6: (2, 1, 1),
                K_F1: (0, 0, -1), K_F2: (0, 1, -1),
                K_F3: (1, 0, -1), K_F4: (1, 1, -1),
                K_F5: (2, 0, -1), K_F6: (2, 1, -1),
            }

            ang_x, ang_y, rot_cube = 0, 0, (0, 0)
            animate, animate_ang, animate_speed = False, 0, 5
            action = (0, 0, 0)
            while True:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            return
                    if event.type == KEYDOWN:
                        if event.key in rot_cube_map:
                            rot_cube = rot_cube_map[event.key]
                        if not animate and event.key in rot_slice_map:
                            animate, action = True, rot_slice_map[event.key]
                    if event.type == KEYUP:
                        if event.key in rot_cube_map:
                            rot_cube = (0, 0)

                ang_x += rot_cube[0] * 2
                ang_y += rot_cube[1] * 2

                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                glTranslatef(0, 0, -40)
                glRotatef(ang_y, 0, 1, 0)
                glRotatef(ang_x, 1, 0, 0)

                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                if animate:
                    if animate_ang >= 90:
                        for cube in self.cubes:
                            cube.update(*action)
                        animate, animate_ang = False, 0

                for cube in self.cubes:
                    cube.draw(colors, surfaces, vertices, animate, animate_ang, *action)
                if animate:
                    animate_ang += animate_speed

                pygame.display.flip()
                pygame.time.wait(10)

    def main():
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

        NewEntireCube = EntireCube(3, 1.5)
        NewEntireCube.mainloop()

    if __name__ == '__main__':
        main()
        pygame.quit()
        quit()


def my_choices_2():
    # Rubik's 3x3x3:
    vertices = (
        (1, -1, -1), (1, 1, -1), (-1, 1, -1),
        (-1, -1, -1), (1, -1, 1), (1, 1, 1),
        (-1, -1, 1), (-1, 1, 1)
    )

    edges = (
        (0, 1), (0, 3), (0, 4),
        (2, 1), (2, 3), (2, 7),
        (6, 3), (6, 4), (6, 7),
        (5, 1), (5, 4), (5, 7)
    )

    surfaces = (
        (0, 1, 2, 3), (3, 2, 7, 6),
        (6, 7, 5, 4), (4, 5, 1, 0),
        (1, 5, 7, 2), (4, 0, 3, 6)
    )

    colors = (
        (1, 0, 0), (0, 1, 0),
        (1, 0.5, 0), (1, 1, 0),
        (1, 1, 1), (0, 0, 1)
    )

    class Cube():
        def __init__(self, id, N, scale):
            self.N = N
            self.scale = scale
            self.init_i = [*id]
            self.current_i = [*id]
            self.rot = [[1 if i == j else 0 for i in range(3)] for j in range(3)]

        def isAffected(self, axis, slice, dir):
            return self.current_i[axis] == slice

        def update(self, axis, slice, dir):

            if not self.isAffected(axis, slice, dir):
                return

            i, j = (axis + 1) % 3, (axis + 2) % 3
            for k in range(3):
                self.rot[k][i], self.rot[k][j] = -self.rot[k][j] * dir, self.rot[k][i] * dir

            self.current_i[i], self.current_i[j] = (
                self.current_i[j] if dir < 0 else self.N - 1 - self.current_i[j],
                self.current_i[i] if dir > 0 else self.N - 1 - self.current_i[i])

        def transformMat(self):
            scaleA = [[s * self.scale for s in a] for a in self.rot]
            scaleT = [(p - (self.N - 1) / 2) * 2.1 * self.scale for p in self.current_i]
            return [*scaleA[0], 0, *scaleA[1], 0, *scaleA[2], 0, *scaleT, 1]

        def draw(self, col, surf, vert, animate, angle, axis, slice, dir):

            glPushMatrix()
            if animate and self.isAffected(axis, slice, dir):
                glRotatef(angle * dir, *[1 if i == axis else 0 for i in range(3)])
            glMultMatrixf(self.transformMat())

            glBegin(GL_QUADS)
            for i in range(len(surf)):
                glColor3fv(colors[i])
                for j in surf[i]:
                    glVertex3fv(vertices[j])
            glEnd()

            glPopMatrix()

    class EntireCube():
        def __init__(self, N, scale):
            self.N = N
            cr = range(self.N)
            self.cubes = [Cube((x, y, z), self.N, scale) for x in cr for y in cr for z in cr]

        def mainloop(self):

            rot_cube_map = {K_UP: (-1, 0), K_DOWN: (1, 0), K_LEFT: (0, -1), K_RIGHT: (0, 1)}
            rot_slice_map = {
                K_1: (0, 0, 1), K_2: (0, 1, 1), K_3: (0, 2, 1),
                K_4: (1, 0, 1), K_5: (1, 1, 1), K_6: (1, 2, 1),
                K_7: (2, 0, 1), K_8: (2, 1, 1), K_9: (2, 2, 1),
                K_F1: (0, 0, -1), K_F2: (0, 1, -1), K_F3: (0, 2, -1),
                K_F4: (1, 0, -1), K_F5: (1, 1, -1), K_F6: (1, 2, -1),
                K_F7: (2, 0, -1), K_F8: (2, 1, -1), K_F9: (2, 2, -1),
            }

            ang_x, ang_y, rot_cube = 0, 0, (0, 0)
            animate, animate_ang, animate_speed = False, 0, 5
            action = (0, 0, 0)
            while True:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            return
                    if event.type == KEYDOWN:
                        if event.key in rot_cube_map:
                            rot_cube = rot_cube_map[event.key]
                        if not animate and event.key in rot_slice_map:
                            animate, action = True, rot_slice_map[event.key]
                    if event.type == KEYUP:
                        if event.key in rot_cube_map:
                            rot_cube = (0, 0)

                ang_x += rot_cube[0] * 2
                ang_y += rot_cube[1] * 2

                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                glTranslatef(0, 0, -40)
                glRotatef(ang_y, 0, 1, 0)
                glRotatef(ang_x, 1, 0, 0)

                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                if animate:
                    if animate_ang >= 90:
                        for cube in self.cubes:
                            cube.update(*action)
                        animate, animate_ang = False, 0

                for cube in self.cubes:
                    cube.draw(colors, surfaces, vertices, animate, animate_ang, *action)
                if animate:
                    animate_ang += animate_speed

                pygame.display.flip()
                pygame.time.wait(10)

    def main():
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

        NewEntireCube = EntireCube(3, 1.5)
        NewEntireCube.mainloop()

    if __name__ == '__main__':
        main()
        pygame.quit()
        quit()


def my_choices_3():
    # Rubik's 6x6x6:
    vertices = (
        (1, -1, -1), (1, 1, -1), (-1, 1, -1),
        (-1, -1, -1), (1, -1, 1), (1, 1, 1),
        (-1, -1, 1), (-1, 1, 1)
    )

    edges = (
        (0, 1), (0, 3), (0, 4),
        (2, 1), (2, 3), (2, 7),
        (6, 3), (6, 4), (6, 7),
        (5, 1), (5, 4), (5, 7)
    )

    surfaces = (
        (0, 1, 2, 3), (3, 2, 7, 6),
        (6, 7, 5, 4), (4, 5, 1, 0),
        (1, 5, 7, 2), (4, 0, 3, 6)
    )

    colors = (
        (1, 0, 0), (0, 1, 0),
        (1, 0.5, 0), (1, 1, 0),
        (1, 1, 1), (0, 0, 1)
    )

    class Cube():
        def __init__(self, id, N, scale):
            self.N = 6
            self.scale = scale
            self.init_i = [*id]
            self.current_i = [*id]
            self.rot = [[1 if i == j else 0 for i in range(3)] for j in range(3)]

        def isAffected(self, axis, slice, dir):
            return self.current_i[axis] == slice

        def update(self, axis, slice, dir):

            if not self.isAffected(axis, slice, dir):
                return

            i, j = (axis + 1) % 3, (axis + 2) % 3
            for k in range(3):
                self.rot[k][i], self.rot[k][j] = -self.rot[k][j] * dir, self.rot[k][i] * dir

            self.current_i[i], self.current_i[j] = (
                self.current_i[j] if dir < 0 else self.N - 1 - self.current_i[j],
                self.current_i[i] if dir > 0 else self.N - 1 - self.current_i[i])

        def transformMat(self):
            scaleA = [[s * self.scale for s in a] for a in self.rot]
            scaleT = [(p - (self.N - 1) / 2) * 2.1 * self.scale for p in self.current_i]
            return [*scaleA[0], 0, *scaleA[1], 0, *scaleA[2], 0, *scaleT, 1]

        def draw(self, col, surf, vert, animate, angle, axis, slice, dir):

            glPushMatrix()
            if animate and self.isAffected(axis, slice, dir):
                glRotatef(angle * dir, *[1 if i == axis else 0 for i in range(3)])
            glMultMatrixf(self.transformMat())

            glBegin(GL_QUADS)
            for i in range(len(surf)):
                glColor3fv(colors[i])
                for j in surf[i]:
                    glVertex3fv(vertices[j])
            glEnd()

            glPopMatrix()

    class EntireCube():
        def __init__(self, N, scale):
            self.N = 6
            cr = range(6)
            self.cubes = [Cube((x, y, z), self.N, scale) for x in cr for y in cr for z in cr]

        def mainloop(self):

            rot_cube_map = {K_UP: (-1, 0), K_DOWN: (1, 0), K_LEFT: (0, -1), K_RIGHT: (0, 1)}
            rot_slice_map = {
                K_1: (0, 0, 1), K_2: (0, 1, 1), K_3: (0, 2, 1), K_4: (0, 3, 1), K_5: (0, 4, 1), K_6: (0, 5, 1),
                K_7: (1, 0, 1), K_8: (1, 1, 1), K_9: (1, 2, 1), K_0: (1, 3, 1), K_MINUS: (1, 4, 1), K_EQUALS: (1, 5, 1),
                K_F1: (2, 0, 1), K_F2: (2, 1, 1), K_F3: (2, 2, 1), K_F4: (2, 3, 1), K_F5: (2, 4, 1), K_F6: (2, 5, 1),
                K_q: (0, 0, -1), K_w: (0, 1, -1), K_e: (0, 2, -1), K_r: (0, 3, -1), K_t: (0, 4, -1), K_y: (0, 5, -1),
                K_a: (1, 0, -1), K_s: (1, 1, -1), K_d: (1, 2, -1), K_f: (1, 3, -1), K_g: (1, 4, -1), K_h: (1, 5, -1),
                K_z: (2, 0, -1), K_x: (2, 1, -1), K_c: (2, 2, -1), K_v: (2, 3, -1), K_b: (2, 4, -1), K_n: (2, 5, -1),
            }

            ang_x, ang_y, rot_cube = 0, 0, (0, 0)
            animate, animate_ang, animate_speed = False, 0, 5
            action = (0, 0, 0)
            while True:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            return
                    if event.type == KEYDOWN:
                        if event.key in rot_cube_map:
                            rot_cube = rot_cube_map[event.key]
                        if not animate and event.key in rot_slice_map:
                            animate, action = True, rot_slice_map[event.key]
                    if event.type == KEYUP:
                        if event.key in rot_cube_map:
                            rot_cube = (0, 0)

                ang_x += rot_cube[0] * 2
                ang_y += rot_cube[1] * 2

                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                glTranslatef(0, 0, -40)
                glRotatef(ang_y, 0, 1, 0)
                glRotatef(ang_x, 1, 0, 0)

                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                if animate:
                    if animate_ang >= 90:
                        for cube in self.cubes:
                            cube.update(*action)
                        animate, animate_ang = False, 0

                for cube in self.cubes:
                    cube.draw(colors, surfaces, vertices, animate, animate_ang, *action)
                if animate:
                    animate_ang += animate_speed

                pygame.display.flip()
                pygame.time.wait(10)

    def main():
        pygame.init()
        display = (1000, 800)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

        NewEntireCube = EntireCube(3, 1.5)
        NewEntireCube.mainloop()

    if __name__ == '__main__':
        main()
        pygame.quit()
        quit()


application = thorpy.Application((500, 500), "Launching alerts")

button1 = thorpy.make_button("Fácil", func=my_choices_1)
button2 = thorpy.make_button("Normal", func=my_choices_2)
button3 = thorpy.make_button("Difícil", func=my_choices_3)
button4 = thorpy.make_button("Sacame de Aquí!")
button4.set_as_exiter()

background = thorpy.Background(image="rubik.jpg", elements=[button1, button2, button3, button4])
thorpy.store(background)

menu = thorpy.Menu(background)
menu.play()

application.quit()
