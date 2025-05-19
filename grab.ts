import { consoleFmt } from "./utils.ts";

type Transaction = {
  blockNumber: string;
  timeStamp: string;
  hash: string;
  from: { ens_domain_name: string; hash: string };
  to: { ens_domain_name: string; hash: string };
  value: string;
  gasUsed: string;
};

let visited: string[] = [];

let transactions: Transaction[] = [];

function sleep(ms : number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function sync() {
  const rawTxns = await fetch(
    "https://eth.blockscout.com/api/v2/transactions",
  );
  const { items }: { items: Transaction[] } = await rawTxns.json();

  let newCount = 0;
  for (const txn of items) {
    try {
      if (visited.includes(txn.hash)) continue;

      const txnData: Transaction = {
        blockNumber: txn.blockNumber,
        timeStamp: txn.timeStamp,
        hash: txn.hash,
        from: {
          ens_domain_name: txn.from.ens_domain_name,
          hash: txn.from.hash,
        },
        to: {
          ens_domain_name: txn.to.ens_domain_name,
          hash: txn.to.hash,
        },
        value: txn.value,
        gasUsed: txn.gasUsed,
      };
      transactions.push(txnData);

      visited.push(txn.hash);
      newCount++;
    } catch (_) {
      continue;
    }
  }

  console.log(
    `Found ${consoleFmt.green(newCount.toString())} new transactions.`,
  );
}

async function loadLocal() {
  const data = await Deno.readTextFile("./data.json");
  const { visited: visitedLocal, transactions: transactionsLocal } = JSON.parse(
    data,
  );
  visited = visitedLocal || [];
  transactions = transactionsLocal || [];
  console.log(
    consoleFmt.yellow(`Loaded ${visited.length} local transactions.`),
  );
}

async function syncLocalFiles() {
  Deno.stdout.writeSync(encoder.encode(consoleFmt.cyan("writing ...")))
  const data = { visited, transactions };

  await Deno.writeTextFile("./data.json", JSON.stringify(data, null, 2));
  await sleep(500 + Math.random() * 500);
  console.log(`\r           \rwritten to local files✅`)
}

const encoder = new TextEncoder();

async function main() {
  let fails = 0;
  await loadLocal();
  sync();
  setInterval(async () => {
    if (Math.random() < 0.2) {
      console.log(
        consoleFmt.green(
          `Total transactions collected so far: ${transactions.length}`,
        ),
      );
    }

    try {
      console.log("Grabbing transactions...");
      await sync();
      await syncLocalFiles();
    } catch (_) {
      fails++;
      console.log(consoleFmt.red("Failed, retrying"));
      console.log(consoleFmt.yellow(`Encountered ${fails} failures\n`));
    }
  }, 15_000);
}

main();
