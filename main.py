#!/usr/bin/env python
import sys
import png
import argparse
from wavefront import Wavefront

class Buffer:
    """A simple buffer class"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [0] * width * height * 3

    def set_pixel(self, x, y, r, g, b):
        if x >=0 and x < self.width and y >= 0 and y < self.height:
            # Ensure that the y axis increases upwards
            inv_y = self.height - 1 - y
            pos = (inv_y * self.width * 3) + (x * 3)
            self.data[pos + 0] = r
            self.data[pos + 1] = b
            self.data[pos + 2] = g

    def write_to_png(self, filename):
        f = open(filename, 'wb')
        w = png.Writer(self.width, self.height)
        w.write_array(f, self.data)
        f.close

class Screen:
    """Manages basic screen primitives that can be drawn to a raw buffer"""
    def __init__(self, buffer):
        self.buffer = buffer

    def draw_line(self, x0,y0, x1,y1, r,g,b):
        steep = False
        if( abs(x0-x1) < abs(y0-y1) ):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        if y0 > y1:
            dy = y0 - y1
            inc_y = -1
        else:
            dy = y1 - y0
            inc_y = 1

        dx = x1 - x0
        d = 2 * dy - dx
        incr_e = 2 * dy
        incr_ne = 2 * (dy - dx)
        x = x0
        y = y0

        if steep == False:
            self.buffer.set_pixel(x, y, r, g, b)
            while x < x1:
                if d <= 0:
                    d = d + incr_e
                    x = x + 1
                else:
                    d = d + incr_ne
                    x = x + 1
                    y = y + inc_y
                self.buffer.set_pixel(x, y, r, g, b)
        else:
            self.buffer.set_pixel(y, x, r, g, b)
            while x < x1:
                if d <= 0:
                    d = d + incr_e
                    x = x + 1
                else:
                    d = d + incr_ne
                    x = x + 1
                    y = y + inc_y
                self.buffer.set_pixel(y, x, r, g, b)

def main():
    parser = argparse.ArgumentParser(description="Process a wavefront object file")
    parser.add_argument('--width', dest='width', type=int, default=800)
    parser.add_argument('--height', dest='height', type=int, default=600)
    parser.add_argument('--file', dest='filename', type=str, required=True)
    args = parser.parse_args()

    buffer = Buffer(args.width, args.height)
    screen = Screen(buffer)

    obj = Wavefront(args.filename)

    max_extent = max(obj.v_extent[0], obj.v_extent[1])
    scale = min(800 / max_extent, 600 / max_extent)
    print scale

    def conv_x(x):
        return int(x * scale + 400.0)
    def conv_y(y):
        return int(y * scale + 0.0)

    for f in obj.f:
        v1 = obj.v[f[0]]
        v2 = obj.v[f[1]]
        v3 = obj.v[f[2]]
        screen.draw_line(conv_x(v1[0]),conv_y(v1[1]), conv_x(v2[0]),conv_y(v2[1]), 255,255,255)
        screen.draw_line(conv_x(v2[0]),conv_y(v2[1]), conv_x(v3[0]),conv_y(v3[1]), 255,255,255)
        screen.draw_line(conv_x(v3[0]),conv_y(v3[1]), conv_x(v1[0]),conv_y(v1[1]), 255,255,255)

    print obj.v_min
    print obj.v_max
    print obj.v_extent

    buffer.write_to_png('output.png')

if __name__ == "__main__":
    main()
