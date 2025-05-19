type Txn = {
    from: {hash : string};
    to: {hash : string};
}

const graph: Record<string, string[]> = {}

async function main() {
    const data = await Deno.readTextFile("./data.json");
    const { transactions: transactionsLocal } = JSON.parse(data);
    const transactions: Txn[] = transactionsLocal;

    for (const tx of transactions) { 
        const from = tx.from.hash
        const to = tx.to.hash
        if (graph[from]) {
            graph[from].push(to);
        } else {
            graph[from] = [to];
        }
    }

    Deno.writeTextFile("./graph.json", JSON.stringify(graph, null, 2));
    console.log(`Generated graph using ${transactions.length} transactions`)
    console.log(`Unique addresses: ${Object.keys(graph).length}`)
}

main()