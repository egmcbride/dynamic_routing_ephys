# -*- coding: utf-8 -*-
"""
Facemap processing: Use Facemap to extract motion energy and motion SVDs from behavior videos

Created on Tue Aug 15 10:24:39 2023

@author: ethan.mcbride
"""

# %%
from facemap import process
import glob
import os
import numpy as np
import cv2
import time


# %%
def crop_behavior_video(vid_path,processed_vid_path):
    
    # Open the video
    cap = cv2.VideoCapture(vid_path)
    
    # Initialize frame counter
    cnt = 0
    
    # Some characteristics from the original video
    # w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)
    
    # Here you can define your croping values
    x,y,w,h = 120,118,100,63
    
    # output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(processed_vid_path, fourcc, fps, (w, h))
    
    
    lastpct=0
    start_time=time.time()
    # Now we start
    while(cap.isOpened()):
        ret, frame = cap.read()

        cnt += 1 # Counting frames
        
        # Avoid problems when video finish
        if ret==True:
            # Croping the frame
            crop_frame = frame[y:y+h, x:x+w]
    
            # Percentage
            xx = cnt *100/frames
            xx=int(xx)
            if xx>lastpct:
                lastpct=xx
                elapsed_time=time.time()-start_time
                print(int(xx),'% complete; time elapsed:',np.round(elapsed_time,decimals=2))
                
            if cnt>1:
                out.write(crop_frame)
    
            # # Just to see the video in real time          
            # cv2.imshow('frame',frame)
            # cv2.imshow('croped',crop_frame)
    
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
# %%
def trim_behavior_video(vid_path,processed_vid_path):
    #just trims the first frame off videos
    
    # Open the video
    cap = cv2.VideoCapture(vid_path)
    
    # Initialize frame counter
    cnt = 0
    
    # Some characteristics from the original video
    w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)
    
    # # Here you can define your croping values
    # x,y,w,h = 120,118,100,63
    
    # output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(processed_vid_path, fourcc, fps, (w_frame, h_frame))
    
    
    lastpct=0
    start_time=time.time()
    # Now we start
    while(cap.isOpened()):
        ret, frame = cap.read()

        cnt += 1 # Counting frames
        
        # Avoid problems when video finish
        if ret==True:
    
            # Percentage
            xx = cnt *100/frames
            xx=int(xx)
            if xx>lastpct:
                lastpct=xx
                elapsed_time=time.time()-start_time
                print(int(xx),'% complete; time elapsed:',np.round(elapsed_time,decimals=2))
                
            if cnt>1:
                out.write(frame)
    
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    

# %% define paths

main_paths = [
    r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_626791_20220815", #need to re-crop video
    r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_626791_20220816",
    r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_626791_20220817",
    
    r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_636766_20230123", 
    r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_636766_20230124", 
    r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_636766_20230125", 
    r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_636766_20230126", 
    r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_644864_20230130",
    r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_644864_20230131", 
    r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_644864_20230201", 
    r"\\allen\programs\mindscope\workgroups\np-exp\PilotEphys\Task 2 pilot\DRpilot_644864_20230202",
    r"\\allen\programs\mindscope\workgroups\np-exp\PilotEphys\Task 2 pilot\DRpilot_644866_20230207", 
    r"Y:\DRpilot_644866_20230208",
    r"Y:\DRpilot_644866_20230209",
    r"Y:\DRpilot_644866_20230210",
    r"Y:\DRpilot_644867_20230220",
    r"Y:\DRpilot_644867_20230221",
    r"Y:\DRpilot_644867_20230222",
    r"Y:\DRpilot_644867_20230223",
    r"Y:\DRpilot_649943_20230213", 
    r"Y:\DRpilot_649943_20230214",
    r"Y:\DRpilot_649943_20230215",
    r"Y:\DRpilot_649943_20230216",
    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_660023_20230808",
    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_660023_20230809",
    
]


ROI_path = r"D:\DR Pilot Data\Behavior_fullvideo_multiROIs.npy"

ROI_params = np.load(ROI_path,allow_pickle=True)
ROI_params.item()['save_mat']=False
# ROI_params.item()['savepath']=None

trimmed_fullvideo_paths=r"D:\DR Pilot Data\DR_trimmed_full_videos"

for mm in main_paths[:]:
    
    vid_path = glob.glob(os.path.join(mm,'Behavior_*.mp4'))[0]
    # processed_vid_path = os.path.join(mm, 'processed', vid_path[vid_path.rfind('\\')+1:-4]+'_cropped.mp4')
    # if os.path.isfile(processed_vid_path) == False:
    #     crop_behavior_video(vid_path,processed_vid_path)
        
    trimmed_video_path = os.path.join(trimmed_fullvideo_paths, vid_path[vid_path.rfind('\\')+1:-4]+'_trimmed.mp4')
    if os.path.isfile(trimmed_video_path) == False:
        trim_behavior_video(vid_path,trimmed_video_path)

    process.run(
        [[trimmed_video_path]],
        sbin=1,
        motSVD=True,
        movSVD=True,
        GUIobject=None,
        parent=None,
        proc=ROI_params.item(),
        savepath=r"D:\DR Pilot Data\full_video_multi_ROI",
    )
    
    print(mm+' complete')
    


