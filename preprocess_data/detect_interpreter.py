"""
    Detects presence of ASL interpreter in videos and returns coordinates of portion of the frame containing
    the ASL human interpreter.
    TODO: Update code to identify interpreter when multiple people are present in the scene.
"""
import os
import cv2
import dlib
import numpy as np
from frame_extractor import FrameExtractor


def multiface_detector(video, fps):
    ## Incomplete function
    n_detect_frames = 2

    # Extract frames from the video
    fe = FrameExtractor(video)
    vid_len = fe.get_video_duration()
    every_x_frame = vid_len * fps // n_detect_frames
    extracted_frames = fe.extract_frames(every_x_frame=1, img_name=os.path.basename(video))

    # Detect human faces
    detected_faces = []
    detector = dlib.get_frontal_face_detector()
    for frame in extracted_frames:
        gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        faces = detector(gray)
        detected_faces.append(faces)

    # for faces in detected_faces:
    #    if len(faces) > 1:


def get_body_crop(video):
    """
    Detects presence of face and return dims to crop for the ASL interprepter
    :param video: Video file path
    :return: x, y, w, h
    """
    crop_scale = 2
    cap = cv2.VideoCapture(video)
    detector = dlib.get_frontal_face_detector()

    while cap.isOpened():
        success, frame = cap.read()
        # shape = frame.shape

        if not success:
            break
        gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        faces = detector(gray)
        if len(faces) > 1:
            face = faces[0]
            x1 = face.left()  # left point
            y1 = face.top()  # top point
            x2 = face.right()  # right point
            y2 = face.bottom()  # bottom point

            x1_crop = int(max(0, x1 - crop_scale * np.abs(x2 - x1)))  # start of crop x-axis
            y1_crop = int(max(0, y1 - crop_scale * np.abs(y2 - y1)))  # start of crop y-axis
            x2_crop = int(min(frame.shape[1], x2 + crop_scale * np.abs(x2 - x1)))  # start of crop x-axis
            y2_crop = int(min(frame.shape[0], y2 + crop_scale * np.abs(y2 - y1)))  # start of crop y-axis

            break

    cap.release()
    cv2.destroyAllWindows()
    return x1_crop, y1_crop, x2_crop, y2_crop


def main():
    get_body_crop('path_to_video.mp4')


if __name__ == "__main__":
    main()
