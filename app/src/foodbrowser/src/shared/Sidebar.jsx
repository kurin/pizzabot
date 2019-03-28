import { includes, map, values } from 'lodash';
import React, { PropTypes } from 'react';

import SearchBox from './SearchBox.jsx';

export default function SearchSidebar({ clickAction, textAction, searchBoxValues,
    activeFilters }) {
    const searchBoxes = map(values(searchBoxValues), (val) => {
        const clickValue = includes(activeFilters, val.ID) ? 'Reset' : 'Search';
        return (
            <SearchBox
                key={val.ID}
                heading={val.heading}
                id={val.ID}
                clickAction={clickAction}
                textAction={textAction}
                clickValue={clickValue}
            />
        );
    });

    return (
        <div>
            {searchBoxes}
        </div>
    );
}

SearchSidebar.propTypes = {
    clickAction: PropTypes.func,
    textAction: PropTypes.func.isRequired,
    activeFilters: PropTypes.arrayOf(PropTypes.string.isRequired),
    searchBoxValues: PropTypes.objectOf(PropTypes.object.isRequired).isRequired,
};
