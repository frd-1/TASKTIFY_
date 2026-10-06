import random
from features.easter_egg.model import Verse


class VerseRepository:
    """Data repository for Easter Egg Bible verses."""

    STATIC_VERSES = [
        Verse("I can do all things through Christ which strengthens me.", "Philippians 4:13"),
        Verse("For I know the plans I have for you,” declares the Lord, “plans to prosper you and not to harm you, plans to give you hope and a future.", "Jeremiah 29:11"),
        Verse("Trust in the LORD with all thine heart; and lean not unto thine own understanding.", "Proverbs 3:5"),
        Verse("Therefore do not be anxious about tomorrow, for tomorrow will be anxious for itself.", "Matthew 6:34"),
        Verse("Let us not become weary in doing good, for at the proper time we will reap a harvest if we do not give up.", "Galatians 6:9"),
        Verse("Commit thy works unto the LORD, and thy thoughts shall be established.", "Proverbs 16:3"),
        Verse("Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.", "Joshua 1:9"),
    ]

    def get_random_verse(self):
        return random.choice(self.STATIC_VERSES)