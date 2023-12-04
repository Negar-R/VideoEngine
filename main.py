import os
from clip import Clip, ClipType, extract_sub_clip, volume_clip_change, speed_clip_change
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


def task02_part_by_part_run():
    clip = Clip(video_src=os.getenv("TASK02_VIDEO_SRC"))
    clip.set_video(ClipType.VIDEO_FILE_CLIP)

    extracted_clip = extract_sub_clip(clip, 5, 15)
    Clip.write(extracted_clip.video, "outputs/task02_part1.mp4")

    volume_changed_clip = volume_clip_change(clip, 5, 10, 0.1)
    Clip.write(volume_changed_clip.video, "outputs/task02_part2.mp4")

    speed_changed_clip = speed_clip_change(clip, 10, None, 1.5)
    Clip.write(speed_changed_clip.video, "outputs/task02_part3.mp4")


def task03_run():
    clip = Clip(width=video_width, height=video_height, duration=5)
    clip.set_video(ClipType.VIDEO_CLIP)
    clip.set_background_img(
        os.getenv("TASK03_IMG_SRC"), resize=False, position=("center", "center")
    )
    clip.set_background_color([204, 198, 200])
    Clip.write(
        clip.create_composite_clip(
            clip.video, clip.background_color, *clip.background_img
        ),
        os.getenv("TASK03_OUTPUT"),
    )


if __name__ == "__main__":
    task01_run()
    task02_part_by_part_run()
    task03_run()
