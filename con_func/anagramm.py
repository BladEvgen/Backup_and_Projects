def is_anagram(source: str, word_to_check: str) -> bool:
    """ Function to check 
    if a given string is anagram 
    and return true if so.

    Args:
        w1 (str): source string with compare
        w2 (str): word with compare

    Returns:
        bool
    """
    if sorted(source) == sorted(word_to_check):
        return True   
    return False


if __name__ == '__main__':
    print("Anagram checking")
    word1 = input("Enter word 1: ").lower()
    word2 = input("Enter word 2: ").lower()
    if is_anagram(source = word1, word_to_check = word2):
        print("Both words are anagram")
    else:
        print("Words are NOT anagram")
        
        
        