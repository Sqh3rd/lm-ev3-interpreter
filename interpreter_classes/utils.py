class Utils:
    def string_contains_only(string, l):
        for s in ''.join(set(string)):
            if not s in l:
                return False
        return True