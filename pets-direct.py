# %matplotlib inline

from __future__ import division,print_function

import os, json
from glob import glob
import numpy as np
import sys
# np.set_printoptions(precision=4, linewidth=100)
# from matplotlib import pyplot as plt

# Import our class, and instantiate
from vgg16 import Vgg16

path = sys.argv[1]

def pet_id(imgs):

  #all_preds = vgg.model.predict(imgs)
  all_preds=vgg.model.predict(imgs)
  
  Beaker_like=[253,225,173,211,193,151,273]
  Baron_like=range(236,240)
  Mildred_like=range(281,289)
  
  #i want Beaker_ary to be a 2d list.
  Beaker_ary=[]
  Baron_ary=[]
  Mildred_ary=[]
  
  for i in range(0,len(imgs)):
    Beaker_ary.append([all_preds[i][x] for x in Beaker_like])
    Baron_ary.append([all_preds[i][x] for x in Baron_like])
    Mildred_ary.append([all_preds[i][x] for x in Mildred_like])
  
  naive_guesses=[]
  
  for i in range(0,len(imgs)):
    Be=np.max(Beaker_ary[i])
    Ba=np.max(Baron_ary[i])
    Mi=np.max(Mildred_ary[i])
    if(Be>Ba):
      if(Be>Mi):
        naive_guesses.append("Beaker")
      else: naive_guesses.append("Mildred")
    else:
      if (Ba>Mi):
        naive_guesses.append("Baron")
      else: naive_guesses.append("Mildred")
    
  print (naive_guesses[0])

vgg = Vgg16()

# could have a line here saying if path is null then
# path='./pets-data/'

# batches = vgg.get_batches(path+'train', batch_size=2)
# batches = vgg.get_batches(path+'onepic', batch_size=1)

# probably need something here to check the file type in the path location and fix it.

batches = vgg.get_batches(path, batch_size=1)
imgs,labels = next(batches)

pet_id(imgs)
