from abi.base_abi import BaseABI
from configurations import GeneralConfig, TOKENConfig


class ETHABI(BaseABI):

    def __init__(self):
        super().__init__(
            chain_id=GeneralConfig.BSC_CHAIN_ID,
            node_url=GeneralConfig.BSC_NODE_URL,
            config=TOKENConfig.ETH_CONTRACT
        )
    
    def _decimals(self):
        return self._send_read_request(
            abi=self._contract.functions._decimals()
        )
    
    def _name(self):
        return self._send_read_request(
            abi=self._contract.functions._name()
        )
    
    def _symbol(self):
        return self._send_read_request(
            abi=self._contract.functions._symbol()
        )
    
    def allowance(self, owner: str, spender: str):
        return self._send_read_request(
            abi=self._contract.functions.allowance(
                owner=owner,
                spender=spender,
            )
        )
    
    def approve(self, address: str, private_key: str, spender: str, amount: int):
        return self._send_write_request(
            address=address,
            private_key=private_key,
            abi=self._contract.functions.approve(
                spender=spender,
                amount=amount,
            )
        )
    
    def balanceOf(self, account: str):
        return self._send_read_request(
            abi=self._contract.functions.balanceOf(
                account=account,
            )
        )
    
    def burn(self, address: str, private_key: str, amount: int):
        return self._send_write_request(
            address=address,
            private_key=private_key,
            abi=self._contract.functions.burn(
                amount=amount,
            )
        )
    
    def decimals(self):
        return self._send_read_request(
            abi=self._contract.functions.decimals()
        )
    
    def decreaseAllowance(self, address: str, private_key: str, spender: str, subtracted_value: int):
        return self._send_write_request(
            address=address,
            private_key=private_key,
            abi=self._contract.functions.decreaseAllowance(
                spender=spender,
                subtractedValue=subtracted_value,
            )
        )
    
    def getOwner(self):
        return self._send_read_request(
            abi=self._contract.functions.getOwner()
        )
    
    def increaseAllowance(self, address: str, private_key: str, spender: str, added_value: int):
        return self._send_write_request(
            address=address,
            private_key=private_key,
            abi=self._contract.functions.increaseAllowance(
                spender=spender,
                addedValue=added_value,
            )
        )
    
    def mint(self, address: str, private_key: str, amount: int):
        return self._send_write_request(
            address=address,
            private_key=private_key,
            abi=self._contract.functions.mint(
                amount=amount,
            )
        )
    
    def name(self):
        return self._send_read_request(
            abi=self._contract.functions.name()
        )
    
    def owner(self):
        return self._send_read_request(
            abi=self._contract.functions.owner()
        )
    
    def renounceOwnership(self, address: str, private_key: str):
        return self._send_write_request(
            address=address,
            private_key=private_key,
            abi=self._contract.functions.renounceOwnership()
        )
    
    def symbol(self):
        return self._send_read_request(
            abi=self._contract.functions.symbol()
        )
    
    def totalSupply(self):
        return self._send_read_request(
            abi=self._contract.functions.totalSupply()
        )
    
    def transfer(self, address: str, private_key: str, recipient: str, amount: int):
        return self._send_write_request(
            address=address,
            private_key=private_key,
            abi=self._contract.functions.transfer(
                recipient=recipient,
                amount=amount,
            )
        )
    
    def transferFrom(self, address: str, private_key: str, sender: str, recipient: str, amount: int):
        return self._send_write_request(
            address=address,
            private_key=private_key,
            abi=self._contract.functions.transferFrom(
                sender=sender,
                recipient=recipient,
                amount=amount,
            )
        )
    
    def transferOwnership(self, address: str, private_key: str, new_owner: str):
        return self._send_write_request(
            address=address,
            private_key=private_key,
            abi=self._contract.functions.transferOwnership(
                newOwner=new_owner,
            )
        )
    