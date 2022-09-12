const puppeteer = require('puppeteer');
const fs = require('fs')



dt = new Date();

function pad2(n) {
    return (n < 10 ? '0' : '') + n;
}
function getFullDateTime() {
    return dt.getFullYear() + '-' +
        pad2(dt.getMonth() + 1) + '-' +
        pad2(dt.getDate()) + '-' +
        pad2(dt.getHours()) + '-' +
        pad2(dt.getMinutes()) + '-' +
        pad2(dt.getSeconds());
}

function copy(oldPath, newPath, callback) {
        var readStream = fs.createReadStream(oldPath);
        var writeStream = fs.createWriteStream(newPath);

        readStream.on('error', callback);
        writeStream.on('error', callback);

        readStream.on('close', function() {
            fs.unlink(oldPath, callback);
        });
 
        readStream.pipe(writeStream);
}


function move(oldPath, newPath, callback) {
    fs.rename(oldPath, newPath, function(err) {
        if(err) {
            if(err.code === 'EXDEV') {
                copy(oldPath, newPath, callback);
            }
            else {
                callback(err);
            }
            return;
         }
         callback();
    })
}








pageURL = "http://data-nifc.opendata.arcgis.com/datasets/nifc::wfigs-2022-wildland-fire-perimeters-to-date/about";

(async() => {
	browser = await puppeteer.launch({
                args: ['--no-sandbox', '--disable-setuid-sandbox'],
                /*dumpio: true,*/
    		headless: true,
                executablePath: '/usr/bin/chromium-browser',
    		ignoreHTTPSErrors: true,
                defaultViewport: {
                    width: 1920,
                    height: 1080
                }
	});

        console.log('cleaning /tmp directory, (current directory = ' + __dirname + ')')
        folder = '/tmp'

        fs.readdir(folder, (err, files) => {
            for(const file of files) {
                try {
                fs.unlinkSync(folder+file);
                } catch(err) {}
            }
        });



	let page = await browser.newPage()
	console.log('navigating to ', pageURL)

	await page.goto(pageURL)

        await page.waitForTimeout(4000)

        console.log('taking screen shot of main page')

        await page.screenshot({path: getFullDateTime() + '-mainpage.png'})


        console.log('setting download options')
        client = await page.target().createCDPSession();

        await client.send('Page.setDownloadBehavior',
             {
              behavior: 'allow',
              downloadPath: '/tmp'
             }
        )

        console.log('clicking main Download button to open flyout')

        await page.evaluate( () => {
            cards = $('hub-download-card');
            $('button:contains("Download")')[1].click()           
        });

        await page.waitForTimeout(5000)

        console.log('taking screen shot of flyout')

        await page.screenshot({path: getFullDateTime() + '-flyout.png'})


        console.log("redirecting internal console.log to this app")
        page.on('console', async (msg) => {
            const msgArgs = msg.args();
            for(let i = 0; i < msgArgs.length; ++i) {
                console.log(await msgArgs[i].jsonValue());
            }
        });


        console.log('clicking shapeFile generate/download button')

        await page.evaluate( () => {
            console.log('finding hub-download-card')
            cards = $('hub-download-card')
            try {
                console.log("trying to click generate button")
                cards[2].shadowRoot.firstChild.children[2].children[1].children[1].children[0].click();                
                console.log("generate button pressed")
            }
            catch(err) {
                console.log("trying to click download button")
                cards[2].shadowRoot.firstChild.children[2].children[1].click();
                console.log("download button pressed")
            }
        });
        console.log('waiting for download to initiate')

        await page.waitForTimeout(10000)

        console.log('capturing download screen')
        await page.screenshot({path: getFullDateTime() + '-download.png'})


        console.log('waiting for download to finish')

        foundCRDownload = true
        for(i=0;i<100 && foundCRDownload;i++) {
            await page.waitForTimeout(1000)
            foundCRDownload = false;
            fs.readdirSync('/tmp').forEach(file => {
                /*console.log(file);*/
                if(file.endsWith("crdownload"))
                    foundCRDownload = true;
            })
        }

       console.log('moving downloads to current directory');
        
       fs.readdir(folder, (err, files) => {
            for(const file of files) {
                    if(file.endsWith('.zip')) {
                        oldname = '/tmp/' + file;
                        newname = __dirname + '/' + getFullDateTime() + '-' + file;
                        console.log("moving " + oldname + " to " + newname);
                        move(oldname, newname, function(err2) {
                            if(err2)
                                console.log("trouble moving files. " + err2);
                        })
                    }
            }
        });

        console.log("closing browser")
        browser.close()
        console.log("done");
})()
