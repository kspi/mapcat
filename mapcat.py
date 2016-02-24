#!/usr/bin/env python3
from PIL import Image
import numpy
import math
from functools import partial



EPSILON = numpy.finfo(numpy.float).eps

GOLDEN_RATIO = (1 + math.sqrt(5)) / 2

def bilinear_interpolate(im, x, y):
    x = numpy.asarray(x)
    y = numpy.asarray(y)

    x0 = numpy.floor(x).astype(int)
    x1 = x0 + 1
    y0 = numpy.floor(y).astype(int)
    y1 = y0 + 1

    x0 = numpy.clip(x0, 0, im.shape[1]-1);
    x1 = numpy.clip(x1, 0, im.shape[1]-1);
    y0 = numpy.clip(y0, 0, im.shape[0]-1);
    y1 = numpy.clip(y1, 0, im.shape[0]-1);

    Ia = im[ y0, x0 ]
    Ib = im[ y1, x0 ]
    Ic = im[ y0, x1 ]
    Id = im[ y1, x1 ]

    wa = (x1-x) * (y1-y)
    wb = (x1-x) * (y-y0)
    wc = (x-x0) * (y1-y)
    wd = (x-x0) * (y-y0)

    return wa*Ia + wb*Ib + wc*Ic + wd*Id


def wrap1(x):
    return numpy.fmod(x + 1 - numpy.ceil(x), 1)

def apply_transform(transform, in_file, out_file, out_size, oversampling=1, negate=False):
    print(out_file)

    out_w, out_h = out_size

    w, h = out_w * oversampling, out_h * oversampling

    element_img = Image.open(in_file)
    element = numpy.asarray(element_img)
    def sample(x, y):
        iy = (wrap1(y) * element.shape[0]).astype(int)
        ix = (wrap1(x) * element.shape[1]).astype(int)
        return element[iy, ix]

    result = numpy.zeros((h, w), dtype=numpy.float32)

    ys = numpy.repeat(numpy.arange(0, result.shape[0]), result.shape[1])
    xs = numpy.tile(numpy.arange(0, result.shape[1]), result.shape[0])
    sigma = 0.5
    size = 2
    for dy in range(-size, size + 1):
        for dx in range(-size, size + 1):
            weight = numpy.exp(-((dx/size*sigma)**2 + (dy/size*sigma)**2) / (2 * sigma**2))
            result[ys, xs] += weight * sample(*transform(((xs + dx / size * sigma) / w, (ys + dy / size * sigma + (w - h) / 2) / w)))

    result *= 255 / numpy.max(result)
    result = result.astype(dtype=numpy.uint8, copy=False)

    if negate:
        result = 255 - result

    out = Image.fromarray(result)
    if oversampling != 1:
        out.thumbnail((out_w, out_h))
    out.save(out_file)


def polar(xy):
    ox, oy = xy

    # centered
    x = ox * 2 - 1
    y = oy * 2 - 1

    r = numpy.sqrt(x * x + y * y)
    phi = numpy.vectorize(math.atan2)(y, x)
    return phi / math.pi / 2, r


def spiral(xy, freq, scale, phase=0, rphase=0):
    phi, r = polar(xy)

    r = scale * numpy.log(0.6 * r + EPSILON) / numpy.log(GOLDEN_RATIO)
    r = 1 - r
    r = r + 1 * phi
    r -= rphase

    phi = phi * freq
    phi -= phase

    return phi, r


#def main():
    #size = 2000
    #oversampling = 3
    #apply_transform(partial(spiral, freq=17, scale=0.6), 'input/mono.png', 'output/mapcat_0.png', size, oversampling)
    #apply_transform(partial(spiral, freq=23, scale=0.8), 'input/mono.png', 'output/mapcat_1.png', size, oversampling)
    #apply_transform(partial(spiral, freq=28, scale=1.0), 'input/mono.png', 'output/mapcat_2.png', size, oversampling)

size = (1920, 1080)
oversampling = 1
fps = 60
length = 5 * 60 + 1 # 5 minutes
frames = fps * length
def make_frame(frame):
    seconds = frame / fps

    turn_period = 8 - 4 * (seconds / length)**1.4
    phase = seconds / turn_period

    scale = 0.55 + 0.25 * (frame / frames)**1.9
    apply_transform(partial(spiral, freq=17, scale=scale, phase=3 * phase, rphase=-1 * phase),
            'input/mono.png',
            'anim_long/{:05}.png'.format(frame),
            size,
            oversampling,
            negate=True)

#make_frame(0)
#make_frame(frames - 1)

import sys
make_frame(int(sys.argv[1]))

#from multiprocessing import Pool
#for frame0 in range(0, frames + 1, 2):
#    with Pool(2) as p:
#        p.map(make_frame, [frame0, frame0 + 1])


#if __name__ == "__main__":
#    main()
