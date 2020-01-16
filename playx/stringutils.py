#!/usr/bin/env python3
"""
    A magic module for various string operations
"""

import difflib
import json
import re
import urllib.parse


def get_closest_match(string_list, string):
    closest_matches = difflib.get_close_matches(string, string_list, len(string_list), 0.3)
    return closest_matches[0] if len(closest_matches)>0 else None


def get_closest_match_ignorecase(string_list, string):
    """
        Find the closest match of a string
        from the list of the string.
        This will ignore the cases
    """
    string_lower = string.lower().strip()
    if not string_list:
        return None

    # create a tuple of lowercased string and corresponding index
    # in the original list
    strings = [ (s.lower(), i) for i, s in enumerate(string_list) ]
    string_matched = get_closest_match( list(zip(*strings))[0], string_lower)
    for tup in strings:
        if string_matched == tup[0]:
            return string_list[tup[1]]
    return None

def escape_characters(string):
    return json.dumps(string)[1:-1]

def escape_quotes(string):
    return re.sub(r'"', '\\"', string)

def remove_multiple_spaces(string):
    return re.sub(r'\s+', ' ', string).strip()

def replace_space(string, replacer):
    return re.sub(r"\s", replacer, string)

def remove_punct(string):
    string = re.sub(r"[']+", '', string)
    return re.sub(r"[-:_!,/\[\].()#?;&\n]+", ' ', string).strip()

def replace_character(string, character, replacer):
    return re.sub(r"{}".format(character), replacer, string)

def compute_jaccard(tokens1, tokens2):
    union = set(tokens1).union(tokens2)
    # input(union)
    intersect = set(tokens1).intersection(tokens2)
    # input(intersect)
    return len(intersect)/len(union)

def urlencode(text):
    """
        Url encode the text
    """
    q = {}
    encoded = ""
    if(text):
        q['q'] = text
        encoded = urllib.parse.urlencode(q)
        encoded = encoded[2::]
    return encoded

def remove_stopwords(string):
    stopwords = ['the', 'in', 'of', 'at', 'by', 'featuring', 'x']
    res = []
    tokens = string.split()
    for token in tokens:
        if token not in stopwords:
            res.append(token)
    res = ' '.join(res)
    return remove_duplicates(res)


def remove_duplicates(string):
    tokens = string.split()
    res = []
    for token in tokens:
        if token not in res:
            res.append(token)

    res = ' '.join(res)
    return res


def fix_title(title):
    if title.endswith('.mp3'):
        title = title[:-4]
    title = remove_punct(title)
    title = remove_multiple_spaces(title)
    if not title.endswith('mp3'):
        title = title + '.mp3'
    return title


def check_keywords(tokens1, tokens2):
    """
        Check if all the tokens from tokens1
        is in tokens2 list
    """
    res = [token in tokens2 for token in tokens1]
    return sum(res) == len(tokens1)


def is_song_url(song):
    return re.match(r"^(?:https?(?:\:\/\/)?)?(?:www\.)?(?:youtu\.be|youtube\.com)/(?:watch\?v=)?[a-zA-Z0-9_-]{11}$|^(https://)?api.soundcloud.com/tracks/.*?$", song)


def url_type(url):
    if len(re.findall(r"^(?:https?(?:\:\/\/)?)?(?:www\.)?(?:youtu\.be|youtube\.com)/(?:watch\?v=)?[a-zA-Z0-9_-]{11}$", url)):
        return 'youtube'
    elif len(re.findall(r"^(https://)?api.soundcloud.com/tracks/.*?$", url)):
        return 'soundcloud'
    else:
        return None

def main():
    url = "https://www.youtube.com/watch?v=M6n-VvCcxTo"
    print(url_type(url))


if __name__ == "__main__":
    main()
