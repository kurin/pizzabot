import React, { PropTypes } from 'react';
import { RadialChart } from 'react-vis';
import { map } from 'lodash';

export default function PieChart({ foodData }) {
    const chartData = map(foodData,
        (e) => ({ angle: e }));

    const foodChart = foodData ?
        (<div className="food-chart">
            <RadialChart
                data={chartData}
                width={400}
                height={400}
            />
        </div>) : null;

    return (
        <div className="panel panel-primary">
            <div className="panel-heading">
                Food Consumed
            </div>
            {foodChart}
        </div>
    );
}

PieChart.propTypes = {
    foodData: PropTypes.arrayOf(PropTypes.number.isRequired),
};
