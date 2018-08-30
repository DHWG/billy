import threading
import time
from configuration import PINS
import RPi.GPIO as GPIO


def wiggle_tail(frequency):
    """Wiggles the tail fin.
    
    Arguments
    ---------
    frequency : float
        Frequency (in Hz)"""
    pin = PINS['tail']
    thread = threading.Thread(target=_oscillate, args=(pin, frequency))
    thread.start()

def speak(frequency):
    """Make a speaking motion with the mouth.
    
    Arguments
    ---------
    frequency : float
        Frequency (in Hz)"""
    pin = PINS['mouth']
    thread = threading.Thread(target=_oscillate, args=(pin, frequency))
    thread.start()

def turn_head(duration = 0):
    """Turns the head.
    
    Arguments
    ---------
    duration : float
        Time (in seconds) to turn the head. 0 (default) means indefinitely."""
    pin = PINS['head']
    thread = threading.Thread(target=_keep_on, args=(pin, duration))
    thread.start()

def stop_all():
    """Stops all movement."""
    for pin in _pin_owners.keys():
        _acquire_owner_id(pin)


GPIO.setmode(GPIO.BCM)  # set board mode to Broadcom

for pin_name in ('head', 'mouth', 'tail'):
    GPIO.setup(PINS[pin_name], GPIO.OUT)

_pin_owners = {pin:0 for pin in PINS.values()}

def _acquire_owner_id(pin):
    """Each action thread must own the pins it's
    acting upon and stop as soon it loses ownership
    of one.
    
    Arguments
    ---------
    pin : int
        The pin to acquire ownership of"""
    new_owner_id = _pin_owners[pin] + 1
    _pin_owners[pin] = new_owner_id
    return new_owner_id

def _oscillate(pin, frequency):
    """Switch pin on and off repeatedly.

    Arguments
    ---------
    pin : int
        The pin to toggle
    frequency : float
        Frequency (in Hz)"""
    owner_id = _acquire_owner_id(pin)
    brake_time = 1.0 / frequency / 2
    while _pin_owners[pin] == owner_id:
        _switch(pin, on=True)
        time.sleep(brake_time)
        _switch(pin, on=False)
        time.sleep(brake_time)

def _keep_on(pin, duration = 0):
    """Keep the pin on, optionally for a specified time only.
    
    Arguments
    ---------
    pin : int
        The pin
    duration : float
        Time (in seconds) to keep the pin switched on"""
    owner_id = _acquire_owner_id(pin)
    start = time.time()
    _switch(pin, on=True)
    while _pin_owners[pin] == owner_id:
        if duration > 0 and ((time.time() - start) >= duration):
            break
        else:
            time.sleep(0.01)
    _switch(pin, on=False)

def _switch(pin, on):
    """Switch a pin on or off.
    
    Arguments
    ---------
    pin : int
        The pin
    on : bool
        Switch pin on or off"""
    GPIO.output(pin, GPIO.HIGH if on else GPIO.LOW)