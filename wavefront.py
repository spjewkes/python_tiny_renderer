import sys
import math

class Point:
    def __init__(self, x, y, z):
        self.p = (x, y, z)

    def __str__(self):
        return '({0},{1},{2})'.format(self.p[0],self.p[1],self.p[2])

    def __getitem__(self, i):
        return self.p[i]

    def __add__(self, p):
        return Point(self.p[0] + p.p[0], self.p[1] + p.p[1], self.p[2] + p.p[2])

    def __iadd__(self, p):
        self.p[0] + p.p[0]
        self.p[1] + p.p[1]
        self.p[2] + p.p[2]
        return self

    def __sub__(self, p):
        return Point(self.p[0] - p.p[0], self.p[1] - p.p[1], self.p[2] - p.p[2])

    def __isub__(self, p):
        self.p[0] - p.p[0]
        self.p[1] - p.p[1]
        self.p[2] - p.p[2]
        return self

class Vector:
    def __init__(self, x, y, z):
        self.v = (x, y, z)

    def __str__(self):
        return '({0},{1},{2},{3})'.format(v[0],v[1],v[2])

    def __getitem__(self, i):
        return self.v[i]

    def __add__(self, v):
        return Vector(self.v[0] + v.v[0], self.v[1] + v.v[1], self.v[2] + v.v[2])

    def __iadd__(self, v):
        self.v[0] + v.v[0]
        self.v[1] + v.v[1]
        self.v[2] + v.v[2]
        return self

    def __sub__(self, v):
        return Vector(self.v[0] - v.v[0], self.v[1] - v.v[1], self.v[2] - v.v[2])

    def __isub__(self, v):
        self.v[0] - v.v[0]
        self.v[1] - v.v[1]
        self.v[2] - v.v[2]
        return self

    def mag(self):
        return math.sqrt((self.p[0] ^ 2) + (self.p[1] ^ 2) + (self.p[2] ^ 2))

    def normalize(self):
        length = self.mag()
        if length == 0.0:
            self.p = (0.0, 0.0, 0.0)
        else:
            self.p = (self.p[0] / length, self.p[1] / length, self.p[2] / length)

    def dot(self, p):
        return (self.p[0] * p.p[0]) + (self.p[1] * p.p[1]) + (self.p[2] * p.p[2])

    def cross(self, p):
        x = (self.p[1] * p.p[2]) - (p.p[1] * self.p[2])
        y = (self.p[2] * p.p[0]) - (p.p[2] * self.p[0])
        z = (self.p[0] * p.p[1]) - (p.p[0] * self.p[1])
        return Point(x, y, z)

class Wavefront:
    def __init__(self, filename):
        self.filename = filename
        self.v = []
        self.v_min = [sys.float_info.max, sys.float_info.max, sys.float_info.max]
        self.v_max = [sys.float_info.min, sys.float_info.min, sys.float_info.min]
        self.v_extent = [0.0, 0.0, 0.0]
        self.f = []
        file = open(filename)
        for line in file:
            data = line.split()

            if data:
                # For any vertex data - add to end of vertex array
                if data[0] == 'v':
                    vertex = Point(float(data[1]), float(data[2]), float(data[3]))
                    for i in range(0,3):
                        if vertex[i] < self.v_min[i]:
                            self.v_min[i] = vertex[i]
                        if vertex[i] > self.v_max[i]:
                            self.v_max[i] = vertex[i]
                    self.v.append(vertex)
                if data[0] == 'f':
                    faces = []
                    for f in data[1:]:
                        faces.append(int(f.split('/')[0]) - 1)
                    self.f.append(faces)

        # Create vertex extents
        for i in range(0, 3):
            self.v_extent[i] = self.v_max[i] - self.v_min[i]
