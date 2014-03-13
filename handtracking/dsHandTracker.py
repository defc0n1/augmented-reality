#!/bin/python2

import DepthSense as ds
import numpy as np
from SimpleCV import *
import sys
ds.initDepthSense()
#disp = Display(flags = pg.FULLSCREEN)
disp = Display()
points = []
squares = []

# Main loop closes only on keyboard kill signal 
while True: 
 
    # Get depth and colour images from the kinect
    image = ds.getColourMap()
    image = image[:,:,::-1]
    img = Image(image.transpose([1,0,2]))
 
    depth = ds.getDepthMap()
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>=2
    depth = depth.astype(np.uint8).transpose()
    depth = Image(depth)
    depth = depth.invert()
 
    # filter out region of depth below given colour distance (minimizes blob confusion)
    #depth.stretch(0,150)
    #depth = depth - depth.colorDistance((200,200,200))
    dblobs = depth.findBlobs(minsize=2000, maxsize=14000)
    #dblobs = depth.findBlobs(threshval=(200,200,200)) #, threshblocksize=1000,appx_level=5)
 
    box_center = None
    box = None
    box_point = None
    z_val = 0
    box_area = 0
    counter = 0
    if not dblobs:
        if len(points) > 2:
            depth.dl().lines(points, Color.BLUE, width=2)
        #depth.show()
        depth.save(disp)
        continue
    for b in dblobs:
        # filter out region of depth above given colour distance (focuses our interest)
        if ((depth[b.centroid()] < (200,200,200)) \
                and (depth[b.centroid()] > (40,40, 40)) \
                and b.rectangleDistance() > 0.18):
            #print depth[b.centroid()], b.area(), b.rectangleDistance()

            old_point = box_point

            bb = b.boundingBox()
            box_center = b.centroid()
            hand = b.contour()
            sorted_hand = copy(hand)
            sorted_hand.sort(key=lambda x: x[1])
            #box_point = [(top_x, top_y) for (top_x, top_y) in hand if top_y == min([y for (x,y) in hand])][0]
            box_point = sorted_hand[0]
            #[depth.dl().circle(p, 15, Color.BLUE) for p in hand if (p[1] , box_point[1]-4))]

            #val = sum([1 if (int(abs(p[1] - box_point[1])) in [0,1,2]) else 0 for p in hand])
            val = sum([(abs(p[0] - box_point[0])) for p in hand if (abs(p[1] - box_point[1]) < 8)])
            if val > 150:
                print val
                box_center = None
                depth.drawRectangle(bb[0], bb[1], bb[2], bb[3], color=Color.VIOLET)
                continue
            depth.dl().circle(box_point, 20, Color.RED)
            depth.dl().polygon(hand, filled=True, color=Color.YELLOW)
            depth.drawRectangle(bb[0], bb[1], bb[2], bb[3], color=Color.GREEN)
 
            # if two hands are found in the scene, record point information
            #counter+=1
            #if counter == 2:
            #    if abs(old_point[0] - box_point[0]) > 100 and abs(box_point[1] - box_point[0]) > 100:
            #        squares = []
            #        top = box_point
            #        bottom = old_point
            #        squares.append(top)
            #        squares.append(bottom)
            #        continue
 
 
    
    # append new point to the point array
    if (len(points) > 0) and (box_center):
        x_delta = abs(box_point[0] - points[-1][0])
        y_delta = abs(box_point[1] - points[-1][1])
        if (x_delta < 100 and y_delta < 100):
            points.append(box_point)
        else:
            # point found faraway from previous point, restart array
            points = []
            points.append(box_point)
    
    # first point in the scene
    elif (box_center):
        points.append(box_point)
 
 
    # draw lines
    if len(points) > 2:
        depth.dl().lines(points, Color.BLUE, width=2)
 
    # draw box
    #if len(squares) == 2:
    #    depth.dl().rectangle2pts(squares[0], squares[1], Color.RED, width=3, filled=False,)
 
    # draw scene
    depth.save(disp)
