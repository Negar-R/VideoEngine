import os
from clip import Clip
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    video_width = int(os.getenv("VIDEO_WIDTH"))
    video_height = int(os.getenv("VIDEO_HEIGHT"))
    short_duration = int(os.getenv("SHORT_DURATION"))

    clip = Clip(video_width, video_height, short_duration)
    clip.set_background_img(os.getenv("TASK01_IMG_SRC"))
    clip.write(os.getenv("TASK01_OUTPUT"))
