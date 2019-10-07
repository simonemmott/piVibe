from gpiozero import OutputDevice
from enum import Enum
import logging
from threading import Thread
from datetime import datetime, timedelta
import time
import random

logger = logging.getLogger(__name__)


mode = 'PI'

class TestingOutputDevice(object):
    def __init__(self, pin, *args, **kw):
        self.pin = pin
        self.active_high = kw.get('active_high', True)
        if kw.get('initial_value', False):
            self._value = 1
        else:
            self._value = 0
        
    def on(self):
        logger.debug('Testing Output Device: ON')
        self._value = 1
        
    def off(self):
        logger.debug('Testing Output Device: OFF')
        self._value = 0
        
    def toggle(self):
        logger.debug('Testing Output Device: TOGGLE')
        if self._value:
            self._value = 0
        else:
            self._value = 1
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, v):
        self._value = v

class VState(Enum):
    OFF = 'OFF'
    ON = 'ON'
    

def gen(states):
    i=0
    while True:
        yield states[i]
        i += 1
        if i >= len(states):
            i=0
    
    
class Mode():
    @property
    def name(self):
        return self.__class__.__name__
    
    def __next__(self):
        return next(self.gen)
    
modes = {}
    
def mode(cls):
    modes[cls.__name__] = cls
    return cls

VL_ON = 0.02
VL_OFF = 0.18

L_ON = 0.08
L_OFF = 0.12

M_ON = 0.09
M_OFF = 0.13

H_ON = 0.1
H_OFF = 0.1

VH_ON = 0.18
VH_OFF = 0.02

@mode
class VeryLow(Mode):
    states = [
        (True, VL_ON),
        (False, VL_OFF),
    ]
    def __init__(self):
        self.gen = gen(Low.states)
    
@mode
class Low(Mode):
    states = [
        (True, L_ON),
        (False, L_OFF),
    ]
    def __init__(self):
        self.gen = gen(Low.states)
    
@mode    
class Medium(Mode):
    states = [
        (True, M_ON),
        (False, M_OFF),
    ]
    def __init__(self):
        self.gen = gen(Medium.states)
    
@mode    
class High(Mode):
    states = [
        (True, H_ON),
        (False, H_OFF),
    ]
    def __init__(self):
        self.gen = gen(High.states)

@mode    
class VeryHigh(Mode):
    states = [
        (True, VH_ON),
        (True, VH_OFF),
    ]
    def __init__(self):
        self.gen = gen(High.states)

@mode        
class Rising(Mode):    
    
    states = [
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        (True, VL_ON),
        (False, VL_OFF),
        
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        (True, L_ON),
        (False, L_OFF),
        
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),
        (True, M_ON),
        (False, M_OFF),

        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),
        (True, H_ON),
        (False, H_OFF),

        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),
        (True, VH_ON),
        (True, VH_OFF),

        (False, 3),
        (True, 1),
        (False, 5),
        (True, 3),
        (False, 3),
        (True, 5),
        (False, 1),
        (True, 5),
        (False, 5),
        
        
    ]
    def __init__(self):
        self.gen = gen(Rising.states)
     
def random_mode():    
    while True:
        on = random.randint(0,5) > 0
        intensity = random.randint(10,90)/100
        s_time = 0.2
        t_on = s_time*intensity
        t_off = 0.2 - t_on
        steps = int(random.randint(10,100)*(0.4/intensity))
        if on:
            toggle = False
            for i in range(steps):
                toggle = not toggle
                if toggle:
                    yield (True, t_on)
                else:
                    yield (False, t_off)
                
        else:
            yield (False, random.randint(5,60))
            
            
        
@mode
class Random(Mode):
    def __init__(self):
        self.gen = random_mode()
    
    
class Vibrator(object):
    def __init__(self, pin, **kw):
        self.state = VState.OFF
        self.mode = VeryLow()
        self.thread = None
        if mode == 'TESTING':
            self.ctl = TestingOutputDevice(pin, **kw)
        else:
            try:
                self.ctl = OutputDevice(pin, active_high=False, **kw)
            except:
                self.ctl = TestingOutputDevice(pin, **kw)
            
    class RunThread(Thread):
        def __init__(self, vibrator):
            self.vibrator = vibrator
            self.go = True
            self.running = False
            Thread.__init__(self)
        
        def run(self):
            self.running = True
            while self.go:
                state, t = next(self.vibrator.mode)
                if state:
                    self.vibrator.ctl.on()
                else:
                    self.vibrator.ctl.off()
                time.sleep(t)
            self.running = False
            
        def stop(self):
            self.go = False
            while self.running:
                pass
            
    
    @property       
    def pin(self):
        return self.ctl.pin
        
    def on(self):
        if self.thread:
            self.thread.stop()
            self.thread = None
        self.state = VState.ON
        self.thread = Vibrator.RunThread(self)
        self.thread.start()
        
    def off(self):
        if self.thread:
            self.thread.stop()
            self.thread = None
        self.state = VState.OFF
        self.ctl.off()
        
    def set_mode(self, mode):
        if self.is_on():
            self.off()
            self.mode = modes[mode]()
            self.on()
        else:
            self.mode = modes[mode]()
        
    def is_on(self):
        return self.state == VState.ON
        
    def is_off(self):
        return self.state == VState.OFF
    
    def to_dict(self):
        return {
            'state': str(self.state),
            'mode': self.mode.name,
            'pin': str(self.pin)
        }
        
            
        
