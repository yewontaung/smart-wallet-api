from enum import Enum


class UserType(str, Enum):
    MANAGER = "Manager"
    WALLET_USER = "Wallet User"

class ManagerRole(str, Enum):
    SUPER_ADMIN = "Super Admin"
    ADMIN = "Admin"
    MODERATOR = "Moderator"

class WalletUserType(str, Enum):
    SPECIAL = "Special"
    NORMAL = "Normal"

class WalletType(str, Enum):
    FUNDING = "Funding"

class TransactionType(str, Enum):
    IN = "Income"
    OUT = "Expense"

class TransactionStatus(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"

class BusinessType(str, Enum):
    STANDALONE = "Standalone"
    ORGANIZATION = "Organization"

class BusinessStatus(str, Enum):
    OPEN = "Open"
    CLOSED = "Closed"