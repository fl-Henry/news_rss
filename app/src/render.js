const puppeteer = require('puppeteer');

// Custom imports
const gm = require('./general_methods/gm');


class PupWrp {

    url;
    browser;
    page;

    constructor(url) {
        this.url = url;
    }

    async startBrowser(headless_ = true, proxy = null, width_px = 1920, height_px = 1080) {
        let args = {};
        args['args'] = [];

        if (headless_) {
            args['headless'] = 'new';
        }
        else {
            args['headless'] = false;
        } 

        if (proxy !== null) {
            args['args'].push(`--proxy-server=${proxy}`)
        }

        this.browser = await puppeteer.launch(args);    
        
        this.page = await this.browser.newPage();
        await this.page.setViewport({
            width: width_px,
            height: height_px,
            deviceScaleFactor: 1,
        });

        // disable images
        await this.page.setRequestInterception(true);
        this.page.on('request', (req) => {
            if(req.resourceType() == 'stylesheet' || req.resourceType() == 'font' || req.resourceType() == 'image'){
                req.abort();
            }
            else {
                req.continue();
            }
        });
    }

    async close() {
        await this.browser.close();
    }

    async loadPage(waitUntil_val = "load") {
        console.log("load: " + this.url)
        await this.page.goto(this.url,
            {
                timeout: 60000,
                waitUntil: waitUntil_val
            }
        )
    }

    async saveHtml(filePath) {
        const html = await this.page.content();
        gm.writeFile(filePath, html)
    }
}

module.exports = {
   PupWrp,
}

