import '../static/main.scss';

import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import { Router, Route, browserHistory } from 'react-router';

import { createStoreWithMiddleware } from './store';
import { mainReducer } from './reducers';

import AppContainer from './App.jsx';

const store = createStoreWithMiddleware(mainReducer);

render(
    <Provider store={store}>
        <Router history={browserHistory}>
            <Route path="/search" component={AppContainer} />
            <Route path="/chart" component={AppContainer} />
            <Route path="*" component={AppContainer} />
        </Router>
    </Provider>,
    document.getElementById('mount')
);
