async function getTxnCount2024() {
    const addr = "0x974caa59e49682cda0ad2bbe82983419a2ecc400"
    const url = `https://etherscan.io/advanced-filter?fadd=${addr}&age=2024-01-01%7e2024-12-31`

    const resp = await fetch(url)
    const data = await resp.text()

    console.log(data)
}

await getTxnCount2024()

export { }

const tops = {
    "0x974caa59e49682cda0ad2bbe82983419a2ecc400" : 2546348,
    "0x1A1c87d9A6F55D3BbB064bfF1059ad37B6Bdc097": 262393,
    "0x46340b20830761efd32832A74d7169B29FEB9758":  4492885,
    "0x28C6c06298d514Db089934071355E5743bf21d60": 4435301
}