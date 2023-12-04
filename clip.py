import numpy as np
from os import path
from enum import Enum
from PIL import Image
from moviepy.editor import (
    VideoClip,
    VideoFileClip,
    ImageClip,
    ColorClip,
    AudioFileClip,
    CompositeVideoClip,
    CompositeAudioClip,
    concatenate_videoclips,
    vfx,
    afx,
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
        self.video_src = kwargs.get("video_src")
        self.frame = None
        self.video = None
        self.background_color = None
        self.background_img = list()
        self.text = list()
        self.audio = list()

    def set_video(self, clip_type: ClipType):
        self.video = (
            VideoFileClip(self.video_src)
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

    def set_audio(self, src: str, start_time: int = 0, duration: int = None):
        self.audio.append(
            AudioFileClip(src).subclip(start_time, duration or self.duration)
        )
        self.video.audio = CompositeAudioClip(self.audio)

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


def extract_sub_clip(clip: Clip, start_second: int = 0, end_second: int = None):
    modified_clip = Clip(video_src=clip.video_src)
    modified_clip.set_video(ClipType.VIDEO_FILE_CLIP)
    try:
        modified_clip.video = modified_clip.video.subclip(start_second, end_second)
        return modified_clip
    except Exception as e:
        print(e)


def fx_modify_clip(*args, **kwargs):
    start_second = kwargs.get("start_second")
    end_second = kwargs.get("end_second")

    modified_clip = Clip(video_src=kwargs.get("clip").video_src)
    modified_clip.set_video(ClipType.VIDEO_FILE_CLIP)

    clip_parts = list()

    try:
        clip_parts.append(extract_sub_clip(modified_clip, 0, start_second).video)
        clip_parts.append(
            modified_clip.video.subclip(start_second, end_second).fx(*args)
        )
        if end_second:
            clip_parts.append(
                extract_sub_clip(
                    modified_clip, end_second, modified_clip.duration
                ).video
            )
        concatenated_clip = concatenate_videoclips(clip_parts)
        modified_clip.video = concatenated_clip
        return modified_clip
    except Exception as e:
        print(e)


def volume_clip_change(
    clip: Clip, start_second: int = 0, end_second: int = None, volume: float = 1.0
):
    return fx_modify_clip(
        afx.volumex,
        volume,
        clip=clip,
        start_second=start_second,
        end_second=end_second,
    )


def speed_clip_change(
    clip: Clip, start_second: int = 0, end_second: int = None, speed: float = 1.0
):
    return fx_modify_clip(
        vfx.speedx,
        speed,
        clip=clip,
        start_second=start_second,
        end_second=end_second,
    )
