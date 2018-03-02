#!/usr/bin/env python
"""Main entry point of application."""
from __future__ import print_function
import argparse
import png
from wavefront import Wavefront

class Buffer(object):
    """
    Manages a buffer for storing images.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [0] * width * height * 3

    def set_pixel(self, pos, color):
        """
        Draw pixel of a specified color to the buffer.
        """
        if pos[0] >= 0 and pos[0] < self.width and pos[1] >= 0 and pos[1] < self.height:
            # Ensure that the y axis increases upwards
            inv_y = self.height - 1 - pos[1]
            pos = (inv_y * self.width * 3) + (pos[0] * 3)
            self.data[pos + 0] = color[0]
            self.data[pos + 1] = color[1]
            self.data[pos + 2] = color[2]

    def write_to_png(self, filename):
        """
        Output the buffer to a PNG file.
        """
        png_file = open(filename, 'wb')
        writer = png.Writer(self.width, self.height)
        writer.write_array(png_file, self.data)
        png_file.close()

class Screen(object):
    """
    Manages basic screen primitives that can be drawn to a raw buffer.
    """
    def __init__(self, _buffer):
        self.buffer = _buffer

    def draw_line(self, pt0, pt1, color):
        """
        Draw a line of a specified color to the buffer.
        """
        steep = False
        if abs(pt0[0]-pt1[0]) < abs(pt0[1]-pt1[1]):
            pt0[0], pt0[1] = pt0[1], pt0[0]
            pt1[0], pt1[1] = pt1[1], pt1[0]
            steep = True

        if pt0[0] > pt1[0]:
            pt0[0], pt1[0] = pt1[0], pt0[0]
            pt0[1], pt1[1] = pt1[1], pt0[1]

        if pt0[1] > pt1[1]:
            dy = pt0[1] - pt1[1]
            inc_y = -1
        else:
            dy = pt1[1] - pt0[1]
            inc_y = 1

        dx = pt1[0] - pt0[0]
        d = 2 * dy - dx
        incr_e = 2 * dy
        incr_ne = 2 * (dy - dx)
        x = pt0[0]
        y = pt0[1]

        if not steep:
            self.buffer.set_pixel((x, y), color)
            while x < pt1[0]:
                if d <= 0:
                    d = d + incr_e
                    x = x + 1
                else:
                    d = d + incr_ne
                    x = x + 1
                    y = y + inc_y
                self.buffer.set_pixel((x, y), color)
        else:
            self.buffer.set_pixel((y, x), color)
            while x < pt1[0]:
                if d <= 0:
                    d = d + incr_e
                    x = x + 1
                else:
                    d = d + incr_ne
                    x = x + 1
                    y = y + inc_y
                self.buffer.set_pixel((y, x), color)

def main():
    """
    Main entry point of application.
    """
    parser = argparse.ArgumentParser(description="Process a wavefront object file")
    parser.add_argument('--width', help="Width of output image", dest='width',
                        type=int, default=800)
    parser.add_argument('--height', help="Height of output image", dest='height',
                        type=int, default=600)
    parser.add_argument('--out', help="Name of output image file", dest='output', type=str,
                        default='output.png')
    parser.add_argument('filename', help="Alias Wavefront file to read as input", type=str)
    args = parser.parse_args()

    back_buffer = Buffer(args.width, args.height)
    screen = Screen(back_buffer)

    obj = Wavefront(args.filename)
    print("Processing {}".format(args.filename))

    max_extent = max(obj.v_extent[0], obj.v_extent[1])
    scale = min(args.width / max_extent, args.height / max_extent)
    translate = ((args.width / 2) + obj.v_min[0] + obj.v_max[0],
                 (args.height / 2) + obj.v_min[1] + obj.v_max[1])
    print("Using scale: {}".format(scale))

    def conv_x(x):
        """ Converts x coordinate."""
        return int(x * scale + translate[0])
    def conv_y(y):
        """ Converts y coordinate."""
        return int(y * scale + translate[1])

    for f in obj.f:
        v1 = obj.v[f[0]]
        v2 = obj.v[f[1]]
        v3 = obj.v[f[2]]
        screen.draw_line((conv_x(v1[0]), conv_y(v1[1])),
                         (conv_x(v2[0]), conv_y(v2[1])),
                         (255, 255, 255))
        screen.draw_line((conv_x(v2[0]), conv_y(v2[1])),
                         (conv_x(v3[0]), conv_y(v3[1])),
                         (255, 255, 255))
        screen.draw_line((conv_x(v3[0]), conv_y(v3[1])),
                         (conv_x(v1[0]), conv_y(v1[1])),
                         (255, 255, 255))

    print("Minimum vector: {}".format(obj.v_min))
    print("Maximum vector: {}".format(obj.v_max))
    print("Calculated extent: {}".format(obj.v_extent))

    back_buffer.write_to_png(args.output)
    print("Written output to {}".format(args.output))

if __name__ == "__main__":
    main()
