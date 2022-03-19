from web3 import Web3

from src.constants import *
from src.utils.exchange_setup import Exchange
from src.utils.logger import *
from src.strategies.naive_arb import NaiveArb

logger = setup_custom_logger("root")

def setup_provider():
    w3 = Web3(Web3.HTTPProvider(AVALANCHE_PUBLIC_RPC))
    logger.info(f"Provider is ready: {w3.isConnected()}")
    return w3

def setup_tokens(token0, token1):
    (token0, token1) = (token0, token1) if (token0 < token1) else (token1, token0)

    logger.info(f"Token0: {token0[0]}")
    logger.info(f"Token1: {token1[0]}")

    return token0, token1

def setup_dexes(w3):
    Joe = Exchange(web3_provider=w3, name="Joe", factory_address=JOE_FACTORY_ADDRESS, router_address=JOE_ROUTER_ADDRESS)
    Pangolin = Exchange(web3_provider=w3, name="Pangolin", factory_address=PANGOLIN_FACTORY_ADDRESS, router_address=PANGOLIN_ROUTER_ADDRESS)
    return Joe, Pangolin

def main(token0, token1):
    logger.info("Trader starting...")
    ping_telegram("Trader starting...")

    w3 = setup_provider()

    token0, token1 = setup_tokens(token0, token1)

    Joe, Pangolin = setup_dexes(w3)

    Joe_pair = Joe.getPair(token0[1], token1[1])
    Pangolin_pair = Pangolin.getPair(token0[1], token1[1])

    logger.info(f"{token0[0]}/{token1[0]} @ JOE {Joe_pair[0]}")
    logger.info(f"{token0[0]}/{token1[0]} @ PANGOLIN {Pangolin_pair[0]}")

    # set target trade size
    strategy = NaiveArb(token0, token1, Joe, Pangolin, Joe_pair, Pangolin_pair)
    strategy.set_token0_size(10)

    strategy.run()

if __name__ == "__main__":
    main(AVALANCHE_USDC, AVALANCHE_WAVAX)
