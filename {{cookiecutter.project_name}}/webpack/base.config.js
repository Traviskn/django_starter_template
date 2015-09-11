var Webpack = require("webpack");
var Path = require("path");
var cssnext = require("cssnext");

var config = {
  context: Path.resolve(__dirname, "../"),

  entry: {
    home: [
      "./static/source/js/index"
    ]
  },

  output: {
    path: Path.resolve(__dirname, "../static/build/"),
    filename: "[name]-[hash].js"
  },

  module: {
    preLoaders: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loaders: ["eslint-loader"]
      }
    ],
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loaders: ["babel"]
      }, {
        test: /\.css$/,
        loaders: ["style", "css", "postcss"]
      }, {
        test: /\.(png|jpg)$/,
        loader: "url?limit=25000"
      }
    ]
  },

  resolve: {
    modulesDirectories: ["node_modules"],
    extensions: ["", ".js", ".jsx"]
  },

  externals: {
    "jquery": "jQuery"
  },

  plugins: [
    new Webpack.NoErrorsPlugin(),
    new Webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    })
    // If multiple entrypoints share code dependencies
    //new Webpack.optimize.CommonsChunkPlugin('common.js')
  ],

  postcss: function() {
    return [cssnext];
  },

  eslint: {
    configFile: ".eslintrc"
  }
};

module.exports = config;
