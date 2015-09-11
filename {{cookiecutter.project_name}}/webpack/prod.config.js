var Webpack = require("webpack");
var config = require("./base.config.js");
var BundleTracker = require("webpack-bundle-tracker");
var Path = require("path");
var Clean = require("clean-webpack-plugin");
var cssnext = require("cssnext");
var csswring = require("csswring");

config.output.path = Path.resolve(__dirname, "../static/deploy/");

config.plugins.push(
  new BundleTracker({
    filename: "./webpack/webpack-stats-prod.json"
  })
);
config.plugins.push(
  new Webpack.DefinePlugin({
    "process.env": {
      "NODE_ENV": JSON.stringify("production")
    }
  })
);
config.plugins.push(new Webpack.optimize.OccurenceOrderPlugin());
config.plugins.push(new Webpack.optimize.DedupePlugin());
config.plugins.push(
  new Webpack.optimize.UglifyJsPlugin({
    compressor: {
      warnings: false
    }
  })
);
config.plugins.push(new Clean(["static/deploy"]));

config.postcss = function() { return [cssnext, csswring]; };

module.exports = config;
