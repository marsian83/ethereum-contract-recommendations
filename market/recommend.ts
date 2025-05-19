import { createPublicClient, http, keccak256 } from "viem";
import { mainnet } from "viem/chains";
import axios from "axios";
import { readFileSync, writeFileSync, existsSync } from "fs";

const ADDRESS = Bun.argv[2];
console.log(`\nGenerating suggestions for address : ${ADDRESS}\n`);

let codeCache: { codeExists: Record<string, boolean> } = { codeExists: {} };
try {
  if (existsSync("./market/recommend.cache")) {
    const cacheContent = readFileSync("./market/recommend.cache", "utf-8");
    if (cacheContent.trim()) {
      codeCache = JSON.parse(cacheContent);
    }
  }
} catch (error) {
  console.log("Error loading cache, creating new cache");
}

const publicClient = createPublicClient({
  chain: mainnet,
  transport: http(),
});

async function getCachedCode(address: string): Promise<boolean> {
  if (
    !address ||
    address === "0x" ||
    address === "0x0" ||
    address.length < 10
  ) {
    return false;
  }

  if (address in codeCache.codeExists) {
    return codeCache.codeExists[address];
  }

  try {
    const code = await publicClient.getCode({ address: address as "0x" });
    const hasCode = code !== "0x";

    codeCache.codeExists[address] = hasCode;
    return hasCode;
  } catch (error) {
    codeCache.codeExists[address] = false;
    return false;
  }
}

function saveCache() {
  try {
    writeFileSync(
      "./market/recommend.cache",
      JSON.stringify(codeCache, null, 2)
    );
  } catch (error) {
    console.log("Error saving cache:", error);
  }
}

const { data } = await axios.get("https://api.etherscan.io/v2/api", {
  params: {
    module: "account",
    action: "txlist",
    address: ADDRESS,
    chainId: 1,
    sort: "desc",
    apiKey: "NTGCF7RQMY8YN7F3KWBZV53SWHG5VQRIJA",
  },
});

const { data: tokens } = await axios.get("https://api.etherscan.io/api", {
  params: {
    module: "account",
    action: "tokentx",
    address: ADDRESS,
    sort: "desc",
    apikey: "NTGCF7RQMY8YN7F3KWBZV53SWHG5VQRIJA",
  },
});

const transactions = data.result
  .slice(0, 100)
  .concat(tokens.result.slice(0, 100));

const totalTransactions = transactions.length;

if (totalTransactions < 30) {
  throw new Error("Not enough transactions to recommend new contracts.");
}

let contractInteractions: Record<string, number> = {};

let progress = 0;

for (const tx of transactions) {
  const { to, from, contractAddress } = tx;

  const toHasCode = await getCachedCode(to);
  const fromHasCode = await getCachedCode(from);

  progress++;
  process.stdout.write("\r" + " ".repeat(8) + "\r");
  process.stdout.write(
    `${Math.floor((progress / totalTransactions) * 100)
      .toString()
      .padStart(2, "0")}% done`
  );

  if (toHasCode) {
    if (contractInteractions[to]) {
      contractInteractions[to]++;
    } else {
      contractInteractions[to] = 1;
    }
  }
  if (fromHasCode) {
    if (contractInteractions[from]) {
      contractInteractions[from]++;
    } else {
      contractInteractions[from] = 1;
    }
  }
  if (contractAddress && contractAddress !== "0x") {
    const contractHasCode = await getCachedCode(contractAddress);
    if (contractHasCode && contractInteractions[contractAddress]) {
      contractInteractions[contractAddress]++;
    } else if (contractHasCode) {
      contractInteractions[contractAddress] = 1;
    }
  }

  if (progress % 20 === 0) {
    saveCache();
  }
}

saveCache();

const contracts = Object.keys(contractInteractions).sort(
  (a, b) => contractInteractions[b] - contractInteractions[a]
);

if (contracts.length < 5) {
  throw new Error("Not enough contracts to recommend new contracts.");
}

let suggestions = contracts.slice(0, 10);

const considered = contracts.slice(0, 30);

let numerator = 500n;
let denominator = 1n;
for (let i = 0; i < considered.length - 3; i += 2) {
  const contract = considered[i];
  if (!contract) continue;
  const addressAsInt = BigInt(contract);
  numerator += addressAsInt;
  const next = considered[i + 1];
  if (!next) continue;
  const address = BigInt(next);
  numerator += address;
  denominator += 2n;
  const suggestion = numerator / denominator;

  suggestions.push(intToAddress(suggestion));
}

function intToAddress(int: bigint): string {
  let hex = int.toString(16).padStart(40, "0");
  return toChecksumAddress(hex);
}

function toChecksumAddress(address: string): string {
  const bytes = new TextEncoder().encode(address.toLowerCase());
  const hash = keccak256(bytes);
  let checksummed = "0x";

  for (let i = 0; i < address.length; i++) {
    checksummed +=
      parseInt(hash[i], 16) >= 8 ? address[i].toUpperCase() : address[i];
  }

  return checksummed;
}

for (const suggestion of new Set(suggestions)) {
  console.log("\nhttps://etherscan.io/address/" + suggestion);
}
