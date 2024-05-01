# All the view modules
from windows.new_transaction import TransactionWindow
from windows.table import TableWindow
from windows.update_transaction import UpdateTransactionWindow
from windows.update_balance import UpdateBalanceWindow
from windows.graphs import GraphWindow
from windows.budget import BudgetWindow
from windows.reminder import ReminderMenu

# Collector class, just to simplify the Window Class file
class All(TransactionWindow,TableWindow,UpdateTransactionWindow,UpdateBalanceWindow,GraphWindow,BudgetWindow,ReminderMenu):
    pass