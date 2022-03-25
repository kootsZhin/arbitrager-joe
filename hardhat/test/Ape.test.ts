import { SignerWithAddress } from "@nomiclabs/hardhat-ethers/signers";
import { expect } from "chai";
import { ethers } from "hardhat";

const factoryJson = require("@uniswap/v2-core/build/UniswapV2Factory.json");
const routerJson = require("@uniswap/v2-periphery/build/UniswapV2Router02.json");
const pairJson = require("@uniswap/v2-core/build/UniswapV2Pair.json");

const MAX_SUPPLY = ethers.utils.parseEther("10000");
const HIGH_POS = ethers.utils.parseEther("8000");
const LOW_POS = ethers.utils.parseEther("2000");

describe("Ape", function () {

    let lp: SignerWithAddress,
        deployer: SignerWithAddress,
        dev0: SignerWithAddress,
        dev1: SignerWithAddress,
        unknown: SignerWithAddress;

    before(async function () {
        [lp, deployer, dev0, dev1, unknown] = await ethers.getSigners();

        this.Factory = new ethers.ContractFactory(factoryJson.abi, factoryJson.bytecode, dev0);
        this.Router = new ethers.ContractFactory(routerJson.abi, routerJson.bytecode, dev0);
        this.Pair = new ethers.ContractFactory(pairJson.abi, pairJson.bytecode, dev0);

        this.Token0 = await ethers.getContractFactory("Token0");
        this.Token1 = await ethers.getContractFactory("Token1");
        this.Weth = await ethers.getContractFactory("WETH9");

        this.Ape = await ethers.getContractFactory("Ape", deployer);
    })

    beforeEach(async function () {
        const blockNumBefore = await ethers.provider.getBlockNumber();
        const blockBefore = await ethers.provider.getBlock(blockNumBefore);

        this.factory0 = await this.Factory.connect(dev0).deploy(dev0.address);
        this.factory1 = await this.Factory.connect(dev1).deploy(dev1.address);

        this.token0 = await this.Token0.connect(lp).deploy(MAX_SUPPLY);
        this.token1 = await this.Token1.connect(lp).deploy(MAX_SUPPLY);
        this.weth = await this.Weth.connect(lp).deploy();

        this.router0 = await this.Router.connect(dev0).deploy(this.factory0.address, this.weth.address);
        this.router1 = await this.Router.connect(dev1).deploy(this.factory1.address, this.weth.address);
        expect(await this.router0.factory()).to.equal(this.factory0.address);
        expect(await this.router1.factory()).to.equal(this.factory1.address);

        this.token0.connect(lp).approve(this.router0.address, MAX_SUPPLY);
        this.token0.connect(lp).approve(this.router1.address, MAX_SUPPLY);
        this.token1.connect(lp).approve(this.router0.address, MAX_SUPPLY);
        this.token1.connect(lp).approve(this.router1.address, MAX_SUPPLY);

        await this.router0.connect(lp).addLiquidity(
            this.token0.address,
            this.token1.address,
            HIGH_POS,
            LOW_POS,
            HIGH_POS,
            LOW_POS,
            lp.address,
            blockBefore.timestamp + 60
        );
        this.pair0 = await this.Pair.attach(
            await this.factory0.getPair(this.token0.address, this.token1.address)
        );
        expect(await this.token0.balanceOf(this.pair0.address)).to.equal(HIGH_POS);
        expect(await this.token1.balanceOf(this.pair0.address)).to.equal(LOW_POS);

        await this.router1.connect(lp).addLiquidity(
            this.token0.address,
            this.token1.address,
            LOW_POS,
            HIGH_POS,
            LOW_POS,
            HIGH_POS,
            lp.address,
            blockBefore.timestamp + 60
        );
        this.pair1 = await this.Pair.attach(
            await this.factory1.getPair(this.token0.address, this.token1.address)
        );
        expect(await this.token0.balanceOf(this.pair1.address)).to.equal(LOW_POS);
        expect(await this.token1.balanceOf(this.pair1.address)).to.equal(HIGH_POS);

        expect(await this.token0.balanceOf(lp.address)).to.equal(ethers.constants.Zero);
        expect(await this.token1.balanceOf(lp.address)).to.equal(ethers.constants.Zero);

        this.ape = await this.Ape.deploy();
    })

    it("dummy", async function () {

    })
})