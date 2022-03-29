"""
Automatically blur multiple images from a folder depending on defined boxes
"""
## load an image
import skimage
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import scipy
from skimage import data
from skimage.color import rgb2gray
from skimage.filters import gaussian
import os
from os import listdir
from os.path import isfile, join
import progressbar
from multiprocessing.dummy import Pool as ThreadPool

filename='obj_train_data/mixed-31-01-22_15-31-39_cam2.png'
out_dir="output"

def blur_image(filename,blur_zones,sig=30,out_dir="output",disp=False):
    assert os.path.isdir(out_dir)
    img = io.imread(filename)
    for key, blur_zone in blur_zones.items():
        # print(key,blur_zone)
        y0,y1=blur_zone[0]
        x0,x1=blur_zone[1]
        # y0,x0=1780,0
        # y1,x1=2100,515
        yrange=np.arange(img.shape[1])
        xrange=np.arange(img.shape[0])
        # xv, yv = np.meshgrid(np.argwhere((y0<yrange)<y1), np.argwhere((x0<xrange)<x1))
        # new_yrange=np.argwhere(np.argwhere((np.arange(img.shape[1])<y1))>y0)[:,0]
        # new_xrange=np.argwhere((np.arange(img.shape[0])<x1)>x0)
        mask_y=(yrange<y1) & (yrange>y0)
        mask_x=(xrange<x1) & (xrange>x0)
        # print(np.sum(mask_x*1))
        new_yrange=yrange[mask_y][np.newaxis,:]
        new_xrange=xrange[mask_x][:,np.newaxis]
        # print(new_xrange,new_yrange)
        # print(img.shape)

        img[new_xrange,new_yrange]=(gaussian(img[new_xrange,new_yrange],sig,multichannel=True)*255).astype(int)
        if disp:
            # print(img.shape[1])
            # print(np.argwhere(np.argwhere((np.arange(img.shape[1])>y0))<y1))
            # print(new_xrange,new_yrange)
            plt.figure(figsize=(10,10))
            plt.axis('off')
            plt.imshow(gaussian(img[new_xrange,new_yrange],sig,multichannel=True))
            plt.show()
        io.imsave(out_dir+"/"+os.path.basename(filename).replace(".png","_blurred.png"),img)
    if disp:
        plt.figure(figsize=(10,10))
        plt.axis('off')
        plt.imshow(img)
        plt.show()

def get_filenames(prefixes, onlyfiles):
    output=dict()
    for m in range(len(prefixes)):
        output.setdefault(prefixes[m],list())
    for k in range(len(onlyfiles)):
        file=onlyfiles[k]
        for m in range(len(prefixes)):
            prefix=prefixes[m]
            if file.endswith(prefix+".png"):
                output[prefix].append(file)
    return output

if __name__=="__main__":
#     filename='obj_train_data/mixed-31-01-22_15-31-39_cam2.png'
#     out_dir="output"
#     blur_zone={"0":[[1780,2100],[0,515]]}
#     blur_zone_cam1={"0":[[209,328],[1109,1702]]}

#     # blur_image(filename,blur_zone,sig=30,out_dir="output",disp=False)
#     # blur_zones_cam1={"0":[[1109,1702],[209,328]],
#     #                  "1":[[1702,2455],[328,605]]}
#     blur_zones_cam1={"0":[[1122,2259],[198,360]],
#                      "1":[[1725,2442],[333,503]]}
#     # 1122   198
#     # 2259   360
#     # 1725   333
#     # 2442   503
#     # blur_zones_cam2={"0":[[4,87],[417,180]],
#     #                  "1":[[592,1398],[92,233]]}
#     blur_zones_cam2={"0":[[600,1395],[8,260]],
#                      "1":[[6,74],[5,471]]}
#     # 4   417
#     # 87   180
#     # 592   92
#     # 1398   233
#     # ##2
#     # 600   8
#     # 1395   260
#     # 6   5
#     # 74   471

#     #### 03-02 ## Dataset
#     # 2120   541
#     # 2676   968
#     #### Zone 2
#     # 1204   120
#     # 1300   360
#     # 1384   232
#     # 1781   347
#     # 1815   161
#     # 2346   558
#     ##
#     # 673   272
#     # 1121   579
#     # 1723   387
#     # 2327   655
#     pool = ThreadPool(12)
#     # in_dir="orig"
#     # onlyfiles = [in_dir+"/"+f for f in listdir(in_dir) if isfile(join(in_dir, f)) and f.endswith("png") and f.startswith("mixed-31-01")]
#     # print(f"{0:^30}".format("dataset1"))
#     # bar=progressbar.ProgressBar(len(onlyfiles))
#     # # bar.start()
#     # # print(onlyfiles)
#     # prefixes=["cam1","cam2"]
#     # blur_zones=[blur_zones_cam1,blur_zones_cam2]
#     # inputs=get_filenames(prefixes, onlyfiles)
#     # # print(inputs)
#     # counter=0
#     # for i in range(0,(len(inputs))):
#     #     for key,files in inputs.items():
#     #         if key==prefixes[i]:
#     #             print(key)
#     #             pool.map(lambda file : blur_image(file,blur_zones[i],sig=30,out_dir="output",disp=False), files)
#     #             # for file in files:
#     #             #     # if prefixes[i] in file:
#     #             #     #     print('nice',end=" ")
#     #             #     # else:
#     #             #     #     print('shit',end=" ")
#     #             #     # print(file,blur_zones[i])
#     #             #     blur_image(file,blur_zones[i],sig=30,out_dir="output",disp=False)
#     #             #     counter+=1
#     #             #     # if len(onlyfiles)//counter==0:
#     #             #     bar.update(counter)
#     print(f"{0:^30}".format("dataset2"))
#     in_dir="orig"
#     onlyfiles = [in_dir+"/"+f for f in listdir(in_dir) if isfile(join(in_dir, f)) and f.endswith("png") and f.startswith("mixed-03-02")]
#     bar=progressbar.ProgressBar(len(onlyfiles))
#     # bar.start()
#     # print(onlyfiles)
#     prefixes=["cam0","cam2", "cam3"]
#     blur_zones_03_02_cam0={"0":[[2120,2676],[541,968]]}
#     blur_zones_03_02_cam2={"0":[[1204,1300],[120,360]],
#                            "1":[[1384,1781],[232,347]],
#                            "2":[[1815,2346],[161,558]]}
#     blur_zones_03_02_cam3={"0":[[673,1121],[272,579]],
#                         "1":[[1723,2327],[387,655]]}
#     blur_zones=[blur_zones_03_02_cam0,blur_zones_03_02_cam2,blur_zones_03_02_cam3]
#     inputs=get_filenames(prefixes, onlyfiles)
#     # print(inputs)
#     counter=0
#     for i in range(0,(len(inputs))):
#         for key,files in inputs.items():
#             if key==prefixes[i]:
#                 print(key)
#                 pool.map(lambda file : blur_image(file,blur_zones[i],sig=30,out_dir="output",disp=False), files)
#                 # for file in files:
#                 #     # if prefixes[i] in file:
#                 #     #     print('nice',end=" ")
#                 #     # else:
#                 #     #     print('shit',end=" ")
#                 #     # print(file,blur_zones[i])
#                 #     blur_image(file,blur_zones[i],sig=30,out_dir="output",disp=False)
#                 #     counter+=1
#                 #     # if len(onlyfiles)//counter==0:
#                 #     bar.update(counter)
    pool = ThreadPool(12)
    blur_zones=[blur_zones_03_02_cam0,blur_zones_03_02_cam2,blur_zones_03_02_cam3]
    onlyfiles = [in_dir+"/"+f for f in listdir(in_dir) if isfile(join(in_dir, f)) and f.endswith("png") and f.startswith("mixed-03-02")]
    prefixes=["cam0","cam2", "cam3"]
    inputs=get_filenames(prefixes, onlyfiles)
    # print(inputs)
    counter=0
    for i in range(0,(len(inputs))):
        for key,files in inputs.items():
            if key==prefixes[i]:
                print(key)
                pool.map(lambda file : blur_image(file,blur_zones[i],sig=30,out_dir="output",disp=False), files)

    
    # blur_image(filename,blur_zones_cam1,sig=100,out_dir="output",disp=True)
