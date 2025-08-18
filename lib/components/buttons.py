from typing import List, Callable
from datetime import datetime, timedelta
import RPi.GPIO as GPIO

class Buttons():
    def __init__(self, button_pins: List[int], functions: List[Callable], num_buttons: int = 3, hold_cutoff: float = 0.75):
        self.num_buttons = num_buttons
        self.button_pins = button_pins
        self.functions = functions
        self.hold_cutoff = hold_cutoff
    
    def initial_setup(self) -> None:
        GPIO.setmode(GPIO.BOARD)
        
        for pin in self.button_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=self._button_actions, bouncetime=50)
        
    def cleanup(self) -> None:
        GPIO.cleanup()

    #This function is on a need by need basis
    def _button_actions(self, channel: int) -> None:
        pin_index = self.button_pins.index(channel)

        if GPIO.input(channel) == GPIO.LOW:
            self.press_time = datetime.now()
            return
        
        hold_time = (datetime.now() - self.press_time).total_seconds()
        self.functions[pin_index](hold_time >= self.hold_cutoff)
        
    