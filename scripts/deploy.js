
const { ethers } = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
    console.log("Memulai deployment AmalTransparan...");

    const AmalTransparan = await ethers.getContractFactory("AmalTransparan");
    const amal = await AmalTransparan.deploy();

    await amal.waitForDeployment();

    const contractAddress = await amal.getAddress();
    const network = await ethers.provider.getNetwork();

    const deploymentData = {
        contractName: "AmalTransparan",
        address: contractAddress,
        network: "localhost",
        chainId: Number(network.chainId)
    };

    const deploymentPath = path.join(__dirname, "..", "deployment.json");

    fs.writeFileSync(
        deploymentPath,
        JSON.stringify(deploymentData, null, 4)
    );

    console.log("==================================");
    console.log("AmalTransparan berhasil di-deploy!");
    console.log("Alamat kontrak:", contractAddress);
    console.log("Network:", "localhost");
    console.log("Chain ID:", Number(network.chainId));
    console.log("Alamat tersimpan di deployment.json");
    console.log("==================================");
}

main().catch((error) => {
    console.error("Deployment gagal:", error);
    process.exitCode = 1;
});
