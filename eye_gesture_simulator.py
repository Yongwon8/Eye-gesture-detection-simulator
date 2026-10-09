"""Toy eye-gesture event detection using simulated one-dimensional samples.

No real EOG recordings or hardware are used. The sample rate is assumed,
so reported delays are confirmation delays rather than measured system latency.
"""

SIGNAL = [0.1, 0.2, 1.8, 2.1, 1.9, 0.2, 0.1, 1.9, 0.1, 0.2, 1.7, 2.0, 1.8, 0.1]
TRUE_GESTURES = [(2, 4), (10, 12)]  # Inclusive sample-index intervals
THRESHOLD = 1.5
SAMPLING_RATE_HZ = 100  # Hypothetical, not a measured hardware sampling rate


def detect_gestures(signal, threshold=THRESHOLD, window_size=3):
    """Return indices where a new gesture is confirmed.

    Requires `window_size` consecutive samples above threshold, and emits
    at most one event per uninterrupted above-threshold run.
    """
    if window_size < 1:
        raise ValueError("window_size must be >= 1")
    consecutive_count = 0
    gesture_active = False
    detections = []
    for index, value in enumerate(signal):
        if value > threshold:
            consecutive_count += 1
            if consecutive_count >= window_size and not gesture_active:
                detections.append(index)
                gesture_active = True
        else:
            consecutive_count = 0
            gesture_active = False
    return detections


def evaluate(detections, true_gestures, sampling_rate_hz=SAMPLING_RATE_HZ):
    """Match each detection to at most one labeled gesture interval."""
    matched = set()
    delays_ms = []
    false_positives = 0
    for detection in detections:
        match = next((i for i, (start, end) in enumerate(true_gestures)
                      if i not in matched and start <= detection <= end), None)
        if match is None:
            false_positives += 1
        else:
            matched.add(match)
            delays_ms.append((detection - true_gestures[match][0]) * 1000 / sampling_rate_hz)
    tp = len(matched)
    fn = len(true_gestures) - tp
    return {
        "TP": tp, "FP": false_positives, "FN": fn,
        "recall": tp / len(true_gestures) if true_gestures else None,
        "mean_confirmation_delay_ms": sum(delays_ms) / len(delays_ms) if delays_ms else None,
    }


def main():
    print("Toy eye-gesture detector | simulated data only")
    print(f"Threshold: {THRESHOLD}; assumed sampling rate: {SAMPLING_RATE_HZ} Hz")
    print("Window | Detections | TP | FP | FN | Recall | Mean confirmation delay")
    for window in (1, 2, 3, 4):
        detections = detect_gestures(SIGNAL, window_size=window)
        result = evaluate(detections, TRUE_GESTURES)
        delay = result["mean_confirmation_delay_ms"]
        delay_str = "N/A" if delay is None else f"{delay:.0f} ms"
        print(f"{window:>6} | {str(detections):>10} | {result['TP']:>2} | "
              f"{result['FP']:>2} | {result['FN']:>2} | "
              f"{result['recall']:.0%} | {delay_str}")


if __name__ == "__main__":
    main()
