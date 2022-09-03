# wordle-solver

This wordle solver uses a straightforward strategy: maintain a set of possible answers,
try to make a guess that would provide the most information given the current set of possible answers, 
and repeat until the set only has one word in it.

### Flaws

- The solver relies on a list of possible answers (which is not what a Wordle player would generally
have memorized)
- Because it only guesses possible words, it can often make suboptimal guesses when it is very
close to getting the word. For example, if the first 4 letters are "STEA_", it will successively
guess "STEAK", "STEAL", "STEAM", etc.; a more optimal strategy would guess a word such as "milky",
which would in a single step provide information on the presence of K, L, or M.
