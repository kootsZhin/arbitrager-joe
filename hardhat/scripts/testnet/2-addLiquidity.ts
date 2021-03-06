// Uniswap factory is connected: true
// Sushiswap factory is connected: true
// Uniswap pair is created: 0x4862AC55395067cF560087d08aF35082Bf4EecD5
// Sushiswap pair is created: 0xd7200a23311e4107740247708dD6B384F131B8f0
// Succefully added liquidity to the exhcanges!

import { expect } from "chai";
import { ethers } from "hardhat";
import { execPath } from "process";
import { Token0 } from "../../typechain";

const UNISWAP_RINKEBY_FACTORY = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f";
const SUSHISWAP_RINKEBY_FACTORY = "0xc35DADB65012eC5796536bD9864eD8773aBc74C4";

const UNISWAP_RINKEBY_ROUTER = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
const SUSHISWAP_RINKEBY_ROUTER = "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506";

const TOKEN0_ADDRESS = "0x08671a22962e961190Eb2dee3571c78e09d167bd";
const TOKEN1_ADDRESS = "0x03a8FcE0A63AAc36bD37c8be9964293dAAd2aA80";

async function main() {
    const [deployer] = await ethers.getSigners();
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

    // Check pools exist
    const uniPairAddress = await uniFactory.getPair(TOKEN0_ADDRESS, TOKEN1_ADDRESS);
    const uniPair = await ethers.getContractAt("IUniswapV2Pair", uniPairAddress);
    console.log(
        "Uniswap pair is created:",
        uniPairAddress
    )

    const sushiPairAddress = await sushiFactory.getPair(TOKEN0_ADDRESS, TOKEN1_ADDRESS);
    const sushiPair = await ethers.getContractAt("IUniswapV2Pair", sushiPairAddress);
    console.log(
        "Sushiswap pair is created:",
        sushiPairAddress
    )

    // Set up testnet routers
    const uniRouter = await ethers.getContractAt("IUniswapV2Router02", UNISWAP_RINKEBY_ROUTER)
    const sushiRouter = await ethers.getContractAt("IUniswapV2Router02", SUSHISWAP_RINKEBY_ROUTER)
    expect(await uniRouter.factory()).to.equal(UNISWAP_RINKEBY_FACTORY);
    expect(await sushiRouter.factory()).to.equal(SUSHISWAP_RINKEBY_FACTORY);

    // Approve tokens
    const token0 = await ethers.getContractAt("IERC20", TOKEN0_ADDRESS)
    const token1 = await ethers.getContractAt("IERC20", TOKEN1_ADDRESS)

    await token0.approve(UNISWAP_RINKEBY_ROUTER, ethers.constants.MaxInt256);
    await token0.approve(SUSHISWAP_RINKEBY_ROUTER, ethers.constants.MaxInt256);
    await token1.approve(UNISWAP_RINKEBY_ROUTER, ethers.constants.MaxInt256);
    await token1.approve(SUSHISWAP_RINKEBY_ROUTER, ethers.constants.MaxInt256);

    // Add liquidity
    const blockNumBefore = await ethers.provider.getBlockNumber();
    const blockBefore = await ethers.provider.getBlock(blockNumBefore);

    await uniRouter.addLiquidity(
        TOKEN0_ADDRESS,
        TOKEN1_ADDRESS,
        ethers.utils.parseEther("2000"),
        ethers.utils.parseEther("8000"),
        ethers.utils.parseEther("2000"),
        ethers.utils.parseEther("8000"),
        deployer.address,
        blockBefore.timestamp + 3600
    );

    await sushiRouter.addLiquidity(
        TOKEN0_ADDRESS,
        TOKEN1_ADDRESS,
        ethers.utils.parseEther("8000"),
        ethers.utils.parseEther("2000"),
        ethers.utils.parseEther("8000"),
        ethers.utils.parseEther("2000"),
        deployer.address,
        blockBefore.timestamp + 3600
    );

    // Get reserves after adding liquidity
    const uniReserves = await uniPair.getReserves();
    const sushiReserves = await sushiPair.getReserves();

    expect(uniReserves[0]).be.equal(ethers.utils.parseEther("8000"));
    expect(uniReserves[1]).be.equal(ethers.utils.parseEther("2000"));
    expect(sushiReserves[0]).be.equal(ethers.utils.parseEther("2000"));
    expect(sushiReserves[1]).be.equal(ethers.utils.parseEther("8000"));

    console.log("Succefully added liquidity to the exhcanges!")
};

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
