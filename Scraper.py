
import time
from selenium import webdriver


def get_videos(valid_video_types, num_requested=100):
    """get video links with selenium from archive.org
    """
    number_of_scrolls = int(num_requested / 100)

    driver = webdriver.Firefox()
    url = "https://archive.org/details/animationandcartoons?and[]=mediatype%3A%22movies%22&sort=-downloads&and[]=collection%3A%22vintage_cartoons%22"
    print("Search url: " + url)
    driver.get(url)

    # scroll to reveal more results
    for _ in range(number_of_scrolls):
        driver.execute_script("window.scrollBy(0, 1000000)")
        time.sleep(2)
    
    cartoons = driver.find_elements_by_class_name('item-ttl')
    video_urls = set()  
    for c in cartoons:
        try:
            link_to_video = c.find_element_by_tag_name('a')
            href = link_to_video.get_attribute('href')
            video_urls.add(href)
        except Exception as e:
            print(e)

    print(f"Found {len(video_urls)} to search")


    link_count = 0
    save_file = 'video-links.txt'
    links = set()
    with open(save_file, 'w') as f:

        for vid in video_urls:
            download_vid = 'https://archive.org/download/' + vid.split('/')[-1]
            driver.get(download_vid)

            download_options = driver.find_element_by_class_name('directory-listing-table')
            urls = download_options.find_elements_by_tag_name('a')
            for url in urls:
                href = url.get_attribute("href")
                video_name = href.split('.')[0]
                video_type = href.split('.')[-1]
                
                if video_name in links:
                    print(video_name)

                if video_type in valid_video_types:
                    f.write(f'{href}\n')
                    links.add(video_name)
                    link_count += 1
                

        print(f"Found {link_count} videos")
        driver.quit()

    return


if __name__ == '__main__':
    valid_video_types = ['mpeg', 'mp4']
    get_videos(valid_video_types)