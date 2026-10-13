from features.easter_egg.repository import VerseRepository


class VerseService:
    # Handles the logic for getting a Bible verse
    def __init__(self, repository=None):
        # Use the given repository or create a new one
        self.repository = repository or VerseRepository()

    # Gets a random Bible verse from the repository
    def get_random_verse(self):
        return self.repository.get_random_verse()

