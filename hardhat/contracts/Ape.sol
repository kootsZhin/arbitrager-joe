//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@uniswap/v2-core/contracts/interfaces/IUniswapV2Pair.sol";
import "@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol";

contract Ape is Ownable {
    function ape(
        IUniswapV2Pair pair0,
        IUniswapV2Router02 router0,
        IUniswapV2Router02 router1,
        IERC20 token0,
        IERC20 token1,
        uint256 amount1
    ) external onlyOwner {
        uint256 token0Start = token0.balanceOf(address(this));
        uint256 amount0Out = 0;
        uint256 amount1Out = amount1;
        bytes memory data = abi.encode(
            pair0,
            router0,
            router1,
            token0,
            token1,
            amount1
        );
        pair0.swap(amount0Out, amount1Out, address(this), data);
        require(token0Start > token0.balanceOf(address(this)), "GG");
    }

    function uniswapV2Call(
        address sender,
        uint256 amount0,
        uint256 amount1,
        bytes calldata data
    ) public {
        (
            IUniswapV2Pair pair0,
            IUniswapV2Router02 router0,
            IUniswapV2Router02 router1,
            IERC20 token0,
            IERC20 token1,
            uint256 amount1Check
        ) = abi.decode(
                data,
                (
                    IUniswapV2Pair,
                    IUniswapV2Router02,
                    IUniswapV2Router02,
                    IERC20,
                    IERC20,
                    uint256
                )
            );
        require(sender == msg.sender, "Senders not match");
        require(
            msg.sender == address(pair0),
            "Sender is not the targeted pair."
        );
        require(amount0 == 0, "amount0 is not 0.");
        require(amount1 == amount1Check, "Token1 amounts do not match.");

        address[] memory path0 = new address[](2);
        path0[0] = address(token0);
        path0[1] = address(token1);

        address[] memory path1 = new address[](2);
        path1[0] = address(token1);
        path1[1] = address(token0);

        uint256 returnAmount0 = router0.getAmountsIn(amount1, path0)[0];

        token1.approve(address(router1), amount1);

        router1.swapExactTokensForTokens(
            amount1,
            0,
            path1,
            address(this),
            block.timestamp + 3600
        );

        token0.transfer(sender, returnAmount0);
    }
}
