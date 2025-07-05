def classify_image(image_path):
    # Simulate classification
    from random import choice
    ripeness = choice(["ripe", "unripe"])
    print(f"[Classifier] Detected fruit ripeness: {ripeness}")
    return "banana", ripeness
