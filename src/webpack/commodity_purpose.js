import vegaEmbed from 'vega-embed'
import getVizContainer from './get-container';

const container = document.getElementById('container');

['1787', '1789'].forEach(date => {

    vizHistogramme(date);

})

/**
 * @param {string|number} date
 * @param {object} action
 * @returns {undefined}
 */

 function vizHistogramme(date, action, commodity) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": `Nombre de bateaux par objet de voyage en ${date}`,
        "mark": "bar",
        "data": {
            "url": `/static/data/commodity_purpose_${date}.csv`
        },
        "encoding": {
            "x": { "field": "nb_boat", "type": "quantitative", "aggregate": "sum", "title": "Nombre de bateaux" },
            "y": { "field": "produit", "type": "nominal", "sort": "-x", "title": "Objet du voyage" }
        },
        "transform": [
            { "filter": "datum.produit != ''" }
        ],
    };

    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg' })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}