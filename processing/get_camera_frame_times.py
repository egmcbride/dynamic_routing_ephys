# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 18:56:48 2021

@author: svc_ccg
"""
import numpy as np
import json

def extract_lost_frames_from_json(cam_json):
    '''
    Get the indices of the lost frames (not written to disk) from the camera
    json file. Note that these indices are for the DATA frames (ie 0 corresponds
    to the first data frame and NOT the prepended metadata frame)
    '''
    
    lost_count = cam_json['RecordingReport']['FramesLostCount']
    if lost_count == 0:
        return []
    
    lost_string = cam_json['RecordingReport']['LostFrames'][0]
    lost_spans = lost_string.split(',')
    
    lost_frames = []
    for span in lost_spans:
        
        start_end = span.split('-')
        if len(start_end)==1:
            lost_frames.append(int(start_end[0]))
        else:
            lost_frames.extend(np.arange(int(start_end[0]), int(start_end[1])+1))
    
    return np.array(lost_frames)-1 #you have to subtract one since the json starts indexing at 1 according to Totte
    

def get_frame_exposure_times(sync_dataset, cam_json, account_for_metadata_frame=True):
    '''
    Returns the experiment timestamps for the frames recorded in an MVR video
    
    sync_dataset should be a Dataset object built from the sync h5 file
    cam_json is the json that MVR writes to accompany each mp4
    
    account_for_metadata_frame: if TRUE prepend a NaN to the exposure times for the
    metadata frame that is prepended to the MVR video
    '''
    
    if isinstance(cam_json, str):
        cam_json = read_json(cam_json)
     
    total_frames_recorded = cam_json['RecordingReport']['FramesRecorded']
    
    exposure_sync_line_label_dict = {
            'Eye': 'eye_cam_exposing',
            'Face': 'face_cam_exposing',
            'Behavior': 'beh_cam_exposing'}
    
    cam_label =  cam_json['RecordingReport']['CameraLabel']
    sync_line = exposure_sync_line_label_dict[cam_label]
    
    exposure_times = sync_dataset.get_rising_edges(sync_line, units='seconds')
    
    lost_frames = extract_lost_frames_from_json(cam_json)
    
    #filter out lost frames from the sync exposure times
    frame_times = [e for ie, e in enumerate(exposure_times) if ie not in lost_frames]
    
    #cut off extra exposure times that didn't make it into the video
    frame_times = frame_times[:total_frames_recorded] #hopefully this becomes obsolete after MVR stop sequence changes
    
    #add a NaN to the beginning for the metadata frame
    if account_for_metadata_frame:
        frame_times = np.insert(frame_times, 0, np.nan)

    return np.array(frame_times)


def read_json(jsonfilepath):
    
    with open(jsonfilepath, 'r') as f:
        contents = json.load(f)
    
    return contents
    