"""Improved quiz game

Features:
- Shuffles questions and choices
- Validates input and allows quitting
- Tracks time taken
- Persists high scores to `quiz_highscores.json`
"""

from pathlib import Path
import json
import random
import time
from datetime import datetime


HIGHSCORE_FILE = Path(__file__).with_name("quiz_highscores.json")


def load_highscores(path=HIGHSCORE_FILE):
	if not path.exists():
		return []
	try:
		return json.loads(path.read_text(encoding="utf-8"))
	except Exception:
		return []


def save_highscores(highscores, path=HIGHSCORE_FILE):
	path.write_text(json.dumps(highscores, indent=2), encoding="utf-8")


def ask_question(qnum, question, choices, answer_index):
	print(f"\nQuestion {qnum}:")
	print(question)

	labels = ["A", "B", "C", "D"]
	for i, choice in enumerate(choices):
		print(f"  {labels[i]}. {choice}")

	while True:
		user = input("Your answer (A/B/C/D) or Q to quit: ").strip().upper()
		if user == "Q":
			return None  # user chose to quit
		if user in labels[: len(choices)]:
			selected = labels.index(user)
			return 1 if selected == answer_index else 0
		print("Invalid input. Please enter A, B, C, D or Q to quit.")


def show_results(score, total, elapsed_seconds):
	print("\n" + "=" * 40)
	print(f"Score: {score}/{total}")
	pct = (score / total) * 100 if total else 0
	print(f"Percentage: {pct:.1f}%")
	print(f"Time taken: {elapsed_seconds:.1f} seconds")
	if pct == 100:
		print("Excellent!")
	elif pct >= 60:
		print("Good Job!")
	else:
		print("Keep Practicing!")
	print("=" * 40)
	return pct


def record_score(name, score, total, pct, highscores):
	entry = {
		"name": name,
		"score": score,
		"total": total,
		"percentage": round(pct, 1),
		"time": datetime.utcnow().isoformat() + "Z",
	}
	highscores.append(entry)
	highscores.sort(key=lambda e: (-e["percentage"], e["time"]))
	# keep top 10
	return highscores[:10]


def main():
	# Questions: list of dicts with question, choices(list) and answer index (0-based)
	questions = [
		{
			"question": "What is the capital of India?",
			"choices": ["Mumbai", "Delhi", "Kolkata", "Chennai"],
			"answer": 1,
		},
		{
			"question": "Which keyword is used to create a function in Python?",
			"choices": ["function", "define", "def", "func"],
			"answer": 2,
		},
		{
			"question": "Which planet is known as the Red Planet?",
			"choices": ["Earth", "Mars", "Venus", "Jupiter"],
			"answer": 1,
		},
		{
			"question": "How many continents are there?",
			"choices": ["5", "6", "7", "8"],
			"answer": 2,
		},
		{
			"question": "Which data type stores True or False?",
			"choices": ["int", "float", "bool", "string"],
			"answer": 2,
		},
	]

	print("=" * 40)
	print("        PYTHON QUIZ GAME")
	print("=" * 40)

	# shuffle question order
	random.shuffle(questions)

	score = 0
	total_asked = 0
	start = time.perf_counter()

	for i, q in enumerate(questions, start=1):
		# shuffle choices but keep track of correct index
		choices = q["choices"].copy()
		correct = q["answer"]
		zipped = list(enumerate(choices))
		random.shuffle(zipped)
		new_choices = [c for _, c in zipped]
		# find new index of the originally correct choice
		original_choice = choices[correct]
		new_answer_index = new_choices.index(original_choice)

		result = ask_question(i, q["question"], new_choices, new_answer_index)
		if result is None:
			print("You chose to quit early.")
			break
		score += result
		total_asked += 1

	elapsed = time.perf_counter() - start

	if total_asked == 0:
		print("No questions answered. Goodbye!")
		return

	pct = show_results(score, total_asked, elapsed)

	highscores = load_highscores()
	name = input("Enter your name to save score (or press Enter to skip): ").strip()
	if name:
		highscores = record_score(name, score, total_asked, pct, highscores)
		save_highscores(highscores)
		print("High scores updated.")

	if highscores:
		print("\nTop scores:")
		for idx, e in enumerate(highscores[:5], start=1):
			when = e.get("time", "-")
			print(f"{idx}. {e['name']} — {e['score']}/{e['total']} ({e['percentage']}%) — {when}")


if __name__ == "__main__":
	main()
