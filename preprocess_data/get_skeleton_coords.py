import cv2
import mediapipe as mp
import numpy as np
import os

def get_input_coords(video_id, in_video, input_coords_dir):
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_holistic = mp.solutions.holistic

    # Input video attributes
    cap = cv2.VideoCapture(in_video)
    frame_count = 0
    w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)

    with mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as holistic:
        count = 0
        x_list = []
        y_list = []
        z_list = []
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # image = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE)
            (h, w) = image.shape[:2]
            empty_image = np.zeros((h, w, 3))
            results = holistic.process(image)

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            """
            mp_drawing.draw_landmarks(
                empty_image,
                results.pose_landmarks,
                mp_holistic.POSE_CONNECTIONS)
    
            mp_drawing.draw_landmarks(
                empty_image,
                results.face_landmarks,
                mp_holistic.FACE_CONNECTIONS)
            """
            mp_drawing.draw_landmarks(
                image,
                results.right_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS)

            mp_drawing.draw_landmarks(
                image,
                results.left_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS)
            if (results.right_hand_landmarks):
                if (count % 4 == 0):
                    x_list.append([data_point.x for data_point in results.right_hand_landmarks.landmark])
                    y_list.append([data_point.y for data_point in results.right_hand_landmarks.landmark])
                    z_list.append([data_point.z for data_point in results.right_hand_landmarks.landmark])
                count = count + 1
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
            if cv2.waitKey(10) & 0xFF == ord('q'):  # or count == 40:
                break
    cap.release()
    cv2.destroyAllWindows()

    np.savetxt(data_path + path_name + '/' + path_name + "_X.txt", np.asarray(x_list), fmt="%f")
    np.savetxt(data_path + path_name + '/' + path_name + "_Y.txt", np.asarray(y_list), fmt="%f")
    np.savetxt(data_path + path_name + '/' + path_name + "_Z.txt", np.asarray(z_list), fmt="%f")