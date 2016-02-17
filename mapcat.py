#!/usr/bin/env python3
from PIL import Image
import numpy
import math
from functools import partial



EPSILON = numpy.finfo(numpy.float).eps

GOLDEN_RATIO = (1 + math.sqrt(5)) / 2


def wrap1(x):
    return numpy.fmod(x + 1 - numpy.ceil(x), 1)

def apply_transform(transform, in_file, out_file, out_size, oversampling=1):
    print(out_file)

    w, h = out_size * oversampling, out_size * oversampling

    element_img = Image.open(in_file)
    element = numpy.asarray(element_img)
    def sample(x, y):
        iy = numpy.floor(wrap1(y) * element.shape[0]).astype(numpy.uint32)
        ix = numpy.floor(wrap1(x) * element.shape[1]).astype(numpy.uint32)
        return element[iy, ix]

    result = numpy.zeros((w, h), dtype=numpy.uint8)

    ys = numpy.repeat(numpy.arange(0, result.shape[0]), result.shape[1])
    xs = numpy.tile(numpy.arange(0, result.shape[1]), result.shape[0])
    result[ys, xs] = sample(*transform((xs / w, ys / w)))

    out = Image.fromarray(result)
    if oversampling != 1:
        out.thumbnail((out_size, out_size))
    out.save(out_file)


def polar(xy):
    ox, oy = xy

    # centered
    x = ox * 2 - 1
    y = oy * 2 - 1

    r = numpy.sqrt(x * x + y * y)
    phi = numpy.vectorize(math.atan2)(y, x)
    return phi / math.pi / 2, r


def spiral(xy, freq, scale):
    phi, r = polar(xy)

    r = scale * numpy.log(scale * r + EPSILON) / numpy.log(GOLDEN_RATIO)
    r = 1 - r
    r = r + 1 * phi

    phi = phi * freq

    return phi, r


def main():
    size = 2000
    oversampling = 3
    apply_transform(partial(spiral, freq=17, scale=0.6), 'input/mono.png', 'output/mapcat_0.png', size, oversampling)
    apply_transform(partial(spiral, freq=23, scale=0.8), 'input/mono.png', 'output/mapcat_1.png', size, oversampling)
    apply_transform(partial(spiral, freq=28, scale=1.0), 'input/mono.png', 'output/mapcat_2.png', size, oversampling)


if __name__ == "__main__":
    main()
