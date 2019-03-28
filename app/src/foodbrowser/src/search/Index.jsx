import React, { PropTypes } from 'react';
import ReactSpinner from 'react-spinjs';

import Table from './components/Table.jsx';

export default function Search({ foodData, fetchingFoodList }) {
    const insetComponent = fetchingFoodList ?
        (<ReactSpinner color="black" />) : (<Table foodData={foodData} />);

    const tableBufferCSSClassName = !fetchingFoodList ?
        'foodbrowser-bootstrap-table-wrapper' : '';
    return (
        <div className="container-fluid">
            <div className={`col-lg-14 main ${tableBufferCSSClassName}`}>
                {insetComponent}
            </div>
        </div>
    );
}

Search.propTypes = {
    foodData: PropTypes.array.isRequired,
    fetchingFoodList: PropTypes.bool.isRequired,
};
