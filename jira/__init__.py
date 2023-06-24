"""Top-level package for Jira."""

__app_name__ = "jira"
__version__ = "0.1.6"
__author__ = "Arash Hatami <info@arash-hatami.ir>"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)
