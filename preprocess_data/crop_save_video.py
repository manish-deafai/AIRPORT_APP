import cv2
import os
from datetime import datetime as dt

def get_crop_paramsfromcsv():
    pass

def crop_video(video, crop_dimensions, save_dir, video_id, start_frame=None, end_frame=None, start_ts=None,
               end_ts=None):
    """

    :param video: Video file path
    :param crop_dimensions: Crop dimensions as x1, y1, width, height
    :param start_ts: Optional: Starting timestamp of video in HH:MM:SS format
    :param end_ts: Optional: Ending timestamp of video in HH:MM:SS format
    :param start_frame: Optional: Start frame of video to crop (Overrides start_ts)
    :param end_frame: Optional: End frame of video to crop (Overrides end_ts)
    :return: Saves cropped video
    """
    cap = cv2.VideoCapture(video)
    frame_count = 0

    # Input video attributes
    w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)
    x1, y1, x2, y2 = crop_dimensions

    # Determine start and end of the cropped video based on input parameters

    if start_frame is None and start_ts is not None:
        start_ts = dt.strptime(start_ts, '%H:%M:%S').time()
        start_seconds = start_ts.hour * 3600 + start_ts.minute * 60 + start_ts.second
        start_frame = fps * start_seconds

    if end_frame is None and end_ts is not None:
        end_ts = dt.strptime(end_ts, '%H:%M:%S').time()
        end_seconds = start_ts.hour * 3600 + start_ts.minute * 60 + start_ts.second
        end_frame = fps * end_seconds

    # output video
    out_video = video_id + '.mp4'
    out_video = os.path.join(save_dir, out_video)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_video, fourcc=fourcc, fps=fps, frameSize=(x2-x1, y2-y1))

    while cap.isOpened():
        ret, frame = cap.read()
        frame_count += 1

        if ret is True:
            # Start and end frame both specified
            if start_frame and end_frame:
                if end_frame > start_frame and frame_count >= start_frame:
                    cropped_frame = frame[y1:y2, x1:x2]
                    out.write(cropped_frame)
                else:
                    print('Please check the start and end frame numbers.')
                    break

            # Only start frame specified
            elif start_frame and frame_count >= start_frame:
                cropped_frame = frame[y1:y2, x1:x2]
                out.write(cropped_frame)

            # Only end frame specified
            elif end_frame and frame_count <= end_frame:
                cropped_frame = frame[y1:y2, x1:x2]
                out.write(cropped_frame)

            # Default when start and end frame are not specified
            else:
                cropped_frame = frame[y1:y2, x1:x2]
                out.write(cropped_frame)

            # Uncomment below lines to see the cropped video in real-time
            # cv2.imshow('frame', frame)
            # cv2.imshow('croped', cropped_frame)

        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def main():
    crop_video()


if __name__ == "__main__":
    main()
