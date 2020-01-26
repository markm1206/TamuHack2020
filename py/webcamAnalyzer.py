import cv2
import io
import numpy as np
from PIL import Image
from google.cloud import vision


client = vision.ImageAnnotatorClient()
response = client.annotate_image({
  'image': {'source': {'image_uri': 'gs://my-test-bucket/image.jpg'}},
  'features': [{'type': vision.enums.Feature.Type.FACE_DETECTION}],
})
##google cloud stuff 


cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False


count = 0 #create a counter so that i can only capture every 20th frame

imgBuff = []

while rval:
    count += 1
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

    a = np.matrix('0 -1 0; -1 5 -1;0 -1 0')

    content = Image.fromarray(frame, 'RGB').tobytes()

    if count == 20 : 
        image = vision.types.Image(content=content)

        response = client.label_detection(image=image)
        labels = response.label_annotations
        print('Labels:')
        print(labels)
        for label in labels:
            print(label.description)
        count = 0

    

    if response.error.message:
        print("bad img")
        """
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))"""
    #frame2 = np.dot(frame,a)
    #cv2.imshow("test",frame2)
cv2.destroyWindow("preview")
cv2.destroyWindow("test")


