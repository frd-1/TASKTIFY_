from features.easter_egg.repository import VerseRepository


class VerseService:
    """Business logic service for Easter Egg feature."""

    def __init__(self, repository: VerseRepository = None):
        self.repository = repository or VerseRepository()

    def get_random_verse(self):
        return self.repository.get_random_verse()