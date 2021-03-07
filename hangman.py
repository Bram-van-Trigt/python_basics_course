# Problem Set 2, hangman.py
# Name: Bram van Trigt

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    length_secret_word = len(secret_word)
    for n in range(length_secret_word):
        if not secret_word[n] in letters_guessed:
            return False
    return True

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    length_secret_word = len(secret_word)
    x = ""
    for n in range(length_secret_word):
        if not secret_word[n] in letters_guessed:
            x = x + "_ "
        if secret_word[n] in letters_guessed:
            x = x + secret_word[n]
    return x

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    length_letters_guessed = len(letters_guessed)
    x = string.ascii_lowercase
    for n in range(length_letters_guessed):
        x = x.replace(letters_guessed[n], "")
    return x

def check_user_input(new_letter, letters_guessed, warnings, remaining_guesses):
    '''
    Check if users guess is an alphabetic letter and only one character.
    Returns the situation.
    '''
    check_isalpha = str.isalpha(new_letter)
    check_length = len(new_letter)
    check_new_letter = new_letter in letters_guessed
    if check_isalpha is True and check_length == 1 and check_new_letter is False:
        new_letter = str.lower(new_letter)
        letters_guessed.append(new_letter)
        return True, new_letter, letters_guessed, warnings, remaining_guesses
    if check_isalpha is False:
        print("Ooh no! Your guess is not a alphabetic character.")
        return False, new_letter, letters_guessed, warnings, remaining_guesses
    if check_length != 1:
        print("Oops, that are to many guesses at once.")
        return False, new_letter, letters_guessed, warnings, remaining_guesses
    if check_new_letter is True:
        if warnings == 0:
            remaining_guesses = remaining_guesses - 1
            print("Guess what! You have tried this letter already and now you have only " + str(remaining_guesses) + " guesses left.")
            return False, new_letter, letters_guessed, warnings, remaining_guesses
        else:
            warnings = warnings - 1
            print("Guess what! You have tried this letter already and now you have only " + str(warnings)  + " warnings left.")
            return False, new_letter, letters_guessed, warnings, remaining_guesses

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    secret_word = choose_word(wordlist)
    remaining_guesses = 6
    warnings = 3
    letters_guessed = ['']
    new_letter = ''
    vowel = ['a','e','i','o','u']
    print("Welcome to the game HANGMAN!!!")
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
    while remaining_guesses > 0:
        print("------------------")
        print("You have " + str(remaining_guesses) + " guesses and " + str(warnings) + " warnings left.")
        print("Your available letters are: " + get_available_letters(letters_guessed))
        new_letter = str(input(print("please guess a letter:")))
        check, new_letter, letters_guessed, warnings, remaining_guesses = check_user_input(new_letter, letters_guessed, warnings, remaining_guesses)
        if check is True:
            if new_letter in secret_word:
                 if is_word_guessed(secret_word, letters_guessed) is True:
                     print("Congratulations you won the game!!!!")
                     print("You scored " + str(remaining_guesses * len(secret_word)) + " points")
                     return
                 else:
                    print("Good guess: " + get_guessed_word(secret_word, letters_guessed))
            else:
                print("That letter is not in my word: ")
                print(get_guessed_word(secret_word, letters_guessed))
                if remaining_guesses <= 0:
                    break
                elif new_letter in vowel:
                    remaining_guesses = remaining_guesses - 2
                else:
                    remaining_guesses = remaining_guesses - 1
    if warnings <= 0:
        print("To bad, you are out of warnings and guesses.")
        print("My word was " + secret_word + ".")
    else:
        print("To bad, you are out of guesses.")
        print("My word was " + secret_word + ".")

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############

# To test part 3 re-comment out the above lines and
# uncomment the following two lines.

# secret_word = choose_word(wordlist)
# hangman_with_hints(secret_word)
