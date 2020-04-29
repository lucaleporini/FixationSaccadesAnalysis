# simple implementation of CAM in PyTorch for the networks such as ResNet, DenseNet, SqueezeNet, Inception

import requests
from PIL import Image
from torchvision import models, transforms
from torch.autograd import Variable
from torch.nn import functional as F
import numpy as np
import cv2


# estrazione dei punti di massima salienza dalla heatmap --------------------------------------------------------------
def bounding_box(pixel_array, width, height):
    min_x = width+1
    max_x = -1
    min_y = height+1
    max_y = -1
    for pixel in pixel_array:
        if pixel[0] < min_x:
            min_x = pixel[0]
        if pixel[1] < min_y:
            min_y = pixel[1]
        if pixel[0] > max_x:
            max_x = pixel[0]
        if pixel[1] > max_y:
            max_y = pixel[1]
    return [(min_x, min_y), (max_x, max_y)]


def heatmap_extracting(heatmap):
    height, width, _ = heatmap.shape
    img_scalegray = cv2.cvtColor(heatmap, cv2.COLOR_BGR2GRAY)
    max_salient_pixels = []
    max_gray = -1
    for x in range(width): # put your block width size
        for y in range(height): # your block heigh size
            current_pixel = img_scalegray[y][x] # reading elements from pixel on location (x,y)
            if current_pixel > max_gray:
                max_gray = current_pixel
                max_salient_pixels = [(x, y)]
            elif current_pixel == max_gray:
                max_salient_pixels.append((x, y))

    return bounding_box(max_salient_pixels, width, height)
    # return max_salient_pixels

# --------------------------------------------------------------------------------------------------------------------


def returnCAM(feature_conv, weight_softmax, class_idx):
    # generate the class activation maps upsample to 256x256
    size_upsample = (256, 256)
    bz, nc, h, w = feature_conv.shape
    output_cam = []
    for idx in class_idx:
        cam = weight_softmax[idx].dot(feature_conv.reshape((nc, h*w)))
        cam = cam.reshape(h, w)
        cam = cam - np.min(cam)
        cam_img = cam / np.max(cam)
        cam_img = np.uint8(255 * cam_img)
        output_cam.append(cv2.resize(cam_img, size_upsample))
    return output_cam


def run(frame, frame_number, model_id, video_folder, option):
    # input image
    LABELS_URL = 'https://s3.amazonaws.com/outcome-blog/imagenet/labels.json'
    #IMG_URL = 'http://media.mlive.com/news_impact/photo/9933031-large.jpg'
    img_to_load = frame

    # networks such as googlenet, resnet, densenet already use global average pooling at the end, so CAM could be used directly.
    #model_id = 1
    if model_id == 1:
        net = models.squeezenet1_1(pretrained=True)
        finalconv_name = 'features' # this is the last conv layer of the network
    elif model_id == 2:
        net = models.resnet18(pretrained=True)
        finalconv_name = 'layer4'
    elif model_id == 3:
        net = models.densenet161(pretrained=True)
        finalconv_name = 'features'

    net.eval()

    # hook the feature extractor
    features_blobs = []

    def hook_feature(module, input, output):
        features_blobs.append(output.data.cpu().numpy())

    net._modules.get(finalconv_name).register_forward_hook(hook_feature)

    # get the softmax weight
    params = list(net.parameters())
    weight_softmax = np.squeeze(params[-2].data.numpy())

    normalize = transforms.Normalize(
       mean=[0.485, 0.456, 0.406],
       std=[0.229, 0.224, 0.225]
    )

    preprocess = transforms.Compose([
       transforms.Resize((224, 224)),
       transforms.ToTensor(),
       normalize
    ])

    # img_pil = Image.open(img_to_load)
    img_pil = Image.fromarray(img_to_load)
    img_tensor = preprocess(img_pil)
    img_variable = Variable(img_tensor.unsqueeze(0))
    logit = net(img_variable)

    # download the imagenet category list
    classes = {int(key):value for (key, value) in requests.get(LABELS_URL).json().items()}

    h_x = F.softmax(logit, dim=1).data.squeeze()
    probs, idx = h_x.sort(0, True)
    probs = probs.numpy()
    idx = idx.numpy()

    # output the prediction
    # for i in range(0, 5):
    #    print('{:.3f} -> {}'.format(probs[i], classes[idx[i]]))

    # generate class activation mapping for the top1 prediction
    CAMs = returnCAM(features_blobs[0], weight_softmax, [idx[0]])

    if frame_number%10 == 0:
        print('---- CAM_frame_'+str(frame_number)+'.jpg for the top1 prediction: {} -> {}'.format(classes[idx[0]], probs[0]))

    height, width, _ = img_to_load.shape
    heatmap = cv2.applyColorMap(cv2.resize(CAMs[0], (width, height)), cv2.COLORMAP_BONE)

    # estraggo il massimo punto di salienza e ottengo un bounding box
    salient_bbox = heatmap_extracting(heatmap)
    max_salient_pixel = ((salient_bbox[0][0] + salient_bbox[1][0])/2, (salient_bbox[0][1] + salient_bbox[1][1])/2)

    # write image CAM with max_salient_pixel
    if option == "w":
        writeImageCAM(heatmap, img_to_load, max_salient_pixel, video_folder, frame_number)

    # return salient_bbox
    return max_salient_pixel


# render the CAM and output
def writeImageCAM(heatmap, image, max_salient_pixel, video_folder, frame_number):
    height, width, _ = image.shape
    # apply the heatmap on the image
    result = heatmap * 0.5 + image * 0.3
    color_white = (255, 255, 255)
    for x in range(int(max_salient_pixel[0])-20, int(max_salient_pixel[0])+20):
        for y in range(int(max_salient_pixel[1])-20, int(max_salient_pixel[1])+20):
            if x < width and y < height:
                result[y][x] = color_white
    cv2.imwrite(video_folder+'/CAM_frame_'+str(frame_number)+'.jpg', result)

