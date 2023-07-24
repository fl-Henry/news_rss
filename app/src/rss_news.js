
// Custom imports
const gm = require('./general_methods/gm');
const render = require('./render')


class RssNews {

    proxyFilepath = 'proxies.txt';
    proxyList;
    proxy;

    url;
    FEEDS_GEN_URL = 'https://rss.app/rss-feed';

    // Puppeteer wraper
    pw;

    feedUrlFilepath = 'feed_url_list.txt';

    constructor(url) {
        this.url = url;
    }

    readProxyFile() {
      let proxyList = gm.readFile(this.proxyFilepath).split("\n");
      if ([null, 'null', '', ' ', "\n", "\r"].includes(proxyList[proxyList.length - 1])) {
        proxyList.pop();
      }
      this.proxyList = proxyList;
    }

    writeProxyFile() {
        const content = this.proxyList.join('\n');
        gm.writeFile(this.proxyFilepath, content);
    }

    nextProxy() {
        // return this.proxyList[~~(this.proxyList.length * Math.random())];
        return this.proxyList.at(-1);
    }

    removeProxy() {
        this.proxyList.pop();
        this.proxyList.push("")
        this.writeProxyFile();
    }

    async startBrowser(useProxy = false) {
        if (useProxy) {
            this.readProxyFile();
            this.proxy = this.nextProxy();
            // TODO remove "false" headless 
            await this.pw.startBrowser(false, this.proxy);
        }
        else {
            // TODO remove "false" headless 
            await this.pw.startBrowser(false);   
        }
    }

    saveFeedUrl(feedUrl) {
        const content = `${this.url} ${feedUrl}`;
        gm.writeFile(this.feedUrlFilepath, content);
    }

    async getFeedUrl() {
        this.pw = new render.PupWrp(this.FEEDS_GEN_URL);
        for (let i = 0; i < 5; i++) {
            await this.startBrowser(useProxy = true);
            try {
                await this.pw.loadPage();  // "domcontentloaded"
                break;
            } catch(err) {
                console.log(String(err) + ' | Next attempt');
                await this.pw.close();

                console.log("Remove proxy: " + this.proxy);
                this.proxy = null;
                this.removeProxy();
                gm.sleep(2);
            }
        }
        
        if (this.proxy === null) {
            console.log("All 5 attempts failed > exit");
            process.exit();    
        } else {
            console.log("proxy: " + this.proxy); 
        }
        
        // Select the input field and insert data
        const inputCSS = '[placeholder*="URL"]';
        const inputTag = await this.pw.page.$(inputCSS);
        await inputTag.type(this.url);

        // Click the submit button
        const buttonCSS = '[type*="submit"]';
        await this.pw.page.click(buttonCSS);

        // Wait for the form submission to complete (if needed)
        await this.pw.page.waitForNavigation(
            {
                timeout: 120000,
                waitUntil: 'networkidle2',
            }
        );

        const feedUrl = await this.pw.page.url();
        this.saveFeedUrl(feedUrl);

        // // Capture a screenshot
        // await this.pw.page.screenshot({ path: './after_submit.png' });
        // await this.pw.saveHtml("./after_submit.html");

        await this.pw.close();
    }

    async getNewsUrls() {
        this.pw = new render.PupWrp(this.FEEDS_GEN_URL);
        await this.startBrowser();
        await this.pw.loadPage();

        gm.sleep(60);

        // scroll down
        // all items: div.MuiBox-root>div.MuiGrid-item
        // news links div.MuiBox-root>div.MuiGrid-item h3>a
        // save links
    }
}


// --help || -h
gm.help(`
    --test: optional
        start tests end exit

    --url: required
        url to perform functions

  functions:
    --feed-url: optional
        generate feed url and save to file

    --new-feed: optional
        fetch news using saved feed url
`)

// Start // If --test
if (gm.fetchFlag("--test")) {
    // const url = "https://apnews.com/world-news"; 
    const url = "https://ipfighter.com/"; 
    const instance = new RssNews(url);
    instance.FEEDS_GEN_URL = "https://ipfighter.com/"; 

    (async () => {
        console.log('getFeedUrl');
        await instance.getFeedUrl();
        // process.exit(0);
    })();
}

// If not --test
else {

    // --url https://...
    const newsUrl = gm.getArg("--url");
    const rssNewsI = new RssNews(newsUrl);

    // --feed-url
    if (gm.fetchFlag("--feed-url")) {
        (async () => {
            await rssNewsI.getFeedUrl();
            process.exit(0);
        })();
    }

    // --new-feed
    else if (gm.fetchFlag("--new-feed")) {
        (async () => {
            await rssNewsI.getNewsUrls();
            process.exit(0);
        })();
    }

}





