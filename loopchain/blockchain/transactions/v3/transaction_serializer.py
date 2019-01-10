from . import Transaction, HASH_SALT
from .. import TransactionSerializer as BaseTransactionSerializer
from ... import Hash32, Signature, Address


class TransactionSerializer(BaseTransactionSerializer):
    _hash_salt = HASH_SALT

    def to_origin_data(self, tx: 'Transaction'):
        params = {
            "version": Transaction.version,
            "from": tx.from_address.hex_xx(),
            "to": tx.to_address.hex_xx(),
            "stepLimit": hex(tx.step_limit),
            "timestamp": hex(tx.timestamp),
            "nid": hex(tx.nid)
        }

        if tx.value is not None:
            params["value"] = hex(tx.value)

        if tx.nonce is not None:
            params['nonce'] = tx.nonce

        if tx.data is not None and tx.data_type is not None:
            if isinstance(tx.data, str):
                params["data"] = tx.data
            else:
                params["data"] = tx.data
            params["dataType"] = tx.data_type
        return params

    def to_raw_data(self, tx: 'Transaction'):
        params = self.to_origin_data(tx)
        params['signature'] = tx.signature.to_base64str()
        return params

    def to_full_data(self, tx: 'Transaction'):
        params = self.to_raw_data(tx)
        params['txHash'] = tx.hash.hex()
        return params

    def from_(self, tx_data: dict) -> 'Transaction':
        tx_data_copied = dict(tx_data)
        tx_data_copied.pop('signature', None)
        tx_data_copied.pop('txHash', None)

        tx_hash = self._hash_generator.generate_hash(tx_data_copied)

        nonce = tx_data.get('nonce')
        if nonce is not None:
            nonce = nonce

        value = tx_data.get('value')
        if value is not None:
            value = int(value, 16)

        return Transaction(
            hash=Hash32(tx_hash),
            signature=Signature.from_base64str(tx_data['signature']),
            timestamp=int(tx_data['timestamp'], 16),
            from_address=Address.fromhex(tx_data['from']),
            to_address=Address.fromhex(tx_data['to']),
            value=value,
            step_limit=int(tx_data['stepLimit'], 16),
            nonce=nonce,
            nid=int(tx_data['nid'], 16),
            data_type=tx_data.get('dataType'),
            data=tx_data.get('data')
        )

    def get_hash(self, tx_dumped: dict) -> str:
        return tx_dumped['txHash']