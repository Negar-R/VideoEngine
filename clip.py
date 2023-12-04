import numpy as np
from os import path
from enum import Enum
from PIL import Image
from moviepy.editor import (
    VideoClip,
    VideoFileClip,
    CompositeVideoClip,
    ImageClip,
    ColorClip,
)
from text import Text
from typing import Tuple, List


class ClipType(Enum):
    VIDEO_FILE_CLIP = "video_file_clip"
    VIDEO_CLIP = "video_clip"


def resize_image(src, width, height):
    img = Image.open(src)
    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    src_base, src_name = path.split(path.abspath(src))
    src = src_base + "/resized_" + src_name
    img_resized.save(src, optimize=True)
    return src


class Clip:
    def __init__(self, **kwargs) -> None:
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.duration = kwargs.get("duration")
        self.frame = None
        self.video = None
        self.background_color = None
        self.background_img = list()
        self.text = list()
        self.audio = list()

    def set_video(self, clip_type: ClipType, src: str = None):
        self.video = (
            VideoFileClip(src)
            if clip_type == ClipType.VIDEO_FILE_CLIP
            else VideoClip(self.make_frame, duration=self.duration)
        )

    def make_frame(self, t):
        return 255 * np.ones((self.height, self.width, 3), dtype=np.uint8)

    def set_background_img(
        self,
        src: str,
        resize: bool,
        start_time: int = 0,
        duration: int = None,
        position: Tuple = (0, 0),
    ):
        img_src = resize_image(src, self.width, self.height) if resize else src
        self.background_img.append(
            ImageClip(img_src)
            .set_start(start_time)
            .set_duration(duration or self.duration)
            .set_pos(position)
        )

    def set_background_color(self, bg_rgb_color_code: List[int], duration: int = None):
        self.background_color = ColorClip(
            size=(1080, 1920),
            color=bg_rgb_color_code,
            duration=duration or self.duration,
        )

    def set_text(self, text: Text, duration: int = None, position: Tuple = (0, 0)):
        self.text.append(
            text.set_duration(duration or self.duration).set_position(position)
        )

    def create_composite_clip(self, *args):
        return CompositeVideoClip([*args])

    @staticmethod
    def write(
        clip,
        dest: str = "output_video.mp4",
        codec: str = "libx264",
        fps: int = 24,
    ):
        clip.write_videofile(dest, codec=codec, fps=fps)
