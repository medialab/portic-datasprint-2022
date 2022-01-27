const container = document.getElementById('container');

['1787', '1789'].forEach(date => {

    [{ field: 'import', label: 'import depuis' }, { field: 'import', label: 'export vers' }].forEach(direction => {

        ['customs_region', 'customs_office'].forEach(localisation => {

            ['product_simplification', 'product_revolutionempire'].forEach(class_produit => {

                vizMatrice(date, direction, localisation, class_produit);

            });

            vizHistogramme(date, direction, localisation);

        });
    
    });

});

/**
 * Get a div (append into page container) to
 * append a viz
 * @returns {HTMLDivElement}
 */

function getVizContainer () {
    const div = document.createElement('div');
    div.classList.add('block', 'viz')
    container.appendChild(div)
    return div;
}

/**
 * @param {string|number} date
 * @param {'import'|'export'} direction
 * @param {'customs_region'|'customs_office'} localisation
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
        "title": `${direction.label} le port de Dunkerque en ${date}, détaillé par produit (classification '${class_produit}') et par ${localisation}, aggrégé par valeur cumulée`,
        "encoding": {
            "x": {
                "field": localisation,
                "type": "nominal",
                "sort": "-color",
                "axis": {
                    "orient": "top"
                },
                "title": localisation
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
    
    vegaEmbed(getVizContainer(), spec, { mode: "vega-lite", renderer: 'svg' })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}

/**
 * @param {string|number} date
 * @param {'import'|'export'} direction
 * @param {'customs_region'|'customs_office'} localisation
 * @returns {undefined}
 */

function vizHistogramme (date, direction, localisation) {
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": `Valeur cummulée des ${direction.label} le port de Dunkerque en ${date} vers des ${localisation}`,
        "mark": "bar",
        "data": {
            "url": "/static/data/product.csv"
        },
        "encoding": {
          "x": {"field": "value", "type": "quantitative", "aggregate": "sum", "title": "Valeur cummulée"},
          "y": {"field": localisation, "type": "nominal", "sort": "-x", "title": "Bureau de ferme"}
        },
        "transform": [
          {"filter": {"field": "year", "equal": date}},
          {"filter": {"field": direction.field, "equal": "yes"}}
        ],
      };
    
    vegaEmbed(getVizContainer(), spec, { mode: "vega-lite" })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}