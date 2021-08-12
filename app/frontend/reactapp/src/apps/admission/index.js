import React from 'react';
import ReactDOM from 'react-dom';

import './index.css';
// import "flatpickr/dist/themes/light.css";
import "flatpickr/dist/themes/dark.css";
// import "flatpickr/dist/themes/airbnb.css";
// airbnb.css
// confetti.css
// dark.css
// light.css
// material_blue.css
// material_green.css
// material_orange.css
// material_red.css


import AdmissionForm from './AdmissionForm.js'


function AdmissionApp() {
    return (
        <React.Fragment>
            <AdmissionForm />
        </React.Fragment>
    );
}


ReactDOM.render(
    <AdmissionApp />,
    document.getElementById('root')
);
