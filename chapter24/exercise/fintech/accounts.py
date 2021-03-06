from abc import ABCMeta
# Accounts module


class BalanceError(Exception):
    """ The Balance will be invalid """

    def __init__(self, account):
        self.account = account


class AmountError(Exception):

    def __init__(self, account, msg):
        self.account = account
        self.message = msg

    def __str__(self):
        return 'AmountError (' + self.message + ') on ' + str(self.account)


class Transaction:
    """ A Class used to represent an individual Transaction """
    def __init__(self, id, action, amount):
        self.id = id
        self.action = action
        self.amount = amount

    def __str__(self):
        return 'Transaction[' + self.id + " - " + self.action + ': ' + str(self.amount) + ']'


class CurrentAccount(metaclass=ABCMeta):
    """" A class used to represent a type of account """

    @classmethod
    def increment_instance_count(cls):
        print('Creating new Account')
        cls.instance_count += 1

    def __init__(self, account_number, account_holder, opening_balance, overdraft_limit):
        self.account_number = account_number
        self.account_holder = account_holder
        self._balance = opening_balance
        self.overdraft_limit = -overdraft_limit
        # Note need to initialise the history list before you try to add a Transaction
        self.history = []
        self._add_deposit_transaction(opening_balance)
        self.transaction_count = 0

    def get_next_transaction_id(self):
        self.transaction += 1
        return self.transaction

    def __enter__(self):
        print('__enter__')
        return self

    def __exit__(self, *args):
        print('__exit__:', args)
        return True

    # Method called if attribute is unknown
    def __getattr__(self, attribute):
        print('__getattr__: unknown attribute accessed - ', attribute)
        return -1

    # Return the transaction hsitory as the iterable object for an Account
    # and any subclass of Account
    def __iter__(self):
        return iter(self.history)

    # Provide internal support for adding transactions
    # Note by convention methods starting with an '_' shoudl not be called
    # by clients of this class
    def _add_transaction(self, transaction):
        self.history.append(transaction)

    # These are convenience methods to make it easier to
    # record a deposit or withdrawal.
    def _add_deposit_transaction(self, amount):
        self._add_transaction(Transaction(self.get_next_transaction_id(), 'deposit', amount))

    def _add_withdraw_transaction(self, amount):
        self._add_transaction(Transaction(self.get_next_transaction_id(), 'withdraw', amount))

    def deposit(self, amount):
        if amount < 0:
            print('You cannot deposit negative amounts')
            raise AmountError(account=self, msg='Cannot deposit negative amounts')
        else:
            self._balance += amount
            self._add_deposit_transaction(amount)

    def withdraw(self, amount):
        if amount < 0:
            print('You cannot withdraw negative amounts')
            raise AmountError(self, 'Cannot withdraw negative amounts')
        elif self.balance - amount < self.overdraft_limit:
            print('Withdrawal would exceed your overdraft limit')
            raise BalanceError(self)
        else:
            self._balance -= amount
            self._add_withdraw_transaction(amount)

    @property
    def balance(self):
        """ Provides the current balance """
        return self._balance

    def __str__(self):
        return 'Account[' + self.account_number + '] - ' + \
               self.account_holder + ', account = ' + str(self.balance) + \
               'overdraft limit: ' + str(self.overdraft_limit)


