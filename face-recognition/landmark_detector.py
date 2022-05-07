import sys
import os
import dlib
import glob
from skimage import io

predictor_path = '../../../libraries/dlib-master/trained-models/shape_predictor_68_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

while True:
    if os.path.exists('tmp/face.png'):
        try:
            img = io.imread('tmp/face.png')
        except:
            continue
        os.remove('tmp/face.png')
        dets = detector(img, 1)
        for k, d in enumerate(dets):
            shape = predictor(img, d)
            fout_handle = open( 'tmp/marks.csv', mode='w')
            for p in range(shape.num_parts):
                fout_handle.write( str(shape.part(p).x) + ',' + str(shape.part(p).y) + '\n' )
            fout_handle.close()
            break; # store only first detected face!
