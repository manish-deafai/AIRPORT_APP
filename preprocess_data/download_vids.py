import os
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import cv2
import pandas
import re
import shutil
import datetime
import matplotlib.pyplot as plt

def extract_youtube_id(url):
    """
    Used to extract video id from the given youtube video url.
    :param url: Youtube video url. Example: https://www.youtube.com/watch?v=xvqyqMl0Adg
    :return: video_id: xvqyqMl0Adg
    """
    vid_id_regex = r'\?v=[a-zA-Z0-9]*'  # Matches an expression like '?v=xvqyqMl0Adg'
    vid_id = re.findall(vid_id_regex, url)
    return vid_id[0][3:]


def download_vid(url, video_dir, audio_dir):
    """
        Downloads video from a given youtube url, and saves audio and video in given directories.
        https://gist.github.com/sidneys/7095afe4da4ae58694d128b1034e01e2
    """
    vid = YouTube(url)
    ext = '.mp4'
    # title = vid.yt.streams[0].default_filename
    video_id = extract_youtube_id(url)
    filename = video_id + '.mp4'
    vid.streams.get_by_itag(135).download(output_path=video_dir, filename=filename)
    vid.streams.get_by_itag(139).download(output_path=audio_dir, filename=filename)


def download_captions(url, captions_dir):
    """
        Downloads captions from a given youtube url.
    """
    video_id = extract_youtube_id(url)
    srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    caption_file_name = video_id + '.txt'
    caption_path = os.path.join(captions_dir, caption_file_name)

    with open(caption_path, "w") as f:
        for i in srt:
            # writing each element of srt on a new line
            f.write("{}\n".format(i))


def download_vidsfromcsv(input_csv, video_dir, audio_dir):
    """
    Downloads videos from a given csv file
    :return:
    """
    video_tag = 135
    audio_tag = 139

    # youtube video stream format codes:
    # https://gist.github.com/sidneys/7095afe4da4ae58694d128b1034e01e2

    video_data_file = pandas.read_csv(input_csv)
    videos = list(video_data_file['videos'])
    captions = list(video_data_file['captions'])

    for url, caption_flag in zip(videos, captions):
        download_vid(url, video_dir, audio_dir)

        if caption_flag:
            download_captions(url, captions_dir)


def main():
    download_vidsfromcsv('path_to_input_csv.csv')


if __name__ == "__main__":
    main()
