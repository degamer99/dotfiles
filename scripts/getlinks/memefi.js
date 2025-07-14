const fs = require('fs');
const puppeteer = require('puppeteer');

function sleep(time) {
    return new Promise(function(resolve) { 
        setTimeout(resolve, time)
    });
 }

(async () => {
    // Get URLs from the text file
    const url = "https://tg-app.memefi.club/#tgWebAppData=query_id%3DAAFO1SlfAAAAAE7VKV_HYj6A%26user%3D%257B%2522id%2522%253A1596577102%252C%2522first_name%2522%253A%2522De%2522%252C%2522last_name%2522%253A%2522Gamer99%2520%25F0%259F%258D%2585%2522%252C%2522username%2522%253A%2522degamer99%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1727700873%26hash%3D1b779a68027a584219f17eba03d7fd5c551238db12063ed9620a36d551fe1efd&tgWebAppVersion=7.10&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23ffffff%22%2C%22section_bg_color%22%3A%22%23ffffff%22%2C%22secondary_bg_color%22%3A%22%23f0f0f0%22%2C%22text_color%22%3A%22%23222222%22%2C%22hint_color%22%3A%22%23a8a8a8%22%2C%22link_color%22%3A%22%232678b6%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23527da3%22%2C%22accent_text_color%22%3A%22%231c93e3%22%2C%22section_header_text_color%22%3A%22%233a95d5%22%2C%22subtitle_text_color%22%3A%22%2382868a%22%2C%22destructive_text_color%22%3A%22%23cc2929%22%2C%22section_separator_color%22%3A%22%23d9d9d9%22%2C%22bottom_bar_bg_color%22%3A%22%23f0f0f0%22%7D";

    // Launch a browser instance
    const browser = await puppeteer.launch({
        executablePath: '/usr/bin/brave-browser',
        headless: false // Optional: Set to true if you want to run in headless mode
    });
    const page = await browser.newPage();
        
        try {
            await page.goto(url);
            await page.waitForSelector('.MuiStack-root.css-g1fud6', { visible: true });
            await page.click('button.css-aq8fga');
            await sleep(1000)
            const buttons = await page.$$('div.css-1dbsckc > button.css-1ru9rcs');
            await buttons[1].click();

        } catch (error) {
            console.log(`Failed to navigate to ${url}:`, error);
             
        }

        try {
            await page.goto("https://tg-app.memefi.club/earn");
        } catch (error) {
            console.log(`Failed to navigate to ${url}:`, error);
             
        }

        // Wait for the element with ID 'dlink2' to be visible
        try {
            await page.waitForSelector('.MuiBox-root.css-1ephh1j');
        } catch (error) {
            console.log(`Tasks not found ${url}:`, error);
             
        }

        // Get the href attribute of the first element with ID 'dlink2'
        const elementToTask = await page.evaluate(() => {
            let tasks = [...document.querySelectorAll('.MuiBox-root.css-1ephh1j')]
            console.log(tasks)
            tasks.at(-1).click()
            return tasks
            // return document.querySelector('.MuiBox-root.css-1ephh1j').getAttribute('href');
        });
        // elementToTask.forEach( async value => { await eachTask(value)} )
        // const eachTask = async (value) => {
        //     const [response] = await Promise.all([
        //         // page.waitForNavigation(waitOptions),
        //         // page.click('a.btn.btn-outline.btn-xs', clickOptions),
        //          page.waitForNavigation(),
        //         page.click('a.btn.btn-outline.btn-xs'),
        //       ]);
        // }




        // const dlink2Href = `https://mobiletvshows.site/${dlink2}`;
        // console.log(`Navigating to: ${dlink2Href}`);

        // try {
        //     await page.goto(dlink2Href, { waitUntil: 'networkidle2' });
        // } catch (error) {
        //     console.log(`Failed to navigate to ${dlink2Href}:`, error);
             
        // }

        // // Wait for the input element with name 'filelink' to be visible
        // try {
        //     await page.waitForSelector('input[name="filelink"]');
        // } catch (error) {
        //     console.log(`Element input[name="filelink"] not found on ${dlink2Href}:`, error);
             
        // }

    
    // Close the browser
    await browser.close();
})();
