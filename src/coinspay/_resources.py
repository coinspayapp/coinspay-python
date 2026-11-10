# Generated from the CoinsPay OpenAPI document. Do not edit.

from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional, Union, cast

from ._model import NOT_GIVEN, Decimalish, NotGiven
from ._resource import Page, Resource
from .models import *  # noqa: F401,F403


class Invoices(Resource):
    """``client.invoices``."""

    def create(
        self,
        *,
        currency: str,
        title: Union[Optional[str], NotGiven] = NOT_GIVEN,
        items: Union[Optional[List[InvoiceItemParams]], NotGiven] = NOT_GIVEN,
        amount: Union[Optional[Decimalish], NotGiven] = NOT_GIVEN,
        pay_options: Union[Optional[List[PayOptionParams]], NotGiven] = NOT_GIVEN,
        stablecoins_only: Union[bool, NotGiven] = NOT_GIVEN,
        buyer_pays_fee: Union[bool, NotGiven] = NOT_GIVEN,
        buyer_pays_network: Union[bool, NotGiven] = NOT_GIVEN,
        lifetime_minutes: Union[int, NotGiven] = NOT_GIVEN,
        reference: Union[Optional[str], NotGiven] = NOT_GIVEN,
        description: Union[Optional[str], NotGiven] = NOT_GIVEN,
        return_url: Union[Optional[str], NotGiven] = NOT_GIVEN,
        auto_return: Union[bool, NotGiven] = NOT_GIVEN,
        idempotency_key: Optional[str] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Invoice:
        """
        Creates an invoice; send the buyer to its ``pay_url``. Without ``idempotency_key``
        the library makes a random one for its own retries; your order number is a better
        key.
        """
        return cast("Invoice", self._call("createInvoice", None, {"title": title, "currency": currency, "items": items, "amount": amount, "pay_options": pay_options, "stablecoins_only": stablecoins_only, "buyer_pays_fee": buyer_pays_fee, "buyer_pays_network": buyer_pays_network, "lifetime_minutes": lifetime_minutes, "reference": reference, "description": description, "return_url": return_url, "auto_return": auto_return}, extra_body, idempotency_key, timeout=timeout, max_retries=max_retries, headers=headers))

    def list(
        self,
        *,
        status: Union[InvoiceStatus, NotGiven] = NOT_GIVEN,
        reference: Union[str, NotGiven] = NOT_GIVEN,
        cursor: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        extra_query: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Page[InvoiceSummary]:
        """List invoices"""
        return cast("Page[InvoiceSummary]", self._call("listInvoices", None, {"status": status, "reference": reference, "cursor": cursor, "limit": limit}, extra_query, None, timeout=timeout, max_retries=max_retries, headers=headers))

    def iterate(
        self,
        *,
        status: Union[InvoiceStatus, NotGiven] = NOT_GIVEN,
        reference: Union[str, NotGiven] = NOT_GIVEN,
        cursor: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        extra_query: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Iterator[InvoiceSummary]:
        """All records that match, page after page: ``for item in client.invoices.iterate()``."""
        return self._iterate("listInvoices", {"status": status, "reference": reference, "cursor": cursor, "limit": limit}, extra_query, timeout=timeout, max_retries=max_retries, headers=headers)

    def get(
        self,
        id: str,
        *,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Invoice:
        """Get an invoice"""
        return cast("Invoice", self._call("getInvoice", id, {}, None, None, timeout=timeout, max_retries=max_retries, headers=headers))

    def cancel(
        self,
        id: str,
        *,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Invoice:
        """
        Cancels an open invoice; one that is no longer open raises ``ConflictError`` with
        code ``INVOICE_NOT_OPEN``.
        """
        return cast("Invoice", self._call("cancelInvoice", id, {}, None, None, timeout=timeout, max_retries=max_retries, headers=headers))


class Addresses(Resource):
    """``client.addresses``."""

    def create(
        self,
        *,
        chain: str,
        reference: Union[Optional[str], NotGiven] = NOT_GIVEN,
        payout: Union[Optional[List[PayoutShareParams]], NotGiven] = NOT_GIVEN,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Address:
        """
        Issues a permanent receiving address. This request has no idempotency key: after an
        ``APIConnectionError`` with ``sent`` look the address up by ``reference`` before
        creating another one.
        """
        return cast("Address", self._call("createAddress", None, {"chain": chain, "reference": reference, "payout": payout}, extra_body, None, timeout=timeout, max_retries=max_retries, headers=headers))

    def list(
        self,
        *,
        chain: Union[str, NotGiven] = NOT_GIVEN,
        reference: Union[str, NotGiven] = NOT_GIVEN,
        address: Union[str, NotGiven] = NOT_GIVEN,
        cursor: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        extra_query: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Page[Address]:
        """List addresses"""
        return cast("Page[Address]", self._call("listAddresses", None, {"chain": chain, "reference": reference, "address": address, "cursor": cursor, "limit": limit}, extra_query, None, timeout=timeout, max_retries=max_retries, headers=headers))

    def iterate(
        self,
        *,
        chain: Union[str, NotGiven] = NOT_GIVEN,
        reference: Union[str, NotGiven] = NOT_GIVEN,
        address: Union[str, NotGiven] = NOT_GIVEN,
        cursor: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        extra_query: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Iterator[Address]:
        """All records that match, page after page: ``for item in client.addresses.iterate()``."""
        return self._iterate("listAddresses", {"chain": chain, "reference": reference, "address": address, "cursor": cursor, "limit": limit}, extra_query, timeout=timeout, max_retries=max_retries, headers=headers)

    def get(
        self,
        id: str,
        *,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Address:
        """Get an address"""
        return cast("Address", self._call("getAddress", id, {}, None, None, timeout=timeout, max_retries=max_retries, headers=headers))


class Deposits(Resource):
    """``client.deposits``."""

    def list(
        self,
        *,
        status: Union[DepositStatus, NotGiven] = NOT_GIVEN,
        chain: Union[str, NotGiven] = NOT_GIVEN,
        asset: Union[str, NotGiven] = NOT_GIVEN,
        reference: Union[str, NotGiven] = NOT_GIVEN,
        address: Union[str, NotGiven] = NOT_GIVEN,
        tx_hash: Union[str, NotGiven] = NOT_GIVEN,
        cursor: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        extra_query: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Page[Deposit]:
        """List payments"""
        return cast("Page[Deposit]", self._call("listDeposits", None, {"status": status, "chain": chain, "asset": asset, "reference": reference, "address": address, "tx_hash": tx_hash, "cursor": cursor, "limit": limit}, extra_query, None, timeout=timeout, max_retries=max_retries, headers=headers))

    def iterate(
        self,
        *,
        status: Union[DepositStatus, NotGiven] = NOT_GIVEN,
        chain: Union[str, NotGiven] = NOT_GIVEN,
        asset: Union[str, NotGiven] = NOT_GIVEN,
        reference: Union[str, NotGiven] = NOT_GIVEN,
        address: Union[str, NotGiven] = NOT_GIVEN,
        tx_hash: Union[str, NotGiven] = NOT_GIVEN,
        cursor: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        extra_query: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Iterator[Deposit]:
        """All records that match, page after page: ``for item in client.deposits.iterate()``."""
        return self._iterate("listDeposits", {"status": status, "chain": chain, "asset": asset, "reference": reference, "address": address, "tx_hash": tx_hash, "cursor": cursor, "limit": limit}, extra_query, timeout=timeout, max_retries=max_retries, headers=headers)

    def get(
        self,
        id: str,
        *,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Deposit:
        """Get a payment"""
        return cast("Deposit", self._call("getDeposit", id, {}, None, None, timeout=timeout, max_retries=max_retries, headers=headers))


class Balances(Resource):
    """``client.balances``."""

    def list(
        self,
        *,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> List[Balance]:
        """Balances"""
        return cast("List[Balance]", self._call("listBalances", None, {}, None, None, timeout=timeout, max_retries=max_retries, headers=headers))


class Payouts(Resource):
    """``client.payouts``."""

    def quote(
        self,
        *,
        asset: str,
        recipients: List[PayoutRecipientParams],
        address_id: Union[str, NotGiven] = NOT_GIVEN,
        address: Union[str, NotGiven] = NOT_GIVEN,
        chain: Union[str, NotGiven] = NOT_GIVEN,
        amount: Union[Decimalish, NotGiven] = NOT_GIVEN,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> PayoutQuote:
        """What a payout would send to each recipient, without sending anything."""
        return cast("PayoutQuote", self._call("quotePayout", None, {"address_id": address_id, "address": address, "chain": chain, "asset": asset, "amount": amount, "recipients": recipients}, extra_body, None, timeout=timeout, max_retries=max_retries, headers=headers))

    def create(
        self,
        *,
        asset: str,
        recipients: List[PayoutRecipientParams],
        address_id: Union[str, NotGiven] = NOT_GIVEN,
        address: Union[str, NotGiven] = NOT_GIVEN,
        chain: Union[str, NotGiven] = NOT_GIVEN,
        amount: Union[Decimalish, NotGiven] = NOT_GIVEN,
        idempotency_key: str,
        extra_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Payout:
        """
        Sends a payout. ``idempotency_key`` is required: take it from your own payout
        record, so that repeating the call after a failure never sends the money twice.
        """
        return cast("Payout", self._call("createPayout", None, {"address_id": address_id, "address": address, "chain": chain, "asset": asset, "amount": amount, "recipients": recipients}, extra_body, idempotency_key, timeout=timeout, max_retries=max_retries, headers=headers))

    def list(
        self,
        *,
        status: Union[PayoutStatus, NotGiven] = NOT_GIVEN,
        chain: Union[str, NotGiven] = NOT_GIVEN,
        address_id: Union[str, NotGiven] = NOT_GIVEN,
        cursor: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        extra_query: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Page[Payout]:
        """List payouts"""
        return cast("Page[Payout]", self._call("listPayouts", None, {"status": status, "chain": chain, "address_id": address_id, "cursor": cursor, "limit": limit}, extra_query, None, timeout=timeout, max_retries=max_retries, headers=headers))

    def iterate(
        self,
        *,
        status: Union[PayoutStatus, NotGiven] = NOT_GIVEN,
        chain: Union[str, NotGiven] = NOT_GIVEN,
        address_id: Union[str, NotGiven] = NOT_GIVEN,
        cursor: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        extra_query: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Iterator[Payout]:
        """All records that match, page after page: ``for item in client.payouts.iterate()``."""
        return self._iterate("listPayouts", {"status": status, "chain": chain, "address_id": address_id, "cursor": cursor, "limit": limit}, extra_query, timeout=timeout, max_retries=max_retries, headers=headers)

    def get(
        self,
        id: str,
        *,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Payout:
        """Get a payout"""
        return cast("Payout", self._call("getPayout", id, {}, None, None, timeout=timeout, max_retries=max_retries, headers=headers))


class ShopResource(Resource):
    """``client.shop``."""

    def get(
        self,
        *,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> ShopDetails:
        """The shop of the key and what the key may do (``key.test``, ``key.access``)."""
        return cast("ShopDetails", self._call("getShop", None, {}, None, None, timeout=timeout, max_retries=max_retries, headers=headers))


class Chains(Resource):
    """``client.chains``."""

    def list(
        self,
        *,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> ChainList:
        """Networks and assets"""
        return cast("ChainList", self._call("listChains", None, {}, None, None, timeout=timeout, max_retries=max_retries, headers=headers))


class Currencies(Resource):
    """``client.currencies``."""

    def list(
        self,
        *,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> CurrencyList:
        """Price currencies"""
        return cast("CurrencyList", self._call("listCurrencies", None, {}, None, None, timeout=timeout, max_retries=max_retries, headers=headers))
