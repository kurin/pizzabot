import { endsWith } from 'lodash';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import { retrieveFoodlist } from './actions.js';

import Header from './shared/Header.jsx';
import Search from './search/Index.jsx';
import Chart from './chart/Index.jsx';

class AppContainer extends Component {
    componentDidMount() {
        this.props.dispatch(retrieveFoodlist());
    }

    render() {
        const { routing, foodData, fetchingFoodList } = this.props;
        const path = routing.location.hash;

        const insetComponentForPath = (endsWith(path, '/chart')) ?
            (<Chart
                foodData={foodData}
                fetchingFoodList={fetchingFoodList}
            />) :
            (<Search
                foodData={foodData}
                fetchingFoodList={fetchingFoodList}
            />);

        return (
            <div>
                <Header />
                {insetComponentForPath}
            </div>
        );
    }
}

AppContainer.propTypes = {
    dispatch: PropTypes.func.isRequired,
    routing: PropTypes.object.isRequired,
    foodData: PropTypes.arrayOf(PropTypes.object.isRequired),
    fetchingFoodList: PropTypes.bool.isRequired,
};

function mapStateToProps(state) {
    return {
        routing: state.routing,
        foodData: state.foodData.data,
        fetchingFoodList: state.foodData.fetchingFoodList,
    };
}

export default connect(mapStateToProps)(AppContainer);
