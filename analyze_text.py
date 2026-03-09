# analyze_text.py
# Part D - AI-Augmented Task
# Improved version after critically evaluating the AI-generated code

# -----------------------------------------------
# STEP 1 - My exact prompt to Claude:
# "Write a Python module with a function called analyze_text(text: str, **options)
#  that accepts any text and keyword arguments for options
#  (count_words=True, count_sentences=True, find_longest_word=True,
#   sentiment_simple=True). Each option enables a different analysis.
#  Use *args and **kwargs, add type hints and Google-style docstrings.
#  Return a dict with all requested analyses."
# -----------------------------------------------

# -----------------------------------------------
# STEP 2 - AI's output (pasted below as-is):
# -----------------------------------------------

def analyze_text_AI_version(text: str, **options) -> dict:
    """Analyze text based on provided options.

    Args:
        text: The input text to analyze.
        **options: Keyword arguments to enable specific analyses.
            count_words (bool): Count total words. Defaults to True.
            count_sentences (bool): Count sentences. Defaults to True.
            find_longest_word (bool): Find the longest word. Defaults to True.
            sentiment_simple (bool): Simple positive/negative sentiment. Defaults to True.

    Returns:
        dict: A dictionary with results of enabled analyses.
    """
    results = {}

    if not text:
        return results

    if options.get('count_words', True):
        results['word_count'] = len(text.split())

    if options.get('count_sentences', True):
        results['sentence_count'] = text.count('.') + text.count('!') + text.count('?')

    if options.get('find_longest_word', True):
        words = text.split()
        results['longest_word'] = max(words, key=len) if words else ''

    if options.get('sentiment_simple', True):
        positive_words = ['good', 'great', 'excellent', 'happy', 'love', 'best', 'wonderful']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'sad']
        lower_text = text.lower()
        pos_count = sum(lower_text.count(w) for w in positive_words)
        neg_count = sum(lower_text.count(w) for w in negative_words)
        if pos_count > neg_count:
            results['sentiment'] = 'positive'
        elif neg_count > pos_count:
            results['sentiment'] = 'negative'
        else:
            results['sentiment'] = 'neutral'

    return results


# -----------------------------------------------
# STEP 3 - Critical Evaluation:
#
# 1. Does it properly use **kwargs?
#    - Yes, options are passed as **kwargs. But the function defaults all options to True,
#      meaning everything runs even if the caller passes nothing. Should default to False
#      so only explicitly requested analyses run.
#
# 2. Are type hints correct?
#    - Mostly yes. Return type dict is correct. But dict[str, Any] would be more precise.
#
# 3. Does it handle edge cases?
#    - Handles empty text but returns an empty dict without any message.
#    - Doesn't handle None input - will crash on text.split() if text=None.
#
# 4. Is the docstring actually useful?
#    - It's decent but a bit boilerplate. The Args section is okay.
#    - Could mention what the returned dict keys will be.
#
# 5. Does it follow Single Responsibility Principle?
#    - No. One function is doing 4 different things. Better to split each
#      analysis into its own helper function and call from analyze_text.
# -----------------------------------------------


# -----------------------------------------------
# STEP 4 - My improved version (split into helpers)
# -----------------------------------------------

def _count_words(text: str) -> int:
    """Count the number of words in text.

    Args:
        text: Input string.

    Returns:
        Word count as integer.
    """
    return len(text.split())


def _count_sentences(text: str) -> int:
    """Count the number of sentences using punctuation (.!?).

    Args:
        text: Input string.

    Returns:
        Sentence count as integer.
    """
    return sum(text.count(p) for p in ['.', '!', '?'])


def _find_longest_word(text: str) -> str:
    """Find the longest word in the text.

    Args:
        text: Input string.

    Returns:
        The longest word as a string. Returns '' if text is empty.
    """
    words = text.split()
    return max(words, key=len) if words else ''


def _simple_sentiment(text: str) -> str:
    """Determine a simple positive/negative/neutral sentiment.

    Uses a small fixed vocabulary. Not ML-based, just a quick indicator.

    Args:
        text: Input string.

    Returns:
        One of: 'positive', 'negative', 'neutral'.
    """
    POSITIVE_WORDS = ['good', 'great', 'excellent', 'happy', 'love', 'best', 'wonderful', 'amazing']
    NEGATIVE_WORDS = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'sad', 'disgusting']

    lower = text.lower()
    pos = sum(lower.count(w) for w in POSITIVE_WORDS)
    neg = sum(lower.count(w) for w in NEGATIVE_WORDS)

    if pos > neg:
        return 'positive'
    elif neg > pos:
        return 'negative'
    return 'neutral'


def analyze_text(text: str, **options) -> dict:
    """Analyze text and return results for each enabled option.

    Each analysis must be explicitly enabled by passing the option as True.
    Nothing runs by default - you get back only what you asked for.

    Args:
        text: The input text to analyze. Must be a non-empty string.
        **options: Keyword arguments enabling specific analyses:
            count_words (bool): Include word count in result.
            count_sentences (bool): Include sentence count in result.
            find_longest_word (bool): Include longest word in result.
            sentiment_simple (bool): Include simple sentiment in result.

    Returns:
        dict: Keys are analysis names, values are the computed results.
              Returns {'error': 'Empty text provided'} if text is empty or None.

    Examples:
        >>> analyze_text("Python is great!", count_words=True, sentiment_simple=True)
        {'word_count': 3, 'sentiment': 'positive'}
    """
    if not text or not text.strip():
        return {'error': 'Empty text provided'}

    results = {}

    if options.get('count_words'):
        results['word_count'] = _count_words(text)

    if options.get('count_sentences'):
        results['sentence_count'] = _count_sentences(text)

    if options.get('find_longest_word'):
        results['longest_word'] = _find_longest_word(text)

    if options.get('sentiment_simple'):
        results['sentiment'] = _simple_sentiment(text)

    return results


# -----------------------------------------------
# Demo
# -----------------------------------------------

if __name__ == "__main__":
    sample = "Python is a great language. I love programming! It is wonderful."

    print("=== AI version (all options default True) ===")
    print(analyze_text_AI_version(sample))

    print("\n=== My improved version (explicit options) ===")
    print(analyze_text(sample, count_words=True, sentiment_simple=True))
    print(analyze_text(sample, count_words=True, count_sentences=True,
                       find_longest_word=True, sentiment_simple=True))

    print("\n=== Edge cases ===")
    print(analyze_text(""))          # should return error
    print(analyze_text("   "))       # blank string
    print(analyze_text("Hello"))     # no options - returns empty dict
