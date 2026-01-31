import puppeteer from "puppeteer";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function parsePairs(argv) {
  const pairs = [];
  let current = {};

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--html") {
      current.html = argv[i + 1];
      i += 1;
      continue;
    }
    if (arg === "--pdf") {
      current.pdf = argv[i + 1];
      i += 1;
      continue;
    }
    if (arg === "--pair") {
      current = { html: argv[i + 1], pdf: argv[i + 2] };
      i += 2;
    }
    if (current.html && current.pdf) {
      pairs.push(current);
      current = {};
    }
  }

  return pairs;
}

async function renderPdf(page, htmlPath, pdfPath) {
  if (!fs.existsSync(htmlPath)) {
    throw new Error(`Missing HTML: ${htmlPath}`);
  }
  const url = new URL(`file://${htmlPath}`);
  await page.goto(url.toString(), { waitUntil: "networkidle0" });
  await page.pdf({
    path: pdfPath,
    format: "A4",
    printBackground: true,
    margin: {
      top: "16mm",
      bottom: "16mm",
      left: "12mm",
      right: "12mm",
    },
  });
}

async function main() {
  const pairs = parsePairs(process.argv.slice(2));
  if (pairs.length === 0) {
    throw new Error(
      "No input pairs provided. Use --html <path> --pdf <path> or --pair <html> <pdf>."
    );
  }

  const browser = await puppeteer.launch({ headless: "new" });
  const page = await browser.newPage();
  for (const file of pairs) {
    await renderPdf(page, file.html, file.pdf);
  }
  await browser.close();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
