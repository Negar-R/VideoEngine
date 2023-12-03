import os
from clip import Clip
from text import Text
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    video_width = int(os.getenv("VIDEO_WIDTH"))
    video_height = int(os.getenv("VIDEO_HEIGHT"))
    short_duration = int(os.getenv("SHORT_DURATION"))

    text = Text(os.getenv("TASK01_FONT_SRC"), os.getenv("TASK01_MSG"))
    text = text.create_text_clip(
        color=os.getenv("TASK01_TXT_COLOR"),
        method=os.getenv("TASK01_TXT_METHOD"),
        size=(int(os.getenv("TASK01_TXT_SIZE_X")), int(os.getenv("TASK01_TXT_SIZE_Y"))),
        fontsize=int(os.getenv("TASK01_TXT_FONTSIZE")),
    )
    clip = Clip(video_width, video_height, short_duration)
    clip.set_background_img(os.getenv("TASK01_IMG_SRC"))
    clip.set_text(text, position=((50, 150)))
    clip.write(os.getenv("TASK01_OUTPUT"))
