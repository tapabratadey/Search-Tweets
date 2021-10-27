<h1 align="center">Welcome to Searching Tweets: Neeva Backend Project 👋</h1>

## Description

**`A search engine to query top 5 recent tweets.`**

## Author

---

👤 **tapa**

- Github: [@tapabratadey](https://github.com/tapabratadey)
- LinkedIn: [@tapabratadey](https://linkedin.com/in/tapabratadey)

## Project Scope

---

1. `Faster searching` on a large set of tweets.
2. Return `top 5 most recent tweets`.
3. Handle search operators like AND `&`, OR `|`, NOT `!` and Grouping `()`

## Approach

---

I used:

1. Inverted indexing to index tweet words to its tweet's timestamp.
2. Reverse polish notation to query words based on its following operators.

## Usage

---

```sh
python3 main.py
```

## Assumptions

---

1. the `OR operator |` is between a single word/expression:

   - **Valid**: </br>
     - `Noovi & is & (fast | (very & quick))` </br>
     - `Noovi & is & (fast | quick)` </br>
     - `Noovi | Neeva`</br>
   - **Invalid**:
     - `Noovi & is & fast | very & quick` (this would be ambiguous without parentheses or prioritizing symbols over one another)</br>

2. The logical `NOT operator !` only applies to the word or expression immediately following it:
   - `Noovi & fast & !quick & fun` should return tweets with words “Noovi” AND “fast” AND “fun” AND without “quick”
   - `Noovi & search & fast & !(slow | sluggish)` should return tweets with “Noovi” AND “search” AND “fast” but neither slow nor sluggish.
3. All queries as `CASE INSENSITIVE` ( “hello” should match “HeLLo”)
4. Recent tweet's timestamps are ordered in ascending order (1, 2, 3...)

## Complexity analysis vs starter code

---

My code: O(n log n) to sort the final tweets query in ascending order

Starter code: O(m \* n)

- m = search list of tweets
- n = search query string

## Project Breakdown

---

1. `& (ampersand)` means `logical AND` (both the word/expression to the left and right
   must exist in the resulting tweet
2. `| = (pipe)` means `logical OR` (either the word/expression to the left or the right
   must be in the resulting tweet, or both)
3. `! (exclamation point) means logical NOT` (the returned tweets should NOT
   contain the following word/expression following this operator)
4. `Spaces` in the query will just exist to separate out words and operators from one
   another

## Examples

---

Query: `Noovi & rocks`

- Could return tweets like:
  - **Noovi rocks**
  - **Noovi discovered rare rocks on mars**
- Wouldn't return tweets like:
  - **Noovi is a rocketship**
  - **Noovi was founded by rockstars**

Query: `Noovi & is & (interesting | exciting) & !boring`

- Could return tweets like:
  - **Fixing Noovi tweet search is an interesting problem**
- Wouldn’t return tweets like:
  - **The work at Noovi is exciting and never boring**

Query: `Noovi & search & ((works & great) | (needs & improvement))`

- Could return tweets like:
  - **Noovi has great search that actually works**
  - **I just tried Noovi tweet search and it needs a lot of improvement**
- Wouldn’t return tweets like:
  - **Noovi search is great**
  - **Noovi search needs more great people to work on it**
