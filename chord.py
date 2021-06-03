# Graham Seamans

import soundfile as sf
import numpy as np
import argparse
import math

ap = argparse.ArgumentParser()
ap.add_argument(
    "base",
    help="base note and chord majorness.",
)
ap.add_argument(
    "just",
    help="Just or equal temperment.",
)
args = ap.parse_args()

base = args.base
if len(base) == 1:
    base_note = base
    is_minor = False
elif len(base) == 2:
    if base[1] == "m":
        base_note = base[0]
        is_minor = True
    else:
        base_note = base
        is_minor = False
else:
    base_note = base[:2]
    is_minor = True

if args.just == "just":
    is_just = True
else:
    is_just = False

samplerate = 48000
length = 1

just_dict = {
    0: 1,
    1: 16 / 15,
    2: 9 / 8,
    3: 6 / 5,
    4: 5 / 4,
    5: 4 / 3,
    6: 45 / 32,
    7: 3 / 2,
    8: 8 / 5,
    9: 5 / 3,
    10: 9 / 5,
    11: 15 / 8,
}

note_dict = {
    "Ab": 415.30,
    "A": 440.00,
    "Bb": 466.16,
    "B": 493.88,
    "C": 523.25,
    "Db": 554.37,
    "D": 587.33,
    "Eb": 622.25,
    "E": 659.25,
    "F": 698.46,
    "Gb": 739.99,
    "G": 783.99,
}

minor = [0, 3, 7]
major = [0, 4, 7]


def make_sine(frequency, len, sample_rate):
    buffer = []
    for i in range(sample_rate * len):
        buffer.append(math.sin(frequency * (2 * math.pi) * i / sample_rate) / 6)
    return buffer


def equal_tempered(frequency, ith_step):
    return frequency * 2 ** (ith_step / 12)


def just_tempered(frequency, ith_step):
    return frequency * just_dict[ith_step]


def det_chord(base_note, is_just, is_minor):
    base_freq = note_dict[base_note]
    notes = []
    frequencies = []

    if is_minor:
        chord = minor
    else:
        chord = major

    for step in chord:
        if is_just:
            frequencies.append(just_tempered(base_freq, step))
        else:
            frequencies.append(equal_tempered(base_freq, step))

    for freq in frequencies:
        notes.append(make_sine(freq, 1, samplerate))

    notes = np.array(notes)
    notes = np.sum(notes, axis=0)
    return notes


out = det_chord(base_note, is_just, is_minor)

sf.write(args.base + "-" + args.just + ".wav", out, samplerate)
