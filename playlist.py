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
# with open ("songs.txt") as songs:
with open ("short_test.txt") as songs:
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
		# each piano song
		for url in playlist:
			try:
				if "shorts" in url:
					print (f'this one is a short and messes everything up lowkey: {url}')
					driver.get (url)
					# load page
					time.sleep (3)
					try:
						video = driver.find_element (By.TAG_NAME, "video")
						driver.execute_script ("arguments [0].click ();", video)
						print ("clicked video to play")
					except Exception as e:
						print (f'could not click video: {e}')
					wait_time = 0
					max_wait = 180
					last_time = 0
					# shorts are designed to play over and over
					# video.ended flag briefly becomes true but then a new <video> element is reinserted , resetting this
					# bruh moment
					loop_detected = False
					while wait_time < max_wait:
						try:
							# querySelector () method returns first Element within document that matches specified CSS selector
							current_time = driver.execute_script ("return document.querySelector ('video')?.currentTime")
							# for some reason my shorts pause immediately
							paused = driver.execute_script ("return document.querySelector ('video')?.paused")
							# ended = driver.execute_script ("return document.querySelector ('video')?.ended")
							# if ended:
							if current_time is not None:
								if float (current_time) < float (last_time) - 1:
									print ("navigating away to stop short from looping")
									driver.get ("about:blank")
									time.sleep (1)
									loop_detected = True
									# print ("short has ended once -- stopping loop")
									# driver.execute_script ("document.querySelector ('video')?.pause ()")
									# go to next song
									break
								# if this doesn't work i don't even know anymore
								last_time = current_time
							if paused:
								driver.execute_script ("document.querySelector ('video')?.play ()")
								print ("resumed video")
						except Exception as e:
							print (f'error chceking if playing short: {e}')
						time.sleep (1)
						wait_time += 1
					print (f'short is done: {url}')
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
					wait_time = 0
					max_wait = 600
					while wait_time < max_wait:
						try:
							ended = driver.execute_script ("return document.querySelector ('video')?.ended")
							if ended:
								break
						except Exception as e:
							print ("error checking if video ended: {e}")
						time.sleep (1)
						wait_time += 1
					print (f'song is done: {url}')
			except Exception as e:
				print (f'error playing {url}: {e}')
finally:
	driver.quit ()
