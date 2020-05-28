import cv2
import numpy as np

# config yolo network
network = cv2.dnn.readNet("config/yolov3-tiny.weights", "config/yolov3-tiny.cfg")

# class labels from names
labels = []
# load names file
with open("config/coco.names", "r") as names_file:
    labels = names_file.read().splitlines()

# print(labels)

