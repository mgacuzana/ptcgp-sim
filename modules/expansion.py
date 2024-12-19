class Expansion:
    def __init__(self, name="Dummy Expansion", set_code="xxx", packs=[]):
        self.name = name
        self.set_code = set_code
        self.packs = packs

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        names = [p.name for p in self.packs]
        return f"{self.name} ({self.set_code}) containing {names}"