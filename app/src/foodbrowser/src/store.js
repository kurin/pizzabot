import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import createLogger from 'redux-logger';
import { browserHistory } from 'react-router';
import { syncHistory } from 'react-router-redux';

const logger = createLogger();
const historyMiddleware = syncHistory(browserHistory);

export const createStoreWithMiddleware = process.env.NODE_ENV === 'development' ?
    applyMiddleware(thunk, logger, historyMiddleware)(createStore) :
    applyMiddleware(thunk, historyMiddleware)(createStore);
