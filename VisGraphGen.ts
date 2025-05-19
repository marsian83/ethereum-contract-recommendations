function adjacencyListToVisGraph(graph: Record<string, string[]>) {
    const edges = new Set<string>(); // To handle duplicate edges
    let output = "graph G {\n";

    for (const node in graph) {
        graph[node].forEach((neighbor) => {
            const edge = `"${node}" -- "${neighbor}"`;
            if (!edges.has(edge)) {
                edges.add(edge);
                output += `\t${edge};\n`; // Append edge to output
            }
        });
    }

    output += "}";

    return output;

}

async function main() {
    const data = await Deno.readTextFile("./graph.json");
    const graph = JSON.parse(data);
    
    const visGraph = adjacencyListToVisGraph(graph)

    Deno.writeTextFileSync("./visGraph.dot", visGraph);

}

main()
