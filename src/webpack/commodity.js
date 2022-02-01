import vegaEmbed from 'vega-embed'
import getVizContainer from './get-container';

const container = document.getElementById('container');

['1787', '1789'].forEach(date => {

    [
        { field: 'in', label: "en train d'entrer" },
        { field: 'out', label: 'en train de sortir' },
        { field:'sailing around', label: 'en train de pêcher' },
        { field:'transit', label: 'en cours de correspondance' },
        { field:'in-out', label: 'entrés et ressortis' },
    ]
        .forEach(action => {

            [{ field: 'departure_fr', label: 'de départ' }, { field: 'destination_fr', label: "d'arrivée" }]
                .forEach(direction => {
        
                    vizMatrice(date, action, direction, 'commodity_standardized_fr');
                    
                })

                vizHistogramme(date, action, 'commodity_standardized_fr');

        })

})

/**
 * @param {string|number} date
 * @param {object} action
 * @param {object} direction
 * @returns {undefined}
 */

function vizMatrice(date, action, direction, commodity) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "mark": "rect",
        "title": `Objet et port ${direction.label} des bateaux attachés au port de Dunkerque (homeport) ${action.label} en ${date}`,
        "data": {
            "url": `/static/data/commodity_${date}.csv`
        },
        "encoding": {
            "x": {
                "field": direction.field,
                "type": "nominal",
                "sort": "-color",
                "axis": {
                    "orient": "top"
                },
                "title": `port ${direction.label}`
            },
            "y": {
                "field": commodity,
                "type": "nominal",
                "sort": "-color",
                "title": "objet du voyage"
            },
            "color": {
                "field": "tonnage",
                "aggregate": "sum",
                "type": "quantitative"
            }
        },
        "transform": [
            { "filter": { "field": "cargo_item_action", "equal": action.field } }
        ],
    };

    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg' })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}

/**
 * @param {string|number} date
 * @param {object} action
 * @returns {undefined}
 */

function vizHistogramme(date, action, commodity) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": `Objet des bateaux commulés ${action.label} et attachés au port de Dunkerque (homeport) en ${date}`,
        "mark": "bar",
        "data": {
            "url": `/static/data/commodity_${date}.csv`
        },
        "encoding": {
            "x": { "field": "tonnage", "type": "quantitative", "aggregate": "sum", "title": "Tonnage cummulée" },
            "y": { "field": commodity, "type": "nominal", "sort": "-x", "title": "Objet du voyage" }
        },
        "transform": [
            { "filter": { "field": "cargo_item_action", "equal": action.field } }
        ],
    };

    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg' })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}


