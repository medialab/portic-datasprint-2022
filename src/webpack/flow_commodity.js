import vegaEmbed from 'vega-embed'
import getVizContainer from './get-container';
import slug from 'slug';

const container = document.getElementById('container')
    , dataPath = '/static/data/flow_commodity.csv';

const dates = [
        '1787',
        '1789'
    ]
    , filters = [
        { field: 'departure', filter: 'Dunkerque', label: "port de départ (Dunkerque)"},
        { field: 'destination', filter: 'Dunkerque', label: "port d'arrivée (Dunkerque)"}
    ]
    , ensembles = [
        { field: 'homeport', label: "port d'attache (homeport)"},
        { field: 'homeport_state_1789_fr', label: "pays d'attache (homeport_state_1789_fr)"},
        { field: 'flag', label: "pays du pavillon (drapeau) (flag)"},
        { field: 'departure_or_destination'},
        { field: 'departure_or_destination_state'}
    ];

dates.forEach(date => {

    filters.forEach(filter => {

        ensembles.forEach((ensemble) => {

            vizMatrice(date, filter, ensemble);

        })

    })

})

function vizMatrice (date, filter, ensemble) {
    if (ensemble.field === 'departure_or_destination') {
        if (filter.field === 'destination') {
            ensemble.field = 'departure'
            ensemble.label = 'port de départ';
        } else {
            ensemble.field = 'destination';
            ensemble.label = 'port de destination';
        }
    }

    if (ensemble.field === 'departure_or_destination_state') {
        if (filter.field === 'destination') {
            ensemble.field = 'departure_state_1789_fr'
            ensemble.label = 'État de départ';
        } else {
            ensemble.field = 'destination_state_1789_fr';
            ensemble.label = 'État de destination';
        }
    }
    

    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "mark": "rect",
        "data": {
            "url": dataPath
        },
        "title": [
            `${ensemble.field} en fonction des objets de voyage aggrégés par tonnage cumulé, pondéré par nombre de commodités par bateau en ${date}`,
            `filtré par ${filter.label}`
        ],
        "encoding": {
            "x": {
                "field": ensemble.field,
                "type": "nominal",
                "sort": "-color",
                "axis": {
                    "orient": "top"
                },
                "title": ensemble.label
            },
            "y": {
                "field": 'commodity_standardized',
                "type": "nominal",
                "sort": "-color",
                "title": "objets de voyage"
            },
            "color": {
                "field": 'tonnage',
                "aggregate": "sum",
                // "aggregate": "count",
                "type": "quantitative",
                "title": "tonnage cumulé, pondéré par nombre de commodités par bateau"
            }
        },
        "transform": [
            { "filter": { "field": "year", "equal": date } },
            { "filter": { "field": filter.field, "equal": filter.filter } },
            { "filter": `datum.${ensemble.field} != ''` }
        ],
        "config": {}
    };
    
    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg', downloadFileName: slug(spec.title.join(' ')) })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}