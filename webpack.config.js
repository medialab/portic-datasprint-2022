const fs = require('fs')
    , path = require('path')
    , yml = require('js-yaml');

let vizList = fs.readFileSync(path.join(__dirname, './src/data/viz.yml'));
vizList = yml.load(vizList);

const entries = {};

for (const item of vizList) {
    entries[item.name] = path.resolve(__dirname, './src/webpack/', item.script)
}

module.exports = {
    entry: entries,
    output: {
        path: path.resolve(__dirname, './src/static/js/'),
        filename: '[name].js',
    },
    module: {
        rules: [
            {
                test: /\.css$/i,
                use: ["style-loader", "css-loader"],
            }
        ]
    },
    mode: 'development'
};