import matlab.engine
import cv2
import os


def createImagesForLowLevelSaliency(video, result_path):
    if not os.path.exists(result_path+"/LLS_images"):
        print("create images for low level saliency ...")
        os.makedirs(result_path+"/LLS_images")
        success, image = video.read()
        count = 1
        while success:
            # from color to gray
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(result_path+"/LLS_images/frame_" + str(count) + ".png", img_gray)

            success, image = video.read()
            count += 1


def run(video_path, result_path):
    vidcap = cv2.VideoCapture(video_path)
    createImagesForLowLevelSaliency(vidcap, result_path)
    # width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # run script matlab for low level saliency
    eng = matlab.engine.start_matlab()
    eng.addpath('LLS_master/', '-end')
    result = eng.LLS(result_path)
    LLS_data = [(i, result[i][1], result[i][0]) for i in range(0, len(result))]
    eng.quit()
    return LLS_data



