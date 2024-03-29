import math
import os
import re


def get_unigram(words):
    """
    Create a unigram model for the words provided
    :param words: List of words
    :return: sorted unigram
    """
    alpha = 0.5
    char_total = 0
    unigram = {}

    # Create dictionary key for each alphabet character and add alpha for smoothing
    a = 97
    while a < 123:
        unigram[str(chr(a))] = alpha
        char_total += alpha
        a += 1

    for word in words:
        for char in word:
            # For each character encountered, increment letter frequency by one
            unigram[char] += 1
            char_total += 1

    # Calculate probability of each letter
    for c in unigram:
        unigram[c] = unigram[c]/char_total

    return unigram


def get_bigram(words):
    """
    Create a bigram model for the words provided
    :param words: List of words
    :return: sorted bigram taking into account word endings
    """
    alpha = 0.5
    bigram_total = 0
    bigram = {}

    # Find all char combinations and add alpha for smoothing
    a = 97
    while a < 123:
        b = 97
        while b < 123:
            w = str(chr(a) + chr(b))
            bigram[w] = alpha
            bigram_total += alpha
            b += 1
        a += 1

    for word in words:
        i = 0
        while i < len(word) - 1:
            w = str(word[i]+word[i+1])
            # For each dual combo, increment letter frequency by one
            bigram[w] += 1
            bigram_total += 1
            i += 1

    # Calculate probability of each letter
    for c in bigram:
        bigram[c] = bigram[c]/bigram_total

    return bigram


def get_trigram(words):
    """
    Create a trigram model for the words provided
    :param words: List of words
    :return: sorted trigram taking into account word endings
    """
    alpha = 0.5
    trigram_total = 0
    trigram = {}

    # Find all char combinations and add alpha for smoothing
    a = 97
    while a < 123:
        b = 97
        while b < 123:
            c = 97
            while c < 123:
                w = str(chr(a) + chr(b) + chr(c))
                trigram[w] = alpha
                trigram_total += alpha
                c += 1
            b += 1
        a += 1

    for word in words:
        i = 0
        while i < len(word) - 2:
            w = str(word[i] + word[i+1] + word[i+2])
            # For each combo, increment letter frequency by one
            trigram[w] += 1
            trigram_total += 1
            i += 1

    # Calculate probability of each letter
    for c in trigram:
        trigram[c] = trigram[c]/trigram_total

    return trigram


def query_unigram(query, english_unigram, french_unigram, german_unigram, welsh_unigram, output_file):
    """
    Query on unigrams to find the most probable language
    :param query: The text query
    :param english_unigram:
    :param french_unigram:
    :param german_unigram:
    :param welsh_unigram:
    :return:
    """
    # Dictionary of log probabilities of each language
    log_probs = {
        'EN': 0,
        'FR': 0,
        'GE': 0,
        'CY': 0
    }

    query_words = re.findall("[a-zA-Z]+", query)
    query = ""
    for word in query_words:
        query += word + " "

    # Open in write mode (Overwrites the file)
    file = open(os.path.abspath(os.path.join(os.getcwd(), "../query_output/", output_file)), "w+")
    file.write(query + "\n\n" + "UNIGRAM MODEL:\n\n")
    # Loop through all characters of the query
    for c in query:
        # If c is not an empty space
        if " " not in c:
            # Add the log base 10 probability
            log_probs['EN'] += math.log(english_unigram[c], 10)
            log_probs['FR'] += math.log(french_unigram[c], 10)
            log_probs['GE'] += math.log(german_unigram[c], 10)
            log_probs['CY'] += math.log(welsh_unigram[c], 10)

            file.write("UNIGRAM: " + c + "\n"
                        "FRENCH: P(" + c + ") = " + str(log_probs['FR']) + "\n" +
                        "ENGLISH: P(" + c + ") = " + str(log_probs['EN']) + "\n" +
                        "GERMAN: P(" + c + ") = " + str(log_probs['GE']) + "\n" +
                        "WELSH: P(" + c + ") = " + str(log_probs['CY']) + "\n\n")

    # Sort the languages by log probability
    sorted_by_value = sorted(log_probs.items(), key=lambda kv: kv[1], reverse=True)

    return sorted_by_value[0]


def query_bigram(query, english_bigram, french_bigram, german_bigram, welsh_bigram, output_file):
    """
    Query on bigrams to find the most probable language
    :param query: The text query
    :param english_bigram:
    :param french_bigram:
    :param german_bigram:
    :param welsh_bigram:
    :return:
    """
    # Dictionary of log probabilities of each language
    log_probs = {
        'EN': 0,
        'FR': 0,
        'GE': 0,
        'CY': 0
    }

    # Clean query
    query_words = re.findall("[a-zA-Z]+", query)
    query = ""
    for word in query_words:
        query += word + " "

    # Open in append mode (Does not overwrite the file)
    file = open(os.path.abspath(os.path.join(os.getcwd(), "../query_output/", output_file)), "a")
    file.write(query + "\n\n" + "BIGRAM MODEL:\n\n")
    # Loop through all characters of the query

    i = 0
    while i < len(query)-1:
        c = str(query[i]+query[i+1])

        # If c is not an empty space
        if " " not in c:
            # Add the log base 10 probability
            log_probs['EN'] += math.log(english_bigram[c], 10)
            log_probs['FR'] += math.log(french_bigram[c], 10)
            log_probs['GE'] += math.log(german_bigram[c], 10)
            log_probs['CY'] += math.log(welsh_bigram[c], 10)

            file.write("BIGRAM: " + c + "\n"
                        "FRENCH: P(" + c + ") = " + str(log_probs['FR']) + "\n" +
                        "ENGLISH: P(" + c + ") = " + str(log_probs['EN']) + "\n" +
                        "GERMAN: P(" + c + ") = " + str(log_probs['GE']) + "\n" +
                        "WELSH: P(" + c + ") = " + str(log_probs['CY']) + "\n\n")
        i += 1

    # Sort the languages by log probability
    sorted_by_value = sorted(log_probs.items(), key=lambda kv: kv[1], reverse=True)

    return sorted_by_value[0]


def query_trigram(query, english_trigram, french_trigram, german_trigram, welsh_trigram, output_file):
    """
    Query on bigrams to find the most probable language
    :param query: The text query
    :param english_trigram:
    :param french_trigram:
    :param german_trigram:
    :param welsh_trigram:
    :return:
    """
    # Dictionary of log probabilities of each language
    log_probs = {
        'EN': 0,
        'FR': 0,
        'GE': 0,
        'CY': 0
    }

    # Clean query
    query_words = re.findall("[a-zA-Z]+", query)
    query = ""
    for word in query_words:
        query += word + " "

    # Open in append mode (Does not overwrite the file)
    file = open(os.path.abspath(os.path.join(os.getcwd(), "../query_output/", output_file)), "a")
    file.write(query + "\n\n" + "TRIGRAM MODEL:\n\n")
    # Loop through all characters of the query

    i = 0
    while i < len(query) - 2:
        c = str(query[i] + query[i+1] + query[i+2])

        # If c is not an empty space
        if " " not in c:
            # Add the log base 10 probability
            log_probs['EN'] += math.log(english_trigram[c], 10)
            log_probs['FR'] += math.log(french_trigram[c], 10)
            log_probs['GE'] += math.log(german_trigram[c], 10)
            log_probs['CY'] += math.log(welsh_trigram[c], 10)

            file.write("TRIGRAM: " + c + "\n"
                        "FRENCH: P(" + c + ") = " + str(log_probs['FR']) + "\n" +
                        "ENGLISH: P(" + c + ") = " + str(log_probs['EN']) + "\n" +
                        "GERMAN: P(" + c + ") = " + str(log_probs['GE']) + "\n" +
                        "WELSH: P(" + c + ") = " + str(log_probs['CY']) + "\n\n")
        i += 1

    # Sort the languages by log probability
    sorted_by_value = sorted(log_probs.items(), key=lambda kv: kv[1], reverse=True)

    return sorted_by_value[0]

