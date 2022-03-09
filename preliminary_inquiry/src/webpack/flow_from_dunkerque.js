import vegaEmbed from 'vega-embed'
import getVizContainer from './get-container';
import slug from 'slug';

const container = document.getElementById('container')
    , dataPath = '/static/data/flows.csv';

const dates = [
    '1787',
    '1789'
], ensembles = [
    { field: '', filter: 'Dunkerque', label: "ville"},
    { field: '_ferme_bureau', filter: 'Dunkerque', label: "bureau de ferme"},
    { field: '_ferme_direction', filter: 'Lille', label: "direction de ferme"},
    { field: '_province', filter: 'Flandre', label: "province"},
    { field: '_admiralty', filter: 'Dunkerque', label: "amirauté"},
    { field: '_state_1789_fr', filter: 'Dunkerque', label: "état 1789"}
]

let spec;

dates.forEach(date => {

    for (let i = 0; i < ensembles.length - 1; i++) {
        for (let j = i + 1; j < ensembles.length; j++) {

            const départ = ensembles[i];
            const arrivée = ensembles[j];

            spec = {
                "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
                "title": [
                    `Destination (${arrivée.label}) aggrégé par tonnage cummulé`,
                    `des navires au départ de ${départ.label} de Dunkerque en ${date}`
                ],
                "mark": "bar",
                "data": {
                    "url": dataPath
                },
                "encoding": {
                    "x": { "field": 'tonnage', "type": "quantitative", "aggregate": "sum", "title": `Tonnage au départ de ${départ.label} de Dunkerque` },
                    "y": { "field": `destination${arrivée.field}`, "type": "nominal", "sort": "-x", "title": `${arrivée.label} de destination` }
                },
                "transform": [
                    { "filter": { "field": "year", "equal": date } },
                    { "filter": { "field": `departure${départ.field}`, "equal": départ.filter } },
                    { "filter": `datum.departure != ''` }
                ],
            };
            
            vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg', downloadFileName: slug(spec.title.join(' ')) })
                .then((response) => { console.log(response) })
                .catch((response) => { console.error(response) });

            spec = {
                "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
                "title": [
                    `Départ (${départ.label}) aggrégé par tonnage cummulé`,
                    `des navires à destination de ${arrivée.label} de Dunkerque en ${date}`
                ],
                "mark": "bar",
                "data": {
                    "url": dataPath
                },
                "encoding": {
                    "x": { "field": 'tonnage', "type": "quantitative", "aggregate": "sum", "title": `Tonnage à l'arrivée de ${arrivée.label} de Dunkerque` },
                    "y": { "field": `departure${départ.field}`, "type": "nominal", "sort": "-x", "title": `${arrivée.label} d'arrivée` }
                },
                "transform": [
                    { "filter": { "field": "year", "equal": date } },
                    { "filter": { "field": `destination${arrivée.field}`, "equal": arrivée.filter } },
                    { "filter": `datum.destination != ''` }
                ],
            };
            
            vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg', downloadFileName: slug(spec.title.join(' ')) })
                .then((response) => { console.log(response) })
                .catch((response) => { console.error(response) });
        }
    }
});