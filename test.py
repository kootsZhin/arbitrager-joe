from web3 import Web3

from src.constants import *
from src.utils.dex_helper import Dex
from src.utils import *

def getToken0Price(pair, router, amount):
    token0_reserve, token1_reserve = pair.functions.getReserves().call()[:2]
    return router.functions.getAmountOut(amount, token0_reserve, token1_reserve).call()

def main():
    w3 = Web3(Web3.HTTPProvider(AVALANCHE_PUBLIC_RPC))

    token0, token1 = get_token0_token1_address(AVALANCHE_JOE_ADDRESS, AVALANCHE_USDT_ADDRESS)

    Joe = Dex(
        web3_provider=w3,
        factory_address=JOE_FACTORY_ADDRESS,
        router_address=JOE_ROUTER_ADDRESS
    )
    Joe_pair = Joe.getPair(token0, token1)
    
    Pangolin = Dex(
        web3_provider=w3,
        factory_address=PANGOLIN_FACTORY_ADDRESS,
        router_address=PANGOLIN_ROUTER_ADDRESS
    )
    Pangolin_pair = Pangolin.getPair(token0, token1)

    amount = 10**18

    # TODO: this is wrong, both are amount out
    Joe_price = getToken0Price(Joe_pair, Joe.router, amount)
    Pangolin_price = getToken0Price(Pangolin_pair, Pangolin.router, amount)

    bps = Joe_price/Pangolin_price - 1

    print(f"Joe: {Joe_price}")
    print(f"Pangolin: {Pangolin_price}")
    print(f"bps: {bps}")

if __name__ == "__main__":
    main()
