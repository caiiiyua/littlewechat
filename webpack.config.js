/**
 * Created by pp on 16/2/21.
 */
'use strict'

var path = require('path');

module.exports = {
    entry: ['webpack/hot/dev-server', path.resolve(__dirname, 'static/js/app.js')],
    output: {
        path: path.resolve(__dirname, 'static'),
        filename: 'bundle.js'
    },
    module: {
        loaders: [
            {test: /\.jsx?$/, loaders: ['jsx?harmony']}
        ]
    }
};