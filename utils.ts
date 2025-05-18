export function cliError(message: unknown) {
  console.error(consoleFmt.red(`${message}`));
  // Deno.exit(1);
}

export const consoleFmt = {
  red: (text: string) => `\x1b[31m${text}\x1b[39m`,
  yellow: (text: string) => `\x1b[33m${text}\x1b[39m`,
  green: (text: string) => `\x1b[32m${text}\x1b[39m`,
  blue: (text: string) => `\x1b[34m${text}\x1b[39m`,
  cyan: (text: string) => `\x1b[36m${text}\x1b[39m`,
  magenta: (text: string) => `\x1b[35m${text}\x1b[39m`,
  white: (text: string) => `\x1b[37m${text}\x1b[39m`,
  gray: (text: string) => `\x1b[90m${text}\x1b[39m`,
  bold: (text: string) => `\x1b[1m${text}\x1b[22m`,
  underline: (text: string) => `\x1b[4m${text}\x1b[24m`,
} as const;
