export default function () {
    vegaEmbed(getVizContainer(container), spec, { mode: "vega-lite" })
        .then((response) => { console.log(response) })
        .catch((response) => { console.error(response) });
}