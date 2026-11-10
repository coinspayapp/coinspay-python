# Generated from the CoinsPay OpenAPI document. Do not edit.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, TypedDict, Union

from ._model import Decimalish, Model, _list, _list_required, _one, _one_required, _value

__all__ = [
    "KeyAccess",
    "ChainFamily",
    "NetworkMode",
    "DepositStatus",
    "PayoutStatus",
    "PayoutOrigin",
    "InvoiceStatus",
    "CurrencyKind",
    "InvoiceOrigin",
    "PaymentEventType",
    "PayoutEventType",
    "InvoiceEventType",
    "Shop",
    "ShopKey",
    "Chain",
    "ChainAsset",
    "ChainList",
    "FiatCurrency",
    "CryptoCurrency",
    "CurrencyList",
    "Address",
    "PayoutShare",
    "Deposit",
    "Balance",
    "Payout",
    "PayoutRecipient",
    "PayoutError",
    "PayoutQuote",
    "PayoutQuoteRecipient",
    "Invoice",
    "InvoiceSummary",
    "InvoiceItem",
    "InvoicePayment",
    "PayOption",
    "PaymentEvent",
    "PaymentEventData",
    "PayoutEvent",
    "PayoutEventData",
    "InvoiceEvent",
    "InvoiceEventData",
    "TestEvent",
    "TestEventData",
    "ShopDetails",
    "AddressCreateParams",
    "PayoutShareParams",
    "PayoutCreateParams",
    "PayoutRecipientParams",
    "InvoiceCreateParams",
    "InvoiceItemParams",
    "PayOptionParams",
    "WebhookEvent",
    "EVENT_CLASSES",
]

KeyAccess = Literal["invoices", "full"]
KEY_ACCESS_VALUES = ("invoices", "full")
ChainFamily = Literal["evm", "tron", "bitcoin", "litecoin", "solana"]
CHAIN_FAMILY_VALUES = ("evm", "tron", "bitcoin", "litecoin", "solana")
NetworkMode = Literal["mainnet", "testnet"]
NETWORK_MODE_VALUES = ("mainnet", "testnet")
DepositStatus = Literal["seen", "pending", "confirmed", "orphaned"]
DEPOSIT_STATUS_VALUES = ("seen", "pending", "confirmed", "orphaned")
PayoutStatus = Literal["pending", "waiting_maturity", "submitted", "broadcast", "confirmed", "failed", "partially_completed", "rejected"]
PAYOUT_STATUS_VALUES = ("pending", "waiting_maturity", "submitted", "broadcast", "confirmed", "failed", "partially_completed", "rejected")
PayoutOrigin = Literal["api", "auto"]
PAYOUT_ORIGIN_VALUES = ("api", "auto")
InvoiceStatus = Literal["open", "paid", "expired", "cancelled"]
INVOICE_STATUS_VALUES = ("open", "paid", "expired", "cancelled")
CurrencyKind = Literal["fiat", "crypto"]
CURRENCY_KIND_VALUES = ("fiat", "crypto")
InvoiceOrigin = Literal["cabinet", "api"]
INVOICE_ORIGIN_VALUES = ("cabinet", "api")
PaymentEventType = Literal["payment.seen", "payment.detected", "payment.confirmed", "payment.orphaned"]
PAYMENT_EVENT_TYPE_VALUES = ("payment.seen", "payment.detected", "payment.confirmed", "payment.orphaned")
PayoutEventType = Literal["payout.broadcast", "payout.confirmed", "payout.failed"]
PAYOUT_EVENT_TYPE_VALUES = ("payout.broadcast", "payout.confirmed", "payout.failed")
InvoiceEventType = Literal["invoice.paid", "invoice.partially_paid", "invoice.expired", "invoice.cancelled"]
INVOICE_EVENT_TYPE_VALUES = ("invoice.paid", "invoice.partially_paid", "invoice.expired", "invoice.cancelled")


@dataclass(frozen=True)
class Shop(Model):
    """Shop object of the API."""

    id: str
    """Public id of the shop."""

    name: str
    """Shop name."""

    created_at: str
    """Creation time, UTC (ISO 8601). ISO 8601 date-time in UTC."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Shop":
        return cls(
            raw=data,
            id=_value(data, "id"),
            name=_value(data, "name"),
            created_at=_value(data, "created_at"),
        )


@dataclass(frozen=True)
class ShopKey(Model):
    """ShopKey object of the API."""

    test: bool
    """`true` for a test key `cpk_test_…`: test invoices only."""

    access: KeyAccess
    """
    Key access: `invoices` covers invoices, the shop, networks and price currencies; `full`
    adds addresses, payments, balances and payouts.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ShopKey":
        return cls(
            raw=data,
            test=_value(data, "test"),
            access=_value(data, "access"),
        )


@dataclass(frozen=True)
class Chain(Model):
    """Chain object of the API."""

    id: str
    """Network id used in requests."""

    name: str
    """Human-readable network name."""

    family: ChainFamily
    """
    Network family: the address format. An EVM address is the same in every EVM network.
    Solana addresses are case-sensitive.
    """

    native_symbol: str
    """Native coin of the network: fees are paid in it."""

    confirmations: int
    """Depth at which a payment is credited (`payment.confirmed`)."""

    block_time_ms: int
    """Average block time, ms."""

    enabled: bool
    """
    `false`: the network is disabled by the administrator; no new addresses, issued ones
    keep working.
    """

    assets: List[ChainAsset]
    """Assets of the network: the coin and tokens."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chain":
        return cls(
            raw=data,
            id=_value(data, "id"),
            name=_value(data, "name"),
            family=_value(data, "family"),
            native_symbol=_value(data, "native_symbol"),
            confirmations=_value(data, "confirmations"),
            block_time_ms=_value(data, "block_time_ms"),
            enabled=_value(data, "enabled"),
            assets=_list_required(data, "assets", ChainAsset),
        )


@dataclass(frozen=True)
class ChainAsset(Model):
    """ChainAsset object of the API."""

    symbol: str
    """Asset ticker."""

    decimals: int
    """Decimal places of the asset: how many base units make one coin."""

    native: bool
    """`true` for the network coin, `false` for a token."""

    contract: Optional[str]
    """Token contract address; `null` for the network coin."""

    stablecoin: bool
    """
    `true` for a stablecoin (USDT, USDC): an invoice with `stablecoins_only` accepts these
    coins.
    """

    enabled: bool
    """Whether the asset is accepted: `false` if it or its network is disabled."""

    payout_minimum: Optional[str]
    """Minimum payout amount; `null` means no minimum. Decimal string."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChainAsset":
        return cls(
            raw=data,
            symbol=_value(data, "symbol"),
            decimals=_value(data, "decimals"),
            native=_value(data, "native"),
            contract=_value(data, "contract"),
            stablecoin=_value(data, "stablecoin"),
            enabled=_value(data, "enabled"),
            payout_minimum=_value(data, "payout_minimum"),
        )


@dataclass(frozen=True)
class ChainList(Model):
    """ChainList object of the API."""

    network_mode: NetworkMode
    """`mainnet` for real money, `testnet` for test networks."""

    chains: List[Chain]
    """Networks of the platform."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChainList":
        return cls(
            raw=data,
            network_mode=_value(data, "network_mode"),
            chains=_list_required(data, "chains", Chain),
        )


@dataclass(frozen=True)
class FiatCurrency(Model):
    """FiatCurrency object of the API."""

    code: str
    """Code: the `currency` value in `POST /invoices`."""

    symbol: str
    """Currency sign."""

    scale: int
    """Decimal places of the invoice prices and amount."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FiatCurrency":
        return cls(
            raw=data,
            code=_value(data, "code"),
            symbol=_value(data, "symbol"),
            scale=_value(data, "scale"),
        )


@dataclass(frozen=True)
class CryptoCurrency(Model):
    """CryptoCurrency object of the API."""

    code: str
    """Code: the `currency` value in `POST /invoices`."""

    scale: int
    """Decimal places of the invoice prices and amount."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CryptoCurrency":
        return cls(
            raw=data,
            code=_value(data, "code"),
            scale=_value(data, "scale"),
        )


@dataclass(frozen=True)
class CurrencyList(Model):
    """CurrencyList object of the API."""

    fiat: List[FiatCurrency]
    """Fiat currencies enabled on the platform."""

    crypto: List[CryptoCurrency]
    """
    Cryptocurrencies: the coin of any network. An invoice in a coin is not converted when
    the buyer pays with the same coin.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CurrencyList":
        return cls(
            raw=data,
            fiat=_list_required(data, "fiat", FiatCurrency),
            crypto=_list_required(data, "crypto", CryptoCurrency),
        )


@dataclass(frozen=True)
class Address(Model):
    """Address object of the API."""

    id: str
    """Public id of the address."""

    chain: str
    """
    Network: `tron`, `ethereum`, `bsc`… All values are in [Networks and
    coins](/docs/networks) and in the `GET /chains` response.
    """

    address: str
    """Address in the network: the buyer sends the payment here."""

    reference: Optional[str]
    """Your order number: comes back in payments and events. Up to 190 characters."""

    payout: Optional[List[PayoutShare]]
    """Payout recipients of this address; `null` means the shop payout rule applies."""

    pay_url: str
    """
    Payment page for the buyer: address, QR code and payments. For an invoice address it is
    the invoice page.
    """

    invoice_id: Optional[str]
    """Invoice the address was issued for; `null` for a standalone address."""

    created_at: str
    """Creation time, UTC (ISO 8601). ISO 8601 date-time in UTC."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Address":
        return cls(
            raw=data,
            id=_value(data, "id"),
            chain=_value(data, "chain"),
            address=_value(data, "address"),
            reference=_value(data, "reference"),
            payout=_list(data, "payout", PayoutShare),
            pay_url=_value(data, "pay_url"),
            invoice_id=_value(data, "invoice_id"),
            created_at=_value(data, "created_at"),
        )


@dataclass(frozen=True)
class PayoutShare(Model):
    """PayoutShare object of the API."""

    address: str
    """Payout recipient address."""

    percent: str
    """Recipient share in percent, up to hundredths. Shares add up to 100. Decimal string."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PayoutShare":
        return cls(
            raw=data,
            address=_value(data, "address"),
            percent=_value(data, "percent"),
        )


@dataclass(frozen=True)
class Deposit(Model):
    """Deposit object of the API."""

    id: str
    """Public id of the payment."""

    status: DepositStatus
    """
    `seen`: the transaction is in the mempool (Bitcoin and Litecoin), not a payment yet;
    `pending`: in a block, waiting for confirmations; `confirmed`: credited; `orphaned`: the
    block was reorganized or the transaction disappeared.
    """

    chain: str
    """
    Network: `tron`, `ethereum`, `bsc`… All values are in [Networks and
    coins](/docs/networks) and in the `GET /chains` response.
    """

    asset: str
    """
    Asset: the network coin (`ETH`, `TRX`, `BTC`…) or a token (`USDT`, `USDC`…). The assets
    of each network are in [Networks and coins](/docs/networks).
    """

    amount: str
    """Payment amount in asset units, as a decimal string. Decimal string."""

    amount_base: str
    """
    The same amount in base units of the asset (satoshi, wei, sun) as an integer string.
    Integer string in base units of the asset.
    """

    decimals: int
    """Decimal places of the asset: how many base units make one coin."""

    amount_usd: Optional[str]
    """
    Value in US dollars at the moment of crediting; `null` before crediting or without a
    rate. Decimal string.
    """

    amounts_fiat: Optional[Dict[str, str]]
    """
    Amounts in all reference currencies fixed at crediting: `{ "USD": "100", "EUR": "92.15"
    }`. `null` as for `amount_usd`.
    """

    address: str
    """Shop address that received the payment."""

    address_id: str
    """id of the shop receiving address."""

    invoice_id: Optional[str]
    """Invoice the address belongs to; `null` if the payment is not for an invoice."""

    reference: Optional[str]
    """Your order number: comes back in payments and events. Up to 190 characters."""

    tx_hash: str
    """Transaction hash in the network."""

    output_index: int
    """
    Output or log index inside the transaction: together with the hash it identifies the
    payment. Negative for SOL on Solana: −(1 + account index in the transaction).
    """

    from_address: Optional[str]
    """Sender if the network knows it; `null` in Bitcoin and Litecoin."""

    block_height: Optional[int]
    """Block with the transaction; `null` while it is in the mempool."""

    confirmations_required: int
    """Confirmations required for crediting."""

    unexpected_chain: bool
    """
    The payment arrived in a different EVM network than the address was issued for: it is
    counted in the actual network.
    """

    expected_chain: Optional[str]
    """Network the address was issued for."""

    rbf: Optional[bool]
    """
    Bitcoin and Litecoin mempool only: the transaction is replaceable (RBF). Otherwise
    `null`.
    """

    double_spend: Optional[bool]
    """Bitcoin mempool only: a conflicting spend of the same coins was seen. Otherwise `null`."""

    created_at: str
    """When the platform first saw the payment, UTC. ISO 8601 date-time in UTC."""

    confirmed_at: Optional[str]
    """When the payment was credited; `null` if not yet. ISO 8601 date-time in UTC."""

    orphaned_at: Optional[str]
    """
    When the payment was cancelled by a reorganization; `null` if never. ISO 8601 date-time
    in UTC.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Deposit":
        return cls(
            raw=data,
            id=_value(data, "id"),
            status=_value(data, "status"),
            chain=_value(data, "chain"),
            asset=_value(data, "asset"),
            amount=_value(data, "amount"),
            amount_base=_value(data, "amount_base"),
            decimals=_value(data, "decimals"),
            amount_usd=_value(data, "amount_usd"),
            amounts_fiat=_value(data, "amounts_fiat"),
            address=_value(data, "address"),
            address_id=_value(data, "address_id"),
            invoice_id=_value(data, "invoice_id"),
            reference=_value(data, "reference"),
            tx_hash=_value(data, "tx_hash"),
            output_index=_value(data, "output_index"),
            from_address=_value(data, "from_address"),
            block_height=_value(data, "block_height"),
            confirmations_required=_value(data, "confirmations_required"),
            unexpected_chain=_value(data, "unexpected_chain"),
            expected_chain=_value(data, "expected_chain"),
            rbf=_value(data, "rbf"),
            double_spend=_value(data, "double_spend"),
            created_at=_value(data, "created_at"),
            confirmed_at=_value(data, "confirmed_at"),
            orphaned_at=_value(data, "orphaned_at"),
        )


@dataclass(frozen=True)
class Balance(Model):
    """Balance object of the API."""

    chain: str
    """
    Network: `tron`, `ethereum`, `bsc`… All values are in [Networks and
    coins](/docs/networks) and in the `GET /chains` response.
    """

    asset: str
    """
    Asset: the network coin (`ETH`, `TRX`, `BTC`…) or a token (`USDT`, `USDC`…). The assets
    of each network are in [Networks and coins](/docs/networks).
    """

    decimals: int
    """Decimal places of the asset: how many base units make one coin."""

    confirmed: str
    """Balance: credited funds minus payouts and fees. Decimal string."""

    pending: str
    """Payments in a block waiting for confirmations. Decimal string."""

    seen: str
    """Payments in the mempool, not credited yet. Decimal string."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Balance":
        return cls(
            raw=data,
            chain=_value(data, "chain"),
            asset=_value(data, "asset"),
            decimals=_value(data, "decimals"),
            confirmed=_value(data, "confirmed"),
            pending=_value(data, "pending"),
            seen=_value(data, "seen"),
        )


@dataclass(frozen=True)
class Payout(Model):
    """Payout object of the API."""

    id: str
    """Public id of the payout."""

    status: PayoutStatus
    """
    `pending`: created; `submitted`: handed over for execution; `broadcast`: transfers are
    in the network; `confirmed`: done; `waiting_maturity`: funds are not deep enough to
    withdraw yet, the payout waits; `failed`: not executed; `partially_completed`: some
    recipients were paid; `rejected`: refused before start, funds stay on the address.
    """

    origin: PayoutOrigin
    """
    `api`: created by an API request; `auto`: automatic payout by the rule when a payment
    was credited.
    """

    chain: str
    """
    Network: `tron`, `ethereum`, `bsc`… All values are in [Networks and
    coins](/docs/networks) and in the `GET /chains` response.
    """

    asset: str
    """
    Asset: the network coin (`ETH`, `TRX`, `BTC`…) or a token (`USDT`, `USDC`…). The assets
    of each network are in [Networks and coins](/docs/networks).
    """

    decimals: int
    """Decimal places of the asset: how many base units make one coin."""

    amount: str
    """Amount leaving the address: recipients and the platform together. Decimal string."""

    amount_base: str
    """
    The same amount in base units of the asset (satoshi, wei, sun) as an integer string.
    Integer string in base units of the asset.
    """

    address: str
    """Shop address the payout is sent from."""

    address_id: str
    """id of the shop receiving address."""

    deposit_id: Optional[str]
    """Payment paid out automatically; `null` for an API payout."""

    recipients: List[PayoutRecipient]
    """Recipients with the calculation and the actual result."""

    error: Optional[PayoutError]
    """Reason of refusal or failure; `null` if there is none."""

    created_at: str
    """Creation time, UTC (ISO 8601). ISO 8601 date-time in UTC."""

    submitted_at: Optional[str]
    """When the payout was handed over for execution. ISO 8601 date-time in UTC."""

    completed_at: Optional[str]
    """When the payout finished, successfully or not. ISO 8601 date-time in UTC."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Payout":
        return cls(
            raw=data,
            id=_value(data, "id"),
            status=_value(data, "status"),
            origin=_value(data, "origin"),
            chain=_value(data, "chain"),
            asset=_value(data, "asset"),
            decimals=_value(data, "decimals"),
            amount=_value(data, "amount"),
            amount_base=_value(data, "amount_base"),
            address=_value(data, "address"),
            address_id=_value(data, "address_id"),
            deposit_id=_value(data, "deposit_id"),
            recipients=_list_required(data, "recipients", PayoutRecipient),
            error=_one(data, "error", PayoutError),
            created_at=_value(data, "created_at"),
            submitted_at=_value(data, "submitted_at"),
            completed_at=_value(data, "completed_at"),
        )


@dataclass(frozen=True)
class PayoutRecipient(Model):
    """PayoutRecipient object of the API."""

    address: str
    """Recipient address."""

    percent: Optional[str]
    """Share if recipients are set by percent. Decimal string."""

    requested: Optional[str]
    """Requested amount if recipients are set by amount (or `MAX`)."""

    amount: Optional[str]
    """Amount for the recipient after deductions; `null` until calculated. Decimal string."""

    sent: Optional[str]
    """Amount actually sent. Decimal string."""

    tx_hash: Optional[str]
    """Hash of the transfer to the recipient."""

    status: Optional[str]
    """Transfer state: `pending`, `signed`, `broadcast`, `confirmed`, `failed`."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PayoutRecipient":
        return cls(
            raw=data,
            address=_value(data, "address"),
            percent=_value(data, "percent"),
            requested=_value(data, "requested"),
            amount=_value(data, "amount"),
            sent=_value(data, "sent"),
            tx_hash=_value(data, "tx_hash"),
            status=_value(data, "status"),
        )


@dataclass(frozen=True)
class PayoutError(Model):
    """PayoutError object of the API."""

    code: str
    """
    Reason code: `BELOW_MINIMUM`, `INSUFFICIENT_BALANCE`, `FUNDS_NOT_MATURE`,
    `COSTS_EXCEED_AMOUNT`, `PAYOUT_NOT_VIABLE`, `PAYOUT_FAILED`.
    """

    message: Optional[str]
    """Explanation in English."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PayoutError":
        return cls(
            raw=data,
            code=_value(data, "code"),
            message=_value(data, "message"),
        )


@dataclass(frozen=True)
class PayoutQuote(Model):
    """PayoutQuote object of the API."""

    chain: str
    """
    Network: `tron`, `ethereum`, `bsc`… All values are in [Networks and
    coins](/docs/networks) and in the `GET /chains` response.
    """

    asset: str
    """
    Asset: the network coin (`ETH`, `TRX`, `BTC`…) or a token (`USDT`, `USDC`…). The assets
    of each network are in [Networks and coins](/docs/networks).
    """

    decimals: int
    """Decimal places of the asset: how many base units make one coin."""

    amount: str
    """Amount that will leave the address. Decimal string."""

    address: str
    """Shop address the payout will be sent from."""

    address_id: str
    """id of the shop receiving address."""

    recipients: List[PayoutQuoteRecipient]
    """What each recipient will get."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PayoutQuote":
        return cls(
            raw=data,
            chain=_value(data, "chain"),
            asset=_value(data, "asset"),
            decimals=_value(data, "decimals"),
            amount=_value(data, "amount"),
            address=_value(data, "address"),
            address_id=_value(data, "address_id"),
            recipients=_list_required(data, "recipients", PayoutQuoteRecipient),
        )


@dataclass(frozen=True)
class PayoutQuoteRecipient(Model):
    """PayoutQuoteRecipient object of the API."""

    address: str
    """Recipient address."""

    percent: Optional[str]
    """Share if recipients are set by percent. Decimal string."""

    requested: Optional[str]
    """Requested amount if recipients are set by amount (or `MAX`)."""

    amount: Optional[str]
    """Amount for the recipient after deductions; `null` until calculated. Decimal string."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PayoutQuoteRecipient":
        return cls(
            raw=data,
            address=_value(data, "address"),
            percent=_value(data, "percent"),
            requested=_value(data, "requested"),
            amount=_value(data, "amount"),
        )


@dataclass(frozen=True)
class Invoice(Model):
    """Invoice object of the API."""

    id: str
    """Public id of the invoice."""

    number: int
    """Invoice number within the shop: 1, 2, 3…"""

    title: Optional[str]
    """
    Custom invoice title; with `null` the dashboard names the invoice by its number, and the
    buyer sees "Order <reference>" or "Payment".
    """

    shop_id: str
    """Public id of the shop."""

    test: bool
    """
    `true` for a test invoice issued with a test key `cpk_test_…`. It has no address; a
    button on the payment page simulates the payment, no money moves.
    """

    status: InvoiceStatus
    """`open`: waiting for payment; `paid`: paid; `expired`: expired; `cancelled`: cancelled."""

    currency: str
    """Price currency: fiat (`USD`, `EUR`…) or crypto (`USDT`, `BTC`…)."""

    currency_kind: CurrencyKind
    """`fiat` or `crypto`."""

    amount: str
    """Invoice total in its currency. Decimal string."""

    amount_paid: str
    """Paid by confirmed payments, in the invoice currency. Decimal string."""

    amount_pending: str
    """Payments in transit: in a block without enough depth or in the mempool. Decimal string."""

    amount_due: str
    """Amount still due: total minus paid and in transit. Decimal string."""

    amount_overpaid: Optional[str]
    """Paid above the total; `null` if there is no overpayment. Decimal string."""

    reference: Optional[str]
    """Your order number: comes back in payments and events. Up to 190 characters."""

    pay_url: str
    """Payment page: send the buyer here."""

    paid_late: bool
    """Paid after the due time."""

    paid_manually: bool
    """Marked as paid manually in the dashboard."""

    expires_at: str
    """Payment deadline, UTC. ISO 8601 date-time in UTC."""

    paid_at: Optional[str]
    """When the invoice was paid. ISO 8601 date-time in UTC."""

    created_at: str
    """Creation time, UTC (ISO 8601). ISO 8601 date-time in UTC."""

    items: List[InvoiceItem]
    """Items; empty for an amount-only invoice."""

    pay_options: Optional[List[PayOption]]
    """Accepted coins; `null` means any enabled coin."""

    buyer_pays_fee: bool
    """The buyer pays the service fee: it is added to the amount."""

    buyer_pays_network: bool
    """The buyer pays the network fee of the future payout."""

    description: Optional[str]
    """Description for the buyer."""

    return_url: Optional[str]
    """
    Where to return the buyer: the "Back to the shop" button on the payment page after the
    invoice is paid, expires or is cancelled.
    """

    auto_return: bool
    """After payment the page takes the buyer to `return_url` by itself in 5 seconds."""

    origin: InvoiceOrigin
    """Where it was created: `api` or `cabinet`."""

    expired_at: Optional[str]
    """When the invoice expired. ISO 8601 date-time in UTC."""

    cancelled_at: Optional[str]
    """When the invoice was cancelled. ISO 8601 date-time in UTC."""

    payments: List[InvoicePayment]
    """Payments for the invoice."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Invoice":
        return cls(
            raw=data,
            id=_value(data, "id"),
            number=_value(data, "number"),
            title=_value(data, "title"),
            shop_id=_value(data, "shop_id"),
            test=_value(data, "test"),
            status=_value(data, "status"),
            currency=_value(data, "currency"),
            currency_kind=_value(data, "currency_kind"),
            amount=_value(data, "amount"),
            amount_paid=_value(data, "amount_paid"),
            amount_pending=_value(data, "amount_pending"),
            amount_due=_value(data, "amount_due"),
            amount_overpaid=_value(data, "amount_overpaid"),
            reference=_value(data, "reference"),
            pay_url=_value(data, "pay_url"),
            paid_late=_value(data, "paid_late"),
            paid_manually=_value(data, "paid_manually"),
            expires_at=_value(data, "expires_at"),
            paid_at=_value(data, "paid_at"),
            created_at=_value(data, "created_at"),
            items=_list_required(data, "items", InvoiceItem),
            pay_options=_list(data, "pay_options", PayOption),
            buyer_pays_fee=_value(data, "buyer_pays_fee"),
            buyer_pays_network=_value(data, "buyer_pays_network"),
            description=_value(data, "description"),
            return_url=_value(data, "return_url"),
            auto_return=_value(data, "auto_return"),
            origin=_value(data, "origin"),
            expired_at=_value(data, "expired_at"),
            cancelled_at=_value(data, "cancelled_at"),
            payments=_list_required(data, "payments", InvoicePayment),
        )


@dataclass(frozen=True)
class InvoiceSummary(Model):
    """InvoiceSummary object of the API."""

    id: str
    """Public id of the invoice."""

    number: int
    """Invoice number within the shop: 1, 2, 3…"""

    title: Optional[str]
    """
    Custom invoice title; with `null` the dashboard names the invoice by its number, and the
    buyer sees "Order <reference>" or "Payment".
    """

    shop_id: str
    """Public id of the shop."""

    test: bool
    """
    `true` for a test invoice issued with a test key `cpk_test_…`. It has no address; a
    button on the payment page simulates the payment, no money moves.
    """

    status: InvoiceStatus
    """`open`: waiting for payment; `paid`: paid; `expired`: expired; `cancelled`: cancelled."""

    currency: str
    """Price currency: fiat (`USD`, `EUR`…) or crypto (`USDT`, `BTC`…)."""

    currency_kind: CurrencyKind
    """`fiat` or `crypto`."""

    amount: str
    """Invoice total in its currency. Decimal string."""

    amount_paid: str
    """Paid by confirmed payments, in the invoice currency. Decimal string."""

    amount_pending: str
    """Payments in transit: in a block without enough depth or in the mempool. Decimal string."""

    amount_due: str
    """Amount still due: total minus paid and in transit. Decimal string."""

    amount_overpaid: Optional[str]
    """Paid above the total; `null` if there is no overpayment. Decimal string."""

    reference: Optional[str]
    """Your order number: comes back in payments and events. Up to 190 characters."""

    pay_url: str
    """Payment page: send the buyer here."""

    paid_late: bool
    """Paid after the due time."""

    paid_manually: bool
    """Marked as paid manually in the dashboard."""

    expires_at: str
    """Payment deadline, UTC. ISO 8601 date-time in UTC."""

    paid_at: Optional[str]
    """When the invoice was paid. ISO 8601 date-time in UTC."""

    created_at: str
    """Creation time, UTC (ISO 8601). ISO 8601 date-time in UTC."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InvoiceSummary":
        return cls(
            raw=data,
            id=_value(data, "id"),
            number=_value(data, "number"),
            title=_value(data, "title"),
            shop_id=_value(data, "shop_id"),
            test=_value(data, "test"),
            status=_value(data, "status"),
            currency=_value(data, "currency"),
            currency_kind=_value(data, "currency_kind"),
            amount=_value(data, "amount"),
            amount_paid=_value(data, "amount_paid"),
            amount_pending=_value(data, "amount_pending"),
            amount_due=_value(data, "amount_due"),
            amount_overpaid=_value(data, "amount_overpaid"),
            reference=_value(data, "reference"),
            pay_url=_value(data, "pay_url"),
            paid_late=_value(data, "paid_late"),
            paid_manually=_value(data, "paid_manually"),
            expires_at=_value(data, "expires_at"),
            paid_at=_value(data, "paid_at"),
            created_at=_value(data, "created_at"),
        )


@dataclass(frozen=True)
class InvoiceItem(Model):
    """InvoiceItem object of the API."""

    name: str
    """Item name."""

    quantity: str
    """Quantity. Decimal string."""

    unit: Optional[str]
    """Unit: "pcs", "h"…"""

    price: str
    """Unit price in the invoice currency. Decimal string."""

    amount: str
    """Item total: quantity × price. Decimal string."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InvoiceItem":
        return cls(
            raw=data,
            name=_value(data, "name"),
            quantity=_value(data, "quantity"),
            unit=_value(data, "unit"),
            price=_value(data, "price"),
            amount=_value(data, "amount"),
        )


@dataclass(frozen=True)
class InvoicePayment(Model):
    """InvoicePayment object of the API."""

    deposit_id: str
    """Payment id: details in `GET /deposits/{id}`."""

    status: DepositStatus
    """Payment state, as in `Deposit.status`."""

    chain: str
    """
    Network: `tron`, `ethereum`, `bsc`… All values are in [Networks and
    coins](/docs/networks) and in the `GET /chains` response.
    """

    asset: str
    """
    Asset: the network coin (`ETH`, `TRX`, `BTC`…) or a token (`USDT`, `USDC`…). The assets
    of each network are in [Networks and coins](/docs/networks).
    """

    amount: str
    """Payment amount in the coin. Decimal string."""

    tx_hash: str
    """Transaction hash in the network."""

    value: str
    """Part of the invoice covered by the payment, in the invoice currency. Decimal string."""

    late: bool
    """Counted at the rate at detection: it came after the quote expired or in another coin."""

    created_at: str
    """When the payment was detected. ISO 8601 date-time in UTC."""

    confirmed_at: Optional[str]
    """When the payment was credited. ISO 8601 date-time in UTC."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InvoicePayment":
        return cls(
            raw=data,
            deposit_id=_value(data, "deposit_id"),
            status=_value(data, "status"),
            chain=_value(data, "chain"),
            asset=_value(data, "asset"),
            amount=_value(data, "amount"),
            tx_hash=_value(data, "tx_hash"),
            value=_value(data, "value"),
            late=_value(data, "late"),
            created_at=_value(data, "created_at"),
            confirmed_at=_value(data, "confirmed_at"),
        )


@dataclass(frozen=True)
class PayOption(Model):
    """PayOption object of the API."""

    chain: str
    """Network."""

    asset: str
    """Asset."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PayOption":
        return cls(
            raw=data,
            chain=_value(data, "chain"),
            asset=_value(data, "asset"),
        )


@dataclass(frozen=True)
class PaymentEvent(Model):
    """PaymentEvent object of the API."""

    id: str
    """
    Event id: a repeated delivery of the same event has the same id; use it to drop
    duplicates.
    """

    type: PaymentEventType
    """Event type."""

    created_at: str
    """Event time, UTC. ISO 8601 date-time in UTC."""

    shop_id: str
    """Public id of the shop."""

    test: bool
    """
    `true` for a test event: sent from the dashboard or about a test invoice. No money
    arrived, do not touch real orders. The field is signed.
    """

    data: PaymentEventData
    """Event data."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PaymentEvent":
        return cls(
            raw=data,
            id=_value(data, "id"),
            type=_value(data, "type"),
            created_at=_value(data, "created_at"),
            shop_id=_value(data, "shop_id"),
            test=_value(data, "test"),
            data=_one_required(data, "data", PaymentEventData),
        )


@dataclass(frozen=True)
class PaymentEventData(Model):
    """Event data."""

    deposit: Deposit
    """The payment, as in `GET /deposits/{id}`."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PaymentEventData":
        return cls(
            raw=data,
            deposit=_one_required(data, "deposit", Deposit),
        )


@dataclass(frozen=True)
class PayoutEvent(Model):
    """PayoutEvent object of the API."""

    id: str
    """
    Event id: a repeated delivery of the same event has the same id; use it to drop
    duplicates.
    """

    type: PayoutEventType
    """Event type."""

    created_at: str
    """Event time, UTC. ISO 8601 date-time in UTC."""

    shop_id: str
    """Public id of the shop."""

    test: bool
    """
    `true` for a test event: sent from the dashboard or about a test invoice. No money
    arrived, do not touch real orders. The field is signed.
    """

    data: PayoutEventData
    """Event data."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PayoutEvent":
        return cls(
            raw=data,
            id=_value(data, "id"),
            type=_value(data, "type"),
            created_at=_value(data, "created_at"),
            shop_id=_value(data, "shop_id"),
            test=_value(data, "test"),
            data=_one_required(data, "data", PayoutEventData),
        )


@dataclass(frozen=True)
class PayoutEventData(Model):
    """Event data."""

    payout: Payout
    """The payout, as in `GET /payouts/{id}`."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PayoutEventData":
        return cls(
            raw=data,
            payout=_one_required(data, "payout", Payout),
        )


@dataclass(frozen=True)
class InvoiceEvent(Model):
    """InvoiceEvent object of the API."""

    id: str
    """
    Event id: a repeated delivery of the same event has the same id; use it to drop
    duplicates.
    """

    type: InvoiceEventType
    """Event type."""

    created_at: str
    """Event time, UTC. ISO 8601 date-time in UTC."""

    shop_id: str
    """Public id of the shop."""

    test: bool
    """
    `true` for a test event: sent from the dashboard or about a test invoice. No money
    arrived, do not touch real orders. The field is signed.
    """

    data: InvoiceEventData
    """Event data."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InvoiceEvent":
        return cls(
            raw=data,
            id=_value(data, "id"),
            type=_value(data, "type"),
            created_at=_value(data, "created_at"),
            shop_id=_value(data, "shop_id"),
            test=_value(data, "test"),
            data=_one_required(data, "data", InvoiceEventData),
        )


@dataclass(frozen=True)
class InvoiceEventData(Model):
    """Event data."""

    invoice: Invoice
    """The invoice, as in `GET /invoices/{id}`."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InvoiceEventData":
        return cls(
            raw=data,
            invoice=_one_required(data, "invoice", Invoice),
        )


@dataclass(frozen=True)
class TestEvent(Model):
    """TestEvent object of the API."""

    id: str
    """
    Event id: a repeated delivery of the same event has the same id; use it to drop
    duplicates.
    """

    type: Literal["webhook.test"]
    """Event type."""

    created_at: str
    """Event time, UTC. ISO 8601 date-time in UTC."""

    shop_id: str
    """Public id of the shop."""

    test: bool
    """
    `true` for a test event: sent from the dashboard or about a test invoice. No money
    arrived, do not touch real orders. The field is signed.
    """

    data: TestEventData
    """Event data."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TestEvent":
        return cls(
            raw=data,
            id=_value(data, "id"),
            type=_value(data, "type"),
            created_at=_value(data, "created_at"),
            shop_id=_value(data, "shop_id"),
            test=_value(data, "test"),
            data=_one_required(data, "data", TestEventData),
        )


@dataclass(frozen=True)
class TestEventData(Model):
    """Event data."""

    message: str
    """Test event text."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TestEventData":
        return cls(
            raw=data,
            message=_value(data, "message"),
        )


@dataclass(frozen=True)
class ShopDetails(Model):
    """ShopDetails object of the API."""

    shop: Shop

    key: ShopKey

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ShopDetails":
        return cls(
            raw=data,
            shop=_one_required(data, "shop", Shop),
            key=_one_required(data, "key", ShopKey),
        )


class _AddressCreateParamsRequired(TypedDict):
    chain: str
    """
    Network of the address: `tron`, `ethereum`, `bitcoin`… All values are in [Networks and
    coins](/docs/networks).
    """


class AddressCreateParams(_AddressCreateParamsRequired, total=False):
    """AddressCreateParams."""
    reference: Optional[str]
    """Your order number: comes back in payments and events. Up to 190 characters."""
    payout: Optional[List[PayoutShareParams]]
    """
    Payout recipients for this address instead of the shop rule: up to 5 addresses, shares
    add up to 100.
    """


class PayoutShareParams(TypedDict):
    """PayoutShareParams."""
    address: str
    """Recipient address."""
    percent: Decimalish
    """Share in percent: a string "33.33". Decimal string."""


class _PayoutCreateParamsRequired(TypedDict):
    asset: str
    """
    Payout asset: the network coin or a token from the network list in [Networks and
    coins](/docs/networks).
    """
    recipients: List[PayoutRecipientParams]
    """Recipients: up to 5, all by percent or all by amount."""


class PayoutCreateParams(_PayoutCreateParamsRequired, total=False):
    """PayoutCreateParams."""
    address_id: str
    """id of the shop address to pay from. Specify it or `address`."""
    address: str
    """The shop address itself instead of `address_id`."""
    chain: str
    """
    Payout network; defaults to the address network. An EVM address may use another EVM
    network.
    """
    amount: Decimalish
    """
    Payout amount with recipients by percent; omit it to pay out everything available. `MAX`
    also means everything available.
    """


class _PayoutRecipientParamsRequired(TypedDict):
    address: str
    """Recipient address."""


class PayoutRecipientParams(_PayoutRecipientParamsRequired, total=False):
    """PayoutRecipientParams."""
    percent: Decimalish
    """Share in percent; shares add up to 100. Decimal string."""
    amount: Decimalish
    """
    Amount for the recipient; `MAX` only with a single recipient. Deductions are taken from
    it.
    """


class _InvoiceCreateParamsRequired(TypedDict):
    currency: str
    """
    Price currency: fiat (`USD`, `EUR`, `RUB`…) or crypto (`USDT`, `BTC`…). All values are
    in `GET /currencies` and [Networks and coins](/docs/networks).
    """


class InvoiceCreateParams(_InvoiceCreateParamsRequired, total=False):
    """InvoiceCreateParams."""
    title: Optional[str]
    """
    Title on the payment page, up to 200 characters. Without it the buyer sees "Order
    <reference>" or "Payment".
    """
    items: Optional[List[InvoiceItemParams]]
    """Items, up to 100. Specify them or `amount`."""
    amount: Optional[Decimalish]
    """Invoice amount without items. Specify it or `items`. Decimal string."""
    pay_options: Optional[List[PayOptionParams]]
    """
    Accepted coins: `chain` and `asset` pairs from [Networks and coins](/docs/networks);
    omit to accept any enabled coin.
    """
    stablecoins_only: bool
    """
    Stablecoins only: USDT and USDC. Without `pay_options` the invoice accepts every enabled
    stablecoin in every network, and `pay_options` in the response lists them. With
    `pay_options`, a coin that is not a stablecoin gives `400 VALIDATION_ERROR`.
    """
    buyer_pays_fee: bool
    """The buyer pays the service fee: it is added to the amount."""
    buyer_pays_network: bool
    """The buyer pays the network fee of the future payout."""
    lifetime_minutes: int
    """Payment time in minutes: 15 to 43200 (30 days), 1440 (one day) by default."""
    reference: Optional[str]
    """Your order number: comes back in payments and events. Up to 190 characters."""
    description: Optional[str]
    """Description for the buyer, up to 1000 characters."""
    return_url: Optional[str]
    """
    Where to return the buyer, up to 500 characters: the "Back to the shop" button after the
    invoice is paid, expires or is cancelled.
    """
    auto_return: bool
    """
    After payment the page takes the buyer to `return_url` by itself in 5 seconds; the buyer
    can press "Stay". Without `return_url` it gives `400 VALIDATION_ERROR`.
    """


class _InvoiceItemParamsRequired(TypedDict):
    name: str
    """Item name, up to 200 characters."""
    quantity: Decimalish
    """Quantity as a string. Decimal string."""
    price: Decimalish
    """Unit price; precision follows the currency. Decimal string."""


class InvoiceItemParams(_InvoiceItemParamsRequired, total=False):
    """InvoiceItemParams."""
    unit: Optional[str]
    """Unit, up to 20 characters."""


class PayOptionParams(TypedDict):
    """PayOptionParams."""
    chain: str
    """Network."""
    asset: str
    """Asset."""


WebhookEvent = Union[PaymentEvent, PayoutEvent, InvoiceEvent, TestEvent]

EVENT_CLASSES: Dict[str, Any] = {
    "payment.seen": PaymentEvent,
    "payment.detected": PaymentEvent,
    "payment.confirmed": PaymentEvent,
    "payment.orphaned": PaymentEvent,
    "payout.broadcast": PayoutEvent,
    "payout.confirmed": PayoutEvent,
    "payout.failed": PayoutEvent,
    "invoice.paid": InvoiceEvent,
    "invoice.partially_paid": InvoiceEvent,
    "invoice.expired": InvoiceEvent,
    "invoice.cancelled": InvoiceEvent,
    "webhook.test": TestEvent,
}
"""Webhook event type -> model class."""
