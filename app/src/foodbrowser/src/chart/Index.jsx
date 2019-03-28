import React, { Component, PropTypes } from 'react';
import ReactSpinner from 'react-spinjs';
import { filter, without } from 'lodash';

import Sidebar from '../shared/Sidebar.jsx';
import PieChart from './components/PieChart.jsx';

const searchBoxValues = {
    first: {
        ID: 'first',
        heading: 'First food',
    },
    second: {
        ID: 'second',
        heading: 'Second food',
    },
    third: {
        ID: 'third',
        heading: 'Third food',
    },
    fourth: {
        ID: 'fourth',
        heading: 'Fourth food',
    },
    fifth: {
        ID: 'fifth',
        heading: 'Fifth food',
    },
};

export default class Chart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            searchFoodOne: '',
            searchFoodTwo: '',
            searchFoodThree: '',
            searchFoodFour: '',
            searchFoodFive: '',
            chartData: [],
        };
        this.handleSearchStringChange = this.handleSearchStringChange.bind(this);
        this.createChart = this.createChart.bind(this);
    }

    handleSearchStringChange(e) {
        const { first, second, third, fourth, fifth } = searchBoxValues;
        switch (e.target.id) {
            case first.ID:
                this.setState({ searchFoodOne: e.target.value });
                break;
            case second.ID:
                this.setState({ searchFoodTwo: e.target.value });
                break;
            case third.ID:
                this.setState({ searchFoodThree: e.target.value });
                break;
            case fourth.ID:
                this.setState({ searchFoodFour: e.target.value });
                break;
            case fifth.ID:
                this.setState({ searchFoodFive: e.target.value });
                break;
            default:
                break;
        }
    }

    createChart() {
        const { searchFoodOne, searchFoodTwo, searchFoodThree,
            searchFoodFour, searchFoodFive } = this.state;
        const { foodData } = this.props;

        const firstDataItem = searchFoodOne ?
            filter(foodData, (e) => e.what.includes(searchFoodOne)).length : null;
        const secondDataItem = searchFoodTwo ?
            filter(foodData, (e) => e.what.includes(searchFoodTwo)).length : null;
        const thirdDataItem = searchFoodThree ?
            filter(foodData, (e) => e.what.includes(searchFoodThree)).length : null;
        const fourthDataItem = searchFoodFour ?
            filter(foodData, (e) => e.what.includes(searchFoodFour)).length : null;
        const fifthDataItem = searchFoodFive ?
            filter(foodData, (e) => e.what.includes(searchFoodFive)).length : null;

        const data = without([firstDataItem, secondDataItem, thirdDataItem,
            fourthDataItem, fifthDataItem], null);
        this.setState({ chartData: data });
    }

    render() {
        const insetComponent = this.props.fetchingFoodList ?
            (<ReactSpinner color="black" />) :
            (<div>
                <div className="col-md-2 sidebar">
                    <Sidebar
                        textAction={this.handleSearchStringChange}
                        searchBoxValues={searchBoxValues}
                    />
                    <button
                        className="btn btn-danger"
                        onClick={this.createChart}
                    >
                        Create Chart!
                    </button>
                </div>
                <div className="col-md-10 main">
                    <PieChart foodData={this.state.chartData} />
                </div>
            </div>);

        return (
            <div className="container-fluid">
                <div className="row">
                    {insetComponent}
                </div>
            </div>
        );
    }
}

Chart.propTypes = {
    foodData: PropTypes.array.isRequired,
    fetchingFoodList: PropTypes.bool.isRequired,
};
