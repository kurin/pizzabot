import React, { PropTypes } from 'react';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';

export default function Table({ foodData }) {
    const paginationOptions = {
        sizePerPageList: [50, 100, 500, 1000],
        sizePerPage: 50,
        paginationShowsTotal: true,
    };

    return (
        <div className="panel panel-primary">
            <div className="panel-heading">
                Food Consumed
            </div>
            <BootstrapTable
                data={foodData}
                striped
                hover
                exportCSV
                csvFileName="fooddata.csv"
                pagination
                options={paginationOptions}
            >
                <TableHeaderColumn
                    dataField="date"
                    isKey
                    hidden
                />
                <TableHeaderColumn
                    dataField="date"
                    csvHeader="Date"
                    width="250"
                    dataSort
                    filter={{ type: 'DateFilter', delay: 1000 }}
                >
                    When
                </TableHeaderColumn>
                <TableHeaderColumn
                    dataField="who"
                    csvHeader="Who"
                    width="175"
                    dataSort
                    filter={{ type: 'TextFilter', delay: 1000 }}
                >
                    Who
                </TableHeaderColumn>
                <TableHeaderColumn
                    dataField="what"
                    csvHeader="What"
                    dataSort
                    filter={{ type: 'TextFilter', delay: 1000 }}
                >
                    What
                </TableHeaderColumn>
            </BootstrapTable>
        </div>
    );
}

Table.propTypes = {
    foodData: PropTypes.arrayOf(PropTypes.object.isRequired),
};
