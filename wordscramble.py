
"""Simple Word Scramble CLI game.

Play multiple rounds, guess scrambled words, request a hint, and track score.
"""

import random
import textwrap

WORDS = [
	"python", "variable", "function", "developer", "keyboard", "monitor",
	"internet", "package", "library", "algorithm", "condition", "loop",
	"string", "integer", "boolean", "scramble", "challenge", "project",
	"terminal", "command", "module", "syntax", "testing", "random",
	"package", "virtual", "environment", "exception", "resource",
]


def scramble_word(word: str) -> str:
	if len(word) <= 1:
		return word
	letters = list(word)
	attempt = 0
	while True:
		random.shuffle(letters)
		scrambled = "".join(letters)
		attempt += 1
		if scrambled != word or attempt > 10:
			return scrambled


def reveal_hint(word: str, revealed: set) -> str:
	# reveal one more letter in its correct position
	indices = [i for i in range(len(word)) if i not in revealed]
	if not indices:
		return "".join([c if i in revealed else "_" for i, c in enumerate(word)])
	idx = random.choice(indices)
	revealed.add(idx)
	return "".join([c if i in revealed else "_" for i, c in enumerate(word)])


def play(rounds: int = 5) -> None:
	score = 0
	print(textwrap.dedent("""
	Welcome to Word Scramble!
	Commands: type your guess, or `hint` for a letter (costs points), `skip` to move on, `quit` to exit.
	"""))

	for r in range(1, rounds + 1):
		word = random.choice(WORDS)
		scrambled = scramble_word(word)
		revealed = set()
		print(f"\nRound {r}/{rounds}")
		print(f"Scrambled: {scrambled}")

		while True:
			ans = input("Your guess (or `hint`/`skip`/`quit`): ").strip().lower()
			if ans == "" or ans.isspace():
				continue
			if ans == "quit":
				print("Thanks for playing!")
				print(f"Final score: {score}")
				return
			if ans == "skip":
				print(f"Skipped. The word was: {word}")
				break
			if ans == "hint":
				# cost 2 points but don't go below 0
				hint_view = reveal_hint(word, revealed)
				score = max(0, score - 2)
				print(f"Hint: {hint_view}  (score -2)")
				continue
			if ans == word:
				# award points: 10 for correct guess, plus 2 per unrevealed letter
				pts = 10 + 2 * (len(word) - len(revealed))
				score += pts
				print(f"Correct! +{pts} points. Total: {score}")
				break
			else:
				print("Nope, try again.")

	print("\nGame over")
	print(f"Final score: {score}")


def self_test() -> bool:
	# quick sanity checks
	for w in ["python", "a", "aa"]:
		s = scramble_word(w)
		if len(s) != len(w):
			return False
	# ensure scramble is usually different
	diff_count = 0
	for _ in range(20):
		if scramble_word("testing") != "testing":
			diff_count += 1
	return diff_count > 0


if __name__ == "__main__":
	try:
		rounds_input = input("How many rounds would you like? (default 5): ")
		rounds = int(rounds_input) if rounds_input.strip() else 5
	except Exception:
		rounds = 5
	try:
		play(rounds=rounds)
	except KeyboardInterrupt:
		print("\nInterrupted. Goodbye.")
