// Deployed token0 at 0x08671a22962e961190Eb2dee3571c78e09d167bd
// Deployed token1 at 0x03a8FcE0A63AAc36bD37c8be9964293dAAd2aA80
// Uniswap factory is connected: true
// Sushiswap factory is connected: true

import { expect } from "chai";
import { ethers } from "hardhat";

const UNISWAP_RINKEBY_FACTORY = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f";
const SUSHISWAP_RINKEBY_FACTORY = "0xc35DADB65012eC5796536bD9864eD8773aBc74C4";

async function main() {
    // Deploy test tokens
    const Token0 = await ethers.getContractFactory("Token0");
    const token0 = await Token0.deploy(ethers.utils.parseEther("10000"));
    await token0.deployed;
    console.log("Deployed token0 at", await token0.address);

    const Token1 = await ethers.getContractFactory("Token1");
    const token1 = await Token1.deploy(ethers.utils.parseEther("10000"));
    await token1.deployed;
    console.log("Deployed token1 at", await token1.address);

    // Set up testnet exchanges
    const uniFactory = await ethers.getContractAt("IUniswapV2Factory", UNISWAP_RINKEBY_FACTORY);
    console.log(
        "Uniswap factory is connected:",
        (await uniFactory.allPairsLength()) !== undefined ? true : false
    )

    const sushiFactory = await ethers.getContractAt("IUniswapV2Factory", SUSHISWAP_RINKEBY_FACTORY);
    console.log(
        "Sushiswap factory is connected:",
        (await sushiFactory.allPairsLength()) !== undefined ? true : false
    )

    // Create Pools
    const uniPair = await uniFactory.createPair(token0.address, token1.address);
    const sushiPair = await sushiFactory.createPair(token0.address, token1.address);
};

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
