"""
A login management system that uses an open addressing hash table.
"""
class LoginManager:
    # A space is empty if it has never had a value.
    EMPTY = -1
    # A space is removed if it previously had a value,
    # but it has since been deleted.
    REMOVED = -2

    """
    Constructor for the LoginManager class.
    """
    def __init__(self, length, max_load_factor=0.7):
        self.table = length * [self.EMPTY]
        self.num_users = 0
        self.max_load_factor = max_load_factor

    """
    Hash function that uses the length of the key.
    """
    def hash_func(self, key):
        return len(key) % len(self.table)

    """
    Resizes the table to be twice the size that it previously was.
    """
    def resize_table(self):
        return

    """
    Register a new username and password combination by adding them to the table.
        Returns True if the user was able to be registered and added to the table.
        Returns False if the table is full or if the user already exists.
    """
    def register_user(self, username, password):
        return False

    """
    Deletes a user from the system by removing them from the table.
        Returns True if the user was removed from the table.
        Returns false if the user was not found in the table.
    """
    def delete_user(self, username):
        i = self.hash_func(username)
        num_checked = 0
        while num_checked < len(self.table) and self.table[i] != self.EMPTY and \
                (self.table[i] == self.REMOVED or self.table[i][0] != username):
            i = (i + 1) % len(self.table)
            num_checked += 1

        if num_checked >= len(self.table) or self.table[i] == self.EMPTY:
            # User was not found in the table.
            return False

        # Remove this user from the table.
        self.table[i] = self.REMOVED
        self.num_users -= 1
        return True

    """
    Checks whether a user can log into the system using the given username and password.
        Returns True if the given (username, password) combination exists.
        Returns False if the given user cannot be found or if the password is incorrect.
    """
    def login(self, username, password):
        return False

    """
    Merges two old accounts into a new account.
        Returns True if the two accounts were successfully replaced by the new account.
        Returns False if the two accounts could not be replaced by the new account.
        old_account1 is a (username, password) tuple.
        old_account2 is a (username, password) tuple.
        new_account is a (username, password) tuple.
    """
    def merge_accounts(self, old_account1, old_account2, new_account):
        return False

    def skip3_probe():
        return [
            # initial iteration:
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            # next iteration here:
            [ ],
        ]
