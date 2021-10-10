# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

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
    #>>> is_word(word_list, 'bat') returns
    True
    #>>> is_word(word_list, 'asdf') returns
    False
    '''

    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words_ps4.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
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
        return list.copy(self.valid_words)

    def build_shift_dict(self, shift) -> object:
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        shift_dict = {}
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        for letter in range(len(lowercase)):
            original_letter = lowercase[letter]
            if (letter + shift) < 26:
                shifted_letter = lowercase[letter + shift]
            else:
                shifted_letter = lowercase[(letter + shift) - 26]
            shift_dict[original_letter] = shifted_letter

        for letter in range(len(uppercase)):
            original_letter = uppercase[letter]
            if (letter + shift) < 26:
                shifted_letter = uppercase[letter + shift]
            else:
                shifted_letter = uppercase[(letter + shift) - 26]
            shift_dict[original_letter] = shifted_letter
        return shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shift_dict = self.build_shift_dict(shift)
        text = self.message_text
        encrypted_text = ''
        for character in range(len(text)):
            if text[character] in shift_dict:
                encrypted_text = encrypted_text + shift_dict.get(text[character])
            else:
                encrypted_text = encrypted_text + text[character]
        return encrypted_text


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)
        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return dict.copy(self.encryption_dict)

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.build_shift_dict(shift)
        self.encryption_dict = Message.build_shift_dict(self, shift)

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)


    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        shift_number = 25
        encrypted_message = self.message_text
        # Loop through all shift numbers from 1 to 26.
        result_dict = {}
        while shift_number >= 1:
            #build a decryption dictionary
            PlaintextMessage.change_shift(self, shift_number)
            decrypt_dict = PlaintextMessage.get_encryption_dict(self)
            decrypted_message = ''
            count_valid_words = 0
            #Shift all characters in the string based on shift_dict, exclude punctuation and white spaces.
            for character in range(len(encrypted_message)):
                if encrypted_message[character] in decrypt_dict:
                    decrypted_message = decrypted_message + decrypt_dict.get(encrypted_message[character])
                else:
                    decrypted_message = decrypted_message + encrypted_message[character]
            #Split string into list of "words".
            list_words = str.split(decrypted_message)
            #Loop through list_words en verify if valid. Count each valid word.
            for word in list_words:
                if is_word(Message.get_valid_words(self), word) is True:
                    count_valid_words = count_valid_words + 1
            #combine valid word count with a tuple of shift number and decrypted textmessage
            result_dict[shift_number, decrypted_message] = count_valid_words
            shift_number = shift_number - 1
        # Select shift with most valid words from library and return.
        best_result = max(result_dict.values())
        # return tuple
        return (list(result_dict.keys())[list(result_dict.values()).index(best_result)])


if __name__ == '__main__':

    #testcase 1
    plaintext = PlaintextMessage('Hello world! here is a little test run of the ceaser encoder.', 19)
    print('Expected Output: Axeeh phkew! axkx bl t ebmmex mxlm kng hy max vxtlxk xgvhwxk.')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    #testcase 2
    ciphertext = CiphertextMessage('Axeeh phkew! axkx bl t ebmmex mxlm kng hy max vxtlxk wxvhwxk.')
    print('Expected Output:', (7, 'Hello world! here is a little test run of the ceaser decoder.'))
    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: best shift value and unencrypted story:

    test_file = open('story_ps4.txt', 'r')
    for story in test_file:
        ciphertext = CiphertextMessage(story)
        print('Best shift value and unencrypted story:', ciphertext.decrypt_message())
