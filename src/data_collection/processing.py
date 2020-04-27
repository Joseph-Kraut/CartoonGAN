"""
This file and its methods are concerned with downloading and processing videos for dataset use
"""
import os
import urllib.request
import sys

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
    :return: None
    """
    # Create download dir if it doesn't already exist
    if not os.path.exists(download_to):
        os.makedirs(download_to)

    download_to = download_to if download_to.endswith("/") else download_to + "/"
    download_path = download_to + url.split("/")[-1]

    urllib.request.urlretrieve(url, download_path)

def download_and_process(image_links, to_folder="./dataset"):
    """
    Downloads and processes images from given list of links
    :param image_links: List of links to pull videos from
    :return: None
    """
    # Ensure download path exists
    if not os.path.exists(to_folder):
        os.makedirs(to_folder)

    for link in image_links:
        verbose_print(f"Downloading {link}...\n")
        download_video(link)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        verbosity = True

    download_and_process(['https://ia601204.us.archive.org/33/items/126BuddiesThickerThanWater1962/001%20%20%20Puss%20Gets%20the%20Boot%20%5B1940%5D.mp4'])
