# Eye Gesture Detection Simulator

A small Python learning project exploring how a threshold-based eye-gesture event detector behaves on **synthetic, one-dimensional signal samples**. Inspired by the challenge of designing reliable gesture-based communication interfaces.

**Scope:** This is a toy simulation, **not** a validated EOG classifier, a real-time hardware system, or a medical communication device. It uses no patient data or recorded eye signals.

## What it does

- Detects a gesture when a configurable number of **consecutive** samples exceed a threshold.
- Uses a simple state variable to emit **one detection per uninterrupted above-threshold event**, instead of repeated commands.
- Compares detection counts, false positives (FP), false negatives (FN), recall, and *confirmation delay* across window sizes.

## Run

Requires Python 3; no third-party dependencies.

```bash
python3 eye_gesture_simulator.py
python3 -m unittest -v
```

## Synthetic example

The included sequence contains two labeled three-sample gestures (indices 2–4 and 10–12), plus one isolated above-threshold spike (index 7). The threshold is 1.5.

| Consecutive samples required | TP | FP | FN | Recall | Mean confirmation delay* |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 2 | 1 | 0 | 100% | 0 ms |
| 2 | 2 | 0 | 0 | 100% | 10 ms |
| 3 | 2 | 0 | 0 | 100% | 20 ms |
| 4 | 0 | 0 | 2 | 0% | N/A |

*Confirmation delay is the difference between the labeled gesture onset and the sample at which detection is confirmed, converted to milliseconds using a **hypothetical** 100 Hz sampling rate. It is **not** measured end-to-end latency or computational runtime. The toy results do not generalize to real EOG data.*

## What I learned

Requiring more consecutive samples can suppress isolated noise spikes, but can also delay or entirely miss short gestures. A zero-FP result is not necessarily useful if the system misses every intended action. The threshold and window length should be evaluated together against the needs of the intended interface.

## Next steps

- Test on realistic labeled recordings, with permission and appropriate data handling.
- Explore signal preprocessing, adaptive thresholds, and multiple gesture classes.
- Evaluate event-level precision/recall and end-to-end latency under streaming input.
