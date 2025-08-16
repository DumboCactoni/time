from datetime import datetime
from zoneinfo import ZoneInfo

class Session:
    def __init__(self):
        self.study_start = None
        self.study_end = None
        self.game_start = None
        self.game_end = None

    def is_complete(self):
        return all([self.study_start, self.study_end, self.game_start, self.game_end])

    def study_duration(self):
        return (self.study_end - self.study_start).total_seconds() / 3600

    def game_duration(self):
        return (self.game_end - self.game_start).total_seconds() / 3600

    def weighted_score(self):
        return self.study_duration() - 2 * self.game_duration()

    def readable(self):
        fmt = "%I:%M %p"
        return f"Study: {self.study_start.strftime(fmt)}–{self.study_end.strftime(fmt)}, " \
               f"Game: {self.game_start.strftime(fmt)}–{self.game_end.strftime(fmt)}"

class Tracker:
    def __init__(self):
        self.history = []
        self.current = Session()
        self.tz = ZoneInfo("America/New_York")

    def _now(self):
        return datetime.now(self.tz)

    def study_start(self):
        self.current.study_start = self._now()
        print(f"📚 Study started at {self.current.study_start.strftime('%I:%M %p')}")

    def study_end(self):
        self.current.study_end = self._now()
        print(f"📚 Study ended at {self.current.study_end.strftime('%I:%M %p')}")

    def game_start(self):
        self.current.game_start = self._now()
        print(f"🎮 Game started at {self.current.game_start.strftime('%I:%M %p')}")

    def game_end(self):
        self.current.game_end = self._now()
        print(f"🎮 Game ended at {self.game_end.strftime('%I:%M %p')}")
        if self.current.is_complete():
            self.history.append(self.current)
            self.current = Session()
            print("✅ Session logged.")

    def history_summary(self):
        print("\n📊 Last 5 Sessions:")
        for session in self.history[-5:]:
            print(session.readable())
        total_score = sum(s.weighted_score() for s in self.history)
        print(f"\n🧮 Total Weighted Score (study - 2×game): {total_score:.2f} hours")

tracker = Tracker()

while True:
    cmd = input("\nType a command (study_start, study_end, game_start, game_end, history, quit): ").strip()

    if cmd == "study_start":
        tracker.study_start()
    elif cmd == "study_end":
        tracker.study_end()
    elif cmd == "game_start":
        tracker.game_start()
    elif cmd == "game_end":
        tracker.game_end()
    elif cmd == "history":
        tracker.history_summary()
    elif cmd == "quit":
        print("👋 Goodbye.")
        break
    else:
        print("❌ Invalid command.")
