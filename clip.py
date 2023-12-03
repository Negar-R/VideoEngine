from os import path
from PIL import Image
from moviepy.editor import (
    CompositeVideoClip,
    ImageClip,
)
from text import Text
from typing import Tuple


def resize_image(src, width, height):
    img = Image.open(src)
    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    src_base, src_name = path.split(path.abspath(src))
    src = src_base + "/resized_" + src_name
    img_resized.save(src, optimize=True)
    return src


class Clip:
    def __init__(self, width: int, height: int, duration: int) -> None:
        self.width = width
        self.height = height
        self.duration = duration
        self.frame = None
        self.background_img = list()
        self.text = list()
        self.audio = list()

    def set_background_img(
        self,
        src: str,
        start_time: int = 0,
        duration: int = None,
        position: Tuple = (0, 0),
    ):
        resized_src = resize_image(src, self.width, self.height)
        self.background_img.append(
            ImageClip(resized_src)
            .set_duration(duration or self.duration)
            .set_start(start_time)
            .set_pos(position)
        )

    def set_text(self, text: Text, duration: int = None, position: Tuple = (0, 0)):
        self.text.append(
            text.set_duration(duration or self.duration).set_position(position)
        )

    def write(
        self,
        dest: str = "output_video.mp4",
        codec: str = "libx264",
        fps: int = 24,
    ):
        CompositeVideoClip(
            [*self.background_img, *self.text, *self.audio]
        ).write_videofile(dest, codec=codec, fps=fps)
