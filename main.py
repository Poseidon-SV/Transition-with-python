from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, CompositeVideoClip, ImageClip, transfx


def transition_pace(fade_duration = 0.5, effect_duration = 0.3, clip_duration = 0.3):
    return fade_duration, effect_duration, clip_duration

fade_duration, effect_duration, clip_duration = transition_pace()


'''FADE TRANSITION'''

width = 854
height = 480
resolution = (height, width)


video_1 = VideoFileClip("output_rupali_with_micro.mp4",target_resolution = resolution)
video_2 = VideoFileClip("1st_output_redcliff_message.mp4",target_resolution = resolution)

fade_video_1 = video_1.fx(vfx.fadein, fade_duration).fx(vfx.fadeout, fade_duration)
fade_video_2 = video_2.fx(vfx.fadein, fade_duration)

final_video = concatenate_videoclips([fade_video_1,fade_video_2])
final_video.write_videofile("fade_transition_video.mp4")


'''SLIDE TRANSITION'''

video_1_duration = video_1.duration
video_1_frame = video_1.get_frame(video_1_duration-0.2)

video_2_frame = video_2.get_frame(0)

clip1 = ImageClip(video_1_frame).set_duration(clip_duration)
clip2 = (ImageClip(video_2_frame).resize(clip1.size).set_duration(clip_duration))

clips = [clip1, clip2]

first_clip = CompositeVideoClip([clips[0].fx(transfx.slide_out, duration=effect_duration, side="left")]).set_start((clip_duration - effect_duration) * 0)
last_clip = CompositeVideoClip([clips[-1].fx(transfx.slide_in, duration=effect_duration, side="right")]).set_start((clip_duration - effect_duration) * (len(clips) - 1))

videos = (
    [first_clip]
    + [
        (
            CompositeVideoClip(
                [clip.fx(transfx.slide_in, duration=effect_duration, side="right")]
            )
            .set_start((clip_duration - effect_duration) * idx)
            .fx(transfx.slide_out, duration=effect_duration, side="left")
        )

        for idx, clip in enumerate(clips[1:-1], start=1)
    ]
    + [last_clip]
)

slide_clip = CompositeVideoClip(videos)

final_video = concatenate_videoclips([video_1,slide_clip,video_2])
final_video.write_videofile("slide_transition_video.mp4")


'''JOINED TRANSITION'''

final_video = concatenate_videoclips([fade_video_1,fade_video_2,video_1,slide_clip,video_2])
final_video.write_videofile("joined_transition_video.mp4")