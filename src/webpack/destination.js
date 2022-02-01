import vegaEmbed from 'vega-embed'
import getVizContainer from './get-container';

const container = document.getElementById('container');

['1787', '1789'].forEach(date => {

    [
        {
            field: 'departure_ferme_bureau',
            label: "bureau de ferme comme point de départ"
        },
        {
            field: 'destination_ferme_bureau',
            label: "bureau de ferme comme point de destination"
        },
        {
            field: 'departure_ferme_direction',
            label: "direction de ferme comme point de départ"
        },
        {
            field: 'destination_ferme_direction',
            label: "direction de ferme comme point de destination"
        },
        {
            field: 'destination_admiralty',
            label: "amirauté comme point de destination"
        },
        {
            field: 'departure_admiralty',
            label: "amirauté comme point de destination"
        },
        {
            field: 'destination_province',
            label: "province comme point de destination"
        },
        {
            field: 'departure_province',
            label: "province comme point de destination"
        },
    ].forEach(lieu => {
        vizHistogramme(date, lieu)
    })

});

/**
 * @param {string|number} date
 * @param {object} action
 * @returns {undefined}
 */

 function vizHistogramme(date, lieu) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": `Tonnage commulé en fonction de la ${lieu.label} en ${date}`,
        "mark": "bar",
        "data": {
            "url": `/static/data/destination_${date}.csv`
        },
        "encoding": {
            "x": { "field": "tonnage", "type": "quantitative", "aggregate": "sum", "title": "Tonnage cummulée" },
            "y": { "field": lieu.field, "type": "nominal", "sort": "-x", "title": lieu.label },
            "color": {
                "condition": {
                    "test": `datum['${lieu.field}'] == 'dunkerque' || datum['${lieu.field}'] == 'flandre'`,
                    "value": "#e39382"
                }
            }
        },
        "transform": [
            
        ],
    };

    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg' })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}