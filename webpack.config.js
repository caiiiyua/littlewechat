/**
 * Created by pp on 16/2/21.
 */
'use strict'

var path = require('path');

module.exports = {
  entry: path.resolve(__dirname, 'static/js/app.js'),
  output: {
      path: path.resolve(__dirname, 'static'),
      filename: 'bundle.js'
  },
  module: {
      loaders:[
          {
              test: /\.js[x]?$/,
              exclude: /node_modules/,
              loader: 'babel',
              query:
              {
                presets:['es2015', 'react']
              }
          }, {
              test: /\.less$/,
              loader: 'style!css!autoprefixer!less'
          }, {
              test: /\.css/,
              loader: 'style!css'
          }, {
              test: /\.(png|jpg)$/,
              loader: 'url?limit=25000'
          }
      ]
  },
};
