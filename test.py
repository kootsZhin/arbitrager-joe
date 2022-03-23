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

    Exchange0 = Dex(
        web3_provider=w3,
        factory_address=JOE_FACTORY_ADDRESS,
        router_address=JOE_ROUTER_ADDRESS
    )
    Exchange0_pair = Exchange0.getPair(token0, token1)
    
    Exchange1 = Dex(
        web3_provider=w3,
        factory_address=PANGOLIN_FACTORY_ADDRESS,
        router_address=PANGOLIN_ROUTER_ADDRESS
    )
    Exchange1_pair = Exchange1.getPair(token0, token1)

    amount = 10**18

    # TODO: this is wrong, both are amount out
    Exchange0_price = getToken0Price(Exchange0_pair, Exchange0.router, amount)
    Exchange1_price = getToken0Price(Exchange1_pair, Exchange1.router, amount)

    bps = Exchange0_price/Exchange1_price - 1

    print(f"Exchange0: {Exchange0_price}")
    print(f"Exchange1: {Exchange1_price}")
    print(f"bps: {bps}")

if __name__ == "__main__":
    main()
