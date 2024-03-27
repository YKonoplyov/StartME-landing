import React from 'react';
import ReactDOM from 'react-dom/client';
import './style/normalize.scss';
import App from './App';
import {BrowserRouter} from "react-router-dom";
import {Helmet} from "react-helmet";
import Images from "@/image/image";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <>
        <Helmet>
            <link rel="apple-touch-icon" sizes="180x180" href={Images.applefavicon}/>
            <link rel="icon" type="image/png" sizes="32x32" href={Images.applefavicon32}/>
            <link rel="icon" type="image/png" sizes="16x16" href={Images.applefavicon16}/>
            <link rel="mask-icon" href={Images.applefaviconsaf} color="#000000"/>
            <link rel="manifest" href="./site.webmanifest"/>
            <meta name="msapplication-TileColor" content="#000000"/>
            <meta name="theme-color" content="#ffffff"/>
        </Helmet>
        <BrowserRouter>
            <App/>
        </BrowserRouter>
    </>
);