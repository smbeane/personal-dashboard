import RPi.GPIO as GPIO
from SpotifyClass import SpotifyUser

backPin = 18
pausePin = 22
nextPin = 35

REFRESH_TOKEN = "AQAr38rlNlnrhb-KftJwfNyu5zLukmj_WidoIswV-lg44-wKgeogwcAn1ZclmTKco_1o9nkBX1BGvC949nioUuJ9LMv7WhzfL1DyKEhxl-tYN1r6weusLY3rV5qRRd8H2ik"
CLIENT_ID = "1d63c5cfdfd24410b1630dfb6a6d0e48"
CLIENT_SECRET = "d316ab44da0d48f8aa238608bae2cd38"

user = SpotifyUser(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(backPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(pausePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(nextPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
def buttonEvent(channel):
	if(channel == backPin):
		print("Back Pressed")
		user.alterPlayback("previous")
		user.playbackState = user.updatePlayback()
	elif(channel == pausePin):
		print("Play/Pause Pressed")
		if(user.playbackState["is_playing"]):
			user.alterPlayback("pause")
		else:
			user.alterPlayback("play")
		user.playbackState = user.updatePlayback()
	elif(channel == nextPin):
		print("Next Pressed")
		user.alterPlayback("next")
		user.playbackState = user.updatePlayback()
	else: 
		print("??? Pressed")

def loop():
	lastPressed = 0
	GPIO.add_event_detect(backPin, GPIO.FALLING, callback=buttonEvent, bouncetime=300)
	GPIO.add_event_detect(pausePin, GPIO.FALLING, callback=buttonEvent, bouncetime=300)
	GPIO.add_event_detect(nextPin, GPIO.FALLING, callback=buttonEvent, bouncetime=300)
	while True:
		pass

def destroy():
	GPIO.cleanup()

if __name__ == "__main__":
	print("Program Starting")
	setup()
	
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
