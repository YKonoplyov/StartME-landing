import React from 'react';
import {Route, Routes} from "react-router-dom";
import HomePage from "@/components/HomePage";
import Table from "@/components/table/Table";

function App() {

    return (
        <Routes>
            <Route exact path="/" element={<HomePage/>}/>
            <Route path="/table" element={<Table/>}/>
        </Routes>
    );
}

export default App;