import vegaEmbed from 'vega-embed'
import getVizContainer from './get-container';
import slug from 'slug';

const container = document.getElementById('container')
    , dataPath = '/static/data/pointcall_commodity.csv';

const dates = [
        '1787',
        '1789'
    ], filters = [
        { field: 'ferme_bureau', filter: 'Dunkerque', label: "bureau de ferme d'enregistrement (Dunkerque)"},
        { field: 'ferme_direction', filter: 'Lille', label: "direction de ferme d'enregistrement (Lille)"},
        { field: 'pointcall_province', filter: 'Flandre', label: "province d'enregistrement (Flandre)"},
        { field: 'pointcall_admiralty', filter: 'Dunkerque', label: "amirauté d'enregistrement (Dunkerque)"}
    ], directions = [
        { field: 'in', label: "en entrée (in)"},
        { field: 'out', label: "en sortie (out)"},
        { field: 'in-out', label: "en correspondance (in-out)"},
        { field: 'sailing around', label: "en pêche (sailing around)"},
        { field: 'transit', label: "en transit (transit)"}
    ], values = [
        // { field: 'tonnage', label: 'tonnage pondéré (divisé par le nombre de commodités)' },
        { field: 'commodity_standardized', label: 'objet navire (commodity standardized)' }
    ]

dates.forEach(date => {
    
    filters.forEach(filter => {
        
        directions.forEach(direction => {

                vizHistogrammeCommodity(date, filter, direction);
                vizHistogrammeTonnage(date, filter, direction);

        })

    })

})

function vizHistogrammeCommodity(date, filter, direction, value= { field: 'commodity_standardized', label: 'objet navire (commodity standardized)' }) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": `${value.label} des navires ${direction.label} des ports du/de la ${filter.label} en ${date}`,
        "mark": "bar",
        "data": {
            "url": dataPath
        },
        "encoding": {
            "y": { "field": value.field, "title": value.label, "sort": "-x" },
            "x": { "aggregate": "count", "title": "nombre de pointcall par objet", "type": "quantitative" },
        },
        "transform": [
            { "filter": { "field": "year", "equal": date } },
            { "filter": { "field": filter.field, "equal": filter.filter } },
            { "filter": { "field": 'pointcall_action', "equal": direction.field } }
        ],
    };

    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg', downloadFileName: slug(spec.title) })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}

function vizHistogrammeTonnage(date, filter, direction, value= { field: 'commodity_standardized', label: 'objet navire (commodity standardized)' }) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": `${value.label} des navires ${direction.label} des ports du/de la ${filter.label} en ${date}`,
        "mark": "bar",
        "data": {
            "url": dataPath
        },
        "encoding": {
            "y": { "field": value.field, "title": value.label, "sort": "-x" },
            "x": { "aggregate": "sum", "title": "tonnage cumulé, pondéré par nombre de commodités par bateau", "type": "quantitative", 'field': 'tonnage' },
        },
        "transform": [
            { "filter": { "field": "year", "equal": date } },
            { "filter": { "field": filter.field, "equal": filter.filter } },
            { "filter": { "field": 'pointcall_action', "equal": direction.field } }
        ],
    };

    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg', downloadFileName: slug(spec.title) })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}