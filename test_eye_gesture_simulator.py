import unittest
from eye_gesture_simulator import detect_gestures, evaluate, SIGNAL, TRUE_GESTURES


class EyeGestureSimulatorTests(unittest.TestCase):
    def test_window_sizes(self):
        expected = {1: (2, 1, 0), 2: (2, 0, 0), 3: (2, 0, 0), 4: (0, 0, 2)}
        for window, metrics in expected.items():
            with self.subTest(window=window):
                detections = detect_gestures(SIGNAL, window_size=window)
                result = evaluate(detections, TRUE_GESTURES)
                self.assertEqual((result['TP'], result['FP'], result['FN']), metrics)

    def test_no_duplicate_events(self):
        self.assertEqual(detect_gestures([2, 2, 2, 2, 0], window_size=2), [1])

    def test_noise_spike_rejected(self):
        self.assertEqual(detect_gestures([0, 2, 0, 0], window_size=2), [])

    def test_invalid_window(self):
        with self.assertRaises(ValueError):
            detect_gestures([0, 2], window_size=0)


if __name__ == '__main__':
    unittest.main()
