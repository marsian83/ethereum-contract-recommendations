const monthly = [
    863231,
    784842,
    863231,
    635343,
    756754,
    598894,
    999576,
    1077765,
    849877,
    971288,
    813428,
    1214110
]

const monthlyAccurate = monthly.map(i => Math.ceil(i * 1.2253))

const days: number[] = []

for (let i = 0; i < 12; i++) {
    const month = monthlyAccurate[i]
    for (let j = 0; j < 30; j++) {
        const day = month / 30 * (1 + Math.random() * 0.4)
        days.push(Math.ceil(day))
    }
}

import * as fs from "fs";

// Function to generate CSV data
function generateCSV(filename: string) {
    const startDate = new Date("2024-01-01");
    const rows: string[] = [];
    
    // Header row
    rows.push(`Date(UTC),UnixTimeStamp,Value`);

    // Generate 365 entries
    for (let i = 0; i < 365; i++) {
        const currentDate = new Date(startDate);
        currentDate.setDate(startDate.getDate() + i);

        const dateStr = currentDate.toLocaleDateString("en-US"); // Format as MM/DD/YYYY
        const unixTimestamp = Math.floor(currentDate.getTime() / 1000); // Convert to Unix timestamp
        const value = days[i % days.length]; // Get value from the days array

        rows.push(`${dateStr},${unixTimestamp},${value}`);
    }

    // Write to CSV file
    fs.writeFileSync(filename, rows.join("\n"), "utf8");
    console.log(`CSV file '${filename}' created successfully!`);
}

// Run the function
generateCSV("output.csv");
