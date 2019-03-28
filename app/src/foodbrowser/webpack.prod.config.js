const webpack = require('webpack');

module.exports = {
    entry: [
        './src/main.js'
    ],
    output: {
        path: __dirname,
        filename: "bundle.js"
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env': {
                'NODE_ENV': JSON.stringify('production'),
            },
        }),
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false,
            }
        }),
        new webpack.LoaderOptionsPlugin({
            minimize: true,
            debug: false,
            test: /\.jsx?$/,
            options: {
                eslint: {
                    configFile: '.eslintrc',
                }
            }
        })
    ],
    module: {
        rules: [{
            test: /\.jsx?$/,
            exclude: /node_modules/,
            loader: 'babel-loader',
            options:
            {
                presets:['es2015', 'react'],
                plugins: ['transform-class-properties'],
            },
        },
        {
            test: /\.scss$/,
            exclude: /node_modules/,
            use: [
                'style-loader',
                'css-loader',
                'sass-loader'
            ],
        },
        {
            test: /\.jsx?/,
            exclude: [/node_modules/, /\.json$/],
            loader: 'eslint-loader',
        }]
    },
};
