import pygame as pg
import numpy as np
import math
import numba

# settings
res = width, height = 800, 450
offset = np.array([1.3 * width, height]) // 2
max_iter = 30
zoom = 2.2 / height
# texture
texture = pg.image.load('src/color_texture.jpg')
texture_size = min(texture.get_size()) - 1
texture_array = pg.surfarray.array3d(texture)


class NumpyFractal:
    def __init__(self, app):
        self.app = app
        self.screen_array = np.full((width, height, 3), [0, 0, 0], dtype=np.uint8)
        self.x = np.linspace(0, width, num=width, dtype=np.float32)
        self.y = np.linspace(0, height, num=height, dtype=np.float32)

    def render(self):
        x = (self.x - offset[0]) * zoom
        y = (self.y - offset[1]) * zoom
        c = x + 1j * y[:, None]
        num_iter = np.full(c.shape, max_iter)
        z = np.empty(c.shape, np.complex64)
        for i in range(max_iter):
            mask = (num_iter == max_iter)
            z[mask] = z[mask] ** 2 + c[mask]
            # num_iter[mask & (np.abs(z) > 2.0)] = i + 1
            num_iter[mask & (z.real ** 2 + z.imag ** 2 > 4.0)] = i + 1
        col = (num_iter.T * texture_size / max_iter).astype(np.uint8)
        self.screen_array = texture_array[col, col]

    def update(self):
        self.render()

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def run(self):
        self.update()
        self.draw()

