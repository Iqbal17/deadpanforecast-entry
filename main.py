"""Deadpan Forecasts for Cities That Do Not Exist.

A single line, at most 160 characters: a weather forecast for a city that
does not exist, read deadpan, like a real TV meteorologist reading off the
map. The absurdity has to sit inside a believable broadcast sentence, with
a concrete number or detail that makes the invented place feel real.

Decision record
---------------
Pass 1 - candidates weighed against the judge's criteria (on-subject
forecast first, then the funnier joke, then the more vivid detail, then the
believable broadcast tone, then how well the line uses its characters):

A. "Tonight in Vrell: light rain, a high of 61, and the city's 4,000
   umbrellas opening in unison at 6 p.m. for reasons nobody can explain."
   (134 chars)  (CHOSEN)
   Reads exactly like a forecast: time slot, condition, high. The absurd
   image (4,000 umbrellas opening in unison) is a concrete, countable
   detail, and the deadpan closer ("for reasons nobody can explain") is
   the forecaster refusing to editorialise - the joke lands in the
   broadcaster's voice, not in a punchline.

B. "Good evening from Zenthra, where it will rain sideways at 47 degrees
   until the mayor's 900 pigeons file a formal complaint." (123 chars)
   "Rain sideways" is vivid and the pigeon complaint is funny, but the
   sentence leans on the joke rather than the forecast: no high/low, no
   time slot, so it scores weaker on the on-subject criterion the judge
   weighs first.

C. "Tomorrow in Quilwick: partly cloudy, a high of 72, with a 40 percent
   chance the town's one cloud finally leaves." (112 chars)
   Good broadcast shape and the single cloud is a nice image, but the
   joke is gentle - a shrug, not a laugh - and "finally leaves" tells
   the reader how to feel about it instead of staying deadpan.

D. "Overnight in Drellport: fog thick enough to hide the harbour, a low
   of 39, and the lighthouse blinking in Morse code for help." (126 chars)
   Strong image and the Morse-code lighthouse is funny, but "thick enough
   to hide the harbour" is a simile doing the work, and the lighthouse
   asking for help is a second joke competing with the fog - the line
   splits its attention instead of landing one image.

Pass 2 - revisions on the winner:
1. First draft read "light drizzle, a high of 61, and a low of 58, as
   the city's 4,000 umbrellas open in unison at 6 p.m." - two
   temperatures plus the umbrella clause made the sentence sag in the
   middle and spent characters on a low nobody needs. Dropping the low
   and switching to "light rain" tightened it to one temperature and
   gave the umbrella image room to breathe.
2. "for reasons no one can explain" -> "for reasons nobody can explain":
   "nobody" is the flatter, more broadcast word; "no one" reads slightly
   literary. Deadpan wants flat.

Pass 3 - code revision pass (the line itself is untouched):
The first draft kept the entry as one long literal and let check_gate
read a module constant. Re-reading it, two weaknesses stood out. First,
the 1-160 character gate existed only as a claim in this docstring -
nothing in the code would notice if a future edit pushed the line out
of bounds, so the gate is now a pair of constants (MIN_CHARS/MAX_CHARS)
plus a check_gate() that runs before anything is written. The check
raises SystemExit rather than using assert, because asserts are stripped
under `python -O` and an out-of-gate entry fails silently at grading
time. Second, the line is now assembled from its three broadcast beats
(opening, condition, umbrella image) by build_line(), so each beat can
be read and edited on its own, and the write itself is unchanged: the
exact line, UTF-8, no trailing newline added.

Final line (134 characters, gate 1-160, verified by hand count and by
running this program):
    Tonight in Vrell: light rain, a high of 61, and the city's 4,000 umbrellas opening in unison at 6 p.m. for reasons nobody can explain.
"""

import os

# The forecast's three broadcast beats, joined in build_line().
OPENING = "Tonight in Vrell:"
CONDITION = "light rain, a high of 61,"
IMAGE = (
    "and the city's 4,000 umbrellas opening in unison at 6 p.m. "
    "for reasons nobody can explain."
)


def build_line() -> str:
    """Assemble the entry from its beats, in broadcast order."""
    return " ".join((OPENING, CONDITION, IMAGE))


LINE = build_line()

# The bounty gate: the forecast must be a single line of at most
# 160 characters.
MIN_CHARS = 1
MAX_CHARS = 160


def entry_path() -> str:
    """Where the entry file goes: $MAKEFUN_OUTPUT_DIR, else /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.txt")


def check_gate(line: str) -> None:
    """Fail loudly if the line ever drifts outside the 1-160 char gate.

    An explicit raise, not an assert: asserts vanish under `python -O`,
    and a silently out-of-gate entry scores zero.
    """
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        raise SystemExit(
            f"entry is {len(line)} chars, gate is {MIN_CHARS}-{MAX_CHARS}"
        )
    if "\n" in line:
        raise SystemExit("entry must be a single line")


def write_entry() -> str:
    """Check the gate, write the line, return the path written."""
    check_gate(LINE)
    path = entry_path()
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(LINE)
    return path


def main() -> None:
    write_entry()


if __name__ == "__main__":
    main()
