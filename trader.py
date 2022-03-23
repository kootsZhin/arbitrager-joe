import json
import os

from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware

from src.constants import *
from src.strategies.naive_arb import NaiveArb
from src.utils.exchange_setup import Exchange
from src.utils.logger import *

logger = setup_custom_logger("root")
load_dotenv()

RINKEBY_INFURA_URL = os.getenv("RINKEBY_INFURA_URL")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

def setup_provider(provider):
    w3 = Web3(Web3.HTTPProvider(provider))
    logger.info(f"Provider is ready: {w3.isConnected()}")
    return w3

def setup_tokens(w3, token0, token1):
    a = token0 if token0 > token1 else token1
    b = token1 if token0 > token1 else token0

    abi = json.load(open("./src/abi/ERC20.json"))["abi"]

    a.append(w3.eth.contract(
        address = a[1],
        abi = abi
    ))

    b.append(w3.eth.contract(
        address = b[1],
        abi = abi
    ))

    logger.info(f"Token0: {a[0]}")
    logger.info(f"Token1: {b[0]}")

    return a, b

def setup_dexes(w3):
    Exchange0 = Exchange(web3_provider=w3, name="Uniswap", factory_address=RINKEBY_UNISWAP_FACTORY_ADDRESS, router_address=RINKEBY_UNISWAP_ROUTER_ADDRESS)
    Exchange1 = Exchange(web3_provider=w3, name="SUSHISWAP", factory_address=RINKEBY_SUSHISWAP_FACTORY_ADDRESS, router_address=RINKEBY_SUSHISWAP_ROUTER_ADDRESS)
    return Exchange0, Exchange1

def main(a, b):
    starting_log = f"Trader starting... Bot @ {PUBLIC_ADDRESS}"
    logger.info(starting_log)
    ping_telegram(starting_log)

    w3 = setup_provider(RINKEBY_INFURA_URL)
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    token0, token1 = setup_tokens(w3, a, b)

    Exchange0, Exchange1 = setup_dexes(w3)

    Exchange0_pair = Exchange0.getPair(token0[1], token1[1])
    Exchange1_pair = Exchange1.getPair(token0[1], token1[1])

    exchange0_log = f"{token0[0]}/{token1[0]} @ Uniswap {Exchange0_pair[0]}"
    exchange1_log = f"{token0[0]}/{token1[0]} @ Sushiswap {Exchange1_pair[0]}"

    logger.info(exchange0_log)
    logger.info(exchange1_log)

    ping_telegram(exchange0_log)
    ping_telegram(exchange1_log)

    # set target trade size
    executor = w3.eth.contract(
        address = RINKEBY_EXECUTOR,
        abi = json.load(open("./src/abi/Ape.json"))["abi"]
    )
    strategy = NaiveArb(w3, token0, token1, Exchange0, Exchange1, Exchange0_pair, Exchange1_pair, executor, PUBLIC_ADDRESS, PRIVATE_KEY)
    strategy.set_token0_size(1)

    strategy.run()

if __name__ == "__main__":
    main(RINKEBY_TOKEN0, RINKEBY_TOKEN1)
