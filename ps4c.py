# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    # >>> is_word(word_list, 'bat') returns
    True
    # >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words_ps4.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words('words_ps4.txt')
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        vowels_list = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
        consonants_dict = {'b': 'b', 'c': 'c', 'd': 'd', 'f': 'f', 'g': 'g', 'h': 'h', 'j': 'j', 'k': 'k', 'l': 'l',
                            'm': 'm', 'n': 'n', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's', 't': 't', 'v': 'v', 'w': 'w',
                            'x': 'x', 'y': 'y', 'z': 'z', 'B': 'B', 'C': 'C', 'D': 'D', 'F': 'F', 'G': 'G', 'H': 'H',
                            'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S',
                            'T': 'T', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'}
        #create a list with lower and upper permutations based on input for method.
        vowels_permutation = vowels_permutation + str.upper(vowels_permutation)
        permutation_list = []
        permutation_list[:0] = vowels_permutation
        #Combine vowel list en permutation list into a dictionary.
        vowels_dict = dict(zip(vowels_list, permutation_list))
        #combine dictionary of vowels and constinants in one transpose dictionary.
        transpose_dict = vowels_dict | consonants_dict
        #return the build transpose dictionary.
        return transpose_dict
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''

        text = self.message_text
        transposed_text = ''
        for character in range(len(text)):
            if text[character] in transpose_dict:
                transposed_text = transposed_text + transpose_dict.get(text[character])
            else:
                transposed_text = transposed_text + text[character]
        return transposed_text
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''

        #First we need all permutations for the string of vowels.
        permutations = get_permutations('aeiou')
        result_dict = {}
        #Loop through all vowel permutations
        for sequence in permutations:
            #create a transpose dict.
            transpose_dict = SubMessage.build_transpose_dict(self, sequence)
            temporary_message = SubMessage.apply_transpose(self, transpose_dict)
            #split decrypted string in to check if words are valid.
            split_message = str.split(temporary_message)
            count_valid_words = 0
            for word in split_message:
                if is_word(SubMessage.get_valid_words(self), word) is True:
                    count_valid_words = count_valid_words + 1
            # list their outcomes in a tuple containing permutations, string.
            result_dict[sequence, temporary_message] = count_valid_words
        # Select sequence with most valid words from library and return.
        best_result = max(result_dict.values())
        return (list(result_dict.keys())[list(result_dict.values()).index(best_result)])


if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    #Test case 1
    message = SubMessage("I was thinking to put a nice movie quote for the test, but I could not pick one. So then still the question what to put in for the next test case.")
    permutation = "oauei"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "U wos thunkung te pit o nuca mevua qieta fer tha tast, bit U ceild net puck ena. Se than stull tha qiastuen whot te pit un fer tha naxt tast cosa.")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    #Test case 2
    message = SubMessage("A movie quot it will be. Are you not entertained?")
    permutation = "aiuoe"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "A movui qeot ut wull bi. Ari yoe not intirtaunid?")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

