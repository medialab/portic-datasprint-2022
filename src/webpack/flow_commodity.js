import vegaEmbed from 'vega-embed'
import getVizContainer from './get-container';
import slug from 'slug';

const container = document.getElementById('container')
    , dataPath = '/static/data/flow_commodity.csv';

const dates = [
        '1787',
        '1789'
    ], filters = [
        { field: 'ferme_bureau', filter: 'Dunkerque', label: "bureau de ferme d'enregistrement (Dunkerque) de départ"},
        { field: 'ferme_direction', filter: 'Lille', label: "direction de ferme d'enregistrement (Lille) de départ"},
        { field: 'province', filter: 'Flandre', label: "province d'enregistrement (Flandre) de départ"},
        { field: 'admiralty', filter: 'Dunkerque', label: "amirauté d'enregistrement (Dunkerque) de départ"}
    ], directions = [
        { field: 'in', label: "en entrée (in)"},
        { field: 'out', label: "en sortie (out)"},
        { field: 'in-out', label: "en correspondance (in-out)"},
        { field: 'sailing around', label: "en pêche (sailing around)"},
        { field: 'transit', label: "en transit (transit)"}
    ], values = [
        { field: 'tonnage', label: 'tonnage pondéré (divisé par le nombre de commodités)' },
        { field: 'commodity_standardized', label: 'objet navire (commodity standardized)' }
    ], actions = [
        { value: 'departure_', label: "d'arrivée" },
        { value: 'destination_', label: "de départ" },
    ]

dates.forEach(date => {

    values.forEach(value => {

        actions.forEach(action => {
    
            filters.forEach(filter => {
                
                directions.forEach(direction => {

                    vizHistogramme(date, action, filter, direction, value);
        
                })
        
            })
        })

    })

})



function vizHistogramme(date, action, filter, direction, value) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": `${value.label} des navires ${direction.label} des ports ${action.label} du/de la ${filter.label} en ${date}`,
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
            { "filter": { "field": action.value + filter.field, "equal": filter.filter } },
            { "filter": { "field": `${action.value}action`, "equal": direction.field } }
        ],
    };

    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg', downloadFileName: slug(spec.title) })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}