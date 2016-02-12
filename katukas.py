#!/usr/bin/env python3
from PIL import Image
import numpy
import math


def compose(*transforms):
    def composed(*xy):
        for t in transforms:
            xy = t(*xy)
        return xy
    return composed


def repeat(xfreq, yfreq):
    def repeat_transform(x, y):
        return x * xfreq, y * yfreq
    return transform


def polar():
    x = vx * 2 - 1
    y = vy * 2 - 1
    r = numpy.sqrt(x * x + y * y)
    phi = numpy.vectorize(math.atan2)(y, x)
    return r, phi / math.pi / 2


def transpose(x, y):
    return y, x


def hyp_x(x, y):
    return 1 / (x or 1e-10), y

def hyp_y(x, y):
    return x, 1 / (y or 1e-10)



def wrap1(x):
    return numpy.fmod(x + 2 - numpy.ceil(x), 1)

def wrap(x, w):
    return (w * wrap1(x / w)).astype(int)

def repeat1(x, n):
    return numpy.repeat(x.reshape(x.shape[0], 1), n, 1)


def apply_transform(transform, in_file, out_file, out_size, oversampling=4):
    ow, oh = out_size, out_size
    w, h = ow * oversampling, oh * oversampling

    kimg = Image.open(in_file)
    k = numpy.asarray(kimg)
    def kget(x, y):
        iy = numpy.floor(wrap1(y) * k.shape[0]).astype(int)
        ix = numpy.floor(wrap1(x) * k.shape[1]).astype(int)
        return k[iy, ix]

    mimg = Image.new(kimg.mode, (w, h))
    m = numpy.zeros_like(numpy.asarray(mimg))

    ys = numpy.repeat(numpy.arange(0, m.shape[0]), m.shape[1])
    xs = numpy.tile(numpy.arange(0, m.shape[1]), m.shape[0])
    m[ys, xs] = kget(*transform(xs / w, ys / w))

    out = Image.fromarray(m)
    out.thumbnail((out_size, out_size))
    out.save(out_file)


def main():
    transform = compose(polar(), transpose(), repeat(55, -3))
    apply_transform(transform, 'input/katukas.png', 'out.png', 1000)


if __name__ == "__main__":
    main()
