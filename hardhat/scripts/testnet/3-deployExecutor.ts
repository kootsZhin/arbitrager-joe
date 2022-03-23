// Succefully deployed contract at: 0x9C90139BB93BB4b8eeC51ed6B2a25856aD255a8C

import { expect } from "chai";
import { ethers } from "hardhat";
import { execPath } from "process";
import { Token0 } from "../../typechain";

async function main() {
    const Ape = await ethers.getContractFactory("Ape");
    const ape = await Ape.deploy();

    await ape.deployed();

    console.log("Succefully deployed contract at:", ape.address)
};

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
