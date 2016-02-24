#!/usr/bin/env python

import numpy
import vispy.app
from PIL import Image
from vispy import gloo
import os

def readfile(filename):
    with open(filename, 'r') as f:
        return f.read()

class Canvas(vispy.app.Canvas):
    def __init__(self):
        self.fbsize = (1920, 1080)

        vispy.app.Canvas.__init__(self, title='logcat',
                            size=(100, 100), keys='interactive')

        element = gloo.Texture2D(Image.open('input/mono.png'),
                                 wrapping='repeat',
                                 interpolation='linear')

        self.render = gloo.Program(readfile('vertex.glsl'), readfile('fragment.glsl'), 4)
        self.render["position"] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
        self.render["texcoord"] = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.render["texture"] = element

        self.anim_duration = 5 * 60 + 1
        self.anim_fps = 60
        self.anim_frames = self.anim_duration * self.anim_fps

        self.render["freq"] = 17
        self.render["fps"] = self.anim_fps
        self.render["duration"] = self.anim_duration

        self.frame = 0

        self.fbo = gloo.FrameBuffer(color=gloo.RenderBuffer((self.fbsize[1], self.fbsize[0]), 'color'))

        self.show()


    def filename(self):
        return 'output/video_frames/{:05d}.png'.format(self.frame)


    def on_draw(self, event):
        while os.path.exists(self.filename()):
            self.frame += 1

        if self.frame > self.anim_frames:
            vispy.app.quit()

        print("{:5d}/{}".format(self.frame, self.anim_frames))
        self.fbo.activate()
        gloo.set_state(depth_test=False, clear_color='black')
        gloo.clear(color=True)
        w, h = self.fbsize
        gloo.set_viewport(0, 0, w, h)
        self.render['aspect'] = w / h
        self.render['width'] = w
        self.render['frame'] = self.frame
        self.render.draw('triangle_strip')
        self.context.finish()

        arr = self.fbo.read().copy()
        arr[:, :, 3] = 255
        img = Image.fromarray(arr)
        img.save(self.filename())

        self.frame += 1
        self.update()

if __name__ == '__main__':
    os.makedirs('output/video_frames')
    canvas = Canvas()
    vispy.app.run()
