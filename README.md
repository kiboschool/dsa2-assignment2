# Assignment 2

In this assignment, you will complete a series of exercises with hash tables.

## Your Task

You are given a partial implementation of a `LoginManager` class that uses an open addressing hash table (with linear probing) to implement a login system for an application or website. The login system accepts new user registrations and adds (username, password) combinations to the hash table to keep track of them. It also supports allowing users to log-in to the application, and deleting users from the application.

Read through the provided code to see what you've been given. You'll notice that you're given a constructor, a `hash_func()` method which computes a hash value given a key, and a `delete_user()` method that deletes a username from the hash table.

You will implement the functionality below, which will assess your knowledge of tracing and implementing hash table algorithms.

## Steps to Complete

Complete the following steps to the best of your ability, and with the following guidelines:

* The use of generative AI tools (e.g., ChatGPT) is not permitted.
* You must only use concepts and programming constructs covered in this class or previous Kibo classes.
* The algorithms you write should be as efficient as possible. For example, to find a key in the hash table, you should use a hash function and probe for the key instead of doing a linear search for the table starting from the beginning.

1. Say that we have an initially empty hash table of size n=11. Show the result of hashing the following keys into the table, using a hash function that corresponds to the first letter of each key:

    ```dog, zebra, cat, giraffe, bird, alpaca, alligator, elephant, baboon```

    Resolve any collisions using the skip-3 probing technique discussed in our live class session.

    Implement your answer in the `skip3_probe()` function as a two-dimensional list. The first sublist in the list should be a list of length 11 filled with `-1` values, since no values are yet in the table. You should then add one sublist to the list for every key that is inserted, such as:

    ```python
    def hashing_example():
        return [
            [ -1, -1, -1, -1, -1 ],
            [ 'a key', -1, -1, -1, -1 ],
            [ 'a key', -1, 'another key', -1, -1 ],
            ...
        ]
    ```

2. Implement the `register_user()` method, which accepts a username and password that represents a new user logging-in to the site. The method should find an empty position in the table using the hash function, resolving collisions as needed using linear probing. It should then insert the `(username, password)` as a Python tuple into the first available slot it finds.

    Notes:

    * If the user already exists in the table, the method should return without making any changes.
    * If a new user is able to be successfully added to the table, the method should return `True`. Otherwise, the method should return `False`.
    * Remember that a hash table can contain positions that are *empty* (i.e., have never had a value) as well as positions that are *removed* (i.e., previously had a value, but that value has since been removed). The constants `self.EMPTY` and `self.REMOVED` in `LoginManager` represent these two states. Your method will need to be aware of these states (and the difference between them).
    * This function should correctly maintain the `self.num_users` variable by incrementing it when a new user is successfully added.

3. Implement the `login()` method, which should try to find the given username in the hash table and check whether the given password matches the password that is stored in the table.

    Notes:

    * If the given (username, password) combination exists, the method should return `True`. Otherwise, it should return `False`.
    * Much of the algorithm that you write should be similar to the algorithm from `register_user()`, with some small differences.

4. The `LoginManager` class has an instance variable named `self.max_load_factor`. This variable represents the load factor at which the table will need to be resized. If the load factor of the table ever reaches this value, the table needs to be resized.

    Implement the `resize_table()` method, which resizes the hash table to exactly twice its previous size. Also, modify the `register_user()` method, so that after a new user is successfully added, it checks whether the load factor of the table has reached `self.max_load_factor`, and if so invokes `resize_table()`.

5. Implement the `merge_accounts()` method, which accepts three tuples as input:

    * `old_account1` and `old_account2`, which represent `(username, password)` combinations currently in the table and which will be removed
    * `new_account`, which is a `(username, password)` tuple that will be added to the table.

    The method should remove `old_account1` and `old_account2` from the hash table (as long as the usernames exist; passwords don't need to be checked), and then add `new_account` to the table.

    Notes:

    * If either of the old account usernames don't exist in the table, the method should return without changing the table.
    * If the new account username already exists in the table, the method should return without changing the table.
    * You may find it useful to invoke one or more of the existing methods in `LoginManager`, though doing so is not required.
    * The `self.num_users` variable should be correctly updated in the method.
    * The method should return `True` if two old accounts are successfully removed and the new account is successfully added. Otherwise, it should return `False`.

## Testing

In `test_login_manager.py`, there are unit tests for the above pieces of functionality. Run the tests to check your code.

When you upload your submission to Gradescope, you will see the results for some tests, but there may be other edge cases we test during grading that you are not able to see when you submit. So be sure to test thoroughly!
