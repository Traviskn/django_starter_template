var Webpack = require("webpack");
var Path = require("path");
var BundleTracker = require("webpack-bundle-tracker");
var Clean = require("clean-webpack-plugin");
var config = require("./base.config.js");

config.output.publicPath = "http://localhost:8080/static/";

config.plugins.push(new Webpack.HotModuleReplacementPlugin());
config.plugins.push(
  new BundleTracker({
    filename: "./webpack/webpack-stats.json"
  })
);
config.plugins.push(new Clean(["static/build"]));

config.devtool = "source-map";

config.devServer = {
  contentBase: Path.resolve(__dirname, "../static/build"),
  hot: true,
  inline: true,
  stats: { colors: true }
};

module.exports = config;
