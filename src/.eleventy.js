const pckData = require('../package.json')
    , yml = require("js-yaml");

module.exports = function(e) {
    e.addGlobalData('pck', pckData);

    e.addDataExtension("yml", contents => yml.load(contents));

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