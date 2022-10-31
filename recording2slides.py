import cv2
from os import mkdir
import argparse
from PIL import Image
from tqdm import tqdm
from imagehash import phash
import get_bounding_box


#TODO create bounding box where to view for phash. exclude zoom thumbnail

def video_to_frames(input_loc, output_loc):
    """Function to extract frames from input video file
    and save them as separate frames in an output directory.
    Args:
        input_loc: Input video file.
        output_loc: Output directory to save the frames.
    Returns:
        None
    """
    try:
        mkdir(output_loc)
    except OSError:
        pass


    interval = 1200 #in milliseconds

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
    # Start converting the video
    for f in tqdm(range(int(frames_to_get))):
        # Extract the frame
        ret, frame = cap.read()
        if ret == False:
            continue

        cap.set(cv2.CAP_PROP_POS_MSEC,(int(f*interval)))
        if ref_img is None: # CODE FOR FIRST LOOP
            ref_img = frame
            cv2.imwrite(output_loc + "/%#05d.jpg" % count, frame)

            bounds = get_bounding_box.get_bounding_box(ref_img)

            img1_PIL = Image.fromarray(ref_img).crop(bounds)
            img1_phash = phash(img1_PIL,hash_size=6)
            count += 1
            continue

        img2 = frame
        img2_PIL = Image.fromarray(img2).crop(bounds)
        img2_phash = phash(img2_PIL,hash_size=6)

        
        hamming_distance = img1_phash - img2_phash
        # print(hamming_distance)


        # if percentage > tolerance:
        if abs(ref_hamming - hamming_distance) > 1:
            # Write the results back to output location.
            cv2.imwrite(output_loc + "/%#05d.jpg" % count, frame)
            count += 1
            ref_img = img2
            ref_hamming = hamming_distance
            continue

    # If there are no more frames left
    # Release the feed
    cap.release()

    # Print stats
    print ("Done extracting frames.\n%d frames extracted" % count)


if __name__=="__main__":


    a = argparse.ArgumentParser()
    a.add_argument("-i", help="path to video")
    a.add_argument("-o", help="path to images")
    args = a.parse_args()
    print(args)
    video_to_frames(args.i, args.o)

#https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames

# use ffmpeg PILLOW 



# Create screenshots of the video
# Pwede remove duplicates na dayon para wala nay IO sa disk
# Done


# https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
# https://github.com/JohannesBuchner/imagehash