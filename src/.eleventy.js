const pckData = require('../package.json')
    // , config = require('../config.json');

module.exports = function(e) {
    e.addGlobalData('pck', pckData);
    // e.addGlobalData('config', config);
    // e.addGlobalData('vizualisations', config.visualizations);

    e.addPassthroughCopy("static");

    return {
        dir: {
            input: "./",
            output: "../dist",
            includes: "includes",
            layouts: "layouts",
            data: "data"
        }
    };
};