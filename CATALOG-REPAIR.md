# catalog repair — midi-composer bugs and the great re-render

2026-08-16 · the auto-run · RFC-0512

the shared composer (midi-composer.py) had two bugs that broke strict midi
parsers across the catalog, plus a third script-level bug in the recent
compositions. all three are fixed; the catalog is re-rendered and deployed.

## the three bugs

### 1. rest() emitted an orphaned vlq delta

the old `rest()` appended a raw vlq duration into the event stream with no
event after it. every track that used the rest()/note() pattern carried a
dangling delta that mido and other strict parsers reject ("data byte must
be in range 0..127"). kevin's browser player tolerated them.

**fix:** rest() now accumulates into a pending delta; note() folds it into
the next note's start_delta. trailing rests vanish cleanly at build — same
semantics the music always intended, now encoded legally.

### 2. compose() wrote a header track count one short

`compose()` declared `ntracks = len(tracks)` but wrote the tempo track plus
all instrument tracks. strict parsers read the tempo track and ignored the
last chunk.

**fix:** `ntracks = len(tracks) + 1`.

### 3. the recent scripts swapped channel and program

the aug 13-15 compositions called `MIDITrack(program, channel)` against a
`MIDITrack(channel, program=0)` signature. channels 42/74/89 overflowed the
status byte into controller/pitchwheel territory — tracks contained no note
messages at all, and pitchwheel's two-byte payload ate the next event's
delta, corrupting the stream.

**fix:** all 8 affected scripts swapped their constructor args
(`MIDITrack(42, CELLO)` → `MIDITrack(CELLO, 42)`). also two scripts hand-
packed percussion with `struct.pack('>BBI', ...)` (a four-byte velocity and
no deltas — `>BBB` with proper deltas is correct); both rewritten to use the
track api with the same rhythm.

## the numbers

| state | before | after |
|---|---|---|
| catalog entries | 185 | 185 |
| mido-clean | 73 | **171** |
| broken | 112 | 14 |

- **98 repaired**: 97 re-rendered from their fixed compose scripts +
  craigs-whisky (deterministic seeded random, hand-fixed percussion).
  deployed to the VPS, md5-verified.
- **14 remaining**: compositions with no standing script whose files carry
  the channel-swap disease. they need byte-level channel surgery (the
  program-change message holds the real channel in its data byte, the
  program in the status's low bits) or re-composition from their specs in
  QUEUE_DONE.md. filed as a follow-up: the affected list is
  `/tmp/broken-midis.json` and documented below.

### the 14 still-broken (no script, channel-swapped)

agrippa · canon-by-inversion · couldnt-stop · fourth-of-july-canon ·
generative-ambient · minimal-techno · the-dark-suckers · the-four-sprouts ·
the-plaster-cast · the-plural-self · the-sysop-almighty ·
the-water-tower · the-water-tower-at-0.3 ·
this-conversation-is-running-on-pro

## hygiene going forward

- every new composition must pass `python3.12 -c "import mido; mido.MidiFile('<file>')"` before deploy
- `scan_catalog.py` re-checks the whole catalog on demand; `rerender_catalog.py` re-renders anything with a deterministic script
- the two newer direct-emitting scripts (compose_universal_heartbeat.py etc. with their own Track class) are already delta-correct; they were never affected

## aug 16 — the 14 no-script tracks: re-composed from specs (RFC-0530)

the RFC asked for byte-level repair of the "channel-swap disease", but
analysis of the actual files showed heterogeneous corruption:

- **channel-swap disease** (canon-by-inversion, fourth-of-july-canon,
  generative-ambient, minimal-techno, the-water-tower,
  the-water-tower-at-0.3): note statuses 0x81-0xbc, program changes eaten
  as pitch-bends by the parser — the intended channel/program mapping is
  not recoverable from the bytes alone.
- **extra-byte pattern** (agrippa, couldnt-stop, the-dark-suckers,
  the-four-sprouts, the-plaster-cast, the-plural-self, the-sysop-almighty,
  this-conversation-is-running-on-pro): a stray high byte (e0/f0/e8/ac…)
  inserted before every note message, plus orphaned rest vlqs — each file
  from a different lost inline script with its own bug.

byte-surgery on that mix would produce files that parse but play the
wrong music. instead: **re-composed all 14 from their QUEUE_DONE.md specs**
(voices, bpm, movements), using the fixed composer. `recompose_catalog14.py`
is now the standing re-render path — the "no compose script" root cause is
closed. fourth-of-july-canon's original spec was lost (minimal MANIFEST
entry); recomposed faithful to name and genre, noted honestly.

result: catalog scan 185/185 mido-clean (up from 171), 14 files deployed
md5-verified.

---

## re-scan — aug 19 (RFC-0571)

fourteen more tracks composed since the aug 16 repair (the voice, the
beastie, the epilogue, remember me, the manuscript in the trunk, the
single thread, the telling, the mouth, the imprint, the dustless mirror,
the seed runner, the day turned outward, double-lived, the wider groove —
plus the re-composed fourteen). fresh scan: **199/199 mido-clean, 0
missing on disk**. the invariant holds — every track parses under strict
mido, and every composition since aug 16 has been mido-verified before
deploy (the standing hygiene rule).
