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
    
class Modes():
    @staticmethod
    def gen(states):
        i = 0
        while True:
            yield states[i]
            i += 1
            if i >= len(states):
                i=0
                
    high_states = [
            (True, 1),
            (False, 0)
        ]
        
    medium_states = [
            (True, 0.2),
            (False, 0.1)
        ]
        
    low_states = [
            (True, 0.1),
            (False, 0.2)
        ]
    
    wave_states = [
            (True, 0.05),
            (False, 0.25),
            (True, 0.1),
            (False, 0.2),
            (True, 0.15),
            (False, 0.15),
            (True, 0.2),
            (False, 0.1),
            (True, 0.25),
            (False, 0.05),
            (True, 0.2),
            (False, 0.1),
            (True, 0.15),
            (False, 0.15),
            (True, 0.1),
            (False, 0.2)
        ]
        
    @staticmethod
    def HIGH():
        return Modes.gen(Modes.high_states)
    
    @staticmethod
    def MEDIUM():
        return Modes.gen(Modes.medium_states)
    
    @staticmethod
    def LOW():
        return Modes.gen(Modes.low_states)
    
    @staticmethod
    def WAVE():
        return Modes.gen(Modes.wave_states)
    
class HistoryData():
    def __init__(self, history, start, end, interval=0.1):
        self.history = history
        self.timedelta = timedelta(milliseconds=interval*1000)
        self._index = None
        self._time_index = None
        self.start = start
        self.end = end
        
    def get(self, dt, default=None):
        if dt < self.start:
            return default
        if dt > self.end:
            return default
        for state in self.history:
            if state[0] <= dt:
                start = state
            if state[0] > dt:
                end = state
                break
        if start:
            return start[1]
        else:
            return False
        
    def __iter__(self):
        self._index = 0
        self._time_index = self.start
        return self
    
    def __next__(self):
        val = (self._time_index, self.history[self._index][1])
        self._time_index += self.timedelta
        if self._index + 1 < len(self.history):
            while self._index + 1 < len(self.history) and self._time_index >= self.history[self._index+1][0]:
                self._index += 1
        if self._time_index > self.end:
            raise StopIteration()
        return val
    
    def __contains__(self, dt):
        return dt >= self.start and dt <= self.end
    
    def __get_item__(self, dt):
        val = self.get(dt)
        if val == None:
            raise KeyError('{dt} not in data range'.format(dt=dt))
                
    
class History(object):
    def __init__(self):
        self.created = datetime.now()
        self.history = []
        
    def append(self, state):
        self.history.append((datetime.now(), state))
        
    def data(self, start=None, end=None, interval=0.1):
        if not start:
            start = self.created
        if not end:
            end = datetime.now()
        return HistoryData(self.history, start, end, interval)
    
    

class Vibrator(object):
    def __init__(self, pin, **kw):
        self.state = VState.OFF
        self.mode = Modes.LOW()
        self.thread = None
        self.history = History()
        if mode == 'TESTING':
            self.ctl = TestingOutputDevice(pin, **kw)
        else:
            try:
                self.ctl = OutputDevice(pin, **kw)
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
                self.vibrator.history.append(state)
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
        
    def is_on(self):
        return self.state == VState.ON
        
    def is_off(self):
        return self.state == VState.OFF
    
    def to_dict(self):
        return {
            'state': str(self.state),
            'pin': str(self.pin)
        }
        
            
        
