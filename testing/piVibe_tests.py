from unittest import TestCase
from unittest.mock import patch
from piVibe import Vibrator, VState, Modes, History, HistoryData
from datetime import datetime, timedelta
import time

class PiVibeTests(TestCase):
    
    def test_create_vibe(self):
        vibe = Vibrator(18)
        self.assertEqual(18, vibe.pin, 'The vibrator is not created with the right pin')
        self.assertEqual(VState.OFF, vibe.state, 'The vibrator is not created in the off state')
        self.assertIsNotNone(vibe.ctl, 'The vibtrator is created without a gpio controller')
        
    def test_vibe_on(self):
        vibe = Vibrator(18)
        self.assertEqual(VState.OFF, vibe.state, 'The vibrator is not created in the off state')
        vibe.on()
        self.assertEqual(VState.ON, vibe.state, 'The vibrator is not turned on')
        vibe.off()

    def test_vibe_off(self):
        vibe = Vibrator(18)
        vibe.on()
        self.assertEqual(VState.ON, vibe.state, 'The vibrator is not turned on')
        vibe.off()
        self.assertEqual(VState.OFF, vibe.state, 'The vibrator is not turned off')
        
    def test_vibe_mode(self):
        vibe = Vibrator(18)
        vibe.on()
        time.sleep(1)
        vibe.mode = Modes.MEDIUM()
        time.sleep(1)
        vibe.mode = Modes.HIGH()
        time.sleep(1)
        vibe.off()
        end = datetime.now()
        start = end - timedelta(seconds=2.5)
        for t, v in vibe.history.data(start, end):
            print('{t}: {v}'.format(t=t, v=v))

    def test_vibe_wave(self):
        vibe = Vibrator(18)
        vibe.mode = Modes.WAVE()
        vibe.on()
        time.sleep(10)
        vibe.off()
        for t, v in vibe.history.data():
            print('{t}: {v}'.format(t=t, v=v))

        
        
    def test_Modes_HIGH(self):
        mode = Modes.HIGH()
        self.assertEqual(Modes.high_states[0], next(mode))
        self.assertEqual(Modes.high_states[1], next(mode))
        self.assertEqual(Modes.high_states[0], next(mode))
        self.assertEqual(Modes.high_states[1], next(mode))
        self.assertEqual(Modes.high_states[0], next(mode))
        self.assertEqual(Modes.high_states[1], next(mode))
        
    def test_Modes_MEDIUM(self):
        mode = Modes.MEDIUM()
        self.assertEqual(Modes.medium_states[0], next(mode))
        self.assertEqual(Modes.medium_states[1], next(mode))
        self.assertEqual(Modes.medium_states[0], next(mode))
        self.assertEqual(Modes.medium_states[1], next(mode))
        self.assertEqual(Modes.medium_states[0], next(mode))
        self.assertEqual(Modes.medium_states[1], next(mode))
        
    def test_Modes_HIGH(self):
        mode = Modes.LOW()
        self.assertEqual(Modes.low_states[0], next(mode))
        self.assertEqual(Modes.low_states[1], next(mode))
        self.assertEqual(Modes.low_states[0], next(mode))
        self.assertEqual(Modes.low_states[1], next(mode))
        self.assertEqual(Modes.low_states[0], next(mode))
        self.assertEqual(Modes.low_states[1], next(mode))
    
    def test_create_History(self):
        h = History()
        self.assertIsNotNone(h.created)
        self.assertEqual(0, len(h.history))
        
    def test_History_append(self):
        h = History()
        h.append((True, 0.2))
        time.sleep(0.2)
        h.append((False, 0.1))
        time.sleep(0.1)
        h.append((True, 0.2))
        time.sleep(0.2)
        h.append((False, 0.1))
        time.sleep(0.1)
        self.assertTrue(isinstance(h.history[0][0], datetime))
        self.assertEqual((True, 0.2), h.history[0][1])
        self.assertTrue(isinstance(h.history[1][0], datetime))
        self.assertEqual((False, 0.1), h.history[1][1])
        self.assertTrue(isinstance(h.history[2][0], datetime))
        self.assertEqual((True, 0.2), h.history[2][1])
        self.assertTrue(isinstance(h.history[3][0], datetime))
        self.assertEqual((False, 0.1), h.history[3][1])
        
    def test_HistoryData(self):
        history = [
                (datetime(2000, 1, 1, second=0), True),
                (datetime(2000, 1, 1, second=2), False),
                (datetime(2000, 1, 1, second=3), True),
                (datetime(2000, 1, 1, second=5), False),
            ]
        data = HistoryData(history, datetime(2000, 1, 1), datetime(2000, 1, 1, second=10))
        self.assertTrue(data.get(datetime(2000, 1, 1, second=0)))
        self.assertTrue(data.get(datetime(2000, 1, 1, second=1)))
        self.assertFalse(data.get(datetime(2000, 1, 1, second=2)))
        self.assertTrue(data.get(datetime(2000, 1, 1, second=3)))
        self.assertTrue(data.get(datetime(2000, 1, 1, second=4)))
        self.assertFalse(data.get(datetime(2000, 1, 1, second=5)))
        self.assertFalse(data.get(datetime(2000, 1, 1, second=6)))
        
        for t, v in data:
            print('{t}: {v}'.format(t=t, v=v))
        
        
    
    
    
    
    
    
    
    
    
    
    
        
        