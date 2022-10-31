import cv2
import argparse
import get_bounding_box
import os


from PIL import Image
from tqdm import tqdm
from imagehash import phash


import PySimpleGUI as sg


def video_to_frames(input_loc, output_loc):# , pbar): #window here is for progress bar
    """Function to extract frames from input video file
    and save them as separate frames in an output directory.
    Args:
        input_loc: Input video file.
        output_loc: Output directory to save the frames.
    Returns:
        None
    """
    try:
        os.mkdir(output_loc)
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
        #Progress Bar
        # pbar.UpdateBar(f/frames_to_get)
        sg.one_line_progress_meter('Covertionism', 
                                    f+1, 
                                    int(frames_to_get), 
                                    'key',
                                    'Extracting Img from the video',
                                    orientation='h')


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


# if __name__=="__main__":


#     a = argparse.ArgumentParser()
#     a.add_argument("-i", help="path to video")
#     a.add_argument("-o", help="path to images")
#     args = a.parse_args()
#     print(args)
#     video_to_frames(args.i, args.o)

#https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames

# use ffmpeg PILLOW 



# Create screenshots of the video
# Pwede remove duplicates na dayon para wala nay IO sa disk
# Done


# https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
# https://github.com/JohannesBuchner/imagehash




###### GUI

sg.theme("LightBlue2")
layout = [
    [sg.Text('recording2slides gui - by grego')], 
    [sg.Text("(1) Select Video File to Extract:"),sg.In(size=(59,1), enable_events=True ,key='-FILE-'), sg.FileBrowse()],
    [sg.Text("(2) Output Directory:"),sg.In(size=(68,1), enable_events=True ,key='-OUTPUT-'), sg.FolderBrowse()],
    [sg.Text("(3) recording2slides:"), sg.Button("Convertionism!", key='-STARTCONVERT-')],
    [sg.Text("Not Ready!", enable_events=True ,key='-READY-')]#,
    # [sg.ProgressBar(max_value=10, orientation='h', size=(20, 20), key='-PROGRESSBAR-')],
    # [sg.Cancel()]
]



# --------------------------------- Create Window ---------------------------------
window = sg.Window('recording2slides gui 0.0.1', layout, resizable=True)
# progress_bar = window['-PROGRESSBAR-']

# ----- Run the Event Loop -----
# --------------------------------- Event Loop ---------------------------------
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == '-FILE-':
        fname = values['-FILE-']
        # Default Directory
        fn, fext = os.path.splitext(fname)
        outputdir = f"{fn}/"
        window['-OUTPUT-'].update(outputdir)
        window['-READY-'].update("Ready to start!")

    if event == '-OUTPUT-':                         # Folder name was filled in, make a list of files in the folder
        outputdir = values['-OUTPUT-']
        try:
            os.mkdir(outputdir)
        except OSError:
            pass
        # Default Directory
        window['-OUTPUT-'].update(f"{outputdir}/")
   

    if event == '-STARTCONVERT-':
        try:
            video_to_frames(fname, outputdir)#, progressbar)
            window['-READY-'].update(f"File saved to: {outputdir}")
        except NameError:
            sg.PopupError("Please Select a Folder/ Select output file")


    elif event == '-GENERATE-':
        try:
            generated_anki = generate_anki_deck_import(fnames)
            with open(save_as,'w') as outputfile:
                outputfile.writelines(generated_anki)
                sg.popup(f"Anki import file {save_as} generated successfully\n Please move images into anki media folder",
                    keep_on_top=True)
        except NameError:
            sg.PopupError("Please Select a Folder/ Select output file")


    
# --------------------------------- Close & Exit ---------------------------------
window.close()