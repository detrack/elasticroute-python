import warnings


class NonStringKeyUsed(UserWarning):
    message = "WARNING: You tried to use non-string keys to access data members of this object. Keys are always converted to string in any data member access operation (using []), so this may have unexpected effects especially if you accidentally pass in a list or dictionary as the key. You might want to revise your code to ensure you only pass in strings."

    def __str__(self):
        return self.message
    pass
