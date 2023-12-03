from moviepy.editor import TextClip
from PIL import ImageFont
from typing import List


class Text:
    def __init__(self, font_file: str, msg: str) -> None:
        self.font_file = font_file
        self.msg = msg
        self.font_name = self.get_name()

    def get_name(self):
        return ImageFont.truetype(font=self.font_file).getname()[0]

    def create_text_clip(self, **kwargs):
        return TextClip(txt=self.msg, font=self.font_name, **kwargs)
