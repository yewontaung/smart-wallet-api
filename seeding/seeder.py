from sqlmodel import Session, select

from app.data.database import engine
from app.data.enums import (
    BusinessApprovalStatus,
    BusinessStatus,
    BusinessType,
    ManagerRole,
    TransactionStatus,
    TransactionType,
    UserType,
    WalletType,
    WalletUserStatus,
    WalletUserType,
)
from app.data.meta_models import District, Township
from app.data.models import (
    Account,
    Address,
    BusinessApprovalRequest,
    BusinessProfile,
    ChatMessage,
    CustomerSupportChat,
    ManagerAccount,
    NRC,
    Transaction,
    TransactionLog,
    Wallet,
    WalletOperation,
    WalletUserAccount,
)
from app.utils import env
from app.utils.hashing import hash_password

hashed_password = hash_password(env.DEMO_PASSWORD)

def seed_database():
    with Session(engine) as session:

        # Prevent duplicate seeding
        if session.exec(select(Account)).first():
            print("Database already contains data.")
            print("Skipping seed.")
            return

        # =========================================================
        # DISTRICTS
        # =========================================================

        yangon = District(
            district_name="Yangon",
        )

        mandalay = District(
            district_name="Mandalay",
        )

        naypyitaw = District(
            district_name="Naypyitaw",
        )

        session.add_all([
            yangon,
            mandalay,
            naypyitaw,
        ])
        session.flush()

        # =========================================================
        # TOWNSHIPS
        # =========================================================

        townships = [
            Township(
                township_name="Kamaryut",
                district_id=yangon.district_id,
            ),
            Township(
                township_name="Hlaing",
                district_id=yangon.district_id,
            ),
            Township(
                township_name="Sanchaung",
                district_id=yangon.district_id,
            ),
            Township(
                township_name="Aungmyaythazan",
                district_id=mandalay.district_id,
            ),
            Township(
                township_name="Chanayethazan",
                district_id=mandalay.district_id,
            ),
            Township(
                township_name="Zabuthiri",
                district_id=naypyitaw.district_id,
            ),
        ]

        session.add_all(townships)
        session.flush()

        kamaryut = townships[0]
        hlaing = townships[1]
        sanchaung = townships[2]

        # =========================================================
        # ACCOUNTS
        # =========================================================

        super_admin = Account(
            full_name="Super Administrator",
            user_type=UserType.MANAGER,
        )

        admin = Account(
            full_name="System Administrator",
            user_type=UserType.MANAGER,
        )

        moderator = Account(
            full_name="Support Moderator",
            user_type=UserType.MANAGER,
        )

        alice = Account(
            full_name="Alice Aung",
            user_type=UserType.WALLET_USER,
        )

        bob = Account(
            full_name="Bob Min",
            user_type=UserType.WALLET_USER,
        )

        charlie = Account(
            full_name="Charlie Win",
            user_type=UserType.WALLET_USER,
        )

        david = Account(
            full_name="David Htet",
            user_type=UserType.WALLET_USER,
        )

        emma = Account(
            full_name="Emma Moe",
            user_type=UserType.WALLET_USER,
        )

        accounts = [
            super_admin,
            admin,
            moderator,
            alice,
            bob,
            charlie,
            david,
            emma,
        ]

        session.add_all(accounts)
        session.flush()

        # =========================================================
        # NRC
        # =========================================================

        nrcs = [
            NRC(
                district_code="12",
                township_code="KMY",
                nrc_type="N",
                nrc_no="123456",
                account_id=super_admin.account_id,
            ),
            NRC(
                district_code="12",
                township_code="HLN",
                nrc_type="N",
                nrc_no="234567",
                account_id=admin.account_id,
            ),
            NRC(
                district_code="12",
                township_code="SCN",
                nrc_type="N",
                nrc_no="345678",
                account_id=moderator.account_id,
            ),
            NRC(
                district_code="12",
                township_code="KMY",
                nrc_type="N",
                nrc_no="456789",
                account_id=alice.account_id,
            ),
            NRC(
                district_code="12",
                township_code="HLN",
                nrc_type="N",
                nrc_no="567890",
                account_id=bob.account_id,
            ),
            NRC(
                district_code="12",
                township_code="SCN",
                nrc_type="N",
                nrc_no="678901",
                account_id=charlie.account_id,
            ),
            NRC(
                district_code="12",
                township_code="KMY",
                nrc_type="N",
                nrc_no="789012",
                account_id=david.account_id,
            ),
            NRC(
                district_code="12",
                township_code="HLN",
                nrc_type="N",
                nrc_no="890123",
                account_id=emma.account_id,
            ),
        ]

        session.add_all(nrcs)

        # =========================================================
        # ADDRESSES
        # =========================================================

        addresses = [
            Address(
                address_content="No. 10, University Road",
                township_id=kamaryut.township_id,
                account_id=super_admin.account_id,
            ),
            Address(
                address_content="No. 25, Insein Road",
                township_id=hlaing.township_id,
                account_id=admin.account_id,
            ),
            Address(
                address_content="No. 31, Pyay Road",
                township_id=sanchaung.township_id,
                account_id=moderator.account_id,
            ),
            Address(
                address_content="No. 42, Baho Road",
                township_id=kamaryut.township_id,
                account_id=alice.account_id,
            ),
            Address(
                address_content="No. 55, Hledan Road",
                township_id=hlaing.township_id,
                account_id=bob.account_id,
            ),
            Address(
                address_content="No. 17, Dhamma Road",
                township_id=sanchaung.township_id,
                account_id=charlie.account_id,
            ),
            Address(
                address_content="No. 81, Yangon Avenue",
                township_id=kamaryut.township_id,
                account_id=david.account_id,
            ),
            Address(
                address_content="No. 93, Hlaing Road",
                township_id=hlaing.township_id,
                account_id=emma.account_id,
            ),
        ]

        session.add_all(addresses)
        session.flush()

        # =========================================================
        # MANAGER ACCOUNTS
        # =========================================================

        manager_accounts = [
            ManagerAccount(
                account_id=super_admin.account_id,
                phone_no="09111111111",
                account_email="superadmin@example.com",
                hashed_password=hashed_password,
                role=ManagerRole.SUPER_ADMIN,
            ),
            ManagerAccount(
                account_id=admin.account_id,
                phone_no="09222222222",
                account_email="admin@example.com",
                hashed_password=hashed_password,
                role=ManagerRole.ADMIN,
            ),
            ManagerAccount(
                account_id=moderator.account_id,
                phone_no="09333333333",
                account_email="moderator@example.com",
                hashed_password=hashed_password,
                role=ManagerRole.MODERATOR,
            ),
        ]

        session.add_all(manager_accounts)
        session.flush()

        # =========================================================
        # WALLET USER ACCOUNTS
        # =========================================================

        wallet_users = [
            WalletUserAccount(
                account_id=alice.account_id,
                phone_no="09411111111",
                pin="1234",
                nick_name="Alice",
                account_type=WalletUserType.SPECIAL,
                account_status=WalletUserStatus.VERIFIED,
                approved_by=super_admin.account_id,
            ),
            WalletUserAccount(
                account_id=bob.account_id,
                phone_no="09422222222",
                pin="1234",
                nick_name="Bob",
                account_type=WalletUserType.NORMAL,
                account_status=WalletUserStatus.VERIFIED,
                approved_by=admin.account_id,
            ),
            WalletUserAccount(
                account_id=charlie.account_id,
                phone_no="09433333333",
                pin="1234",
                nick_name="Charlie",
                account_type=WalletUserType.NORMAL,
                account_status=WalletUserStatus.VERIFIED,
                approved_by=admin.account_id,
            ),
            WalletUserAccount(
                account_id=david.account_id,
                phone_no="09444444444",
                pin="1234",
                nick_name="David",
                account_type=WalletUserType.SPECIAL,
                account_status=WalletUserStatus.VERIFIED,
                approved_by=super_admin.account_id,
            ),
            WalletUserAccount(
                account_id=emma.account_id,
                phone_no="09455555555",
                pin="1234",
                nick_name="Emma",
                account_type=WalletUserType.NORMAL,
                account_status=WalletUserStatus.PENDING,
                approved_by=None,
            ),
        ]

        session.add_all(wallet_users)
        session.flush()

        # =========================================================
        # WALLETS
        # =========================================================

        wallets = [
            Wallet(
                wallet_type=WalletType.FUNDING,
                current_balance=150000,
                last_balance=150000,
                version=1,
                wallet_account_id=alice.account_id,
                approved_by=super_admin.account_id,
            ),
            Wallet(
                wallet_type=WalletType.FUNDING,
                current_balance=85000,
                last_balance=85000,
                version=1,
                wallet_account_id=bob.account_id,
                approved_by=admin.account_id,
            ),
            Wallet(
                wallet_type=WalletType.FUNDING,
                current_balance=50000,
                last_balance=50000,
                version=1,
                wallet_account_id=charlie.account_id,
                approved_by=admin.account_id,
            ),
            Wallet(
                wallet_type=WalletType.FUNDING,
                current_balance=250000,
                last_balance=250000,
                version=1,
                wallet_account_id=david.account_id,
                approved_by=super_admin.account_id,
            ),
            Wallet(
                wallet_type=WalletType.FUNDING,
                current_balance=0,
                last_balance=0,
                version=0,
                wallet_account_id=emma.account_id,
                approved_by=None,
            ),
        ]

        session.add_all(wallets)
        session.flush()

        alice_wallet = wallets[0]
        bob_wallet = wallets[1]
        charlie_wallet = wallets[2]
        david_wallet = wallets[3]
        emma_wallet = wallets[4]

        # =========================================================
        # WALLET OPERATIONS
        # =========================================================

        operations = [
            WalletOperation(operation_name="Wallet Deposit"),
            WalletOperation(operation_name="Wallet Withdrawal"),
            WalletOperation(operation_name="Wallet Transfer"),
            WalletOperation(operation_name="Mobile Top Up"),
            WalletOperation(operation_name="Business Payment"),
        ]

        session.add_all(operations)
        session.flush()

        deposit_operation = operations[0]
        transfer_operation = operations[2]
        topup_operation = operations[3]
        business_payment_operation = operations[4]

        # =========================================================
        # TRANSACTIONS
        # =========================================================

        transactions = [
            Transaction(
                amount=100000,
                status=TransactionStatus.COMPLETED,
                note="Initial wallet deposit",
                operation_id=deposit_operation.operation_id,
                receiver_wallet_id=alice_wallet.wallet_id,
                sender_wallet_id=alice_wallet.wallet_id,
            ),
            Transaction(
                amount=25000,
                status=TransactionStatus.COMPLETED,
                note="Transfer to Bob",
                operation_id=transfer_operation.operation_id,
                receiver_wallet_id=bob_wallet.wallet_id,
                sender_wallet_id=alice_wallet.wallet_id,
            ),
            Transaction(
                amount=10000,
                status=TransactionStatus.PENDING,
                note="Pending transfer to Charlie",
                operation_id=transfer_operation.operation_id,
                receiver_wallet_id=charlie_wallet.wallet_id,
                sender_wallet_id=alice_wallet.wallet_id,
            ),
            Transaction(
                amount=15000,
                status=TransactionStatus.FAILED,
                note="Failed mobile top up",
                operation_id=topup_operation.operation_id,
                receiver_wallet_id=bob_wallet.wallet_id,
                sender_wallet_id=bob_wallet.wallet_id,
            ),
            Transaction(
                amount=50000,
                status=TransactionStatus.COMPLETED,
                note="Business payment",
                operation_id=business_payment_operation.operation_id,
                receiver_wallet_id=charlie_wallet.wallet_id,
                sender_wallet_id=david_wallet.wallet_id,
            ),
        ]

        session.add_all(transactions)
        session.flush()

        # =========================================================
        # TRANSACTION LOGS
        # =========================================================

        logs = [
            TransactionLog(
                trx_type=TransactionType.IN,
                wallet_id=alice_wallet.wallet_id,
                trx_id=transactions[0].trx_id,
            ),
            TransactionLog(
                trx_type=TransactionType.OUT,
                wallet_id=alice_wallet.wallet_id,
                trx_id=transactions[1].trx_id,
            ),
            TransactionLog(
                trx_type=TransactionType.IN,
                wallet_id=bob_wallet.wallet_id,
                trx_id=transactions[1].trx_id,
            ),
            TransactionLog(
                trx_type=TransactionType.OUT,
                wallet_id=alice_wallet.wallet_id,
                trx_id=transactions[2].trx_id,
            ),
            TransactionLog(
                trx_type=TransactionType.IN,
                wallet_id=charlie_wallet.wallet_id,
                trx_id=transactions[2].trx_id,
            ),
            TransactionLog(
                trx_type=TransactionType.OUT,
                wallet_id=david_wallet.wallet_id,
                trx_id=transactions[4].trx_id,
            ),
            TransactionLog(
                trx_type=TransactionType.IN,
                wallet_id=charlie_wallet.wallet_id,
                trx_id=transactions[4].trx_id,
            ),
        ]

        session.add_all(logs)

        # =========================================================
        # BUSINESS APPROVAL REQUESTS
        # =========================================================

        approval_requests = [
            BusinessApprovalRequest(
                qualified_name="Alice Fashion Store",
                description="Online fashion and clothing store.",
                business_type=BusinessType.STANDALONE,
                status=BusinessApprovalStatus.PENDING,
                owner_id=alice.account_id,
                updated_by=None,
            ),
            BusinessApprovalRequest(
                qualified_name="Bob Electronics",
                description="Consumer electronics and accessories.",
                business_type=BusinessType.STANDALONE,
                status=BusinessApprovalStatus.UNDER_REVIEW,
                remark="Documents are being reviewed.",
                owner_id=bob.account_id,
                updated_by=admin.account_id,
            ),
            BusinessApprovalRequest(
                qualified_name="David Holdings",
                description="Small business organization.",
                business_type=BusinessType.ORGANIZATION,
                status=BusinessApprovalStatus.REJECTED,
                remark="Additional documents required.",
                owner_id=david.account_id,
                updated_by=moderator.account_id,
            ),
        ]

        session.add_all(approval_requests)

        # =========================================================
        # BUSINESS PROFILES
        # =========================================================

        businesses = [
            BusinessProfile(
                qualified_name="Charlie Cafe",
                description="Local coffee and food business.",
                business_type=BusinessType.STANDALONE,
                status=BusinessStatus.OPEN,
                owner_id=charlie.account_id,
                approved_by=admin.account_id,
            ),
            BusinessProfile(
                qualified_name="David Digital",
                description="Digital products and services.",
                business_type=BusinessType.ORGANIZATION,
                status=BusinessStatus.OPEN,
                owner_id=david.account_id,
                approved_by=super_admin.account_id,
            ),
            BusinessProfile(
                qualified_name="Alice Old Store",
                description="Old demo business.",
                business_type=BusinessType.STANDALONE,
                status=BusinessStatus.CLOSED,
                owner_id=alice.account_id,
                approved_by=admin.account_id,
            ),
        ]

        session.add_all(businesses)

        # =========================================================
        # CUSTOMER SUPPORT CHATS
        # =========================================================

        chats = [
            CustomerSupportChat(chat_id=alice.account_id),
            CustomerSupportChat(chat_id=bob.account_id),
            CustomerSupportChat(chat_id=charlie.account_id),
        ]

        session.add_all(chats)
        session.flush()

        # =========================================================
        # CHAT MESSAGES
        # =========================================================

        messages = [
            ChatMessage(
                message_content="Hello, I need help with my wallet.",
                is_read=True,
                account_id=alice.account_id,
                support_chat_id=alice.account_id,
            ),
            ChatMessage(
                message_content="Sure. How can we help you?",
                is_read=True,
                account_id=moderator.account_id,
                support_chat_id=alice.account_id,
            ),
            ChatMessage(
                message_content="My transfer is still pending.",
                is_read=False,
                account_id=bob.account_id,
                support_chat_id=bob.account_id,
            ),
            ChatMessage(
                message_content="Can you check my business account?",
                is_read=False,
                account_id=charlie.account_id,
                support_chat_id=charlie.account_id,
            ),
        ]

        session.add_all(messages)

        # =========================================================
        # COMMIT
        # =========================================================

        session.commit()

        print("==========================================")
        print(" Database seeding completed successfully ")
        print("==========================================")
        print()
        print("Manager accounts:")
        print("  superadmin@example.com")
        print("  admin@example.com")
        print("  moderator@example.com")
        print()
        print("Wallet users:")
        print("  09411111111 - Alice")
        print("  09422222222 - Bob")
        print("  09433333333 - Charlie")
        print("  09444444444 - David")
        print("  09455555555 - Emma")
        print()
        print("Demo PIN: 1234")


if __name__ == "__main__":
    seed_database()
