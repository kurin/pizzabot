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
        new webpack.SourceMapDevToolPlugin({
            filename: '[file].map',
            exclude: ['vendor.bundle.js'],
        }),
        new webpack.DefinePlugin({
            'process.env': {
                'NODE_ENV': JSON.stringify('development'),
            },
        }),
        new webpack.LoaderOptionsPlugin({
            test: /\.jsx?$/,
            options: {
                eslint: {
                    configFile: '.eslintrc',
                }
            }
        }),
    ],
    module: {
        rules: [{
            test: /\.jsx?$/,
            exclude: /node_modules/,
            loader: 'babel-loader',
            query:
            {
                presets:['es2015', 'react'],
                plugins: ['transform-class-properties'],
                env: {
                    development: {
                        presets: ['react-hmre'],
                    },
                },
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
    watchOptions: {
        poll: 1000,
    },
    devServer: {
        historyApiFallback: {
            index: '/',
        },
    },
};
