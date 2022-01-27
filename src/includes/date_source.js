const container = document.getElementById('viz');
const output = document.querySelector('output');

['export', 'import'].forEach(direction => {
    const titleDirection = document.createElement('h2')
    titleDirection.textContent = direction;
    titleDirection.classList.add('title', 'is-4')
    container.appendChild(titleDirection)


    for (const file of vizConfig.build.files) {
        const vizContainer = document.createElement('div')
        vizContainer.classList.add('box')
        const vizTitle = document.createElement('h3')
        vizTitle.classList.add('title', 'is-6')
        vizTitle.textContent = file;
        container.appendChild(vizTitle)
        container.appendChild(vizContainer)
    
    
        const spec = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "A simple bar chart with embedded data.",
            "data": {
                // "url": `/static/data/${'rand.csv'}`
                "url": `/static/data/${file}`
            },
            "mark": {
                type: "bar",
                tooltip: true
            },
            "width": 1200,
            "height": 200,
            "encoding": {
                "y": {
                    "field": "year",
                    // "type": "temporal",
                    "type": "ordinal",
                    "timeUnit": {
                        unit: "year",
                        // step: 1
                    },
                    "title": "Années"
                },
                "x": {"field": "value", "type": "quantitative", "aggregate": "sum", "title": "Sommes des valeurs"}
            },
            "transform": [
                {"filter": {"field": direction, "equal": "yes"}}
            ],
            "config": {}
        };
        
        vegaEmbed(vizContainer, spec, {mode: "vega-lite"})
            .then((response) => { console.log(response) })
            .catch((response) => { output.textContent = response });
    }
})