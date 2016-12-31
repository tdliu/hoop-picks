var webpack = require('webpack');
var path = require('path');
 
var BUILD_DIR = path.resolve(__dirname, '../public/js');
var APP_DIR = path.resolve(__dirname, 'src/app');
 
var config = {
    entry: {
        goatreact: APP_DIR + '/goatreact.jsx'
    },
    output: {
        path: BUILD_DIR,
        filename: "[name].bundle.js"
    },
    module : {
        loaders : [
            {
                test : /\.jsx?/,
                include : APP_DIR,
                loader : 'babel'
            },
            {include: /\.json$/, loaders: ["json-loader"]}
        ]
    }
};
 
module.exports = config;