# import the necessary packages
import argparse
import dlib
# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-p", "--predictor", required=True,
# 	help="path to trained dlib shape predictor model")
# ap.add_argument("-x", "--xml", required=True,
# 	help="path to input training/testing XML file")
# args = vars(ap.parse_args())
# compute the error over the supplied data split and display it to
# our screen
print("[INFO] evaluating shape predictor...")
error = dlib.test_shape_predictor('D:/Hoc_Tap/Ki2_Nam3/PBL5/ibug_300W_large_face_landmark_dataset/labels_ibug_300W_train_eyes.xml', 'D:/Hoc_Tap/Ki2_Nam3/PBL5/code/eye_predictor.dat')
print("[INFO] error: {}".format(error))