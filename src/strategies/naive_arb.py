import logging
from time import sleep
from src.utils.logger import *

logger = logging.getLogger("root")

class NaiveArb:
    def __init__(self, token0, token1, exchange1, exchange2, exchange1_pair, exchange2_pair):
        self.token0 = token0
        self.token1 = token1
        self.exchange1 = exchange1
        self.exchange2 = exchange2
        self.exchange1_pair = exchange1_pair
        self.exchange2_pair = exchange2_pair
        self._is_run = True

    def set_token0_size(self, size):
        self.token0_size = size * 10 ** self.token0[2]

    def buy_token1_exchange1(self, exchange1_reserve, exchange2_reserve):

        logger.info(f"Buy {self.token1[0]} @ {self.exchange1.name}, sell {self.token0[0]} @ {self.exchange2.name}")

        exchange1_token1_out = self.exchange1.router.functions.getAmountOut(self.token0_size, exchange1_reserve[0], exchange1_reserve[1]).call()
        exchange2_token0_out = self.exchange2.router.functions.getAmountOut(exchange1_token1_out, exchange2_reserve[1], exchange2_reserve[0]).call()
        
        trade_1 = f"{self.token0_size / 10 ** self.token0[2]} {self.token0[0]} -> {exchange1_token1_out / 10 ** self.token1[2]} {self.token1[0]}"
        trade_2 = f"{exchange1_token1_out / 10 ** self.token1[2]} {self.token1[0]} -> {exchange2_token0_out / 10 ** self.token0[2]} {self.token0[0]}"

        logger.info(f"{trade_1} @ {self.exchange1.name}")
        logger.info(f"{trade_2} @ {self.exchange2.name}")

        pnl = exchange2_token0_out/self.token0_size - 1
        logger.info(f"{(exchange2_token0_out-self.token0_size) / 10 ** self.token0[2]} {self.token0[0]} ({round(pnl*100, 5)}%)")

        if pnl > 0:
            ping_telegram(f"{trade_1} @ {self.exchange1.name}")
            ping_telegram(f"{trade_2} @ {self.exchange2.name}")
            ping_telegram(f"{(exchange2_token0_out-self.token0_size) / 10 ** self.token0[2]} {self.token0[0]} ({round(pnl*100, 5)}%)")


    def buy_token1_exchange2(self, exchange1_reserve, exchange2_reserve):

        logger.info(f"Buy {self.token1[0]} @ {self.exchange2.name}, sell {self.token0[0]} @ {self.exchange1.name}")

        exchange2_token1_out = self.exchange2.router.functions.getAmountOut(self.token0_size, exchange2_reserve[0], exchange2_reserve[1]).call()
        exchange1_token0_out = self.exchange1.router.functions.getAmountOut(exchange2_token1_out, exchange1_reserve[1], exchange1_reserve[0]).call()
        
        trade_1 = f"{self.token0_size / 10 ** self.token0[2]} {self.token0[0]} -> {exchange2_token1_out / 10 ** self.token1[2]} {self.token1[0]}"
        trade_2 = f"{exchange1_token0_out / 10 ** self.token1[2]} {self.token1[0]} -> {exchange1_token0_out / 10 ** self.token0[2]} {self.token0[0]}"

        logger.info(f"{trade_1} @ {self.exchange2.name}")
        logger.info(f"{trade_2} @ {self.exchange1.name}")

        pnl = exchange1_token0_out/self.token0_size - 1
        logger.info(f"{(exchange1_token0_out-self.token0_size) / 10 ** self.token0[2]} {self.token0[0]} ({round(pnl*100, 5)}%)")

        if pnl > 0:
            ping_telegram(f"{trade_1} @ {self.exchange2.name}")
            ping_telegram(f"{trade_2} @ {self.exchange1.name}")
            ping_telegram(f"{(exchange1_token0_out-self.token0_size) / 10 ** self.token0[2]} {self.token0[0]} ({round(pnl*100, 5)}%)")


    def run(self):
        while self._is_run:
            exchange1_reserve = self.exchange1_pair[1].functions.getReserves().call()
            exchange2_reserve = self.exchange2_pair[1].functions.getReserves().call()

            self.buy_token1_exchange1(exchange1_reserve, exchange2_reserve)
            self.buy_token1_exchange2(exchange1_reserve, exchange2_reserve)