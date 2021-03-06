from collections import OrderedDict
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping
from .. import Hash32, ExternalAddress, Signature
from ..transactions import Transaction


@dataclass(frozen=True)
class BlockHeader:
    hash: Hash32
    prev_hash: Hash32
    height: int
    timestamp: int
    peer_id: ExternalAddress
    signature: Signature

    version = ''


@dataclass(frozen=True)
class BlockBody:
    transactions: Mapping[Hash32, Transaction]

    def __init__(self, transactions: Mapping[Hash32, Transaction]):
        object.__setattr__(self, "transactions", MappingProxyType(OrderedDict(transactions)))


@dataclass(frozen=True)
class Block:
    header: BlockHeader
    body: BlockBody

