import logging
from time import sleep
from src.utils.logger import *

logger = logging.getLogger("root")

class NaiveArb:
    def __init__(self, w3, token0, token1, exchange0, exchange1, exchange0_pair, exchange1_pair, executor, address, key):
        self.w3 = w3
        self.token0 = token0
        self.token1 = token1
        self.exchange0 = exchange0
        self.exchange1 = exchange1
        self.exchange0_pair = exchange0_pair
        self.exchange1_pair = exchange1_pair
        self.executor = executor;
        self.address = address
        self.key = key
        self._update_balance()
        self._is_run = True


    def set_token0_size(self, size):
        self.token0_size = size * 10 ** self.token0[2]
        size_log = f"Set token0 trading size to {size} {self.token0[0]}"
        logging.info(size_log)
        ping_telegram(size_log)


    def _update_balance(self):
        self.token0_bal = self.token0[3].functions.balanceOf(self.address).call() / 10 ** self.token0[2]
        self.token1_bal = self.token1[3].functions.balanceOf(self.address).call() / 10 ** self.token1[2]


    def ape(self, pair0, pair1, router0, router1, token0, token1, amount1):

        token0_before = self.token0_bal
        token1_before = self.token1_bal

        aping_log = f"Aping: token0 - {token0_before}, token1 - {token1_before}"
        logger.info(aping_log)
        ping_telegram(aping_log)

        tx = self.executor.functions.ape(
                pair0, pair1, router0, router1, token0, token1, amount1
            ).buildTransaction({
                "from": self.address,
                "gas": 2500000,
                "nonce": self.w3.eth.get_transaction_count(self.address)
            })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.key)
        h = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction).hex()

        self.w3.eth.wait_for_transaction_receipt(h)

        self._update_balance()

        token0_after = self.token0_bal
        token1_after = self.token1_bal

        
        token0_diff = token0_after - token0_before
        token0_pnl = (token0_diff / token0_before) if token0_diff else token0_diff

        token1_diff = token1_after - token1_before
        token1_pnl = (token1_diff / token31_before) if token1_diff else token1_diff

        aped_log = \
        f"Aped: token0 - {token0_after}, token1 - {token1_after}\n" + \
        f"Token0: diff - {round(token0_diff, 3)}, pnl - {round(token0_pnl*100, 3)}%\n" + \
        f"Token1: diff - {round(token1_diff, 3)}, pnl - {round(token1_pnl*100, 3)}%\n" + \
        f"TX hash: {h}"

        logger.info(aped_log)
        ping_telegram(aped_log)


    def buy_token1_exchange0(self, exchange0_reserve, exchange1_reserve):

        logger.debug(f"Buy {self.token1[0]} @ {self.exchange0.name}, sell {self.token0[0]} @ {self.exchange1.name}")

        exchange0_token1_out = self.exchange0.router.functions.getAmountOut(self.token0_size, exchange0_reserve[0], exchange0_reserve[1]).call()
        exchange1_token0_out = self.exchange1.router.functions.getAmountOut(exchange0_token1_out, exchange1_reserve[1], exchange1_reserve[0]).call()
        
        trade_1 = f"{self.token0_size / 10 ** self.token0[2]} {self.token0[0]} -> {exchange0_token1_out / 10 ** self.token1[2]} {self.token1[0]}"
        trade_2 = f"{exchange0_token1_out / 10 ** self.token1[2]} {self.token1[0]} -> {exchange1_token0_out / 10 ** self.token0[2]} {self.token0[0]}"

        logger.debug(f"{trade_1} @ {self.exchange0.name}")
        logger.debug(f"{trade_2} @ {self.exchange1.name}")

        pnl = exchange1_token0_out/self.token0_size - 1
        logger.debug(f"PNL: {(exchange1_token0_out-self.token0_size) / 10 ** self.token0[2]} {self.token0[0]} ({round(pnl*100, 5)}%)")

        if pnl > 0:
             self.ape(
                self.exchange0_pair[0],
                self.exchange1_pair[0],
                self.exchange0.router_address,
                self.exchange1.router_address,
                self.token0[1],
                self.token1[1],
                exchange0_token1_out
            )


    def buy_token1_exchange1(self, exchange0_reserve, exchange1_reserve):

        logger.debug(f"Buy {self.token1[0]} @ {self.exchange1.name}, sell {self.token0[0]} @ {self.exchange0.name}")

        exchange1_token1_out = self.exchange1.router.functions.getAmountOut(self.token0_size, exchange1_reserve[0], exchange1_reserve[1]).call()
        exchange0_token0_out = self.exchange0.router.functions.getAmountOut(exchange1_token1_out, exchange0_reserve[1], exchange0_reserve[0]).call()
        
        trade_1 = f"{self.token0_size / 10 ** self.token0[2]} {self.token0[0]} -> {exchange1_token1_out / 10 ** self.token1[2]} {self.token1[0]}"
        trade_2 = f"{exchange1_token1_out / 10 ** self.token1[2]} {self.token1[0]} -> {exchange0_token0_out / 10 ** self.token0[2]} {self.token0[0]}"

        logger.debug(f"{trade_1} @ {self.exchange1.name}")
        logger.debug(f"{trade_2} @ {self.exchange0.name}")

        pnl = exchange0_token0_out/self.token0_size - 1
        logger.debug(f"PNL: {(exchange0_token0_out-self.token0_size) / 10 ** self.token0[2]} {self.token0[0]} ({round(pnl*100, 5)}%)")

        if pnl > 0:
            self.ape(
                self.exchange1_pair[0],
                self.exchange0_pair[0],
                self.exchange1.router_address,
                self.exchange0.router_address,
                self.token0[1],
                self.token1[1],
                exchange1_token1_out
            )



    def run(self):
        while self._is_run:
            exchange0_reserve = self.exchange0_pair[1].functions.getReserves().call()
            exchange1_reserve = self.exchange1_pair[1].functions.getReserves().call()

            self.buy_token1_exchange0(exchange0_reserve, exchange1_reserve)
            self.buy_token1_exchange1(exchange0_reserve, exchange1_reserve)