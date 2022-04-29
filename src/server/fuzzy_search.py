def is_match(pattern, line):
    """Fuzzy search.

    Returns:
        True if pattern is "fuzzy" contained in line
        False otherwise
    """
    if len(pattern) == 0:
        return True

    pattern = pattern.lower()
    line = line.lower()

    pattern_index = 0
    for letter in line:
        if pattern[pattern_index] == letter:
            pattern_index += 1
            if len(pattern) == pattern_index:
                return True

    return False
