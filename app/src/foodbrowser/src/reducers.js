import { combineReducers } from 'redux';
import { routeReducer } from 'react-router-redux';

import { START_FETCH_FOOD_LIST, COMPLETE_FETCH_FOODLIST, FAIL_FETCH_FOODLIST } from './actions';

const initialDataState = {
    data: [],
    fetchingFoodList: false,
};

export function foodData(state = initialDataState, action) {
    switch (action.type) {
        case START_FETCH_FOOD_LIST:
            return Object.assign({}, state, {
                fetchingFoodList: true,
            });
        case COMPLETE_FETCH_FOODLIST:
            return Object.assign({}, state, {
                data: action.data,
                fetchingFoodList: false,
            });
        case FAIL_FETCH_FOODLIST:
            return Object.assign({}, state, {
                fetchingFoodList: false,
            });
        default:
            return state;
    }
}

export const mainReducer = combineReducers({
    foodData,
    routing: routeReducer,
});
