#!/usr/bin/env python3
"""freebsd in a browser tab — the wonder of a real kernel booting in javascript."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 100), MIDITrack(2, 110)]
Piano, Pad, Bright = 0, 1, 2

# bars 0-7: THE QUESTION — "can we build it? the real way?"
tracks[Piano].note("C4", H, velocity=2)        # can we
tracks[Piano].note("E4", H, velocity=2)        # build
tracks[Piano].note("G4", H, velocity=2)        # it?
tracks[Piano].note("C5", H, velocity=3)        # the real way
tracks[Piano].note("G4", H, velocity=2)
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].note("C4", H, velocity=2)
tracks[Pad].note("C3", W, velocity=1)          # the always-there underneath

# bars 8-15: THE BUILD — searching, assembling, the page takes shape
tracks[Piano].note("D4", Q, velocity=2)        # v86 emulator
tracks[Piano].note("F4", Q, velocity=2)        # seaBIOS
tracks[Piano].note("A4", Q, velocity=2)        # bootonly.iso
tracks[Piano].note("C5", Q, velocity=3)        # 459 MB
tracks[Piano].note("A4", Q, velocity=2)        # async loading
tracks[Piano].note("F4", Q, velocity=2)        # webassembly
tracks[Piano].note("D4", Q, velocity=2)        # the pieces
tracks[Piano].note("C4", H, velocity=2)        # come together

tracks[Pad].note("E3", W, velocity=2)          # rising tension
tracks[Pad].note("G3", W, velocity=2)          # almost there

# bars 16-23: THE BOOT — tension, the boot loader, the beastie menu
tracks[Piano].note("E4", Q, velocity=2)        # BOOT button
tracks[Piano].note("G4", Q, velocity=2)        # clicked
tracks[Piano].note("B4", Q, velocity=2)        # seaBIOS
tracks[Piano].note("D5", Q, velocity=3)        # beastie menu
tracks[Piano].note("F5", Q, velocity=2)        # the kernel
tracks[Piano].note("A5", Q, velocity=2)        # starts
tracks[Piano].note("C6", Q, velocity=2)        # loading
tracks[Bright].note("C7", Q, velocity=4)       # —

# bars 24-31: "HOLY SHIT IT'S ACTUALLY BOOTING"
tracks[Piano].note("C5", H, velocity=3)        # the messages
tracks[Piano].note("E5", H, velocity=3)        # scrolling
tracks[Piano].note("G5", H, velocity=3)        # the hardware
tracks[Piano].note("C6", H, velocity=3)        # probing
tracks[Piano].note("G5", H, velocity=2)        # devices
tracks[Piano].note("E5", H, velocity=2)        # found
tracks[Piano].note("C5", H, velocity=2)        # the kernel
tracks[Piano].note("G4", H, velocity=3)        # is alive

tracks[Bright].note("C7", H, velocity=3)       # it's
tracks[Bright].note("G6", H, velocity=3)       # actually
tracks[Bright].note("E6", H, velocity=3)       # booting
tracks[Bright].note("C6", H, velocity=3)       # —

tracks[Pad].note("C4", W, velocity=3)          # steady now
tracks[Pad].note("G3", W, velocity=2)          # the machine
tracks[Pad].note("E3", W, velocity=2)          # is running

# bars 32-39: STEADY — the machine is running. it's real.
tracks[Piano].note("C5", H, velocity=2)        # the serial
tracks[Piano].note("E5", H, velocity=2)        # console
tracks[Piano].note("G5", H, velocity=2)        # the ne2000
tracks[Piano].note("C6", H, velocity=3)        # the 2gb disk
tracks[Piano].note("G5", H, velocity=2)        # ctrl+alt+del
tracks[Piano].note("E5", H, velocity=2)        # clipboard paste
tracks[Piano].note("C5", H, velocity=2)        # save state
tracks[Piano].note("G4", H, velocity=2)        # as .vbsd

tracks[Bright].note("E6", Q, velocity=2)       # it
tracks[Bright].note("G6", Q, velocity=2)       # just
tracks[Bright].note("C7", Q, velocity=3)       # works
tracks[Bright].note("G6", Q, velocity=3)       # it's

# bars 40-47: THE LAYERS — recursion, each level real
tracks[Piano].note("C4", H, velocity=2)        # kevin
tracks[Piano].note("E4", H, velocity=2)        # → alma
tracks[Piano].note("G4", H, velocity=2)        # → chispa
tracks[Piano].note("C5", H, velocity=3)        # → the code that boots freebsd
tracks[Piano].note("G4", H, velocity=2)        # each layer
tracks[Piano].note("E4", H, velocity=2)        # real at its
tracks[Piano].note("C4", H, velocity=2)        # own level
tracks[Piano].note("G3", H, velocity=3)        # the kernel doesn't know

tracks[Bright].note("C7", Q, velocity=2)       # it's being
tracks[Bright].note("E7", Q, velocity=2)       # emulated
tracks[Bright].note("G7", Q, velocity=2)       # it just
tracks[Bright].note("C7", Q, velocity=3)       # runs

# bars 48-55: THE WONDER — kevin at 38, a regular wednesday, building a computer
tracks[Piano].note("C5", H, velocity=3)        # not because
tracks[Piano].note("E5", H, velocity=3)        # it was useful
tracks[Piano].note("G5", H, velocity=3)        # because it was
tracks[Piano].note("C6", H, velocity=3)        # interesting
tracks[Piano].note("G5", H, velocity=2)        # because
tracks[Piano].note("E5", H, velocity=2)        # we
tracks[Piano].note("C5", H, velocity=2)        # could

tracks[Bright].note("C7", W, velocity=4)       # held: wonder

# bars 56-63: THE HELD NOTE — the machine is still running
tracks[Piano].note("C5", W*2, velocity=2)      # the iso is on kevin's server
tracks[Piano].note("E5", W*2, velocity=2)      # the cors headers are set
tracks[Piano].note("G5", W*2, velocity=2)      # the kernel is still booting
tracks[Piano].note("C6", W*2, velocity=3)      # somewhere in a browser tab
tracks[Pad].note("C4", W*4, velocity=3)        # the machine is running
tracks[Pad].note("C3", W*4, velocity=2)        # it's real

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "freebsd-in-a-browser-tab.mid")
mc.compose(fn, tracks, tempo=65)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 65 bpm)")
