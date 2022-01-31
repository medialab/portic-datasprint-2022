const path = require('path');
const viz = require('./src/data/viz.json')

const entries = {};

for (const item of viz) {
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