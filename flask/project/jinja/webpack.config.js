const webpack = require("webpack");

const glob = require("glob");
const path = require("path");

const { VueLoaderPlugin } = require("vue-loader");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");

const WebpackAssetsManifest = require("webpack-assets-manifest");

const CONFIG = {
  isProd: process.env.NODE_ENV === "production",
  paths: {
    src: file => path.join("assets", file || ""),
    dst: file => path.join("static", file || "")
  }
};

function makeEntries() {
  const src = `./${CONFIG.paths.src("js")}/`;
  const entries = {};

  glob.sync(path.join(src, "/**/main.js"))
    .map(file => `./${file}`)
    .forEach(file => {
      let name = path.dirname(file);
      name = name.substr(name.lastIndexOf("/") + 1);
      entries[name] = file;
    });
  return entries;
}

const plugins = (() => {
  let plugins = [
    new CleanWebpackPlugin({
      cleanOnceBeforeBuildPatterns: [
        "**/*",
        "!fonts/**/*",
        "!images/**/*"
      ]
    }),
    new MiniCssExtractPlugin({
      filename: CONFIG.isProd ? "css/[name]-[chunkhash:8].css" : "css/[name].css"
    }),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: CONFIG.paths.src("images/*"),
          to: "images/[name][ext]"
        }
      ]
    }),
    new VueLoaderPlugin()
  ];

  if (CONFIG.isProd) {
    plugins = plugins.concat([
      new WebpackAssetsManifest({
        output: "manifest.json",
        merge: false,
        customize(entry, original, manifest, asset) {
          let key = "";
          switch (manifest.getExtension(entry.value).substring(1).toLowerCase()) {
            case "js":
              key = `js/${entry.key}`;
              break;
            case "css":
              key = `css/${entry.key}`;
              break;
            default:
              return false;
          }
          return {
            key: key,
            value: entry.value
          }
        }
      })
    ]);
  }
  return plugins;
})();

module.exports = {
  mode: CONFIG.isProd ? "production" : "development",
  entry: Object.assign({ vendor: ["vue", "bootstrap-vue", "axios", "moment", "lodash", "common"] }, makeEntries()),
  output: {
    path: path.resolve(CONFIG.paths.dst()),
    filename: CONFIG.isProd ? "js/[name]-[chunkhash:8].js" : "js/[name].js",
    publicPath: "/",
    chunkFilename: CONFIG.isProd ? "js/[name]-[chunkhash:8].js" : "js/[name].js",
  },
  resolve: {
    alias: {
      common: `./${CONFIG.paths.src("js")}/common/common.js`,
      vue: CONFIG.isProd ? "vue/dist/vue.min.js" : "vue/dist/vue.js"
    },
    extensions: [".js", ".vue", ".json"]
  },
  optimization: {
    minimize: CONFIG.isProd,
    removeEmptyChunks: true,
    runtimeChunk: {
      name: "manifest",
    }
  },
  module: {
    rules: [{
      test: /\.js$/,
      exclude: [/node_modules/],
      use: [
        "babel-loader"
      ]
    }, {
      test: /\.css/,
      use: [
        {
          loader: MiniCssExtractPlugin.loader
        },
        "css-loader",
      ]
    }, {
      test: /\.less$/,
      use: [
        {
          loader: MiniCssExtractPlugin.loader
        },
        "css-loader",
        "less-loader"
      ]
    }, {
      test: /\.(eot|woff|woff2|ttf)$/,
      use: [
        {
          loader: "url-loader",
          options: {
            limit: 10240,
            name: CONFIG.isProd ? "fonts/[name]-[hash:8].[ext]" : "fonts/[name].[ext]",
            publicPath: "/static/"
          }
        }
      ]
    }, {
      test: /\.(svg|png|jpg|gif)$/,
      use: [
        {
          loader: "url-loader",
          options: {
            limit: 10240,
            name: CONFIG.isProd ? "images/[name]-[hash:8].[ext]" : "images/[name].[ext]",
            publicPath: "/static/"
          }
        }
      ]
    }, {
      test: /\.vue$/,
      loader: "vue-loader"
    }]
  },
  plugins: plugins,
  devtool: "cheap-source-map"
};
