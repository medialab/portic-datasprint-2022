/**
 * This script builds a docx file from visualizations_list.csv editorialization of automatically generated visualizations
 */

const fs = require('fs-extra');
const dsv = require('d3-dsv');
const pandoc = require('node-pandoc');
const path = require('path');

const URL_PREFIX = '';

(async () => {
  let visualizations = await fs.readFile('../visualizations/visualizations_list.csv', 'utf8');
  visualizations = dsv.csvParse(visualizations);
  let parts = visualizations
  .filter(v => v.include === '1')
  .filter(({fileName}) => fs.existsSync(`../visualizations/${fileName}`))
  .reduce((cur, visualization) => {
    const {part} = visualization;
    if (!cur.has(part)) {
      cur.add(part);
    }
    return cur;
  }, new Set());
  parts = Array.from(parts);
  // @todo include subparts ?
  const html = `
<!DOCTYPE html>
<html>
<head><title>Rapport d'exploration</title></head>
<body>
  ${
    parts
    .map((part) => {
      return `
        <h1>${part}</h1>
        <div>
        ${
          visualizations
          .filter(v => v.part === part)
          .map(({title, fileName}) => {
            return `
              <div>
                <h2>${title}</h2>
                <img src="${path.resolve(__dirname + '/../visualizations')}/${fileName}"></img>
              </div>
              `;
            })
            .join('\n\n')
          }
        </div>
      `;
    })
    .join('\n')
  }
</body>
</html>  
`;
  console.log('write html file');
  await fs.writeFile('../visualizations/index.html', html, 'utf8');
  console.log('write docx file');
  const args = '-f html -t docx -o ../visualizations/visualizations.docx';
  // await new Promise((resolve, reject) => {
    pandoc('../visualizations/index.html', args, (err) => {
      if (err) {
        console.log(err)
      }
      // resolve();
    })
  // })

}

)();