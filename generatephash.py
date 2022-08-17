import cv2
import argparse
from PIL import Image
from tqdm import tqdm
from imagehash import phash
import get_bounding_box
import csv


#TODO create bounding box where to view for phash. exclude zoom thumbnail

def video_to_frames(input_loc):
    """Function to extract frames from input video file
    and save them as separate frames in an output directory.
    Args:
        input_loc: Input video file.
    Returns:
        None
    """
    interval = 800 #in milliseconds

    # Start capturing the feed
    cap = cv2.VideoCapture(input_loc)

    duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS) # frame_count/fps
    frames_to_get = duration / (interval/1000)

    # Duration
    print(f"Duration of video: {duration:.2f} s")
    print(f"Capture interval: Every {interval/1000} seconds")
    print(f"Total number of frames to get: {frames_to_get:.2f}")
    print("Converting video...")

    ref_img = None
    count = 0
    ref_hamming = 0

    with open(f"{input_loc}.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ', quotechar="|", quoting=csv.QUOTE_MINIMAL)

        # Start converting the video
        for f in tqdm(range(int(frames_to_get))):
            # Extract the frame
            ret, frame = cap.read()
            if ret == False:
                continue
            ref_img = frame
            if f == 0:
                bounds = get_bounding_box.get_bounding_box(ref_img)
            
            cap.set(cv2.CAP_PROP_POS_MSEC,(int(f*interval)))

            

            img1_PIL = Image.fromarray(ref_img).crop(bounds)
            img1_phash = phash(img1_PIL,hash_size=6)
            print(img1_phash)
            csvwriter.writerow([f,str(img1_phash)])


    # If there are no more frames left
    # Release the feed
    cap.release()

    # Print stats
    print ("Done extracting frames.\n%d frames extracted" % count)



if __name__=="__main__":


    a = argparse.ArgumentParser()
    a.add_argument("-i", help="path to video")
    args = a.parse_args()
    print(args)
    video_to_frames(args.i)

#https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames
