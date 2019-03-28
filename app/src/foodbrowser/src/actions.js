import axios from 'axios';

export const START_FETCH_FOOD_LIST = 'START_FETCH_FOOD_LIST';
export const COMPLETE_FETCH_FOODLIST = 'COMPLETE_FETCH_FOODLIST';
export const FAIL_FETCH_FOODLIST = 'FAIL_FETCH_FOODLIST';

const foodlistAPI = 'http://talking.pizza:5000/foodlist-api';

function startFetchFoodList() {
    return {
        type: START_FETCH_FOOD_LIST,
    };
}

export function completeFetchFoodlist(data) {
    return {
        type: COMPLETE_FETCH_FOODLIST,
        data,
    };
}

export function failFetchFoodlist() {
    return {
        type: FAIL_FETCH_FOODLIST,
    };
}

export function retrieveFoodlist() {
    return (dispatch) => {
        dispatch(startFetchFoodList());
        axios.get(foodlistAPI)
            .then(response => dispatch(completeFetchFoodlist(response.data)))
            .catch(() => dispatch(failFetchFoodlist()));
    };
}
