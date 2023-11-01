import unittest
import io
import sys
from login_manager import LoginManager

class TestLoginManager(unittest.TestCase):
    def setUp(self):
        self.manager = LoginManager(11)

    def test_register_user_no_collision(self):
        self.manager.register_user('kibo', 'climbKibo123')
        self.assertEqual(self.manager.table, [-1, -1, -1, -1, ('kibo', 'climbKibo123'), -1, -1, -1, -1, -1, -1])
        self.assertEqual(self.manager.num_users, 1)

    def test_register_user_collision(self):
        self.manager.register_user('kibo', 'climbKibo123')
        self.manager.register_user('user', 'passwd')
        self.assertEqual(self.manager.table, [-1, -1, -1, -1, ('kibo', 'climbKibo123'), ('user', 'passwd'), -1, -1, -1, -1, -1])
        self.assertEqual(self.manager.num_users, 2)

    def test_register_user_collision_first_removed(self):
        self.manager.table = [-1, -1, -1, -1, ('kibo', 'climbKibo123'), -2, ('user', 'passwd'), -1, -1, -1, -1]
        self.manager.num_users = 2
        self.manager.register_user('quad', 'passwd')
        self.assertEqual(self.manager.table, [-1, -1, -1, -1, ('kibo', 'climbKibo123'), ('quad', 'passwd'), ('user', 'passwd'), -1, -1, -1, -1])
        self.assertEqual(self.manager.num_users, 3)

    def test_register_user_collision_first_removed_retval(self):
        self.manager.table = [-1, -1, -1, -1, ('kibo', 'climbKibo123'), -2, ('user', 'passwd'), -1, -1, -1, -1]
        self.manager.num_users = 2
        self.assertEqual(self.manager.register_user('quad', 'passwd'), True)

    def test_register_user_collision_skip_first_removed(self):
        self.manager.table = [-1, -1, -1, -1, ('kibo', 'climbKibo123'), -2, ('user', 'passwd'), ('quad', 'passwd'), -1, -1, -1]
        self.manager.num_users = 3
        self.manager.register_user('quad', 'passwd')
        self.assertEqual(self.manager.table, [-1, -1, -1, -1, ('kibo', 'climbKibo123'), -2, ('user', 'passwd'), ('quad', 'passwd'), -1, -1, -1])
        self.assertEqual(self.manager.num_users, 3)

    def test_register_user_collision_skip_first_removed_retval(self):
        self.manager.table = [-1, -1, -1, -1, ('kibo', 'climbKibo123'), -2, ('user', 'passwd'), ('quad', 'passwd'), -1, -1, -1]
        self.manager.num_users = 3
        self.assertEqual(self.manager.register_user('quad', 'passwd'), False)

    def test_delete_user_no_collision(self):
        self.manager.table = [-1, -1, -1, -1, ('kibo', 'climbKibo123'), ('user', 'passwd'), -1, -1, -1, -1, -1]
        self.manager.num_users = 2
        self.manager.delete_user('kibo')
        self.assertEqual(self.manager.table, [-1, -1, -1, -1, -2, ('user', 'passwd'), -1, -1, -1, -1, -1])
        self.assertEqual(self.manager.num_users, 1)

    def test_delete_user_collision(self):
        self.manager.table = [-1, -1, -1, -1, ('kibo', 'climbKibo123'), ('user', 'passwd'), -1, -1, -1, -1, -1]
        self.manager.num_users = 2
        self.manager.delete_user('user')
        self.assertEqual(self.manager.table, [-1, -1, -1, -1, ('kibo', 'climbKibo123'), -2, -1, -1, -1, -1, -1])
        self.assertEqual(self.manager.num_users, 1)

    def test_delete_user_both(self):
        self.manager.table = [-1, -1, -1, -1, ('kibo', 'climbKibo123'), ('user', 'passwd'), -1, -1, -1, -1, -1]
        self.manager.num_users = 2
        self.manager.delete_user('kibo')
        self.assertEqual(self.manager.table, [-1, -1, -1, -1, -2, ('user', 'passwd'), -1, -1, -1, -1, -1])
        self.manager.delete_user('user')
        self.assertEqual(self.manager.table, [-1, -1, -1, -1, -2, -2, -1, -1, -1, -1, -1])
        self.assertEqual(self.manager.num_users, 0)

    def test_login_valid(self):
        self.manager.table = [-1, -1, -1, -1, ('kibo', 'climbKibo123'), ('user', 'passwd'), -1, -1, -1, -1, -1]
        self.manager.num_users = 2
        self.assertEqual(self.manager.login('kibo', 'climbKibo123'), True)

    def test_login_invalid(self):
        self.manager.table = [-1, -1, -1, -1, ('kibo', 'climbKibo123'), ('user', 'passwd'), -1, -1, -1, -1, -1]
        self.manager.num_users = 2
        self.assertEqual(self.manager.login('kibo', 'climbKibo124'), False)

    def test_login_valid_removed(self):
        self.manager.table = [-1, -1, -1, -1, ('kibo', 'climbKibo123'), -2, ('user', 'passwd'), -1, -1, -1, -1]
        self.manager.num_users = 2
        self.assertEqual(self.manager.login('user', 'passwd'), True)

    def test_resize_table_no_change(self):
        self.manager.register_user('1', '1')
        self.manager.register_user('2', '1')
        self.manager.register_user('3', '1')
        self.manager.register_user('4', '1')
        self.manager.register_user('5', '1')
        self.manager.register_user('6', '1')
        self.manager.register_user('7', '1')
        # no change yet
        self.assertEqual(len(self.manager.table), 11)

    def test_resize_table(self):
        self.manager.register_user('1', '1')
        self.manager.register_user('2', '1')
        self.manager.register_user('3', '1')
        self.manager.register_user('4', '1')
        self.manager.register_user('5', '1')
        self.manager.register_user('6', '1')
        self.manager.register_user('7', '1')
        self.manager.register_user('8', '1')
        # now table should be twice the size
        self.assertEqual(len(self.manager.table), 22)

    def test_merge_accounts(self):
        tuple1 = ('kibo', 'climbKibo123')
        tuple2 = ('user', 'passwd')
        self.manager.table = [-1, -1, -1, -1, tuple1, tuple2, -1, -1, -1, -1, -1]
        self.manager.num_users = 2
        ret = self.manager.merge_accounts(tuple1, tuple2, ('new', 'pass'))
        self.assertEqual(ret, True)
        self.assertEqual(self.manager.table, [-1, -1, -1, ('new', 'pass'), -2, -2, -1, -1, -1, -1, -1])
        self.assertEqual(self.manager.num_users, 1)

    def test_merge_accounts_does_not_exist(self):
        tuple1 = ('kibo', 'climbKibo123')
        tuple2 = ('user5', 'passwd')
        self.manager.table = [-1, -1, -1, -1, -1, tuple2, -1, -1, -1, -1, -1]
        self.manager.num_users = 1
        ret = self.manager.merge_accounts(tuple1, tuple2, ('new', 'pass'))
        self.assertEqual(ret, False)
        # no change because old_account1 does not exist
        self.assertEqual(self.manager.table, [-1, -1, -1, -1, -1, tuple2, -1, -1, -1, -1, -1])
        self.assertEqual(self.manager.num_users, 1)
