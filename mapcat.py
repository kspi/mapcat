#!/usr/bin/env python3
from PIL import Image
import numpy
import math
from functools import partial


def wrap1(x):
    return numpy.fmod(x + 2 - numpy.ceil(x), 1)

def polar(xy):
    vx, vy = xy
    x = vx * 2 - 1
    y = vy * 2 - 1
    r = numpy.sqrt(x * x + y * y)
    phi = numpy.vectorize(math.atan2)(y, x)
    return phi / math.pi / 2, r

def fascale(xy, kx=0, ky=0):
    x, y = xy
    return x * (1 + kx * numpy.floor(y)), y * (1 + ky * numpy.floor(x))



def repeat1(x, n):
    return numpy.repeat(x.reshape(x.shape[0], 1), n, 1)


def apply_transform(transform, in_file, out_file, out_size, oversampling=1):
    ow, oh = out_size, out_size
    w, h = ow * oversampling, oh * oversampling

    kimg = Image.open(in_file)
    k = numpy.asarray(kimg)
    def kget(x, y):
        x = numpy.nan_to_num(x)
        y = numpy.nan_to_num(y)
        iy = numpy.floor(wrap1(y) * k.shape[0]).astype(int)
        ix = numpy.floor(wrap1(x) * k.shape[1]).astype(int)
        return k[iy, ix]

    mimg = Image.new(kimg.mode, (w, h))
    m = numpy.zeros_like(numpy.asarray(mimg))

    ys = numpy.repeat(numpy.arange(0, m.shape[0]), m.shape[1])
    xs = numpy.tile(numpy.arange(0, m.shape[1]), m.shape[0])
    m[ys, xs] = kget(*transform((xs / w, ys / w)))

    out = Image.fromarray(m)
    if oversampling != 1:
        out.thumbnail((out_size, out_size))
    out.save(out_file)


def spiral(xy, freq, scale=1, power=math.exp(1)):
    phi, r = polar(xy)

    r = 1 - r
    r_ofs = 0.7
    r = scale * ((r + r_ofs)**power - r_ofs**power)
    r = r + 1 * phi

    phi = phi * freq

    return phi, r


def main():
    size = 1000
    oversampling = 6
    apply_transform(partial(spiral, freq=21, scale=1.0), 'input/mono.png', 'mapcat_0.png', size, oversampling)
    apply_transform(partial(spiral, freq=35, scale=1.4), 'input/mono.png', 'mapcat_1.png', size, oversampling)
    apply_transform(partial(spiral, freq=40, scale=1.8), 'input/mono.png', 'mapcat_2.png', size, oversampling)


if __name__ == "__main__":
    main()
