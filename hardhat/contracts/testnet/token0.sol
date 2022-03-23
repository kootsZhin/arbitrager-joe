//// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Token0 is ERC20 {
    constructor(uint256 initialSupply) ERC20("Test Token 0", "TOKEN0") {
        _mint(msg.sender, initialSupply);
    }
}
