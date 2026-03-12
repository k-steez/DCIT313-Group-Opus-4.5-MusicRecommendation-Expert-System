import sys
import os
from pathlib import Path
from pyswip import Prolog

# ── Valid atoms (must match knowledge_base/mood_profiles.pl and activity_profiles.pl)
MOODS = [
    "happy", "energetic", "motivated", "confident",
    "angry", "anxious", "stressed",
    "sad", "melancholic", "tired", "bored",
    "calm", "romantic", "nostalgic", "focused",
]

ACTIVITIES = [
    "studying", "deep_work", "light_work",
    "working_out", "commuting", "chores",
    "socializing", "romance", "grieving_venting",
    "relaxing", "sleeping", "meditating",
]

# Lyric preference maps to cognitive load for the Prolog engine:
#   instrumental  → high  (forces simple/instrumental tracks)
#   with_lyrics   → low   (any lyric complexity accepted)
#   no_preference → moderate (all complexities accepted)
LYRIC_PREFS = ["with_lyrics", "instrumental", "no_preference"]
LYRIC_PREF_TO_COGNITIVE_LOAD = {
    "with_lyrics":   "low",
    "instrumental":  "high",
    "no_preference": "moderate",
}

# ── Helpers: display a numbered menu and return the chosen atom

def prompt_choice(prompt_title: str, options: list[str]) -> str:
    """Display a numbered list of options and return the selected atom.

    Accepts either a number (1-based) or the atom name directly.
    Loops until a valid choice is entered.
    """
    print(f"\n{prompt_title}")
    print("-" * len(prompt_title))
    for i, opt in enumerate(options, start=1):
        print(f"  {i:>2}. {opt}")

    while True:
        raw = input("Enter number or name: ").strip().lower()

        # Accept numeric input
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
            print(f"  [!] Please enter a number between 1 and {len(options)}.")
            continue

        # Accept atom name directly
        if raw in options:
            return raw

        print(f"  [!] '{raw}' is not a valid option. Try again.")


def prompt_limit(default: int = 10) -> int:
    """Ask the user for an integer playlist size, defaulting to `default`."""
    while True:
        raw = input(f"\nPlaylist size (press Enter for {default}): ").strip()
        if raw == "":
            return default
        if raw.isdigit() and int(raw) > 0:
            return int(raw)
        print("  [!] Please enter a positive integer.")


# ---------------------------------------------------------------------------
# Prolog bridge
# ---------------------------------------------------------------------------

def load_knowledge_base() -> Prolog:
    """Initialise the SWI-Prolog engine and consult the top-level .pl file."""
    prolog = Prolog()
    kb_path = str(
        (Path(__file__).parent / ".." / "knowledge_base" / "moodbeats.pl").resolve()
    )
    try:
        prolog.consult(kb_path)
        print(f"[MoodBeats] Knowledge base loaded from '{kb_path}'.")
    except Exception as exc:
        print(f"[MoodBeats] ERROR – could not load knowledge base: {exc}")
        sys.exit(1)
    return prolog


def run_query(prolog: Prolog, mood: str, activity: str,
              cognitive_load: str, limit: int) -> None:
    """Build and execute the Prolog goal run/4, then display results.

    run/4 is defined in moodbeats.pl.  It calls safe_recommend/5 internally,
    prints the playlist and explanations via format/2, and handles the
    fallback message when no exact match is found.
    """
    goal = f"run({mood}, {activity}, {cognitive_load}, {limit})"

    print("\n" + "=" * 60)
    print(f"  Querying Prolog: {goal}")
    print("=" * 60)

    try:
        results = list(prolog.query(goal))

        if not results:
            print("\n[MoodBeats] The inference engine returned no solution.")
            print("  This may mean the knowledge base has no songs that match")
            print("  your parameters even after fallback. Try different inputs.")
    except Exception as exc:
        print(f"\n[MoodBeats] ERROR during query: {exc}")


# ---------------------------------------------------------------------------
# Main interactive loop
# ---------------------------------------------------------------------------

def main() -> None:
    """Entry point: interactive CLI for the MoodBeats expert system."""
    print("\n" + "#" * 60)
    print("#       MoodBeats – Music Recommendation Expert System      #")
    print("#                  DCIT 313 · Team Opus 4.5                 #")
    print("#" * 60)

    # Step 1 – Load the Prolog knowledge base once
    prolog = load_knowledge_base()

    while True:
        print("\n" + "~" * 60)
        print("  Answer the questions below to generate your playlist.")
        print("~" * 60)

        # Step 2 – Collect user preferences
        mood       = prompt_choice("1. Select your current MOOD",   MOODS)
        activity   = prompt_choice("2. Select your ACTIVITY",        ACTIVITIES)
        lyric_pref = prompt_choice("3. Lyric preference",            LYRIC_PREFS)
        limit      = prompt_limit(default=10)

        # Map lyric preference to cognitive load atom
        cognitive_load = LYRIC_PREF_TO_COGNITIVE_LOAD[lyric_pref]

        # Step 3 – Run the Prolog inference engine
        run_query(prolog, mood, activity, cognitive_load, limit)

        # Step 4 – Ask whether to generate another playlist
        print("\n" + "-" * 60)
        again = input("Generate another playlist? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("\n[MoodBeats] Goodbye – enjoy your music!\n")
            break


if __name__ == "__main__":
    main()
