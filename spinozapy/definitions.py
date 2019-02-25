class ImmutableError(Exception):
    pass


class Substance():

    class __God:
        """Spinoza's choice of word. Equivalent to 'all'."""
        def __init__(self):
            self.existant = True
            self._immutable_attributes = ['exists', 'existant']

        @property
        def exists(self):
            return self.existant

    instance = None

    def __init__(self):
        if not Substance.instance:
            Substance.instance = Substance.__God()
        self._immutable_attributes.append('instance')

    def __setattr__(self, name, value):
        if name in self._immutable_attributes:
            raise ImmutableError(f"Attribute `{name}` is immutable.")

    def __getattr__(self, name):
        return getattr(self.instance, name)


# UNIT TESTS ###############################################################################
permanent_thing = Substance()
assert permanent_thing.exists

permanent_thing2 = Substance()
assert permanent_thing2.exists

assert permanent_thing.instance is permanent_thing2.instance

try:
    permanent_thing.exists = False
except ImmutableError:
    pass
else:
    raise AssertionError("Substance is permanent, and can neither be created or destroyed.")

try:
    permanent_thing.existant = False
except ImmutableError:
    pass
else:
    raise AssertionError("Substance is permanent, and can neither be created or destroyed.")

try:
    permanent_thing.instance = True
except ImmutableError:
    pass
else:
    raise AssertionError("Substance is permanent, and can neither be created or destroyed.")
# /UNIT TESTS ###############################################################################


