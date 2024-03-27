const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const CopyPlugin = require("copy-webpack-plugin");

const isProduction = process.env.NODE_ENV === 'production';

module.exports = {
    mode: isProduction ? 'production' : 'development',
    entry: './src/index.js',
    output: {
        filename: '[name].[contenthash].js',
        path: path.resolve(__dirname, 'dist'),
        clean: true
    },
    optimization: {
        usedExports: true,
        splitChunks: {
            chunks: 'all',
            //name: 'vendor'
        },
        minimize: true,
        minimizer: [
            new CssMinimizerPlugin(),
            new TerserPlugin()
        ]
    },
    devServer: {
        static: {
            directory: path.join(__dirname, 'src'),
        },
        compress: true,
        historyApiFallback: true,
        port: 9000,
        allowedHosts: 'all',
    },
    resolve: {
        extensions: ['.js', '.json', '.jsx', '.scss'],
        alias: {
            '@styles': path.resolve(__dirname, 'src/style'),
            '@': path.resolve(__dirname, 'src'),
        }
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-react'],
                    },
                },
            },
            {
                test: /\.css$/i,
                use: [MiniCssExtractPlugin.loader, 'css-loader'],
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    {
                        loader: 'postcss-loader',
                        options: {
                            postcssOptions: {
                                config: './postcss.config.js',
                            },
                        },
                    },
                    "sass-loader"
                ],
            },
            {
                test: /\.(png|webp|jpg|jpeg|svg|gif|ico)$/i,
                type: 'asset/resource',
                generator: {
                    filename: 'image/[name].[contenthash].[ext]'
                }
            },
            {
                test: /\.(ttf|woff|woff2|eot)$/i,
                type: 'asset/resource',
                generator: {
                    filename: 'fonts/[name].[ext]'
                }
            },
            {
                test: /\.xml$/i,
                use: ['xml-loader']
            }
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './public/index.html',
            minify: isProduction ? {
                removeAttributeQuotes: true,
                collapseWhitespace: true,
                removeComments: true,
            } : false,
        }),
        new CopyPlugin({
            patterns: [
                { from: "public/site.webmanifest", to: "" },
                { from: "src/components/table/records.json", to: "" },
            ],
        }),
        new CleanWebpackPlugin(
        ),
        new MiniCssExtractPlugin({
            filename: '[name].[contenthash].css'
        }),
        //new webpack.HotModuleReplacemenPlugin()
    ],
};