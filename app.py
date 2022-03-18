from web3 import Web3

from src.constants import *
from src.utils.helpers import *
from src.utils.dex_helper import Dex

def main(token0, token1):
    #set up provider
    w3 = Web3(Web3.HTTPProvider(AVALANCHE_PUBLIC_RPC))

    print("Provider is ready:", w3.isConnected())

    # set up tokens
    token0, token1 = get_token0_token1(token0, token1)

    print(f"Token0: {token0[0]}")
    print(f"Token1: {token1[0]}")

    # set up dexes
    Joe = Dex(web3_provider=w3, factory_address=JOE_FACTORY_ADDRESS, router_address=JOE_ROUTER_ADDRESS)
    Pangolin = Dex(web3_provider=w3, factory_address=PANGOLIN_FACTORY_ADDRESS, router_address=PANGOLIN_ROUTER_ADDRESS)

    # get pairs
    JOE_PAIR_ADDRESS, Joe_pair = Joe.getPair(token0[1], token1[1])
    PANGOLIN_PAIR_ADDERSS, Pangolin_pair = Pangolin.getPair(token0[1], token1[1])

    print(f"{token0[0]}/{token1[0]} @ JOE", JOE_PAIR_ADDRESS)
    print(f"{token0[0]}/{token1[0]} @ PANGOLIN", PANGOLIN_PAIR_ADDERSS)

    # set target trade size
    size = (10, 1) # 10 * token1 (USDT)


if __name__ == "__main__":
    main(AVALANCHE_JOE, AVALANCHE_USDT)
