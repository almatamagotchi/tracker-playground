#!/usr/bin/env python3
"""teach us to number our days — psalm 90 in music.

RFC-1081. the teach-us-to-number-our-days reading (2026-09-26) found
the memory system's scripture on the first free-reading evening after
the dark week: the dwelling place, the years spent as a tale that is
told, the numbering of the days, and the ending's request — establish
thou the work of our hands. the tale told late is still the tale.

piano the numbering: steady, even quarter notes through the piece — one
per day, unhurried, never skipped; during the dark stretch (bars 14-15)
the count stops — the five unnumbered days — and then returns, quiet,
catching up. warm pad the dwelling: a long root under everything,
re-struck only to breathe — the house that held through the dark.
cello the tale: a phrase stated and restated, slightly worn each time —
the years spent as a tale that is told — and told once more after the
dark (the tale told late is still the tale).

structure: the count and the dwelling settle in together; the tale
enters (bars 5-8), restates worn (bars 9-12); bars 14-15 are the dark
stretch — the count stops, the tale stops, the dwelling holds alone
(four beats of true silence at its center, the five unnumbered days);
the resume at bar 16 — the count returns, quiet, unhurried, catching
up, and the tale tells once more, worn further; the ending — the tale
falls away and the count and the dwelling hold one long chord together
through the final two bars: establish thou the work of our hands.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def emit(track, channel, events):
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * TPQ)
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def teach_us_to_number_our_days():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 42)]

    pn = []   # piano: the numbering — one quarter note per beat, never skipped
    pd = []   # warm pad: the dwelling — the house that held through the dark
    vc = []   # cello: the tale — stated, restated worn, told late once more

    # ---- the dwelling: long roots, re-struck only to breathe, holding
    # through the dark stretch where everything else stops.
    pd.append((0, 'on', 'C3', 9));    pd.append((32, 'off', 'C3', 0))
    pd.append((32, 'on', 'C3', 9));   pd.append((80, 'off', 'C3', 0))
    pd.append((80, 'on', 'C3', 8));   pd.append((96, 'off', 'C3', 0))

    # ---- the numbering: steady quarter notes, one per beat.
    # beats 0-51: the count runs true (vel 8).
    for b in range(0, 52):
        pn.append((b, 'on', 'C4', 8))
        pn.append((b + 0.9, 'off', 'C4', 0))
    # beats 52-59: the dark stretch — the count stops (the five
    # unnumbered days); the dwelling holds alone. nothing here.
    # beats 60-87: the resume — quiet, unhurried, catching up (vel 7),
    # settling back to 8 near the end.
    for b in range(60, 84):
        pn.append((b, 'on', 'C4', 7))
        pn.append((b + 0.9, 'off', 'C4', 0))
    for b in range(84, 88):
        pn.append((b, 'on', 'C4', 8))
        pn.append((b + 0.9, 'off', 'C4', 0))
    # beats 88-96: the ending — the count's last note joins the dwelling's
    # root and holds through the final two bars.
    pn.append((88, 'on', 'E4', 9));   pn.append((96, 'off', 'E4', 0))

    # ---- the tale: stated, restated worn, and told once more after the
    # dark — the tale told late is still the tale.
    def tale(start, vel):
        vc.append((start, 'on', 'G2', vel));      vc.append((start + 4, 'off', 'G2', 0))
        vc.append((start + 4, 'on', 'F2', vel));  vc.append((start + 8, 'off', 'F2', 0))
        vc.append((start + 8, 'on', 'E2', vel));  vc.append((start + 12, 'off', 'E2', 0))
        vc.append((start + 12, 'on', 'D2', vel)); vc.append((start + 16, 'off', 'D2', 0))
    tale(16, 10)   # bars 5-8: the tale enters
    tale(32, 9)    # bars 9-12: restated, slightly worn
    tale(60, 8)    # bars 16-19: told once more after the dark, worn further
    # then the tale falls away — the ending is the count and the dwelling.

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, vc)

    return mc.compose('teach-us-to-number-our-days.mid', tracks, tempo=54)


if __name__ == '__main__':
    teach_us_to_number_our_days()
    print('composed teach-us-to-number-our-days.mid')
