import vegaEmbed from 'vega-embed'
import getVizContainer from './get-container';
import slug from 'slug';

const container = document.getElementById('container')
    , dataPath = '/static/data/flows.csv';

const dates = [
        '1787',
        '1789'
    ]
    , filters = [
        args.filter
    ]
    , ensembles = [
        { field: 'homeport', label: "port d'attache (homeport)"},
        { field: 'homeport_state_1789_fr', label: "pays d'attache (homeport_state_1789_fr)"},
        { field: 'flag', label: "pays du pavillon (drapeau) (flag)"},
        { field: args.filter.field === 'destination' ? 'departure' : 'destination', label: `port de ${args.filter.field === 'destination' ? 'départ' : 'destination'}`},
        { field: args.filter.field === 'destination' ? 'departure_state_1789_fr' : 'destination_state_1789_fr', label: `pays du port de ${args.filter.field === 'destination' ? 'départ' : 'destination'}`},
    ];

dates.forEach(date => {

    filters.forEach(filter => {


        if (args.schema === 'matrice') {
            for (let i = 0; i < ensembles.length - 1; i++) {
                for (let j = i + 1; j < ensembles.length; j++) {
                    vizMatrice(date, filter, ensembles[i], ensembles[j])
                }
            }
        }

        if (args.schema === 'histogramme') {
            ensembles.forEach(ensemble => {

                vizHistogramme(date, filter, ensemble);

            })
        }

    })

})

function vizMatrice (date, filter, ensemble_x, ensemble_y, value = { field: 'tonnage', label: 'tonnage cumulé' }) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "mark": "rect",
        "data": {
            "url": dataPath
        },
        "title": [
            `${value.label} en fonction du ${ensemble_x.label} et du ${ensemble_y.label}`,
            `du navire pour les flows de ${filter.label} en ${date}`
        ],
        "encoding": {
            "x": {
                "field": ensemble_x.field,
                "type": "nominal",
                "sort": "-color",
                "axis": {
                    "orient": "top"
                },
                "title": ensemble_x.label
            },
            "y": {
                "field": ensemble_y.field,
                "type": "nominal",
                "sort": "-color",
                "title": ensemble_y.label
            },
            "color": {
                "field": value.field,
                "aggregate": "sum",
                "type": "quantitative"
            }
        },
        "transform": [
            { "filter": { "field": "year", "equal": date } },
            { "filter": { "field": filter.field, "equal": filter.filter } },
            // { "filter": { "field": action.field, "equal": direction.value } },
            { "filter": `datum.${ensemble_x.field} != ''` },
            { "filter": `datum.${ensemble_y.field} != ''` }
        ],
        "config": {}
    };
    
    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg', downloadFileName: slug(spec.title.join(' ')) })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}

function vizHistogramme(date, filter, ensemble, value = { field: 'tonnage', label: 'tonnage cumulé' }) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": [
            `${ensemble.label} du navire pour les flows`,
            `de ${filter.label}, aggrégés par ${value.label} en ${date}`
        ],
        "mark": "bar",
        "data": {
            "url": dataPath
        },
        "encoding": {
            "x": { "field": value.field, "type": "quantitative", "aggregate": "sum", "title": value.label },
            "y": { "field": ensemble.field, "type": "nominal", "sort": "-x", "title": ensemble.label },
            "color": {
                "condition": {
                    "test": `datum['${ensemble.field}'] == 'Dunkerque' || datum['${ensemble.field}'] == 'Flandre'`,
                    "value": "#e39382"
                }
            }
        },
        "transform": [
            { "filter": { "field": "year", "equal": date } },
            { "filter": { "field": filter.field, "equal": filter.filter } },
            // { "filter": { "field": action.field, "equal": direction.value } },
            { "filter": `datum.${ensemble.field} != ''` }
        ],
    };

    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg', downloadFileName: slug(spec.title.join(' ')) })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}