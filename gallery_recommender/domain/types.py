from enum import StrEnum


class DataCategory(StrEnum):
    # the categories of data that can be stored in the database
    PROMPT = "prompt"
    QUERIES = "queries"

    
    GALLERY = "gallery"
    EXHIBITION = "exhibition"
    USER = "user"
    REFLECTION = "reflection"
