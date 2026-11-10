# Generated from the CoinsPay OpenAPI document. Do not edit.

from typing import Any, Dict

OPERATIONS: Dict[str, Dict[str, Any]] = {
    "createInvoice": {
        "method": "POST",
        "path": "/invoices",
        "retry": "idempotent",
        "idempotency": "optional",
        "unwrap": "invoice",
        "page": None,
        "many": False,
        "returns": "Invoice",
        "params": {
            "title": True,
            "currency": True,
            "items": {
                "name": True,
                "quantity": True,
                "unit": True,
                "price": True,
            },
            "amount": True,
            "pay_options": {
                "chain": True,
                "asset": True,
            },
            "stablecoins_only": True,
            "buyer_pays_fee": True,
            "buyer_pays_network": True,
            "lifetime_minutes": True,
            "reference": True,
            "description": True,
            "return_url": True,
            "auto_return": True,
        },
        "decimals": ("items[].quantity", "items[].price", "amount"),
    },
    "listInvoices": {
        "method": "GET",
        "path": "/invoices",
        "retry": "safe",
        "idempotency": None,
        "unwrap": None,
        "page": "invoices",
        "many": False,
        "returns": "InvoiceSummary",
        "params": {
            "status": True,
            "reference": True,
            "cursor": True,
            "limit": True,
        },
        "decimals": (),
    },
    "getInvoice": {
        "method": "GET",
        "path": "/invoices/{id}",
        "retry": "safe",
        "idempotency": None,
        "unwrap": "invoice",
        "page": None,
        "many": False,
        "returns": "Invoice",
        "params": None,
        "decimals": (),
    },
    "cancelInvoice": {
        "method": "POST",
        "path": "/invoices/{id}/cancel",
        "retry": "cancel",
        "idempotency": None,
        "unwrap": "invoice",
        "page": None,
        "many": False,
        "returns": "Invoice",
        "params": None,
        "decimals": (),
    },
    "createAddress": {
        "method": "POST",
        "path": "/addresses",
        "retry": "unsafe",
        "idempotency": None,
        "unwrap": "address",
        "page": None,
        "many": False,
        "returns": "Address",
        "params": {
            "chain": True,
            "reference": True,
            "payout": {
                "address": True,
                "percent": True,
            },
        },
        "decimals": ("payout[].percent",),
    },
    "listAddresses": {
        "method": "GET",
        "path": "/addresses",
        "retry": "safe",
        "idempotency": None,
        "unwrap": None,
        "page": "addresses",
        "many": False,
        "returns": "Address",
        "params": {
            "chain": True,
            "reference": True,
            "address": True,
            "cursor": True,
            "limit": True,
        },
        "decimals": (),
    },
    "getAddress": {
        "method": "GET",
        "path": "/addresses/{id}",
        "retry": "safe",
        "idempotency": None,
        "unwrap": "address",
        "page": None,
        "many": False,
        "returns": "Address",
        "params": None,
        "decimals": (),
    },
    "listDeposits": {
        "method": "GET",
        "path": "/deposits",
        "retry": "safe",
        "idempotency": None,
        "unwrap": None,
        "page": "deposits",
        "many": False,
        "returns": "Deposit",
        "params": {
            "status": True,
            "chain": True,
            "asset": True,
            "reference": True,
            "address": True,
            "tx_hash": True,
            "cursor": True,
            "limit": True,
        },
        "decimals": (),
    },
    "getDeposit": {
        "method": "GET",
        "path": "/deposits/{id}",
        "retry": "safe",
        "idempotency": None,
        "unwrap": "deposit",
        "page": None,
        "many": False,
        "returns": "Deposit",
        "params": None,
        "decimals": (),
    },
    "listBalances": {
        "method": "GET",
        "path": "/balances",
        "retry": "safe",
        "idempotency": None,
        "unwrap": "balances",
        "page": None,
        "many": True,
        "returns": "Balance",
        "params": None,
        "decimals": (),
    },
    "quotePayout": {
        "method": "POST",
        "path": "/payouts/quote",
        "retry": "safe",
        "idempotency": None,
        "unwrap": "quote",
        "page": None,
        "many": False,
        "returns": "PayoutQuote",
        "params": {
            "address_id": True,
            "address": True,
            "chain": True,
            "asset": True,
            "amount": True,
            "recipients": {
                "address": True,
                "percent": True,
                "amount": True,
            },
        },
        "decimals": ("amount", "recipients[].percent", "recipients[].amount"),
    },
    "createPayout": {
        "method": "POST",
        "path": "/payouts",
        "retry": "idempotent",
        "idempotency": "required",
        "unwrap": "payout",
        "page": None,
        "many": False,
        "returns": "Payout",
        "params": {
            "address_id": True,
            "address": True,
            "chain": True,
            "asset": True,
            "amount": True,
            "recipients": {
                "address": True,
                "percent": True,
                "amount": True,
            },
        },
        "decimals": ("amount", "recipients[].percent", "recipients[].amount"),
    },
    "listPayouts": {
        "method": "GET",
        "path": "/payouts",
        "retry": "safe",
        "idempotency": None,
        "unwrap": None,
        "page": "payouts",
        "many": False,
        "returns": "Payout",
        "params": {
            "status": True,
            "chain": True,
            "address_id": True,
            "cursor": True,
            "limit": True,
        },
        "decimals": (),
    },
    "getPayout": {
        "method": "GET",
        "path": "/payouts/{id}",
        "retry": "safe",
        "idempotency": None,
        "unwrap": "payout",
        "page": None,
        "many": False,
        "returns": "Payout",
        "params": None,
        "decimals": (),
    },
    "getShop": {
        "method": "GET",
        "path": "/shop",
        "retry": "safe",
        "idempotency": None,
        "unwrap": None,
        "page": None,
        "many": False,
        "returns": "ShopDetails",
        "params": None,
        "decimals": (),
    },
    "listChains": {
        "method": "GET",
        "path": "/chains",
        "retry": "safe",
        "idempotency": None,
        "unwrap": None,
        "page": None,
        "many": False,
        "returns": "ChainList",
        "params": None,
        "decimals": (),
    },
    "listCurrencies": {
        "method": "GET",
        "path": "/currencies",
        "retry": "safe",
        "idempotency": None,
        "unwrap": None,
        "page": None,
        "many": False,
        "returns": "CurrencyList",
        "params": None,
        "decimals": (),
    },
}

ERROR_CODES = {
    "400": ("VALIDATION_ERROR", "UNKNOWN_CHAIN", "UNKNOWN_ASSET", "CHAIN_DISABLED", "INVALID_ADDRESS", "IDEMPOTENCY_KEY_REQUIRED"),
    "401": ("UNAUTHORIZED",),
    "403": ("SHOP_DISABLED", "IP_NOT_ALLOWED", "TEST_MODE_UNSUPPORTED", "KEY_ACCESS_DENIED"),
    "404": ("NOT_FOUND",),
    "409": ("IDEMPOTENCY_CONFLICT", "INVOICE_NOT_OPEN"),
    "422": ("INSUFFICIENT_BALANCE", "FUNDS_NOT_MATURE", "BELOW_MINIMUM", "COSTS_EXCEED_AMOUNT", "PAYOUT_NOT_VIABLE"),
    "429": ("RATE_LIMITED",),
    "500": ("INTERNAL_ERROR",),
    "503": ("CORE_UNAVAILABLE", "RATE_UNAVAILABLE", "NETWORK_FEE_TOO_HIGH"),
}
"""Error codes of the API by HTTP status; branch on ``code``, not on the message."""


class ErrorCode:
    """Error codes of the API: ``error.code == ErrorCode.KEY_ACCESS_DENIED``."""

    VALIDATION_ERROR = "VALIDATION_ERROR"
    UNKNOWN_CHAIN = "UNKNOWN_CHAIN"
    UNKNOWN_ASSET = "UNKNOWN_ASSET"
    CHAIN_DISABLED = "CHAIN_DISABLED"
    INVALID_ADDRESS = "INVALID_ADDRESS"
    IDEMPOTENCY_KEY_REQUIRED = "IDEMPOTENCY_KEY_REQUIRED"
    UNAUTHORIZED = "UNAUTHORIZED"
    SHOP_DISABLED = "SHOP_DISABLED"
    IP_NOT_ALLOWED = "IP_NOT_ALLOWED"
    TEST_MODE_UNSUPPORTED = "TEST_MODE_UNSUPPORTED"
    KEY_ACCESS_DENIED = "KEY_ACCESS_DENIED"
    NOT_FOUND = "NOT_FOUND"
    IDEMPOTENCY_CONFLICT = "IDEMPOTENCY_CONFLICT"
    INVOICE_NOT_OPEN = "INVOICE_NOT_OPEN"
    INSUFFICIENT_BALANCE = "INSUFFICIENT_BALANCE"
    FUNDS_NOT_MATURE = "FUNDS_NOT_MATURE"
    BELOW_MINIMUM = "BELOW_MINIMUM"
    COSTS_EXCEED_AMOUNT = "COSTS_EXCEED_AMOUNT"
    PAYOUT_NOT_VIABLE = "PAYOUT_NOT_VIABLE"
    RATE_LIMITED = "RATE_LIMITED"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    CORE_UNAVAILABLE = "CORE_UNAVAILABLE"
    RATE_UNAVAILABLE = "RATE_UNAVAILABLE"
    NETWORK_FEE_TOO_HIGH = "NETWORK_FEE_TOO_HIGH"
