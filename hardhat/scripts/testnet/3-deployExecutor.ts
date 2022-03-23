// Succefully deployed contract at: 0x41a879537E1e0367D7137802d4DAfe0C5759e10b

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
