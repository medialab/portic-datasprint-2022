const container = document.getElementById('container');

['1787', '1789'].forEach(date => {

    [{ field: 'in', label: 'entréd' }, { field: 'out', label: 'sortie' }]
        .forEach(direction => {

            vizMatrice(date, direction);
            vizHistogramme(date, direction);

        })

})

/**
 * @param {string|number} date
 * @param {object} direction
 * @returns {undefined}
 */

function vizMatrice(date, direction) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "mark": "rect",
        "title": `Objet et zone de départ des bateaux attachés à Dunkerque en ${direction.label} en ${date}`,
        "data": {
            "url": "/static/data/commodity.csv"
        },
        "encoding": {
            "x": {
                "field": "departure_fr",
                "type": "nominal",
                "sort": "-color",
                "axis": {
                    "orient": "top"
                },
                "title": "port de départ"
            },
            "y": {
                "field": "commodity_purpose",
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
            { "filter": { "field": "year", "equal": date } },
            { "filter": { "field": "cargo_item_action", "equal": direction.field } }
        ],
    };

    vegaEmbed(getVizContainer(), spec, { mode: "vega-lite", renderer: 'svg' })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}

/**
 * @param {string|number} date
 * @param {object} direction
 * @returns {undefined}
 */

function vizHistogramme(date, direction) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": `Objet des bateaux commulés en ${direction.label} et attachés au port de Dunkerque en ${date}`,
        "mark": "bar",
        "data": {
            "url": "/static/data/commodity.csv"
        },
        "encoding": {
            "x": { "field": "tonnage", "type": "quantitative", "aggregate": "sum", "title": "Tonnage cummulée" },
            "y": { "field": "commodity_purpose", "type": "nominal", "sort": "-x", "title": "Objet du voyage" }
        },
        "transform": [
            { "filter": { "field": "year", "equal": date } },
            { "filter": { "field": "cargo_item_action", "equal": direction.field } }
        ],
    };

    vegaEmbed(getVizContainer(), spec, { mode: "vega-lite" })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}

/**
 * Get a div (append into page container) to
 * append a viz
 * @returns {HTMLDivElement}
 */

function getVizContainer() {
    const div = document.createElement('div');
    div.classList.add('block', 'viz')
    container.appendChild(div)
    return div;
}
