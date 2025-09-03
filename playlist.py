# playing some unlisted videos that i enjoy . over and over again

# imports to open songs in browser
import time
# youtube lowkey is onto me . fuck
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# urls
with open ("songs.txt") as songs:
	playlist = [song.rstrip () for song in songs if song.strip ()]

print (playlist)

# Selenium webdriver -- open-source framework for controlling web interactions
options = uc.ChromeOptions ()
# shut up "Chrome is being controlled by automated software"
# tbh doesn't work
options.add_argument ("--disable-infobars")
options.add_argument ("--window-size=800,600")

driver = uc.Chrome (options = options)

try:
	# forever piano !!!
	while True:
		for url in playlist:
			try:
				if "shorts" in url:
					print (f'this one is a short and messes everything up lowkey: {url}')
					driver.get (url)
					# load page
					time.sleep (2)
					try:
						video = driver.find_element (By.TAG_NAME, "video")
						driver.execute_script ("arguments [0].click ();", video)
						print ("clicked video to play")
					except Exception as e:
						print (f'could not click video: {e}')
					# longest short in my playlist is 2:29
					# could probably scrape this but no xx
					time.sleep (149)
				else:
					print (f'playing normal video: {url}')
					driver.get (url)
					# load page
					time.sleep (3)
					try:
						play_button = WebDriverWait (driver, 10).until (EC.element_to_be_clickable ((By.CSS_SELECTOR, ("button.ytp-large-play-button"))))
						play_button.click ()
						print ("clicked play to start video with sound")
					except Exception as e:
						print (f'could not click play button: {e}')
					WebDriverWait (driver, 600).until (EC.title_is ("ENDED"))
					print (f'song is done: {url}')
			except Exception as e:
				print (f'error playing {url}: {e}')
finally:
	driver.quit ()
