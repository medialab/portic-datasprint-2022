const vegaEmbed = require('vega-embed');
const slug = require( 'slug');
const vega = require( 'vega');
const lite = require( 'vega-lite');
const fs = require( 'fs');
const path = require( 'path');
const { csvParse } = require('d3-dsv');

vizMatrice();

/**
 * @param {string|number} date
 * @param {'import'|'export'} direction
 * @param {object} localisation
 * @param {string} class_produit
 * @returns {undefined}
 */

function vizMatrice () {
    const spec = {
        $schema: 'https://vega.github.io/schema/vega-lite/v2.0.json',
        description: 'A simple bar chart with embedded data.',
        data: {
          values: [
            {a: 'A', b: 28},
            {a: 'B', b: 55},
            {a: 'C', b: 43},
            {a: 'D', b: 91},
            {a: 'E', b: 81},
            {a: 'F', b: 53},
            {a: 'G', b: 19},
            {a: 'H', b: 87},
            {a: 'I', b: 52}
          ]
        },
        mark: 'bar',
        encoding: {
          x: {field: 'a', type: 'ordinal'},
          y: {field: 'b', type: 'quantitative'}
        }
      };

    let vegaspec = lite.compile(spec, { logger: console.log }).spec;
    // return console.log(vegaspec.data);
    var view = new vega.View(vega.parse(spec), 
    {renderer: "svg"})
    view.toSVG()
    .then(function(svg) {
        console.log(svg);
        // fs.writeFileSync(
        //     path.join(__dirname, '../includes/', slug(spec.title.join(' ')) + '.svg'),
        //     svg
        // )
    })
    .catch(function(err) { console.error(err); });
}