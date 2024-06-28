# import torch
# import torchvision.handlers as handlers
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from pathlib import Path
import os

class FaceRec():
  def __init__(self) -> None:
    
    self.app = FaceAnalysis(allowed_modules=['detection']) # enable detection handler only
    self.app.prepare(ctx_id=0, det_size=(640, 640))
    cwd = Path(__file__).parent
    handler_path = os.path.join(cwd,"model","model.onnx") 

    self.handler = insightface.model_zoo.get_model(handler_path)
    self.handler.prepare(ctx_id=0)

  def findCosineDistance(self,source_representation, test_representation):
      a = np.matmul(np.transpose(source_representation), test_representation)
      b = np.sum(np.multiply(source_representation, source_representation))
      c = np.sum(np.multiply(test_representation, test_representation))
      return 1 - (a / (np.sqrt(b) * np.sqrt(c)))


  def get_face(self,image,bbox):
    ystart=int(np.round(bbox[1]))
    ystop=int(np.round(bbox[3]))
    xstart=int(np.round(bbox[0]))
    xstop=int(np.round(bbox[2]))


    return image[ystart:ystop, xstart:xstop]
  def get_faces(self,image_file,app):
    print(image_file)
    image=cv2.imread(image_file)
    print("ran successsfuly")
    faces=self.app.get(image)
    faces_cropped=[]
    for i in faces:
      faces_cropped.append(self.get_face(image,i['bbox']))
    return faces_cropped
  def get_feats(self,image):
    return self.handler.get_feat(self.get_faces(image,self.app))

  def verify_face(self,src_feats, tar_feats ,match_thresh=0.7 ):
    
    #src_feats=self.handler.get_feat(self.get_faces(src_image,self.app))
    min=100
    image_found=None
    for i in range(len(tar_feats)):
      #tar_feats=self.handler.get_feat(self.get_faces(image,self.app))
      for k in src_feats:
        for j in tar_feats[i]:
          diff=self.findCosineDistance(k,j)
          if (diff<=match_thresh and diff<min):
            min=diff
            image_found=i
    return image_found

# src_image="C:\\Users\\2016n\\OneDrive\\Desktop\\FaceRecExt\\find-person-main\\static\\photos\\died_eliz1_4L1D4Hu.jpg"
# tar_images=["C:\\Users\\2016n\\OneDrive\\Desktop\\FaceRecExt\\find-person-main\\static\\photos\\e.jpg"]
# FA=FaceRec()
# print(FA.verify_face(src_image,tar_images))
