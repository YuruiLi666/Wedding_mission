from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import VideoClip
from moviepy.video.VideoClip import ColorClip
from moviepy.video.VideoClip import ImageClip
from PIL import Image
import numpy as np

# === 加载背景视频和地图图像 ===
video = VideoFileClip("合成.mp4")
map_img = Image.open("American_map.png")

# 缩放地图图像
scale = 0.8
target_width = int(video.w * scale)
target_height = int(video.h * scale)
map_img = map_img.resize((target_width, target_height))

# === 动画帧生成函数（展开效果）===
def make_frame(t):
    start_time = 1.0
    duration = 2.0
    progress = np.clip((t - start_time) / duration, 0, 1)

    # 计算左右展开的裁切区域
    half_width = int(target_width * 0.5 * progress)
    left = (target_width // 2) - half_width
    right = (target_width // 2) + half_width

    if half_width <= 0:
        return np.zeros((target_height, target_width, 3), dtype=np.uint8)

    cropped = map_img.crop((left, 0, right, target_height)).resize((target_width, target_height))
    # 创建空画布，把裁剪部分居中贴上去
    canvas = Image.new("RGB", (target_width, target_height), (0, 0, 0))
    canvas.paste(cropped, ((target_width - cropped.width) // 2, 0))

    return np.array(cropped)

# === 自定义地图动画片段（必须设置 size） ===
class CustomMapClip(VideoClip):
    def __init__(self, duration):
        super().__init__(duration=duration)
        self.size = (target_width, target_height)
        self.frame_function = make_frame

    def get_frame(self, t):
        return self.frame_function(t)

# === 创建地图展开动画并添加位置与透明度 ===
'''
scroll_video = VideoFileClip("合成.mp4")

map_clip = (
    ImageClip("American_map.png")
    .resized(0.76)  # 实际缩小地图
    .with_duration(scroll_video.duration)
    .with_position("center")
    .with_opacity(0.80)
)
'''
animated_map = (
    CustomMapClip(duration=video.duration)
    .resized(0.76)
    .with_position(("center", "center"))
    .with_opacity(0.95)
)

# === 合成最终视频 ===
final = CompositeVideoClip([video, animated_map])
final.write_videofile("final_scroll_combined_final.mp4", codec="libx264", audio=False)
