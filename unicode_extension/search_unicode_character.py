from rapidfuzz import process, fuzz
from .unicode_character import UnicodeCharacter


def processor_for_extract(data):

    if isinstance(data, UnicodeCharacter):
        return data._string_data_for_search

    if isinstance(data, str):
        return data.upper()

    return data


def search_unicode_character(
    query: str, unicode_character_list: list[UnicodeCharacter], limit: int = 10
) -> list:
    """Search Unicode character

    Using RaidFuzz

    Args:
        query: Query for search
        unicode_character_list: Searching from this list.
        limit: Search result item number.

    Returns:
        List of Tuple. (Result from RapidFuzz)

        [(UnicodeCharacter, score, index), ...]

        `UnicodeCharacter`: UnicodeCharacter
        `score`: Similarity with Query
        `index`: Index from result

    """

    search_result = process.extract(
        query=query,
        choices=unicode_character_list,
        # scorer=scorer_for_extract,
        processor=processor_for_extract,
        score_cutoff=1,  # For cut 0 score result
        limit=limit,
    )

    return search_result
