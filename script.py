import random
from enum import Enum

alpha = 'abcdefghijklmnopqrstuvwxyz'
with open('dictionary.txt', 'r') as f:
    words = f.read().split()
letter_freqs = {
    "a": 8.167,
    "b": 1.492,
    "c": 2.782,
    "d": 4.253,
    "e": 12.702,
    "f": 2.228,
    "g": 2.015,
    "h": 6.094,
    "i": 6.966,
    "j": 0.153,
    "k": 0.772,
    "l": 4.025,
    "m": 2.406,
    "n": 6.749,
    "o": 7.507,
    "p": 1.929,
    "q": 0.095,
    "r": 5.987,
    "s": 6.327,
    "t": 9.056,
    "u": 2.758,
    "v": 0.978,
    "w": 2.360,
    "x": 0.150,
    "y": 1.974,
    "z": 0.074
}

class Feedback(Enum):
    WRONG_LETTER = 1
    WRONG_POSITION = 2
    CORRECT = 3

def gen_feedback(secret_word, guess):
    letters = [c for c in secret_word]
    feedback = [Feedback.WRONG_LETTER for _ in range(5)]
    for i in range(len(guess)):
        if secret_word[i] == guess[i]:
            feedback[i] = Feedback.CORRECT
            letters.remove(secret_word[i])
    for i in range(len(guess)):
        if guess[i] in letters and feedback[i] == Feedback.WRONG_LETTER:
            feedback[i] = Feedback.WRONG_POSITION
    return feedback

word_char_rev_index = { str(c):set() for c in alpha }
word_char_pos_rev_index = { str(k):{ c:set() for c in alpha } for k in range(5) }
for word in words:
    for i in range(len(word)):
        word_char_rev_index[word[i]].add(word)
        word_char_pos_rev_index[str(i)][word[i]].add(word)

# hint : (guess, feedback)
def make_guess(hints):
    global word_char_rev_index
    global word_char_pos_rev_index

    search_space = set(words)
    for (guess, feedback) in hints:
        for i in range(len(guess)):
            if feedback[i] == Feedback.CORRECT:
                search_space = search_space & word_char_pos_rev_index[str(i)][guess[i]]
    for (guess, feedback) in hints:
        for i in range(len(guess)):
            if feedback[i] == Feedback.WRONG_LETTER:
                for j in range(len(guess)):
                    if feedback[j] != Feedback.CORRECT:
                        search_space = search_space - word_char_pos_rev_index[str(j)][guess[i]]
    for (guess, feedback) in hints:
        for i in range(len(guess)):
            if feedback[i] == Feedback.WRONG_POSITION:
                s = set()
                for j in range(len(guess)):
                    if i == j:
                        continue
                    if feedback[j] == Feedback.CORRECT:
                        continue
                    s = s | word_char_pos_rev_index[str(j)][guess[i]]
                search_space = search_space & s
    
    # Scores a guess by how desireable it is
    def score_guess(word):
        score = 0
        for c in set(word):
            score += letter_freqs[c]
        return score

    best_score = -1
    for word in search_space:
        score = score_guess(word)
        if score > best_score:
            best_score = score
            best_guess = word
    
    return best_guess

# Returns (win: bool, num_guesses: int)
def run_game(secret_word, silent=True, print_fails=False):
    guesses = []
    feedbacks = []

    while len(guesses) < 6:
        guess = make_guess([(guesses[i], feedbacks[i]) for i in range(len(guesses))])
        guesses.append(guess)
        feedback = gen_feedback(secret_word, guess)
        feedbacks.append(feedback)
        
        if guess == secret_word:
            if not silent:
                print("Guesses:")
                for guess in guesses:
                    print(guess)
                print("Feedback:")
                for feedback in feedbacks:
                    print(feedback)
                print("Correctly guessed! The word was %s." % secret_word)
            return True, len(guesses)

    if not silent or print_fails:
        print("Guesses:")
        for guess in guesses:
            print(guess)
        print("Feedback:")
        for feedback in feedbacks:
            print(feedback)
        print("Too many guesses. The word was %s." % secret_word)
    return False, len(guesses)

def run_experiment():
    scores = []
    wins = 0
    for word in words:
        (win, score) = run_game(word, print_fails=True)
        if win:
            wins += 1
            scores.append(score)
    return (scores, wins)

(scores, wins) = run_experiment()
print("Win ratio: %.2f" % (wins / len(words)))
score_dict = [0 for _ in range(7)]
for score in scores:
    score_dict[score] += 1
print("Average # of guesses: %.2f" % (sum(scores) / wins))
for i in range(1, 7):
    print("%d guess: %d." % (i, score_dict[i]))
print("Losses: %d." % (len(words) - wins))
