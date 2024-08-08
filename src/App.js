import './css/App.css';
import { Route, Routes } from 'react-router-dom';
import React from 'react';

import Feedback from './page/feedback';

const PART_A = 0;
const PART_B = 1;

    

function App() {
    // var q_num = 2; //Math.floor(Math.random() * Q_NUM) + 1;

    return (
        <Routes>
            <Route  path='/' element= {<Feedback/>} />
        </Routes>
    );
}

export default App;
