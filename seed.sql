BEGIN;

-- ============================================================
-- DISTRICTS
-- ============================================================

INSERT INTO district (
    district_id,
    district_name,
    created_at,
    updated_at
)
VALUES
    (1, 'Yangon', NOW(), NOW()),
    (2, 'Mandalay', NOW(), NOW()),
    (3, 'Naypyitaw', NOW(), NOW());


-- ============================================================
-- TOWNSHIPS
-- ============================================================

INSERT INTO township (
    township_id,
    township_name,
    district_id,
    created_at,
    updated_at
)
VALUES
    (1, 'Kamaryut', 1, NOW(), NOW()),
    (2, 'Hlaing', 1, NOW(), NOW()),
    (3, 'Sanchaung', 1, NOW(), NOW()),
    (4, 'Aungmyaythazan', 2, NOW(), NOW()),
    (5, 'Chanayethazan', 2, NOW(), NOW()),
    (6, 'Zabuthiri', 3, NOW(), NOW());


-- ============================================================
-- ACCOUNTS
-- ============================================================

INSERT INTO account (
    account_id,
    full_name,
    user_type,
    profile_url,
    is_disable,
    is_deleted,
    created_at,
    updated_at
)
VALUES
    (1, 'Super Administrator', 'Manager', NULL, FALSE, FALSE, NOW(), NOW()),
    (2, 'System Administrator', 'Manager', NULL, FALSE, FALSE, NOW(), NOW()),
    (3, 'Support Moderator', 'Manager', NULL, FALSE, FALSE, NOW(), NOW()),
    (4, 'Alice Aung', 'Wallet User', NULL, FALSE, FALSE, NOW(), NOW()),
    (5, 'Bob Min', 'Wallet User', NULL, FALSE, FALSE, NOW(), NOW()),
    (6, 'Charlie Win', 'Wallet User', NULL, FALSE, FALSE, NOW(), NOW()),
    (7, 'David Htet', 'Wallet User', NULL, FALSE, FALSE, NOW(), NOW()),
    (8, 'Emma Moe', 'Wallet User', NULL, FALSE, FALSE, NOW(), NOW());


-- ============================================================
-- NRC
-- ============================================================

INSERT INTO nrc (
    nrc_id,
    district_code,
    township_code,
    nrc_type,
    nrc_no,
    account_id,
    created_at,
    updated_at
)
VALUES
    (1, '12', 'KMY', 'N', '123456', 1, NOW(), NOW()),
    (2, '12', 'HLN', 'N', '234567', 2, NOW(), NOW()),
    (3, '12', 'SCN', 'N', '345678', 3, NOW(), NOW()),
    (4, '12', 'KMY', 'N', '456789', 4, NOW(), NOW()),
    (5, '12', 'HLN', 'N', '567890', 5, NOW(), NOW()),
    (6, '12', 'SCN', 'N', '678901', 6, NOW(), NOW()),
    (7, '12', 'KMY', 'N', '789012', 7, NOW(), NOW()),
    (8, '12', 'HLN', 'N', '890123', 8, NOW(), NOW());


-- ============================================================
-- ADDRESSES
-- ============================================================

INSERT INTO address (
    address_id,
    address_content,
    township_id,
    account_id,
    created_at,
    updated_at
)
VALUES
    (1, 'No. 10, University Road', 1, 1, NOW(), NOW()),
    (2, 'No. 25, Insein Road', 2, 2, NOW(), NOW()),
    (3, 'No. 31, Pyay Road', 3, 3, NOW(), NOW()),
    (4, 'No. 42, Baho Road', 1, 4, NOW(), NOW()),
    (5, 'No. 55, Hledan Road', 2, 5, NOW(), NOW()),
    (6, 'No. 17, Dhamma Road', 3, 6, NOW(), NOW()),
    (7, 'No. 81, Yangon Avenue', 1, 7, NOW(), NOW()),
    (8, 'No. 93, Hlaing Road', 2, 8, NOW(), NOW());


-- ============================================================
-- MANAGER ACCOUNTS
-- ============================================================

INSERT INTO manageraccount (
    account_id,
    phone_no,
    account_email,
    hashed_password,
    role,
    created_at,
    updated_at
)
VALUES
    (
        1,
        '09111111111',
        'superadmin@example.com',
        '$argon2id$v=19$m=65536,t=3,p=4$I0GDFbhhN7pnTRMCVCER0g$yUCpJASyqfaZY4CiMkf1mOo2CWLZ/w5mD5awc3cdVis',
        'Super Admin',
        NOW(),
        NOW()
    ),
    (
        2,
        '09222222222',
        'admin@example.com',
        '$argon2id$v=19$m=65536,t=3,p=4$I0GDFbhhN7pnTRMCVCER0g$yUCpJASyqfaZY4CiMkf1mOo2CWLZ/w5mD5awc3cdVis',
        'Admin',
        NOW(),
        NOW()
    ),
    (
        3,
        '09333333333',
        'moderator@example.com',
        '$argon2id$v=19$m=65536,t=3,p=4$I0GDFbhhN7pnTRMCVCER0g$yUCpJASyqfaZY4CiMkf1mOo2CWLZ/w5mD5awc3cdVis',
        'Moderator',
        NOW(),
        NOW()
    );


-- ============================================================
-- WALLET USER ACCOUNTS
-- ============================================================

INSERT INTO walletuseraccount (
    account_id,
    phone_no,
    pin,
    nick_name,
    hashed_password,
    account_type,
    account_status,
    approved_by,
    created_at,
    updated_at
)
VALUES
    (
        4,
        '09411111111',
        '1234',
        'Alice',
        NULL,
        'Special',
        'Verified',
        1,
        NOW(),
        NOW()
    ),
    (
        5,
        '09422222222',
        '1234',
        'Bob',
        NULL,
        'Normal',
        'Verified',
        2,
        NOW(),
        NOW()
    ),
    (
        6,
        '09433333333',
        '1234',
        'Charlie',
        NULL,
        'Normal',
        'Verified',
        2,
        NOW(),
        NOW()
    ),
    (
        7,
        '09444444444',
        '1234',
        'David',
        NULL,
        'Special',
        'Verified',
        1,
        NOW(),
        NOW()
    ),
    (
        8,
        '09455555555',
        '1234',
        'Emma',
        NULL,
        'Normal',
        'Pending',
        NULL,
        NOW(),
        NOW()
    );


-- ============================================================
-- WALLETS
-- ============================================================

INSERT INTO wallet (
    wallet_id,
    wallet_type,
    current_balance,
    last_balance,
    version,
    wallet_account_id,
    approved_by,
    created_at,
    updated_at
)
VALUES
    (1, 'Funding', 150000, 150000, 1, 4, 1, NOW(), NOW()),
    (2, 'Funding', 85000, 85000, 1, 5, 2, NOW(), NOW()),
    (3, 'Funding', 50000, 50000, 1, 6, 2, NOW(), NOW()),
    (4, 'Funding', 250000, 250000, 1, 7, 1, NOW(), NOW()),
    (5, 'Funding', 0, 0, 0, 8, NULL, NOW(), NOW());


-- ============================================================
-- WALLET OPERATIONS
-- ============================================================

INSERT INTO walletoperation (
    operation_id,
    operation_name,
    created_at,
    updated_at
)
VALUES
    (1, 'Wallet Deposit', NOW(), NOW()),
    (2, 'Wallet Withdrawal', NOW(), NOW()),
    (3, 'Wallet Transfer', NOW(), NOW()),
    (4, 'Mobile Top Up', NOW(), NOW()),
    (5, 'Business Payment', NOW(), NOW());


-- ============================================================
-- TRANSACTIONS
-- ============================================================

INSERT INTO transaction (
    trx_id,
    amount,
    status,
    note,
    operation_id,
    receiver_wallet_id,
    sender_wallet_id,
    created_at,
    updated_at
)
VALUES
    (
        '11111111-1111-1111-1111-111111111111',
        100000,
        'Completed',
        'Initial wallet deposit',
        1,
        1,
        1,
        NOW(),
        NOW()
    ),
    (
        '22222222-2222-2222-2222-222222222222',
        25000,
        'Completed',
        'Transfer to Bob',
        3,
        2,
        1,
        NOW(),
        NOW()
    ),
    (
        '33333333-3333-3333-3333-333333333333',
        10000,
        'Pending',
        'Pending transfer to Charlie',
        3,
        3,
        1,
        NOW(),
        NOW()
    ),
    (
        '44444444-4444-4444-4444-444444444444',
        15000,
        'Failed',
        'Failed mobile top up',
        4,
        2,
        2,
        NOW(),
        NOW()
    ),
    (
        '55555555-5555-5555-5555-555555555555',
        50000,
        'Completed',
        'Business payment',
        5,
        3,
        4,
        NOW(),
        NOW()
    );


-- ============================================================
-- TRANSACTION LOGS
-- ============================================================

INSERT INTO transactionlog (
    log_id,
    trx_type,
    wallet_id,
    trx_id,
    created_at,
    updated_at
)
VALUES
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
        'Income',
        1,
        '11111111-1111-1111-1111-111111111111',
        NOW(),
        NOW()
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
        'Expense',
        1,
        '22222222-2222-2222-2222-222222222222',
        NOW(),
        NOW()
    ),
    (
        'cccccccc-cccc-cccc-cccc-cccccccccccc',
        'Income',
        2,
        '22222222-2222-2222-2222-222222222222',
        NOW(),
        NOW()
    ),
    (
        'dddddddd-dddd-dddd-dddd-dddddddddddd',
        'Expense',
        1,
        '33333333-3333-3333-3333-333333333333',
        NOW(),
        NOW()
    ),
    (
        'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
        'Income',
        3,
        '33333333-3333-3333-3333-333333333333',
        NOW(),
        NOW()
    ),
    (
        'ffffffff-ffff-ffff-ffff-ffffffffffff',
        'Expense',
        4,
        '55555555-5555-5555-5555-555555555555',
        NOW(),
        NOW()
    ),
    (
        '99999999-9999-9999-9999-999999999999',
        'Income',
        3,
        '55555555-5555-5555-5555-555555555555',
        NOW(),
        NOW()
    );


-- ============================================================
-- BUSINESS APPROVAL REQUESTS
-- ============================================================

INSERT INTO businessapprovalrequest (
    request_id,
    qualified_name,
    description,
    banner_url,
    business_type,
    status,
    remark,
    owner_id,
    updated_by,
    created_at,
    updated_at
)
VALUES
    (
        1,
        'Alice Fashion Store',
        'Online fashion and clothing store.',
        NULL,
        'Standalone',
        'Pending',
        NULL,
        4,
        NULL,
        NOW(),
        NOW()
    ),
    (
        2,
        'Bob Electronics',
        'Consumer electronics and accessories.',
        NULL,
        'Standalone',
        'Under Review',
        'Documents are being reviewed.',
        5,
        2,
        NOW(),
        NOW()
    ),
    (
        3,
        'David Holdings',
        'Small business organization.',
        NULL,
        'Organization',
        'Rejected',
        'Additional documents required.',
        7,
        3,
        NOW(),
        NOW()
    );


-- ============================================================
-- BUSINESS PROFILES
-- ============================================================

INSERT INTO businessprofile (
    business_id,
    qualified_name,
    description,
    banner_url,
    business_type,
    is_deleted,
    status,
    owner_id,
    approved_by,
    created_at,
    updated_at
)
VALUES
    (
        1,
        'Charlie Cafe',
        'Local coffee and food business.',
        NULL,
        'Standalone',
        FALSE,
        'Open',
        6,
        2,
        NOW(),
        NOW()
    ),
    (
        2,
        'David Digital',
        'Digital products and services.',
        NULL,
        'Organization',
        FALSE,
        'Open',
        7,
        1,
        NOW(),
        NOW()
    ),
    (
        3,
        'Alice Old Store',
        'Old demo business.',
        NULL,
        'Standalone',
        FALSE,
        'Closed',
        4,
        2,
        NOW(),
        NOW()
    );


-- ============================================================
-- CUSTOMER SUPPORT CHATS
-- ============================================================

INSERT INTO customersupportchat (
    chat_id,
    created_at,
    updated_at
)
VALUES
    (4, NOW(), NOW()),
    (5, NOW(), NOW()),
    (6, NOW(), NOW());


-- ============================================================
-- CHAT MESSAGES
-- ============================================================

INSERT INTO chatmessage (
    message_id,
    message_content,
    is_read,
    account_id,
    support_chat_id,
    created_at,
    updated_at
)
VALUES
    (
        1,
        'Hello, I need help with my wallet.',
        TRUE,
        4,
        4,
        NOW(),
        NOW()
    ),
    (
        2,
        'Sure. How can we help you?',
        TRUE,
        3,
        4,
        NOW(),
        NOW()
    ),
    (
        3,
        'My transfer is still pending.',
        FALSE,
        5,
        5,
        NOW(),
        NOW()
    ),
    (
        4,
        'Can you check my business account?',
        FALSE,
        6,
        6,
        NOW(),
        NOW()
    );


COMMIT;
