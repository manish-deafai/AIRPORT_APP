"""
Configs in this file:
video : path to video
frame_save_dir : path to save the extracted frames
"""


import math
import os
import cv2
import datetime

class FrameExtractor():
    """
    Class used for extracting frames from a video file.
    Code borrowed from https://towardsdatascience.com/the-easiest-way-to-download-youtube-videos-using-python-2640958318ab
    """

    def __init__(self, video_dir):
        self.video_dir = video_dir
        self.vid_cap = cv2.VideoCapture(video_dir)
        self.n_frames = int(self.vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.vid_cap.get(cv2.CAP_PROP_FPS))

    def get_video_duration(self):
        duration = self.n_frames / self.fps
        print(f'Duration: {datetime.timedelta(seconds=duration)}')

    def get_n_images(self, every_x_frame):
        n_images = math.floor(self.n_frames / every_x_frame) + 1
        print(f'Extracting every {every_x_frame} (nd/rd/th) frame would result in {n_images} images.')

    def extract_frames(self, every_x_frame, img_name, dest_path=None, img_ext='.jpg'):
        if not self.vid_cap.isOpened():
            self.vid_cap = cv2.VideoCapture(self.video_dir)

        if dest_path is None:
            dest_path = os.getcwd()
        else:
            if not os.path.isdir(dest_path):
                os.mkdir(dest_path)
                print(f'Created the following directory: {dest_path}')

        frame_cnt = 0
        img_cnt = 0

        while self.vid_cap.isOpened():

            success, image = self.vid_cap.read()

            if not success:
                break

            if frame_cnt % every_x_frame == 0:
                img_path = os.path.join(dest_path, ''.join([img_name, '_', str(img_cnt), img_ext]))
                cv2.imwrite(img_path, image)
                img_cnt += 1

            frame_cnt += 1

        self.vid_cap.release()
        cv2.destroyAllWindows()


def main():
    video = 'path_to_video'
    frame_save_dir = 'frame_path'
    fe = FrameExtractor(video)
    fe.get_video_duration()
    fe.extract_frames(every_x_frame=1,img_name=os.path.basename(video), dest_path= frame_save_dir)


if __name__ == "__main__":
    main()
