const puppeteer = require('puppeteer');

// Custom imports
const gm = require('./general_methods/gm');



if (process.argv[2] && process.argv[2] === '--url' && process.argv[3]) {
    URL = process.argv[3]
} else {
    console.log(process.argv)
    console.log('Required --url');
    process.exit(1)
}


(async () => {
    const browser = await puppeteer.launch({
        headless: 'new',
    });
    try {
        const page = await browser.newPage();
        await page.setViewport({
            width: 1920,
            height: 1080,
            deviceScaleFactor: 1,
        });

        await page.goto(URL,
            {
                timeout: 60000,
                waitUntil: 'networkidle0'
            }
        )

        const html = await page.content();
        gm.writeFile("result_common_rendered.txt", html)
        await page.screenshot({ path: 'hello_world.png'});
    } catch (e) {
        console.error(e);
    } finally {
        await browser.close();
    }
})();
