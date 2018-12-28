""" Jokebot for CSM Tech Comm Take-home. """

import time
import csv
import sys
import requests
from pathlib import Path

def deliverer(prompt, punchline):
	""" Prints prompt, waits 2 secs, prints punchline. """
	print(prompt)
	time.sleep(2)
	print(punchline + "\n")

def input_reader():
	""" Reads user input, outputs True if user wants another joke,
	False if not, keeps asking for appropriate response otherwise.
	"""
	action = -1
	while action != "yes" and action != "no":
		action = input("Do you want to hear another one?\n").lower()
		if action == "yes":
			return True
		elif action == "no":
			return False
		print("Sorry, I don't understand.")
		print("Hint: Respond with 'yes' or 'no'.\n")

def joke_reader(file):
	""" Reads jokes from csv file and outputs them into a list. """
	with open(file) as csv_file:
		reader = csv.reader(csv_file, delimiter=",")
		jokes = []
		for row in reader:
			jokes.append((row[0], row[1]))
		return jokes

def dad_jokes():
	""" Returns a list of jokes if a csv is not given. """
	r = requests.get('https://www.reddit.com/r/dadjokes.json', headers={"user-agent" : "jokebot"})
	jokes_dict = r.json()["data"]["children"]
	jokes_dict = [j for j in jokes_dict if not j["data"]["over_18"] and
					(j["data"]["title"].lower().startswith("why") or
					 j["data"]["title"].lower().startswith("what") or
					 j["data"]["title"].lower().startswith("how"))]
	return [(j["data"]["title"].encode('unicode-escape').decode('utf-8').replace("\\u2019", "'").replace("\\n", " "),
		j["data"]["selftext"].encode('unicode-escape').decode('utf-8').replace("\\u2019", "'").replace("\\n", " ")) for j in jokes_dict]

def csv_or_Reddit():
	""" Asks user if they have their own jokes. If so, returns title of csv.
	If not, returns False.
	"""
	action = -1
	while action != "yes" and action != "no":
		action = input("Hello, do you have any jokes for me to tell?\n").lower()
		if action == "yes":
			for _ in range(3):
				name = input("\nGreat, what file are they in?\n").lower()
				file = Path(name)
				if not name.endswith(".csv"):
					print("Sorry, it should be a csv file!\n")
				elif file.is_file():
					print()
					return name;
				else:
					print("Sorry, I can't find the file!\n")
			action = "no"
		if action == "no":
			print("That's okay. I have some of my own!\n")
			return False
		print("Sorry, I don't understand.")
		print("Hint: Respond with 'yes' or 'no'.\n")

def main():
	if len(sys.argv) > 1:
		print("Wrong number of arguments.")
		sys.exit()

	csv = csv_or_Reddit()

	if csv:
		jokes = joke_reader(csv)
	else:
		jokes = dad_jokes()
		

	action = True
	index = 0
	while action:
		curr = jokes[index]
		deliverer(curr[0], curr[1])
		index += 1
		if index == len(jokes):
			break
		action = input_reader()
		print()
	print("Sorry, that's all folks! Thanks for listening!")


if __name__ == '__main__': main()