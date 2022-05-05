def is_match(pattern, line):
    """Fuzzy search.

    Assumptions:
        pattern is not None
        pattern is lower case
        line is lower case

    Returns:
        indexes (set) of matched indexes
            if pattern is "fuzzy" contained in line
        None otherwise
    """
    indexes = set()

    pattern_index = 0
    for i, letter in enumerate(line):
        if pattern[pattern_index] == letter:
            indexes.add(i)
            pattern_index += 1
            if len(pattern) == pattern_index:
                return indexes

    return None
