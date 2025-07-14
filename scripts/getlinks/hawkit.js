const puppeteer = require('puppeteer');


function sleep(time) {
   return new Promise(function(resolve) { 
       setTimeout(resolve, time)
   });
}

(async () => {
    // Path to Brave browser executable
    const BRAVE_PATH = '/opt/brave.com/brave/brave'; // Change this to your Brave browser executable path

    // Path to your Brave user data directory
    const USER_DATA_DIR = '/home/deen/.config/BraveSoftware/Brave-Browser/Default'; // Change this to your Brave user data directory path

     // Set the timeout value to 2 minutes (120000 milliseconds)
     const TIMEOUT = 120000;

    // Launch Puppeteer with Brave settings
    const browser = await puppeteer.launch({
        headless: false, // Set to true if you don't need to see the browser UI
        executablePath: BRAVE_PATH,
        userDataDir: USER_DATA_DIR,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--disable-dev-shm-usage'
        ]
    });

    const page = await browser.newPage();

    page.setDefaultTimeout(TIMEOUT);
    
    // Navigate to the website
    await page.goto('https://hawkit.ng/#/earn/630f312f7c7abf307845262d/pending');
    
    const createTask = async () => {
        await page.waitForSelector('button.btn.btn-coloured-heavy', { visible: true });
        console.log('Button is visible!');
        await page.click('button.btn.btn-coloured-heavy');
        await sleep(3000)
         // Wait for the second button to be visible and click it
        await page.waitForSelector('button.mr-1.btn.btn-success.btn-rounded', { visible: true });
        await page.click('button.mr-1.btn.btn-success.btn-rounded');

        // Wait for 3 seconds
        await sleep(3000)
    }

    const gotoTask = async () => {
        // await page.waitForSelector('a.btn.btn-outline.btn-xs', { visible: true });
        const [response] = await Promise.all([
            // page.waitForNavigation(waitOptions),
            // page.click('a.btn.btn-outline.btn-xs', clickOptions),
             page.waitForNavigation(),
            page.click('a.btn.btn-outline.btn-xs'),
          ]);

    }


    // Function to check element visibility and run appropriate function
    const checkElementVisibility = async (selector, timeout = 150000) => {
        try {
            await page.waitForSelector(selector, { visible: true, timeout });
            console.log('Element is visible!');
            gotoTask()
        } catch (error) {
            console.log('Element is not visible!');
            createTask()
        }
    };
    
    checkElementVisibility('a.btn.btn-outline.btn-xs');

    // Optionally close the browser
    // await browser.close();
})();
