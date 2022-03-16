import json

FACTORY_ABI_PATH = "./src/abi/IUniswapV2Factory.json"
ROUTER_ABI_PATH = "./src/abi/IUniswapV2Router02.json"
PAIR_ABI_PATH = "./src/abi/IUniswapV2Pair.json"

class Dex():
    def __init__(self, web3_provider, factory_address, router_address):
        self.w3 = web3_provider
        self.factory_address = factory_address
        self.router_address = router_address
        
        self.factory = self._getContract(self.factory_address, FACTORY_ABI_PATH)
        self.router = self._getContract(self.router_address, ROUTER_ABI_PATH)

    def _getContract(self, address, abi_path):
        abi = json.load(open(abi_path))["abi"]
        return self.w3.eth.contract(
            address = address,
            abi = abi
        )

    def getPair(self, token0, token1):
        pair_address = self.factory.functions.getPair(token0, token1).call()
        return self._getContract(pair_address, PAIR_ABI_PATH)
        