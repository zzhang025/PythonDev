from abc import ABC, abstractmethod

class Transaction(ABC):
    def __init__(self, customerId, tellerId):
        self._customerId = customerId
        self._tellerId = tellerId

    def get_customer_id(self):
        return self._customerId

    def get_teller_id(self):
        return self._tellerId

    @abstractmethod
    def get_transaction_description(self):
        pass

class Deposit(Transaction):
    def __init__(self, customerId, tellerId, amount):
        super().__init__(customerId, tellerId)
        self._amount = amount

    def get_transaction_description(self):
        return f'Teller {self.get_teller_id()} deposited {self._amount} to account {self.get_customer_id()}'
    
class Withdraw(Transaction):
    def __init__(self, customerId, tellerId, amount):
        super().__init__(customerId, tellerId)
        self._amount = amount
    
    def get_transaction_description(self):
        return f'Teller {self.get_teller_id()} withdrew {self._amount} from account {self.get_customer_id()}'
    
class OpenAccount(Transaction):
    def __init__(self, customerId, tellerId):
        super().__init__(customerId, tellerId)
    
    def get_transaction_description(self):
        return f'Teller {self.get_teller_id()} opened account {self.get_customer_id()}'

class Transfer(Transaction):
    def __init__(self, customerId, tellerId, targetCustomerId, amount):
        super().__init__(customerId, tellerId)
        self._targetCustomerId = targetCustomerId
        self._amount = amount

    def get_transaction_description(self):
        return f'Teller {self.get_teller_id()} transferred {self._amount} from account {self.get_customer_id()} to account {self._targetCustomerId}'
    
class BankTeller:
    def __int__(self, id):
        self._id = id
    
    def get_id(self):
        return self._id

class BankAccount:
    def __init__(self,customerId, name, balance):
        self._customerId = customerId
        self._name = name
        self._balance = balance
    def get_customer_id(self):
        return self._customerId 
    def get_balance(self):
        return self._balance
    def deposit(self, amount):
        self._balance += amount
    def withdraw(self, amount):
        if self._balance < amount:
            return False
        else:
            self._balance -= amount
            return True

class BankSystem:
    def __init__(self,accounts,transactions):
        self._accounts = accounts
        self._transactions = transactions
    
    def get_account(self, customerId):
        return self._accounts[customerId]

    def get_accounts(self):
        return self._accounts
    
    def get_tranasactions(self):
        return self._transactions

    def open_account(self, customer_name, teller_id):
        customerId = len(self._accounts())
        account = BankAccount(customerId, customer_name, 0)
        self._accounts.append(account)

        #log 
        transaction = OpenAccount(customerId, teller_id)
        self._transactions.append(transaction)
        return customerId
    
    def deposit(self, customer_Id, teller_id, amount):
        account = self.get_account(customer_Id)
        account.deposit(amount)

        transaction = Deposit(customer_Id, teller_id, amount)
        self._transactions.append(transaction)
    
    def withdraw(self, customer_Id, teller_id, amount):
        if amount > self.get_account(customer_Id).get_balance():
            raise Exception('Insufficient balance')
        
        account = self.get_account(customer_Id)
        account.withdraw(amount)

        transaction = Withdraw(customer_Id, teller_id, amount)
        self._transactions.append(transaction)
    
    