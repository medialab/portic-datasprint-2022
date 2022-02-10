import vegaEmbed from 'vega-embed'
import getVizContainer from './get-container';

const container = document.getElementById('container');

['1787', '1789'].forEach(date => {

    [
        { field: 'import', label: 'import depuis le port de Dunkerque (Dunkerque vers le reste de la France)' },
        { field: 'export', label: 'export vers le port de Dunkerque (le reste de la France vers Dunkerque)' }
    ].forEach(direction => {

        [
            { field: 'customs_region', label: 'bureau de ferme' },
            { field: 'customs_office', label: 'direction de ferme' },
            { field: 'origin', label: 'origine' },
            { field: 'origin_province', label: 'province d\'origine' }
        ].forEach(localisation => {

            ['product_simplification', 'product_revolutionempire', 'product_sitc_FR', 'product_RE_aggregate'].forEach(class_produit => {

                vizMatrice(date, direction, localisation, class_produit);

            });

            vizHistogramme(date, direction, localisation);

        });
    
    });

});

/**
 * @param {string|number} date
 * @param {'import'|'export'} direction
 * @param {object} localisation
 * @param {string} class_produit
 * @returns {undefined}
 */

function vizMatrice (date, direction, localisation, class_produit) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "mark": "rect",
        "data": {
            "url": "/static/data/product.csv"
        },
        "title": [
            `${direction.label} de produits (aggrégés par valeur cumulée) détaillés`,
            `selon la classification "${class_produit}" et pointés par ${localisation.label} en ${date}`
        ],
        "encoding": {
            "x": {
                "field": localisation.field,
                "type": "nominal",
                "sort": "-color",
                "axis": {
                    "orient": "top"
                },
                "title": localisation.label
            },
            "y": {
                "field": class_produit,
                "type": "nominal",
                "sort": "-color",
                "title": `produits (classification '${class_produit}')`
            },
            "color": {
                "field": "value",
                "aggregate": "sum",
                "type": "quantitative"
            }
        },
        "transform": [
            { "filter": { "field": "year", "equal": date } },
            { "filter": { "field": direction.field, "equal": "yes" } }
        ],
        "config": {}
    };
    
    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg' })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}

/**
 * @param {string|number} date
 * @param {'import'|'export'} direction
 * @param {object} localisation
 * @returns {undefined}
 */

function vizHistogramme (date, direction, localisation) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": `Valeur cummulée des ${direction.label} en ${date} vers des ${localisation.label}`,
        "mark": "bar",
        "data": {
            "url": "/static/data/product.csv"
        },
        "encoding": {
          "x": {"field": "value", "type": "quantitative", "aggregate": "sum", "title": "Valeur cummulée"},
          "y": {"field": localisation.field, "type": "nominal", "sort": "-x", "title": localisation.label}
        },
        "transform": [
          {"filter": {"field": "year", "equal": date}},
          {"filter": {"field": direction.field, "equal": "yes"}}
        ],
      };
    
    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite", renderer: 'svg' })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}