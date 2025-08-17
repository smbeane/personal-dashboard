from typing import List
from datetime import datetime, timedelta
import RPi.GPIO as GPIO

class Buttons():
    def __init__(self, button_pins: List[int], num_buttons: int = 3):
        self.num_buttons = num_buttons
        self.button_pins = button_pins

    def initial_setup(self) -> None:
        GPIO.setmode(GPIO.BOARD)
        for pin in self.button_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=self._button_actions, bouncetime=200)
        
    def cleanup(self) -> None:
        GPIO.cleanup()
            
    def _button_actions(self, channel: int) -> None:
        pass