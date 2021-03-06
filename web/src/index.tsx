import React from 'react';
import ReactDOM from 'react-dom';
import { HashRouter } from 'react-router-dom';

import { CssBaseline } from '@material-ui/core';

import App from './components/App/App';
import * as serviceWorker from './utils/serviceWorker';

const app = (
    <React.Fragment>
        <CssBaseline />
        <HashRouter>
            <App />
        </HashRouter>
    </React.Fragment>
);

ReactDOM.render(app, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
