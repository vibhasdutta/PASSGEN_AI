import re
from zxcvbn import zxcvbn
import pwnedpasswords
import mmap
import os
import chardet
from bisect import bisect_left

def detect_encoding(filepath):
    """Detect the file encoding using chardet."""
    with open(filepath, 'rb') as file:
        raw_data = file.read(10000)  #* Read a sample of the file -->
    result = chardet.detect(raw_data)
    return result['encoding']

def load_wordlist(wordlist_folder):
    """Load all wordlists from the specified folder into a dictionary with words as keys and filenames as values."""
    wordlist_dict = {}
    try:
        for filename in os.listdir(wordlist_folder):
            filepath = os.path.join(wordlist_folder, filename)
            try:
                #* Detect the file encoding -->
                encoding = detect_encoding(filepath)
                with open(filepath, 'r', encoding=encoding) as file:
                    mmapped_file = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
                    try:
                        for line in iter(mmapped_file.readline, b""):
                            try:
                                word = line.strip().decode(encoding)
                                wordlist_dict[word] = filename
                            except UnicodeDecodeError:
                                #* Skip lines that can't be decoded -->
                                continue
                    finally:
                        mmapped_file.close()
            except (OSError, IOError) as e:
                print(f"Error reading file {filename}: {e}")
    except Exception as e:
        print(f"Error accessing wordlist folder: {e}")
    
    #* Sort the words in the dictionary -->
    sorted_words = sorted(wordlist_dict.keys())
    return sorted_words, wordlist_dict

def binary_search(sorted_list, target):
    """Perform binary search on a sorted list."""
    index = bisect_left(sorted_list, target)
    if index < len(sorted_list) and sorted_list[index] == target:
        return index
    return -1

def analyze_password(password, sorted_words, wordlist_dict):
    analysis_result = {}
    try:
        #* 1. Zxcvbn Analysis -->
        zxcvbn_analysis = zxcvbn(password)
        zxcvbn_score = zxcvbn_analysis['score']
        zxcvbn_feedback = zxcvbn_analysis['feedback']
        analysis_result['zxcvbn_score'] = f"{zxcvbn_score}/4"
        analysis_result['zxcvbn_feedback'] = zxcvbn_feedback
    except Exception as e:
        print(f"Error during Zxcvbn analysis: {e}")
        analysis_result['zxcvbn_score'] = 0
        analysis_result['zxcvbn_feedback'] = {'warning': 'Error analyzing password'}

    try:
        #* 2. Pwned Passwords Check -->
        breaches = pwnedpasswords.check(password)
        analysis_result['breaches'] = breaches
    except Exception as e:
        print(f"Error during Pwned Passwords check: {e}")
        analysis_result['breaches'] = 0

    try:
        #* 3. Custom Regex Analysis -->
        patterns = {
            'uppercase': r'[A-Z]',
            'lowercase': r'[a-z]',
            'digit': r'\d',
            'special': r'[!@#$%^&*(),.?":{}|<>]'
        }

        regex_strength = {
            'uppercase': bool(re.search(patterns['uppercase'], password)),
            'lowercase': bool(re.search(patterns['lowercase'], password)),
            'digit': bool(re.search(patterns['digit'], password)),
            'special': bool(re.search(patterns['special'], password)),
        }
        analysis_result['regex_strength'] = regex_strength
    except Exception as e:
        print(f"Error during regex analysis: {e}")
        analysis_result['regex_strength'] = {}

    try:
        #* 4. Wordlist Check using Binary Search -->
        index = binary_search(sorted_words, password)
        found_in_wordlists = []
        if index != -1:
            found_in_wordlists.append(wordlist_dict[sorted_words[index]])
            analysis_result['found_in_wordlists'] = found_in_wordlists
        else:
            analysis_result['found_in_wordlists'] = "Password not found in any of the wordlists"
    except Exception as e:
        print(f"Error checking password in wordlists: {e}")
        analysis_result['found_in_wordlists'] = []

    return analysis_result

    
if __name__ == "__main__":
    
    wordlist_folder = r'./PassGen_Wordlist'  #* Replace with your wordlist folder path -->
    sorted_words, wordlist_dict = load_wordlist(wordlist_folder)

    user_password = input("Enter your current password: ")

    #* Analyze the password -->
    analysis = analyze_password(user_password, sorted_words, wordlist_dict)

    for key, value in analysis.items():
        print(f"{key}: {value}")
