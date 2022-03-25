import { SignerWithAddress } from "@nomiclabs/hardhat-ethers/signers";
import { expect } from "chai";
import { ethers } from "hardhat";
import { Token0 } from "../typechain";

describe("Ape", function () {
    const MAX_SUPPLY = ethers.utils.parseEther("10000");

    let lp: SignerWithAddress,
        deployer: SignerWithAddress,
        dev0: SignerWithAddress,
        dev1: SignerWithAddress,
        unknown: SignerWithAddress;

    before(async function () {
        [lp, deployer, dev0, dev1, unknown] = await ethers.getSigners();

        this.Factory0 = await ethers.getContractFactory("UniswapV2Factory");
        this.Factory1 = await ethers.getContractFactory("UniswapV2Factory");
        this.Router0 = await ethers.getContractFactory("UniswapV2Router02");
        this.Router1 = await ethers.getContractFactory("UniswapV2Router02");

        this.Token0 = await ethers.getContractFactory("Token0");
        this.Token1 = await ethers.getContractFactory("Token1");
        this.Weth = await ethers.getContractFactory("WETH9");

        this.Ape = await ethers.getContractFactory("Ape", deployer);
    })

    beforeEach(async function () {
        const blockNumBefore = await ethers.provider.getBlockNumber();
        const blockBefore = await ethers.provider.getBlock(blockNumBefore);

        this.factory0 = await this.Factory0.connect(dev0).deploy(dev0.address);
        this.factory1 = await this.Factory1.connect(dev1).deploy(dev1.address);

        this.token0 = await this.Token0.connect(lp).deploy(MAX_SUPPLY);
        this.token1 = await this.Token1.connect(lp).deploy(MAX_SUPPLY);
        this.weth = await this.Weth.connect(lp).deploy();

        this.router0 = await this.Router0.connect(dev0).deploy(this.factory0.address, this.weth.address);
        this.router1 = await this.Router1.connect(dev1).deploy(this.factory1.address, this.weth.address);
        expect(await this.router0.factory()).to.equal(this.factory0.address);
        expect(await this.router1.factory()).to.equal(this.factory1.address);

        this.token0.connect(lp).approve(this.router0.address, MAX_SUPPLY);
        this.token0.connect(lp).approve(this.router1.address, MAX_SUPPLY);
        this.token1.connect(lp).approve(this.router0.address, MAX_SUPPLY);
        this.token1.connect(lp).approve(this.router1.address, MAX_SUPPLY);

        await this.router0.connect(lp).addLiquidity(
            this.token0.address,
            this.token1.address,
            ethers.utils.parseEther("8000"),
            ethers.utils.parseEther("2000"),
            ethers.utils.parseEther("8000"),
            ethers.utils.parseEther("2000"),
            lp.address,
            blockBefore.timestamp + 60
        );

        this.ape = await this.Ape.deploy();
    })

    it("dummy", async function () {

    })
})