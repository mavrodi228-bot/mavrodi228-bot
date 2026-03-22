from alembic import op
import sqlalchemy as sa

revision = '20260322_0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('category',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=120), nullable=False, unique=True),
        sa.Column('slug', sa.String(length=120), nullable=False, unique=True),
        sa.Column('icon', sa.String(length=50), nullable=False, server_default='wallet'),
        sa.Column('color', sa.String(length=20), nullable=False, server_default='#64748b'),
        sa.Column('type', sa.Enum('income', 'expense', 'transfer', 'system', name='category_type'), nullable=False),
        sa.Column('parent_id', sa.Integer(), sa.ForeignKey('category.id', ondelete='SET NULL')),
    )
    op.create_table('goal',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('target_amount', sa.Numeric(14, 2), nullable=False),
        sa.Column('current_amount', sa.Numeric(14, 2), nullable=False, server_default='0'),
        sa.Column('deadline', sa.Date()),
        sa.Column('monthly_target', sa.Numeric(14, 2)),
        sa.Column('status', sa.Enum('active', 'completed', 'paused', name='goal_status'), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table('bankconnection',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('provider_name', sa.String(length=120), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('auth_type', sa.String(length=50), nullable=False),
        sa.Column('encrypted_credentials_json', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table('importsession',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('source_type', sa.Enum('tbank_business_api', 'tbank_csv', 'manual', 'future', name='import_source_type'), nullable=False),
        sa.Column('file_name', sa.String(length=255)),
        sa.Column('imported_rows', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('skipped_rows', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('finished_at', sa.DateTime(timezone=True)),
        sa.Column('status', sa.Enum('pending', 'processing', 'completed', 'failed', name='import_status'), nullable=False, server_default='pending'),
        sa.Column('error_message', sa.Text()),
    )
    op.create_table('categoryrule',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('keyword', sa.String(length=120)),
        sa.Column('merchant_pattern', sa.String(length=120)),
        sa.Column('mcc', sa.String(length=8)),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('category.id', ondelete='CASCADE'), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=False, server_default='100'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_table('transaction',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('external_id', sa.String(length=255)),
        sa.Column('source_type', sa.Enum('tbank_business_api', 'tbank_csv', 'manual', 'future', name='source_type'), nullable=False),
        sa.Column('account_id', sa.String(length=255)),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('posted_at', sa.DateTime(timezone=True)),
        sa.Column('amount', sa.Numeric(14, 2), nullable=False),
        sa.Column('currency', sa.String(length=8), nullable=False, server_default='RUB'),
        sa.Column('direction', sa.Enum('income', 'expense', 'transfer', 'refund', name='transaction_direction'), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('merchant', sa.String(length=255)),
        sa.Column('mcc', sa.String(length=8)),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('category.id', ondelete='SET NULL')),
        sa.Column('raw_category', sa.String(length=120)),
        sa.Column('is_recurring', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('is_transfer', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('is_hidden', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_transaction_external_id', 'transaction', ['external_id'])
    op.create_index('ix_transaction_account_id', 'transaction', ['account_id'])
    op.create_index('ix_transaction_date', 'transaction', ['date'])
    op.create_index('ix_transaction_merchant', 'transaction', ['merchant'])
    op.create_index('ix_transaction_mcc', 'transaction', ['mcc'])
    op.create_index('ix_transaction_category_id', 'transaction', ['category_id'])

    category_table = sa.table('category',
        sa.column('name', sa.String()), sa.column('slug', sa.String()), sa.column('icon', sa.String()), sa.column('color', sa.String()), sa.column('type', sa.String()), sa.column('parent_id', sa.Integer())
    )
    op.bulk_insert(category_table, [
        {'name': 'Other', 'slug': 'other', 'icon': 'circle-help', 'color': '#94a3b8', 'type': 'expense', 'parent_id': None},
        {'name': 'Groceries', 'slug': 'groceries', 'icon': 'shopping-basket', 'color': '#10b981', 'type': 'expense', 'parent_id': None},
        {'name': 'Cafes', 'slug': 'cafes', 'icon': 'coffee', 'color': '#f97316', 'type': 'expense', 'parent_id': None},
        {'name': 'Subscriptions', 'slug': 'subscriptions', 'icon': 'repeat', 'color': '#8b5cf6', 'type': 'expense', 'parent_id': None},
        {'name': 'Taxi', 'slug': 'taxi', 'icon': 'car', 'color': '#eab308', 'type': 'expense', 'parent_id': None},
        {'name': 'Transport', 'slug': 'transport', 'icon': 'train', 'color': '#06b6d4', 'type': 'expense', 'parent_id': None},
        {'name': 'Pharmacy', 'slug': 'pharmacy', 'icon': 'pill', 'color': '#ef4444', 'type': 'expense', 'parent_id': None},
        {'name': 'Marketplaces', 'slug': 'marketplaces', 'icon': 'package', 'color': '#6366f1', 'type': 'expense', 'parent_id': None},
        {'name': 'Salary', 'slug': 'salary', 'icon': 'badge-russian-ruble', 'color': '#22c55e', 'type': 'income', 'parent_id': None},
        {'name': 'Transfers', 'slug': 'transfers', 'icon': 'arrow-left-right', 'color': '#64748b', 'type': 'transfer', 'parent_id': None},
        {'name': 'Housing', 'slug': 'housing', 'icon': 'house', 'color': '#0f766e', 'type': 'expense', 'parent_id': None},
    ])
    op.execute("""
        INSERT INTO categoryrule (keyword, merchant_pattern, mcc, category_id, priority, is_active)
        SELECT 'пятерочка', 'пятерочка', NULL, id, 10, true FROM category WHERE slug = 'groceries';
        INSERT INTO categoryrule (keyword, merchant_pattern, mcc, category_id, priority, is_active)
        SELECT 'перекресток', 'перекресток', NULL, id, 10, true FROM category WHERE slug = 'groceries';
        INSERT INTO categoryrule (keyword, merchant_pattern, mcc, category_id, priority, is_active)
        SELECT 'coffee', 'coffee', NULL, id, 20, true FROM category WHERE slug = 'cafes';
        INSERT INTO categoryrule (keyword, merchant_pattern, mcc, category_id, priority, is_active)
        SELECT 'yandex go', 'yandex go', NULL, id, 20, true FROM category WHERE slug = 'taxi';
        INSERT INTO categoryrule (keyword, merchant_pattern, mcc, category_id, priority, is_active)
        SELECT 'metro', 'metro', NULL, id, 20, true FROM category WHERE slug = 'transport';
        INSERT INTO categoryrule (keyword, merchant_pattern, mcc, category_id, priority, is_active)
        SELECT 'аптека', 'аптека', NULL, id, 20, true FROM category WHERE slug = 'pharmacy';
        INSERT INTO categoryrule (keyword, merchant_pattern, mcc, category_id, priority, is_active)
        SELECT 'ozon', 'ozon', NULL, id, 20, true FROM category WHERE slug = 'marketplaces';
        INSERT INTO categoryrule (keyword, merchant_pattern, mcc, category_id, priority, is_active)
        SELECT 'wildberries', 'wildberries', NULL, id, 20, true FROM category WHERE slug = 'marketplaces';
        INSERT INTO categoryrule (keyword, merchant_pattern, mcc, category_id, priority, is_active)
        SELECT 'salary', 'salary', NULL, id, 5, true FROM category WHERE slug = 'salary';
        INSERT INTO categoryrule (keyword, merchant_pattern, mcc, category_id, priority, is_active)
        SELECT 'перевод', 'transfer', NULL, id, 5, true FROM category WHERE slug = 'transfers';
        INSERT INTO categoryrule (keyword, merchant_pattern, mcc, category_id, priority, is_active)
        SELECT 'netflix', 'netflix', NULL, id, 10, true FROM category WHERE slug = 'subscriptions';
    """)


def downgrade() -> None:
    op.drop_index('ix_transaction_category_id', table_name='transaction')
    op.drop_index('ix_transaction_mcc', table_name='transaction')
    op.drop_index('ix_transaction_merchant', table_name='transaction')
    op.drop_index('ix_transaction_date', table_name='transaction')
    op.drop_index('ix_transaction_account_id', table_name='transaction')
    op.drop_index('ix_transaction_external_id', table_name='transaction')
    op.drop_table('transaction')
    op.drop_table('categoryrule')
    op.drop_table('importsession')
    op.drop_table('bankconnection')
    op.drop_table('goal')
    op.drop_table('category')
    sa.Enum(name='transaction_direction').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='source_type').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='import_status').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='import_source_type').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='goal_status').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='category_type').drop(op.get_bind(), checkfirst=False)
