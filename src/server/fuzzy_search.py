def is_match(pattern, line):
    """Fuzzy search.

    Assumptions:
        pattern is not None
        pattern is lower case
        line is lower case

    Returns:
        True if pattern is "fuzzy" contained in line
        False otherwise
    """
    pattern_index = 0
    for letter in line:
        if pattern[pattern_index] == letter:
            pattern_index += 1
            if len(pattern) == pattern_index:
                return True

    return False
