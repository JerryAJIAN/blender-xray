import math

import bgl


def matrix_to_buffer(matrix):
    buff = bgl.Buffer(bgl.GL_FLOAT, len(matrix.row) * len(matrix.col))
    for i, row in enumerate(matrix.row):
        buff[4 * i:4 * i + 4] = row
    return buff


def draw_wire_cube(hsx, hsy, hsz):
    bgl.glBegin(bgl.GL_LINE_LOOP)
    bgl.glVertex3f(-hsx, -hsy, -hsz)
    bgl.glVertex3f(+hsx, -hsy, -hsz)
    bgl.glVertex3f(+hsx, +hsy, -hsz)
    bgl.glVertex3f(-hsx, +hsy, -hsz)
    bgl.glEnd()
    bgl.glBegin(bgl.GL_LINE_LOOP)
    bgl.glVertex3f(-hsx, -hsy, +hsz)
    bgl.glVertex3f(+hsx, -hsy, +hsz)
    bgl.glVertex3f(+hsx, +hsy, +hsz)
    bgl.glVertex3f(-hsx, +hsy, +hsz)
    bgl.glEnd()
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex3f(-hsx, -hsy, -hsz)
    bgl.glVertex3f(-hsx, -hsy, +hsz)
    bgl.glVertex3f(+hsx, -hsy, -hsz)
    bgl.glVertex3f(+hsx, -hsy, +hsz)
    bgl.glVertex3f(+hsx, +hsy, -hsz)
    bgl.glVertex3f(+hsx, +hsy, +hsz)
    bgl.glVertex3f(-hsx, +hsy, -hsz)
    bgl.glVertex3f(-hsx, +hsy, +hsz)
    bgl.glEnd()


# pylint: disable=C0103
def gen_arc(radius, start, end, num_segments, fconsumer, close=False):
    theta = (end - start) / num_segments
    cos_th, sin_th = math.cos(theta), math.sin(theta)
    x, y = radius * math.cos(start), radius * math.sin(start)
    for _ in range(num_segments):
        fconsumer(x, y)
        _ = x
        x = x * cos_th - y * sin_th
        y = _ * sin_th + y * cos_th
    if close:
        fconsumer(x, y)


# pylint: disable=C0103
def gen_circle(radius, num_segments, fconsumer):
    gen_arc(radius, 0, 2.0 * math.pi, num_segments, fconsumer)


# pylint: disable=C0103
def gen_limit_circle(rotate, radius, num_segments, fconsumer, color, min_limit, max_limit):
    def gen_arc_vary(radius, start, end):
        num_segs = math.ceil(num_segments * abs(end - start) / (math.pi * 2.0))
        if num_segs:
            gen_arc(radius, start, end, num_segs, fconsumer, close=True)

    grey_color = (0.5, 0.5, 0.5, 0.8)

    bgl.glLineWidth(2)
    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glColor4f(*color)
    gen_arc_vary(radius, min_limit, max_limit)
    bgl.glColor4f(*grey_color)
    gen_arc_vary(radius, max_limit, 2.0 * math.pi + min_limit)
    bgl.glEnd()

    bgl.glPointSize(6)
    bgl.glColor4f(1.0, 1.0, 0.0, 1.0)
    bgl.glBegin(bgl.GL_POINTS)
    gen_arc(radius, rotate, rotate + 1, 1, fconsumer)
    bgl.glEnd()


def draw_joint_limits(rotate, min_limit, max_limit, axis, radius):
    colors = {
        'X': (1.0, 0.0, 0.0, 1.0),
        'Y': (0.0, 1.0, 0.0, 1.0),
        'Z': (0.0, 0.0, 1.0, 1.0)
    }
    draw_functions = {
        'X': (lambda x, y: bgl.glVertex3f(0, -x, y)),
        'Y': (lambda x, y: bgl.glVertex3f(-y, 0, x)),
        'Z': (lambda x, y: bgl.glVertex3f(-x, -y, 0))
    }
    color = colors[axis]
    gen_limit_circle(
        rotate, radius, 24, draw_functions[axis], color,
        min_limit, max_limit
    )


def draw_wire_sphere(radius, num_segments):
    bgl.glBegin(bgl.GL_LINE_LOOP)
    gen_circle(radius, num_segments, lambda x, y: bgl.glVertex3f(x, y, 0))
    bgl.glEnd()
    bgl.glBegin(bgl.GL_LINE_LOOP)
    gen_circle(radius, num_segments, lambda x, y: bgl.glVertex3f(0, x, y))
    bgl.glEnd()
    bgl.glBegin(bgl.GL_LINE_LOOP)
    gen_circle(radius, num_segments, lambda x, y: bgl.glVertex3f(y, 0, x))
    bgl.glEnd()


def draw_wire_cylinder(radius, half_height, num_segments):
    bgl.glBegin(bgl.GL_LINE_LOOP)
    gen_circle(radius, num_segments, lambda x, y: bgl.glVertex3f(x, -half_height, y))
    bgl.glEnd()
    bgl.glBegin(bgl.GL_LINE_LOOP)
    gen_circle(radius, num_segments, lambda x, y: bgl.glVertex3f(x, +half_height, y))
    bgl.glEnd()
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex3f(-radius, -half_height, 0)
    bgl.glVertex3f(-radius, +half_height, 0)
    bgl.glVertex3f(+radius, -half_height, 0)
    bgl.glVertex3f(+radius, +half_height, 0)
    bgl.glVertex3f(0, -half_height, -radius)
    bgl.glVertex3f(0, +half_height, -radius)
    bgl.glVertex3f(0, -half_height, +radius)
    bgl.glVertex3f(0, +half_height, +radius)
    bgl.glEnd()

def draw_cross(size):
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex3f(-size, 0, 0)
    bgl.glVertex3f(+size, 0, 0)
    bgl.glVertex3f(0, -size, 0)
    bgl.glVertex3f(0, +size, 0)
    bgl.glVertex3f(0, 0, -size)
    bgl.glVertex3f(0, 0, +size)
    bgl.glEnd()
