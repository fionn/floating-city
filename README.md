# Floating City

_The [@floatingcitybot](https://twitter.com/floatingcitybot) appeared suddenly._

## About

A Twitter bot that tweets _Marvels of a Floating City_ by Xi Xi.[^1]

[^1]: As translated by Linda Jaivin and Geremie Barmé, sourced from [China Heritage](https://chinaheritage.net/journal/the-floating-city-%E6%B5%AE%E5%9F%8E/) and reproduced (with minor corrections) in [`data/floating_city_en.md`](data/floating_city_en.md).

We take paragraphs from the source material and greedily split them into groups of sentences, maximising length subject to the character limit. If this is not possible (i.e. we have very long sentences), we split by delimiter instead.

State is maintained by Twitter, so we check what the last tweet was, find it in our array of text groups and tweet the next element. If there is no last tweet, start from the start. If the last tweet is the last text group in our array, we've finished, so do nothing (as opposed to restarting).

## Usage

Requires the standard Twitter API environment variables. Generate them with [fionn/twitter-authenticator](https://github.com/fionn/twitter-authenticator).

Run `src/tweetify.py` to print each text group.

Run `src/main.py` to tweet once and exit.

## Deploy

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/fionn/floating-city)

Add the remote with `git remote add heroku https://git.heroku.com/app-name.git` and use `git push heroku` to deploy.
