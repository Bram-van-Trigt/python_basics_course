# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    # Determine sequence length.
    sequence_length = len(sequence)
    permutations = []
    sub_permutations = []
    # Basecase: if length is 1 return sequence as permutation.
    if sequence_length <= 1:
        permutations.append(sequence)
        return permutations
    else:
        # Recursive solution: give sequence letters except first letter into get_permutations.
        sub_permutations.extend(get_permutations(sequence[1:sequence_length]))
        #walk with the first letter of sequence through sub_permutations to find all possible permutations.
        #loop through every sequence in de list sub_permutations.
        for sub_sequences in range(len(sub_permutations)):
            temporary_sequence = sub_permutations[sub_sequences]
            #loop through all positions in sub_permutation
            for position in range(len(temporary_sequence)+1):
                letter = sequence[0]
                new_sequence = temporary_sequence[:position] + letter + temporary_sequence[position:]
                #Add permutation to the list permutations if not already listed.
                if new_sequence not in permutations:
                    permutations.append(new_sequence,)
        return permutations


if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    test_input1 = 'de'
    expected_test_output1 = ['de', 'ed']
    print('Input:', test_input1)
    print('Expected Output:', expected_test_output1)
    print('Actual Output:', get_permutations(test_input1))

    test_input2 = 'def'
    expected_test_output2 = ['def', 'dfe', 'edf', 'efd', 'fde', 'fed']
    print('Input:', test_input2)
    print('Expected Output:', expected_test_output2)
    print('Actual Output:', get_permutations(test_input2))

    test_input3 = 'ooh'
    expected_test_output3 = ['ooh', 'oho', 'hoo']
    print('Input:', test_input3)
    print('Expected Output:', expected_test_output3)
    print('Actual Output:', get_permutations(test_input3))
