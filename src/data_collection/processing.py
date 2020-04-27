"""
This file and its methods are concerned with downloading and processing videos for dataset use
"""
import os
import urllib.request
import sys
import cv2

verbosity = False

def verbose_print(string):
    """
    Prints only if verbose is true
    :param string: The string to print
    :return: None
    """
    global verbosity

    if verbosity:
        print(string)

def download_video(url, download_to="./downloads"):
    """
    Downloads the video served at the given url
    :param url: The URL of the video to access
    :param download_to: The location to download the video to
    :return: The path the image was downloaded to
    """
    # Create download dir if it doesn't already exist
    if not os.path.exists(download_to):
        os.makedirs(download_to)

    download_to = download_to if download_to.endswith("/") else download_to + "/"
    download_path = download_to + url.split("/")[-1]

    urllib.request.urlretrieve(url, download_path)

    return download_path

def split_into_frames(video_capture):
    """
    A generator that yields frames from the video capture given
    :param video_capture: The given OpenCV video capture
    :return: None
    """
    success, frame = video_capture.read()
    frames = []

    while success:
        frames.append(frame)
        success, frame = video_capture.read()

    return frames

def process_video(local_path, to_folder, video_number, start_after=60, cut_last=60, delete_after=True):
    """
    Processes the image at <local_path> and places in dataset folder
    :param local_path: The local path where the image currently resides
    :param to_folder: The folder to put the processed frames into
    :param video_number: The index of the video for file naming purposes
    :param start_after: The number of seconds into the video to start recording
    :param cut_last: The number of seconds to cut off the end of the video
    :param delete_after: Whether or not to delete the video after processing
    :return: None
    """
    # Setup the to_folder
    to_folder = to_folder if to_folder.endswith("/") else to_folder + "/"
    # Load the video into an OpenCV object
    video_capture = cv2.VideoCapture(local_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    video_frames = split_into_frames(video_capture)
    frame_start = fps * start_after
    frame_end = len(video_frames) - fps * cut_last
    verbose_print(f"Frame start: {frame_start}\nFrame end: {frame_end}")

    for frame_index, frame in enumerate(video_frames):
        # Save this frame if it is in the desired range
        if frame_index < frame_start:
            continue
        elif frame_index > frame_end:
            break
        save_path = to_folder + f"{video_number}-frame{frame_index}.png"
        cv2.imwrite(save_path, frame)

    if delete_after:
        os.remove(local_path)

def download_and_process(image_links, to_folder="./dataset"):
    """
    Downloads and processes images from given list of links
    :param image_links: List of links to pull videos from
    :return: None
    """
    # Ensure download path exists
    if not os.path.exists(to_folder):
        os.makedirs(to_folder)

    count = 0
    for link in image_links:
        verbose_print(f"Downloading {link}...\n")
        local_path = download_video(link)

        verbose_print(f"Processing video at {local_path}")
        process_video(local_path, to_folder, count)
        count += 1

    verbose_print("Done building dataset...")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        verbosity = True

    download_and_process(['https://ia601204.us.archive.org/33/items/126BuddiesThickerThanWater1962/001%20%20%20Puss%20Gets%20the%20Boot%20%5B1940%5D.mp4'])
