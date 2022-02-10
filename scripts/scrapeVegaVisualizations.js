/**
 * This script extracts all visualizations as images
 */

const puppeteer = require('puppeteer');
const chalk = require('chalk');
const fs = require('fs-extra');
const dsv = require('d3-dsv');

const siteBaseURL = 'http://localhost:8080';
const vizBasePath = '../visualizations/';

const PAGE_WIDTH = 1500;
const PAGE_HEIGHT = 1000;

const slugify = str => {
  return str.toLowerCase().replace(/\W/gi, '_').replace(/éèê/gi, 'e').replace(/à/gi, 'a');
}

(async () => {
  const visualizations = [];
  const browser = await puppeteer.launch({
    headless: true
  });
  const page = await browser.newPage();
  await page.setViewport({
    width: PAGE_WIDTH,
    height: PAGE_HEIGHT,
    deviceScaleFactor: 1,
  });
  await page.goto(siteBaseURL);
  const pages = await page.evaluate(({baseURL}) => {
    const linksEls = Array.from(document.querySelectorAll('ul li a'));
    const links = linksEls.map(el => `${baseURL}${el.getAttribute('href')}`);
    return links;
  }, {baseURL: siteBaseURL});

  await pages.reduce((cur, URL) => 
  cur
  .then(() => new Promise(async (resolve, reject) => {
    console.log(chalk.yellow('goto ' + URL));
    // await page.waitForTimeout(3000);
    await page.goto(URL);
    console.log(chalk.green('done goto ' + URL));
    await page.waitForTimeout(3000);

    console.log(chalk.yellow('getting specs'));
    let specs = await page.evaluate(() => {
      let untitledIndex = 0;
      const pageTitle = document.querySelector('h1.title').textContent;
      // lister les SVG
      const svgs = Array.from(document.querySelectorAll('svg.marks'));
      // récupérer contenu du SVG
      return svgs.map((element) => {
        // récupérer le titre
        let title = element.querySelector('.role-title-text')
        if (title !== null) {
          title = title.textContent;
        } else {
          untitledIndex++;
          title = pageTitle + '_untitled_vis' + untitledIndex;
        }
        // retourner la liste des specs 
        const svg = element.outerHTML; 
        return {
          title,
          svg
        }
      })
    });

    specs = specs.map(({title, ...rest}) => ({
      ...rest,
      title,
      fileName: `${slugify(title)}.png`,
      id: `${slugify(title)}`,
    }));

    specs.forEach(({title, fileName, id}) => {
      visualizations.push({
        title,
        fileName,
        id,
        part: '',
        subpart: '',
        include: '',
      })
    });
    
    console.log(chalk.green(specs.length + ' specs discovered'));

    await specs.reduce(async (cur1, {svg, title, fileName}, index) => 
      cur1.then(() => new  Promise (async (res1, rej1) => {
        const screenshotPage = await browser.newPage();
        await screenshotPage.goto(URL);
        await screenshotPage.setViewport({
          width: PAGE_WIDTH,
          height: PAGE_HEIGHT,
          deviceScaleFactor: 1,
        });
        await screenshotPage.evaluate((svg) => {
          document.body.innerHTML = svg;
        }, svg);
        const imagePath = `${vizBasePath}${fileName}`;
        console.log(chalk.blue('==='));
        console.log(chalk.blue('Process ' + (index + 1) + '/' + specs.length + ':'))
        console.log(chalk.blue(title));
        console.log(chalk.green('write image at: ' + `${vizBasePath}${fileName}`));
        await screenshotPage.screenshot({path: imagePath, fullPage: true});
        screenshotPage.close();
        return res1();
      }))
    , Promise.resolve())
    resolve()
  }))
  , Promise.resolve());

  console.log(chalk.yellow('writing csv'));
  const csv = dsv.csvFormat(visualizations);
  await fs.writeFile('../visualizations/visualizations_list.csv', csv, 'utf8');

  console.log(chalk.green('all done, goodbye !'));

  await browser.close();
})();