# imports to open songs in browser
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64

# urls
with open ("songs.txt") as songs:
	playlist = [song.rstrip () for song in songs]

print (playlist)

# so that we know when the video is over
template = """
<!DOCTYPE html>
<html>
	<body>
		<div id = "player"> </div>
		<script>
			// creating our script element (JavaScript)
			var tag = document.createElement ("script");
			<!-- this API lets us control videos -->
			tag.src = "https://www.youtube.com/iframe_api";
			var first = document.getElementsByTagName ("script") [0];
			first.parentNode.insertBefore (tag, first);
			var player;
			// global
			function onYouTubeIframeAPIReady () 
			{
				player = new YT.Player ("player", {
					height: "390",
					width: "640",
					videoId: "%s",
					events: {
						"onStateChange": on_player_state_change
					}
				});
			}

			function on_player_state_change (event)
			{
				if (event.data == YT.PlayerState.ENDED)
				{
					document.title = "ENDED";
				}
			}
		</script>
	</body>
</html>
"""

# Selenium webdriver -- open-source framework for controlling web interactions
options = Options ()
# shut up "Chrome is being controlled by automated software"
options.add_argument ("--disable-infobars")
options.add_argument ("--window-size=800,600")
driver = webdriver.Chrome (options = options)

try:
	# forever piano !!!
	while True:
		for song in playlist:
			# create HTML
			html = template % song
			# for embedding
			encoded_html = base64.b64encode (html.encode ("utf-8")).decode ()
			uri = f'data:text/html;base64,{encoded_html}'
			driver.get (uri)
			WebDriverWait (driver, 600).until (EC.title_is ("ENDED"))
			print (f'Brandon is done with {song}')
finally:
	driver.quit ()
