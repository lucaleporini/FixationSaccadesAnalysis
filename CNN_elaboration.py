import os
import cv2
from CAM_master import pytorch_CAM


def run(video_path, result_path, model_CAM, w_option=None):

    vidcap = cv2.VideoCapture(video_path)

    images_folder = ""
    if w_option is not None:
        # create folder for images CAM
        images_folder = result_path+"/CAM_images_mod_"+str(model_CAM)
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)


    tracking_salient_points = []

    # split video frame x frame
    success, image = vidcap.read()
    count = 0
    while success:
        max_salient_pixel = pytorch_CAM.run(image, count, model_CAM, images_folder, w_option)
        tracking_salient_points.append((count, max_salient_pixel[0], max_salient_pixel[1]))
        success, image = vidcap.read()
        count += 1

    return tracking_salient_points



