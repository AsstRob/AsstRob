import cv2
import numpy as np

# config yolo network
network = cv2.dnn.readNet("config/tiny/yolov3-tiny.weights", "config/tiny/yolov3-tiny.cfg")
# network = cv2.dnn.readNet("config/416/yolov3-416.weights", "config/416/yolov3-416.cfg")

# class labels from names
labels = []
# load names file
with open("config/coco.names", "r") as names_file:
    labels = names_file.read().splitlines()

# print(labels)
# image (no loop)
# img = cv2.imread("img.jpg")
# video capture
capture = cv2.VideoCapture(0)
while True:
    _, img = capture.read()

    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1/255, (416,416), (0,0,0), swapRB=True, crop=False)
    network.setInput(blob)
    output_layer_names = network.getUnconnectedOutLayersNames()
    layer_outputs = network.forward(output_layer_names)

    boxes = []
    confidences = []
    label_ids = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            label_id = np.argmax(scores)
            confidence = scores[label_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)

                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x,y,w,h])
                confidences.append(float(confidence))
                label_ids.append(label_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(boxes), 3))

    if len(indexes) > 0:
        for i in indexes.flatten():
            x,y,w,h = boxes[i]
            label = str(labels[label_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            cv2.putText(img, label + "" + confidence, (x, y+20), font, 2, (255, 255, 255), 2)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    # breaks loop on Esc key press
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()