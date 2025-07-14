    // copy to get urls list
    // document.querySelectorAll(".mainbox").forEach( x => console.log(x.querySelector('a').href))
    // copy to remove in vim
    // :%s/VM491:1 //g
const fs = require('fs');
const puppeteer = require('puppeteer');

// Function to read URLs from a text file and convert them to an array
function getUrlsFromFile(filePath) {
    const fileContent = fs.readFileSync(filePath, 'utf8');
    return fileContent.split('\n').filter(Boolean); // Split by newline and remove empty lines
}

// Function to check if a file link is already in the output file
function isLinkInFile(link, filePath) {
    if (!fs.existsSync(filePath)) return false; // If the file doesn't exist, no links are in it yet
    const fileContent = fs.readFileSync(filePath, 'utf8');
    const existingLinks = fileContent.split('\n').filter(Boolean); // Split by newline and remove empty lines
    return existingLinks.includes(link);
}

(async () => {
    // Get URLs from the text file
    const urls = getUrlsFromFile('./arrowS2parent.txt');

    // Launch a browser instance
    const browser = await puppeteer.launch({
        executablePath: '/usr/bin/brave-browser',
        headless: false // Optional: Set to true if you want to run in headless mode
    });
    const page = await browser.newPage();

    // File to store the output
    const outputFile = 'arrowS2.txt';

    // Process each URL in the list
    for (const url of urls) {
        console.log(`Processing: ${url}`);
        
        try {
            await page.goto(url);
        } catch (error) {
            console.log(`Failed to navigate to ${url}:`, error);
            continue; // Skip to the next URL on failure
        }

        // Wait for the element with ID 'dlink2' to be visible
        try {
            await page.waitForSelector('#dlink2');
        } catch (error) {
            console.log(`Element #dlink2 not found on ${url}:`, error);
            continue; // Skip to the next URL on failure
        }

        // Get the href attribute of the first element with ID 'dlink2'
        const dlink2 = await page.evaluate(() => {
            return document.querySelector('#dlink2').getAttribute('href');
        });
        const dlink2Href = `https://mobiletvshows.site/${dlink2}`;
        console.log(`Navigating to: ${dlink2Href}`);

        try {
            await page.goto(dlink2Href, { waitUntil: 'networkidle2' });
        } catch (error) {
            console.log(`Failed to navigate to ${dlink2Href}:`, error);
            continue; // Skip to the next URL on failure
        }

        // Wait for the input element with name 'filelink' to be visible
        try {
            await page.waitForSelector('input[name="filelink"]');
        } catch (error) {
            console.log(`Element input[name="filelink"] not found on ${dlink2Href}:`, error);
            continue; // Skip to the next URL on failure
        }

        // Get the value of the input element
        const fileLinkValue = await page.evaluate(() => {
            return document.querySelector('input[name="filelink"]').value;
        });

        console.log(`File link: ${fileLinkValue}`);

        // Check if the link is already in the file
        if (!isLinkInFile(fileLinkValue, outputFile)) {
            // Save the file link to a text file if it's not already there
            fs.appendFileSync(outputFile, `${fileLinkValue}\n`, 'utf8');
            console.log(`Saved link: ${fileLinkValue}`);
        } else {
            console.log(`Link already exists: ${fileLinkValue}`);
        }
    }

    // Close the browser
    await browser.close();
})();
