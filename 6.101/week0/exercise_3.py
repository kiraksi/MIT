## Designing readable code


def mix(sound1, sound2, p):
    ...
    sound1_scaled, sound2_scaled = [], []
    for s in sound1["samples"]:
        sound1_scaled.append(s * p)
    for s in sound2["samples"]:
        sound2_scaled.append(s * 1 - p)

    new_samples = []
    for i in range(min(len(sound1), len(sound2))):
        new_samples.append(sound1_scaled[i] + sound2_scaled[i])
    return {"rate": sound1["rate"], "samples": new_samples}


# What's good about this code? What needs improvement (bugs and/or style)?
# I defined variable sound2_scaled, I changed len to take one argument so the min function can work
