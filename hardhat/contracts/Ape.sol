//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@uniswap/v2-core/contracts/interfaces/IUniswapV2Pair.sol";
import "@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol";

contract Ape is Ownable {
    function ape(
        IUniswapV2Pair pair0,
        IUniswapV2Pair pair1,
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
            pair1,
            router0,
            router1,
            token0,
            token1,
            amount1
        );
        pair0.swap(amount0Out, amount1Out, address(this), data);
        require(token0Start < token0.balanceOf(address(this)), "GG");
    }

    function uniswapV2Call(
        address sender,
        uint256 amount0,
        uint256 amount1,
        bytes calldata data
    ) external {
        (
            IUniswapV2Pair pair0,
            IUniswapV2Pair pair1,
            IUniswapV2Router02 router0,
            IUniswapV2Router02 router1,
            IERC20 token0,
            IERC20 token1,
            uint256 amount1Check
        ) = abi.decode(
                data,
                (
                    IUniswapV2Pair,
                    IUniswapV2Pair,
                    IUniswapV2Router02,
                    IUniswapV2Router02,
                    IERC20,
                    IERC20,
                    uint256
                )
            );
        require(
            msg.sender == address(pair0),
            "Sender is not the targeted pair."
        );
        require(amount0 == 0, "Token0 amount is not 0.");
        require(amount1 == amount1Check, "Token1 amounts do not match.");
        require(
            amount1 == token1.balanceOf(address(this)),
            "Token1 balance does not match."
        );

        address[] memory path = new address[](2);
        path[0] = address(token1);
        path[1] = address(token0);

        uint256 returnAmount0 = ((1000 *
            token0.balanceOf(address(pair0)) *
            amount1) / (997 * token1.balanceOf(address(pair0)))) + 1;

        token1.approve(address(pair1), amount1);
        token1.approve(address(router1), amount1);

        router1.swapExactTokensForTokens(
            amount1,
            returnAmount0,
            path,
            address(this),
            block.timestamp + 60
        );
        token0.transfer(msg.sender, returnAmount0);
    }
}
