ROCK = "rock"
PAPER = "paper"
SCISSORS = "scissors"

moves = {"A": ROCK,
         "B": PAPER,
         "C": SCISSORS,
         "X": ROCK,
         "Y": PAPER,
         "Z": SCISSORS}

scores = {"win": 6,
          "tie": 3,
          "loss": 0,
          "rock": 1,
          "paper": 2,
          "scissors": 3}

results = {"X": "loss",
           "Y": "tie",
           "Z": "win"}

def get_input(filename):
    with open(filename, "r") as inp:
        return [i.split() for i in inp.readlines()]

def score(them, you):
    wins = ((ROCK, SCISSORS),
            (PAPER, ROCK),
            (SCISSORS, PAPER))

    # Check for tie
    if them == you:
        return scores["tie"] + scores[you]

    # Check for win
    for y, t in wins:
        if you == y and them == t:
            return scores["win"] + scores[you]

    # Loss
    return scores["loss"] + scores[you]

def total(inp):
    total = 0
    for them, you in inp:
        their_move = moves[them]
        your_move = moves[you]
        total += score(their_move, your_move)
    return total

def part_two_total(inp):
    total = 0

    # Map of what beats what
    beats = {ROCK: SCISSORS,
             SCISSORS: PAPER,
             PAPER: ROCK}

    # Map of what loses to what
    loses = {ROCK: PAPER,
             PAPER: SCISSORS,
             SCISSORS: ROCK}

    for them, result in inp:
        their_move = moves[them]
        if results[result] == "tie":
            your_move = their_move
        elif results[result] == "win":
            your_move = loses[their_move]
        elif results[result] == "loss":
            your_move = beats[their_move]
        total += score(their_move, your_move)

    return total

if __name__ == "__main__":
    inp = get_input("input1.txt")

    print(total(inp))
    print(part_two_total(inp))

