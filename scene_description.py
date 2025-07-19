import random

def generate_description(detections, frame_shape):
    height, width, _ = frame_shape

    # Classify object positions
    descriptions = []
    positions = []

    for det in detections:
        cls = det['name']
        box = det['box']
        x_center = (box[0] + box[2]) / 2

        if x_center < width / 3:
            position = "left"
        elif x_center < 2 * width / 3:
            position = "center"
        else:
            position = "right"

        positions.append(f"{cls} at your {position}")
        descriptions.append(cls)

    if not positions:
        return "I don't see anything specific around you right now."

    # Natural intro phrases
    starters = [
        "Looks like this around you:",
        "I can see the following:",
        "Here’s what I noticed:",
        "You're surrounded by:",
        "This is what's in your area:",
        "I spotted this nearby:",
        "Let me describe what I see:"
    ]
    intro = random.choice(starters)

    # Combine object and position info
    object_summary = ", ".join(positions)

    # Optional safety warning
    warnings = []
    if 'chair' in descriptions or 'bench' in descriptions:
        warnings.append("Watch out for furniture ahead.")
    if 'cup' in descriptions or 'bottle' in descriptions:
        warnings.append("Be careful not to knock over any small items.")
    if 'person' in descriptions:
        warnings.append("There are people around, stay aware.")

    warning_text = " ".join(warnings)

    return f"{intro} {object_summary}. {warning_text}"
