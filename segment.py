import math
import sys
import time

sys.setrecursionlimit(10**6)
word_dictionary_unigrams = dict()
word_dictionary_bigrams = dict()
word_dictionary_unigrams_sum = 0
word_dictionary_bigrams_sum = 0

#memo decoraror
def memoize(f):
    memo = {}
    def helper(*x):
        if x not in memo:
            memo[x] = f(*x)
        return memo[x]
    return helper
    
#calculates the probability of a given words\combinations
def words_probability(words):
    list_words_freq = list()
    for word in words:
        list_words_freq.append(word_freq_unigrams(word))
    return product(list_words_freq)
    
#helper function to calculate the product of a list
def product(nums):
    prod = 1
    for num in nums:
        prod *= num
    return prod
    
#returns list of all possible pairs for a given sentence
def split_sentence_to_pairs(sentence, max_word_len = 20):
    list_of_possiple_pairs = list()
    for i in range(min(len(sentence), max_word_len)):
        list_of_possiple_pairs.append((sentence[:i+1], sentence[i+1:]))
    return list_of_possiple_pairs
    
#returns the word freq if found in unigram file. Otherwise, it will give it alow freq
def word_freq_unigrams(word):
    if word in word_dictionary_unigrams.keys():
        return ((word_dictionary_unigrams[word])/word_dictionary_unigrams_sum)
    else:
        return (1.0/(word_dictionary_unigrams_sum * 10**(len(word)-2)))

#segment using unigram    
@memoize
def segment_unigrams(sentence):
    if not sentence:
        return 0.0, []
    sements = list()
    for first, second in split_sentence_to_pairs(sentence):
        prob, words = segment_unigrams(second)
        current_words_probability = words_probability([first] + words)
        sements.append((current_words_probability, ([first] + words)))
    return max(sements)
    
#calculates the probability of a word given the previous word
def words_conditional_probability(word, prev):
    try:
        return word_dictionary_bigrams[prev + ' ' + word]/float(word_dictionary_unigrams[prev])
    except KeyError:
        return word_freq_unigrams(word)
 
#segment using bigram 
@memoize
def segment_bigrams(sentence, prev = '<S>'):
    if not sentence:
        return 0.0, []
    sements = list()
    for first, second in split_sentence_to_pairs(sentence):
        second_probability, words = segment_bigrams(second, first)
        first_probability = math.log10(words_conditional_probability(first, prev))
        sements.append((first_probability +  second_probability, ([first] + words)))
    return max(sements)
    
#Read unigram file
for line in open('unigrams.txt'):
    word, count = line[:-1].split('\t')
    word_dictionary_unigrams[word] = int(count)
word_dictionary_unigrams_sum = float(sum(word_dictionary_unigrams.values()))

#Read pigram file
for line in open('bigrams.txt'):
    word, count = line[:-1].split('\t')
    word_dictionary_bigrams[word] = int(count)
word_dictionary_bigrams_sum = float(sum(word_dictionary_bigrams.values()))

def start_segmentation(sentence):
    if not sentence:
        print("Invalid Sentence")
        exit(0)
    sentence = sentence.lower()
    sentence =  sentence.replace(" ", "").replace('\n', "").replace('\r', "").replace('\t', "")
    
    time_unigram = time.time()
    unigram_result = segment_unigrams(sentence)[1]
    time_unigram = time.time() - time_unigram
    
    time_bigram = time.time()
    bigram_result = segment_bigrams(sentence)[1]
    time_bigram = time.time() - time_bigram
    
    return unigram_result, bigram_result, time_unigram, time_bigram