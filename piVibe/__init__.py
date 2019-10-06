from gpiozero import OutputDevice
from enum import Enum
import logging
from threading import Thread
from datetime import datetime, timedelta
import time

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
    
class Gen():
    def __init__(self, name, states):
        self.states = states
        self.name = name
        
    def gen(self):
        i=0
        while True:
            yield self.states[i]
            i += 1
            if i >= len(self.states):
                i=0

    
class Low(Gen):
    def __init__(self):
        super(Low, self).__init__(
            'LOW',
            [
                (True, 0.01),
                (False, 0.09)
            ]
        )
    
class Medium(Gen):
    def __init__(self):
        super(Medium, self).__init__(
            'MEDIUM',
            [
                (True, 0.05),
                (False, 0.05)
            ]
        )
    
class High(Gen):
    def __init__(self):
        super(Medium, self).__init__(
            'HIGH',
            [
                (True, 1),
                (False, 0)
            ]
        )
    
class Waves(Gen):
    def __init__(self):
        super(Medium, self).__init__(
            'WAVES',
            [
                (True, 0.01),
                (False, 0.09),
                (True, 0.01),
                (False, 0.09),
                (True, 0.01),
                (False, 0.09),
                
                (True, 0.02),
                (False, 0.08),
                (True, 0.02),
                (False, 0.08),
                (True, 0.02),
                (False, 0.08),
                
                (True, 0.03),
                (False, 0.07),
                (True, 0.03),
                (False, 0.07),
                (True, 0.03),
                (False, 0.07),
    
                (True, 0.04),
                (False, 0.06),
                (True, 0.04),
                (False, 0.06),
                (True, 0.04),
                (False, 0.06),
    
                (True, 0.05),
                (False, 0.05),
                (True, 0.05),
                (False, 0.05),
                (True, 0.05),
                (False, 0.05),
    
                (True, 0.06),
                (False, 0.04),
                (True, 0.06),
                (False, 0.04),
                (True, 0.06),
                (False, 0.04),
    
                (True, 0.07),
                (False, 0.03),
                (True, 0.07),
                (False, 0.03),
                (True, 0.07),
                (False, 0.03),
    
                (True, 0.08),
                (False, 0.02),
                (True, 0.08),
                (False, 0.02),
                (True, 0.08),
                (False, 0.02),
    
                (True, 0.09),
                (False, 0.01),
                (True, 0.09),
                (False, 0.01),
                (True, 0.09),
                (False, 0.01),
    
                (True, 1),
                (False, 1),
                (True, 1),
                (False, 1),
                (True, 1),
                (False, 1),
            ]
        )
    
    
    
class Vibrator(object):
    def __init__(self, pin, **kw):
        self.state = VState.OFF
        self.mode = Medium()
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
        
    def _change_mode(self, mode):
        if self.is_on():
            self.off()
            self.mode = mode
            self.on()
        else:
            self.mode = mode
        
    def low(self):
        self._change_mode(Low())
        
    def medium(self):
         self._change_mode(Medium())
        
    def high(self):
        self._change_mode(High())
        
    def waves(self):
        self._change_mode(Waves())
        
    def is_on(self):
        return self.state == VState.ON
        
    def is_off(self):
        return self.state == VState.OFF
    
    def to_dict(self):
        return {
            'state': str(self.state),
            'mode': str(self.mode.name),
            'pin': str(self.pin)
        }
        
            
        
