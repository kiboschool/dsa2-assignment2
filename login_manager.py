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
        new_table = LoginManager(2 * len(self.table), self.max_load_factor)
        for entry in self.table:
            if entry == self.EMPTY or entry == self.REMOVED:
                continue
            new_table.register_user(entry[0], entry[1])
        self.table = new_table.table
        self.num_users = new_table.num_users

    """
    Register a new username and password combination by adding them to the table.
        Returns True if the user was able to be registered and added to the table.
        Returns False if the table is full or if the user already exists.
    """
    def register_user(self, username, password):
        i = self.hash_func(username)

        if self.num_users >= len(self.table):
            # Table is full, and user might already exist.
            return False

        removed_spot = -1
        num_checked = 0
        while num_checked < len(self.table) and self.table[i] != self.EMPTY:
            if self.table[i] == self.REMOVED:
                if removed_spot == -1:
                    removed_spot = i
            elif self.table[i][0] == username:
                return False

            i = (i + 1) % len(self.table)
            num_checked += 1

        if self.table[i] == self.EMPTY:
            # This user is not already in the table. Add the user
            # in either the first empty or first removed spot.
            if removed_spot != -1:
                self.table[removed_spot] = (username, password)
            else:
                self.table[i] = (username, password)

            self.num_users += 1

            if self.num_users / len(self.table) > self.max_load_factor:
                self.resize_table()

            return True
        elif num_checked >= len(self.table) and removed_spot != -1:
            self.table[removed_spot] = (username, password)
            self.num_users += 1
            if self.num_users / len(self.table) > self.max_load_factor:
                self.resize_table()
            return True
        else:
            # This case shoulnd't be possible -- we already checked
            # to make sure the table wasn't full, but if we've gotten
            # here it means that we went through the entire table
            # and didn't find any empty or removed spots.
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
        i = self.hash_func(username)
        num_checked = 0
        removed_spot = -1
        while num_checked < len(self.table) and self.table[i] != self.EMPTY:
            if self.table[i] == self.REMOVED or self.table[i][0] != username:
                i = (i + 1) % len(self.table)
                num_checked += 1
            elif self.table[i][0] == username:
                break

        if num_checked >= len(self.table):
            # Checked the whole table and user is not present.
            return False

        if self.table[i] == self.EMPTY:
            # User is not present.
            return False

        # Only let user login if given password matches what's in table.
        return self.table[i][1] == password

    """
    Merges two old accounts into a new account.
        Returns True if the two accounts were successfully replaced by the new account.
        Returns False if the two accounts could not be replaced by the new account.
        old_account1 is a (username, password) tuple.
        old_account2 is a (username, password) tuple.
        new_account is a (username, password) tuple.
    """
    def merge_accounts(self, old_account1, old_account2, new_account):
        old_accounts_found = [False, False]

        i = self.hash_func(old_account1[0])
        num_checked = 0
        while num_checked < len(self.table):
            if self.table[i] == self.EMPTY:
                return False
            elif self.table[i] == self.REMOVED or self.table[i][0] != old_account1[0]:
                i = (i + 1) % len(self.table)
                num_checked += 1
                continue
            else:
                break # found the account

        i = self.hash_func(old_account2[0])
        num_checked = 0
        while num_checked < len(self.table):
            if self.table[i] == self.EMPTY:
                return False
            elif self.table[i] == self.REMOVED or self.table[i][0] != old_account2[0]:
                i = (i + 1) % len(self.table)
                num_checked += 1
                continue
            else:
                break # found the account

        i = self.hash_func(new_account[0])
        num_checked = 0
        while num_checked < len(self.table):
            if self.table[i] == self.EMPTY:
                break
            elif self.table[i] == self.REMOVED or self.table[i][0] != old_account2[0]:
                i = (i + 1) % len(self.table)
                num_checked += 1
                continue
            else:
                return False # new account already exists

        self.delete_user(old_account1[0])
        self.delete_user(old_account2[0])
        self.register_user(new_account[0], new_account[1])
        return True

    def skip3_probe():
        return [
            # initial iteration:
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            # next iteration here:
            [ -1, -1, -1, 'dog', -1, -1, -1, -1, -1, -1, -1],
            [ -1, -1, -1, 'dog', 'zebra', -1, -1, -1, -1, -1, -1],
            [ -1, -1, 'cat', 'dog', 'zebra', -1, -1, -1, -1, -1, -1],
            [ -1, -1, 'cat', 'dog', 'zebra', -1, 'giraffe', -1, -1, -1, -1],
            [ -1, 'bird', 'cat', 'dog', 'zebra', -1, 'giraffe', -1, -1, -1, -1],
            [ 'alpaca', 'bird', 'cat', 'dog', 'zebra', -1, 'giraffe', -1, -1, -1, -1],
            [ 'alpaca', 'bird', 'cat', 'dog', 'zebra', -1, 'giraffe', -1, -1, 'alligator', -1],
            [ 'alpaca', 'bird', 'cat', 'dog', 'zebra', -1, 'giraffe', 'elephant', -1, 'alligator', -1],
            [ 'alpaca', 'bird', 'cat', 'dog', 'zebra', -1, 'giraffe', 'elephant', -1, 'alligator', 'baboon']
        ]
