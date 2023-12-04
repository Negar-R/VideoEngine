import os
from clip import Clip, ClipType
from text import Text
from dotenv import load_dotenv

load_dotenv()

video_width = int(os.getenv("VIDEO_WIDTH"))
video_height = int(os.getenv("VIDEO_HEIGHT"))
short_duration = int(os.getenv("SHORT_DURATION"))


def task01_run():
    text = Text(os.getenv("TASK01_FONT_SRC"), os.getenv("TASK01_MSG"))
    text = text.create_text_clip(
        color=os.getenv("TASK01_TXT_COLOR"),
        method=os.getenv("TASK01_TXT_METHOD"),
        size=(int(os.getenv("TASK01_TXT_SIZE_X")), int(os.getenv("TASK01_TXT_SIZE_Y"))),
        fontsize=int(os.getenv("TASK01_TXT_FONTSIZE")),
    )
    clip = Clip(width=video_width, height=video_height, duration=short_duration)
    clip.set_background_img(os.getenv("TASK01_IMG_SRC"), resize=True)
    clip.set_text(text, position=((50, 150)))
    Clip.write(
        clip.create_composite_clip(*clip.background_img, *clip.text),
        os.getenv("TASK01_OUTPUT"),
    )


def task03_run():
    clip = Clip(width=video_width, height=video_height, duration=5)
    clip.set_video(ClipType.VIDEO_CLIP)
    clip.set_background_img(
        "assets/task03_img.jpg", resize=False, position=("center", "center")
    )
    clip.set_background_color([113, 181, 184])
    Clip.write(
        clip.create_composite_clip(
            clip.video, clip.background_color, *clip.background_img
        ),
        "outputs/task03.mp4",
    )


if __name__ == "__main__":
    task01_run()
    task03_run()
