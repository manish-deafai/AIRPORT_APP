import os

from download_vids import download_vid, download_captions, extract_youtube_id
from crop_save_video import crop_video
from detect_interpreter import get_body_crop


def prepare_dirs():
    root = os.path.dirname(os.getcwd())
    data_dir = os.path.join(root, 'data')
    video_dir = os.path.join(data_dir, 'video')
    audio_dir = os.path.join(data_dir, 'audio')
    captions_dir = os.path.join(data_dir, 'captions')
    cropped_vid_dir = os.path.join(data_dir, 'cropped_vids')
    input_skeleton_coords_dir = os.path.join(data_dir, 'in_coords')

    if not os.path.exists(data_dir):
        os.makedirs(audio_dir)
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    if not os.path.exists(video_dir):
        os.makedirs(video_dir)
    if not os.path.exists(captions_dir):
        os.makedirs(captions_dir)
    if not os.path.exists(cropped_vid_dir):
        os.makedirs(cropped_vid_dir)

    return root, data_dir, video_dir, audio_dir, captions_dir, cropped_vid_dir


def main():
    root, data_dir, video_dir, audio_dir, captions_dir, cropped_vid_dir = prepare_dirs()

    # Input list of urls here or use download or use download_vidfromcsv function
    urls = ['https://www.youtube.com/watch?v=tkMg8g8vVUo']
    for url in urls:
        download_vid(url, video_dir, audio_dir)
        # download_captions(url, captions_dir)
        video_id = extract_youtube_id(url)
        video = os.path.join(video_dir, str(video_id + '.mp4'))

        body_crop_dims = get_body_crop(video)

        crop_video(video, body_crop_dims, cropped_vid_dir, video_id)


if __name__ == "__main__":
    main()
