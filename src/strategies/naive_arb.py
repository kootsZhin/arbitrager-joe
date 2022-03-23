import logging
from time import sleep
from src.utils.logger import *

logger = logging.getLogger("root")

class NaiveArb:
    def __init__(self, w3, token0, token1, exchange0, exchange1, exchange0_pair, exchange1_pair, executor, key):
        self.w3 = w3
        self.token0 = token0
        self.token1 = token1
        self.exchange0 = exchange0
        self.exchange1 = exchange1
        self.exchange0_pair = exchange0_pair
        self.exchange1_pair = exchange1_pair
        self.executor = executor;
        self.key = key
        self._is_run = True

    def set_token0_size(self, size):
        self.token0_size = size * 10 ** self.token0[2]

    def buy_token1_exchange0(self, exchange0_reserve, exchange1_reserve):

        logger.info(f"Buy {self.token1[0]} @ {self.exchange0.name}, sell {self.token0[0]} @ {self.exchange1.name}")

        exchange0_token1_out = self.exchange0.router.functions.getAmountOut(self.token0_size, exchange0_reserve[0], exchange0_reserve[1]).call()
        exchange1_token0_out = self.exchange1.router.functions.getAmountOut(exchange0_token1_out, exchange1_reserve[1], exchange1_reserve[0]).call()
        
        trade_1 = f"{self.token0_size / 10 ** self.token0[2]} {self.token0[0]} -> {exchange0_token1_out / 10 ** self.token1[2]} {self.token1[0]}"
        trade_2 = f"{exchange0_token1_out / 10 ** self.token1[2]} {self.token1[0]} -> {exchange1_token0_out / 10 ** self.token0[2]} {self.token0[0]}"

        # logger.info(f"{trade_1} @ {self.exchange0.name}")
        # logger.info(f"{trade_2} @ {self.exchange1.name}")

        pnl = exchange1_token0_out/self.token0_size - 1
        # logger.info(f"PNL: {(exchange1_token0_out-self.token0_size) / 10 ** self.token0[2]} {self.token0[0]} ({round(pnl*100, 5)}%)")

        if pnl > 0:
            ping_telegram(
                "Trade Opportunity\n\n" + \
                f"{trade_1} @ {self.exchange0.name}\n" + \
                f"{trade_2} @ {self.exchange1.name}\n"+ \
                f"{(exchange1_token0_out-self.token0_size) / 10 ** self.token0[2]} {self.token0[0]} ({round(pnl*100, 5)}%)"
            )

    def buy_token1_exchange1(self, exchange0_reserve, exchange1_reserve):

        logger.info(f"Buy {self.token1[0]} @ {self.exchange1.name}, sell {self.token0[0]} @ {self.exchange0.name}")

        exchange1_token1_out = self.exchange1.router.functions.getAmountOut(self.token0_size, exchange1_reserve[0], exchange1_reserve[1]).call()
        exchange0_token0_out = self.exchange0.router.functions.getAmountOut(exchange1_token1_out, exchange0_reserve[1], exchange0_reserve[0]).call()
        
        trade_1 = f"{self.token0_size / 10 ** self.token0[2]} {self.token0[0]} -> {exchange1_token1_out / 10 ** self.token1[2]} {self.token1[0]}"
        trade_2 = f"{exchange1_token1_out / 10 ** self.token1[2]} {self.token1[0]} -> {exchange0_token0_out / 10 ** self.token0[2]} {self.token0[0]}"

        # logger.info(f"{trade_1} @ {self.exchange1.name}")
        # logger.info(f"{trade_2} @ {self.exchange0.name}")

        pnl = exchange0_token0_out/self.token0_size - 1
        logger.info(f"PNL: {(exchange0_token0_out-self.token0_size) / 10 ** self.token0[2]} {self.token0[0]} ({round(pnl*100, 5)}%)")

        if pnl > 0:
            print(self.exchange1_pair[0])
            print(self.exchange0_pair[0])
            print(exchange0_token0_out)
            tx = self.executor.functions.ape(
                self.exchange1_pair[0],
                self.exchange0_pair[0],
                self.exchange1.router_address,
                self.exchange0.router_address,
                self.token0[1],
                self.token1[1],
                exchange1_token1_out
            ).buildTransaction({
                "from": "0x058C6fC2cDf791e7B2516E931F112CC5556077Bc",
                "gas": 2500000,
                "nonce": self.w3.eth.get_transaction_count("0x058C6fC2cDf791e7B2516E931F112CC5556077Bc")
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.key)
            h = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction).hex()
            print(h)
            # ping_telegram(
            #     "Trade Opportunity\n\n" + \
            #     f"{trade_1} @ {self.exchange1.name}\n" + \
            #     f"{trade_2} @ {self.exchange0.name}\n" + \
            #     f"{(exchange0_token0_out-self.token0_size) / 10 ** self.token0[2]} {self.token0[0]} ({round(pnl*100, 5)}%)"
            # )


    def run(self):
        while self._is_run:
            exchange0_reserve = self.exchange0_pair[1].functions.getReserves().call()
            exchange1_reserve = self.exchange1_pair[1].functions.getReserves().call()
            print(exchange0_reserve)
            print(exchange1_reserve)
            self.buy_token1_exchange0(exchange0_reserve, exchange1_reserve)
            self.buy_token1_exchange1(exchange0_reserve, exchange1_reserve)