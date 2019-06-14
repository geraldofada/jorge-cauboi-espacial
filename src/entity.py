from pygame import math

from library.PPlay.animation import Animation
from library.PPlay.gameimage import load_image
import globals


class Entity(object):
    def __init__(self, window, sprite_path, frames):
        self.window = window
        self.animation = Animation(sprite_path, frames)
        self.animation.set_sequence_time(0, frames, globals.FRAME_SPEED)
        self.animation.play()

        self.colliding = {"left": False, "right": False, "top": False, "bottom": False}

        self.velocity = math.Vector2(0, 0)

        self.direction = {"left": False, "right": True}
        self.state = {"idle": True, "running": False}

    def update(self):
        self.animation.x += self.velocity.x * self.window.delta_time()
        self.animation.y += self.velocity.y * self.window.delta_time()

    def render(self):
        self.animation.update()
        self.animation.draw()

    def move(self, vector):
        self.velocity = vector

    def set_animation(self, sprite_path, frames):
        self.animation.image, self.animation.rect = load_image(sprite_path, alpha=True)
        self.animation.total_frames = frames
        self.animation.set_total_duration(frames * globals.FRAME_SPEED)

    def set_position(self, x, y):
        self.animation.set_position(x, y)

    def set_direction(self, direction):
        for key, _ in self.direction.items():
            if key == direction:
                self.direction[key] = True
            else:
                self.direction[key] = False

    def set_state(self, state):
        for key, _ in self.state.items():
            if key == state:
                self.state[key] = True
            else:
                self.state[key] = False
