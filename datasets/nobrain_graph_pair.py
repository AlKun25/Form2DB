import torch.utils.data
import numpy as np
import json, re
#from skimage import io
#from skimage import draw
#import skimage.transform as sktransform
import os
import math, random
from collections import defaultdict, OrderedDict
from utils.funsd_annotations import createLines
import timeit
from .graph_pair import GraphPairDataset

import utils.img_f as img_f

SKIP=['174']#['193','194','197','200']
ONE_DONE=[]


def collate(batch):
    assert(len(batch)==1)
    return batch[0]


class NobrainGraphPair(GraphPairDataset):
    """
    Class for reading forms dataset and creating starting and ending gt
    """


    def __init__(self, dirPath=None, split=None, config=None, images=None):
        super(NobrainGraphPair, self).__init__(dirPath,split,config,images)

        self.images=[]
        self.images.append({'id':'0', 'imagePath':'../data/FUNSD/training_data/images/12825369.png', 'annotationPath':'../data/english_char_set.json', 'rescaled':1.0, 'imageName':'0'})

        if 'textfile' in config:
            with open(config['textfile']) as f:
                text = f.read()
            text=re.sub('\s+',' ',text)
            self.words = text.strip().split(' ')
        else:
            self.words = None



    def parseAnn(self,annotations,s):
        numClasses=4

        bbs = np.empty((1,0, 8+8+numClasses), dtype=np.float32) #2x4 corners, 2x4 cross-points, n classes


        word_boxes=[]
        word_trans=[]

        if self.words is None:
            bb=[None]*16
            lX=0
            rX=10
            tY=0
            bY=10
            bb[0]=lX*s
            bb[1]=bY*s
            bb[2]=lX*s
            bb[3]=tY*s
            bb[4]=rX*s
            bb[5]=tY*s
            bb[6]=rX*s
            bb[7]=bY*s
            bb[8]=s*(lX+rX)/2.0
            bb[9]=s*bY
            bb[10]=s*(lX+rX)/2.0
            bb[11]=s*tY
            bb[12]=s*lX
            bb[13]=s*(tY+bY)/2.0
            bb[14]=s*rX
            bb[15]=s*(tY+bY)/2.0
            word_boxes.append(bb)
            word_trans.append('name:')

            bb=[None]*16
            lX=10
            rX=20
            tY=0
            bY=10
            bb[0]=lX*s
            bb[1]=bY*s
            bb[2]=lX*s
            bb[3]=tY*s
            bb[4]=rX*s
            bb[5]=tY*s
            bb[6]=rX*s
            bb[7]=bY*s
            bb[8]=s*(lX+rX)/2.0
            bb[9]=s*bY
            bb[10]=s*(lX+rX)/2.0
            bb[11]=s*tY
            bb[12]=s*lX
            bb[13]=s*(tY+bY)/2.0
            bb[14]=s*rX
            bb[15]=s*(tY+bY)/2.0
            word_boxes.append(bb)
            word_trans.append('Skynet')

            bb=[None]*16
            lX=0
            rX=10
            tY=10
            bY=20
            bb[0]=lX*s
            bb[1]=bY*s
            bb[2]=lX*s
            bb[3]=tY*s
            bb[4]=rX*s
            bb[5]=tY*s
            bb[6]=rX*s
            bb[7]=bY*s
            bb[8]=s*(lX+rX)/2.0
            bb[9]=s*bY
            bb[10]=s*(lX+rX)/2.0
            bb[11]=s*tY
            bb[12]=s*lX
            bb[13]=s*(tY+bY)/2.0
            bb[14]=s*rX
            bb[15]=s*(tY+bY)/2.0
            word_boxes.append(bb)
            word_trans.append('Month:')

            bb=[None]*16
            lX=10
            rX=20
            tY=10
            bY=20
            bb[0]=lX*s
            bb[1]=bY*s
            bb[2]=lX*s
            bb[3]=tY*s
            bb[4]=rX*s
            bb[5]=tY*s
            bb[6]=rX*s
            bb[7]=bY*s
            bb[8]=s*(lX+rX)/2.0
            bb[9]=s*bY
            bb[10]=s*(lX+rX)/2.0
            bb[11]=s*tY
            bb[12]=s*lX
            bb[13]=s*(tY+bY)/2.0
            bb[14]=s*rX
            bb[15]=s*(tY+bY)/2.0
            word_boxes.append(bb)
            word_trans.append('May')
        else:
            self.qa=[]
            cY=0
            for i in range(self.questions):
                words = random.sample(self.words,k=4)
                q = words[0]+' '+words[1]
                a = words[2]+' '+words[3]

                bb=[None]*16
                lX=0
                rX=10
                tY=cY
                bY=cY+10
                bb[0]=lX*s
                bb[1]=bY*s
                bb[2]=lX*s
                bb[3]=tY*s
                bb[4]=rX*s
                bb[5]=tY*s
                bb[6]=rX*s
                bb[7]=bY*s
                bb[8]=s*(lX+rX)/2.0
                bb[9]=s*bY
                bb[10]=s*(lX+rX)/2.0
                bb[11]=s*tY
                bb[12]=s*lX
                bb[13]=s*(tY+bY)/2.0
                bb[14]=s*rX
                bb[15]=s*(tY+bY)/2.0
                word_boxes.append(bb)
                word_trans.append(q)

                bb=[None]*16
                lX=10
                rX=20
                tY=cY
                bY=cY+10
                bb[0]=lX*s
                bb[1]=bY*s
                bb[2]=lX*s
                bb[3]=tY*s
                bb[4]=rX*s
                bb[5]=tY*s
                bb[6]=rX*s
                bb[7]=bY*s
                bb[8]=s*(lX+rX)/2.0
                bb[9]=s*bY
                bb[10]=s*(lX+rX)/2.0
                bb[11]=s*tY
                bb[12]=s*lX
                bb[13]=s*(tY+bY)/2.0
                bb[14]=s*rX
                bb[15]=s*(tY+bY)/2.0
                word_boxes.append(bb)
                word_trans.append(a)

                self.qa.append((q,a,None))

                cY+=11

        word_boxes = np.array(word_boxes)
        trans = []
        groups = []

        return bbs, list(range(bbs.shape[1])), numClasses, trans, groups, {}, {'word_boxes':word_boxes, 'word_trans':word_trans}


    def getResponseBBIdList(self,queryId,annotations):
        if self.split_to_lines:
            return annotations['linking'][queryId]
        else:
            boxes=annotations['form']
            cto=[]
            boxinfo = boxes[queryId]
            for id1,id2 in boxinfo['linking']:
                if id1==queryId:
                    cto.append(id2)
                else:
                    cto.append(id1)
            return cto

    def makeQuestions(self,bbs,transcription,groups,groups_adj):
        if self.words is not None:
            return self.qa
        new_all_q_a=[]
        new_all_q_a.append(('name:','skynet',None))
        new_all_q_a.append(('month:','may',None))
        return new_all_q_a


