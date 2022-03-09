import vegaEmbed from 'vega-embed'
import getVizContainer from './get-container';
import slug from 'slug';

const container = document.getElementById('container')
    , dataPath = '/static/data/pointcalls.csv';

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
        { field: 'tonnage_class', label: "tonnage en classe (tonnage_class)"}
    ]
    , directions = [
        { value: 'in', label: "en entrée (in)"},
        { value: 'out', label: "en sortie (out)"},
        { value: 'in-out', label: "en correspondance (in-out)"},
        { value: 'sailing around', label: "en pêche (sailing around)"},
        { value: 'transit', label: "en transit (transit)"}
    ];

dates.forEach(date => {

    filters.forEach(filter => {

        directions.forEach(direction => {

            if (args.schema === 'matrice') {
                for (let i = 0; i < ensembles.length - 1; i++) {
                    for (let j = i + 1; j < ensembles.length; j++) {
                        vizMatrice(date, filter, ensembles[i], ensembles[j], direction)
                    }
                }
            }

            if (args.schema === 'histogramme') {
                ensembles.forEach(ensemble => {
    
                    vizHistogramme(date, filter, ensemble, direction);
    
                })
            }


        })
        

    })

})

function vizMatrice (date, filter, ensemble_x, ensemble_y, direction, value = { field: 'tonnage', label: 'tonnage cumulé' }) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "mark": "rect",
        "data": {
            "url": dataPath
        },
        "title": [
            `${ensemble_x.label} en fonction de ${ensemble_y.label} aggrégé par ${value.label}`,
            `du navire pour les pointcalls (${direction.label}) de ${filter.label} en ${date}`
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
            { "filter": { "field": 'pointcall_action', "equal": direction.value } },
            { "filter": `datum.${ensemble_x.field} != ''` },
            { "filter": `datum.${ensemble_y.field} != ''` }
        ],
        "config": {}
    };
    
    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg', downloadFileName: slug(spec.title.join(' ')) })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}

function vizHistogramme(date, filter, ensemble, direction, value = { field: 'tonnage', label: 'tonnage cumulé' }) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": [
            `${ensemble.label} du navire pour les pointcalls (${direction.label})`,
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
            { "filter": { "field": 'pointcall_action', "equal": direction.value } },
            { "filter": `datum.${ensemble.field} != ''` }
        ],
    };

    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg', downloadFileName: slug(spec.title.join(' ')) })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}


