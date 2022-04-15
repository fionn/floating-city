#!/usr/bin/env python3
"""Break text into tweet-sized chunks"""

import os
from functools import reduce
from operator import iconcat

import nltk

MAX_LENGTH = 280
LANG = os.environ.get("FLOATING_CITY_LANGUAGE", "en")

if LANG == "tc":
    MAX_LENGTH = int(MAX_LENGTH / 2)


def fold_sentences(sentences: list, space: str = " ") -> list:
    """Try to join sentences, keeping under the limit"""
    i = 0
    while i < len(sentences) - 1:
        if len(sentences[i]) + len(sentences[i + 1]) < MAX_LENGTH:
            sentences[i] += (space + sentences.pop(i + 1))
        else:
            i += 1

    return sentences


def split(paragraph: str) -> list:
    """Greedily split up text"""
    if len(paragraph) <= MAX_LENGTH:
        return [paragraph]

    # Split into sentences, then greedily join the sentences.
    if "。" in paragraph:
        sentences = [line + "。" for line in paragraph.split("。") if line]
        substrings = fold_sentences(sentences, space="")
    else:
        sentences = nltk.tokenize.sent_tokenize(paragraph)
        substrings = fold_sentences(sentences)

    # If any substrings are over the limit, we have to split them up more
    # finely than at the sentence level.
    deliminators = [";", ",", "；", "，", "、"]
    for i, substring in enumerate(substrings):
        if len(substring) > MAX_LENGTH:
            short_substring = substring[:MAX_LENGTH]
            for deliminator in deliminators:
                if deliminator in short_substring:
                    index = short_substring.rfind(deliminator) + 1
                    break
            substrings[i] = [substring[:index]] + split(substring[index + 1:])

    # The previous sub-sentence splitting put arrays in our array, so we have
    # to flatten it.
    flat_substrings = []
    for substring in substrings:
        if isinstance(substring, str):
            flat_substrings.append(substring)
        else:
            flat_substrings += substring

    return flat_substrings


def tweetify(path: str) -> list:
    """Split a file up into tweetable chunks"""
    with open(path, encoding="utf-8") as text_fd:
        text = text_fd.readlines()

    text = [line.strip().lstrip("# ") for line in text if line != "\n"]
    return reduce(iconcat, [split(paragraph) for paragraph in text])


def main() -> None:
    """Entry point"""
    tweets = tweetify(f"data/floating_city_{LANG}.md")
    for tweet in tweets:
        assert len(tweet) <= MAX_LENGTH
        print(tweet)
        print()


if __name__ == "__main__":
    main()
