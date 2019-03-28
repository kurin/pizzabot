import React, { PropTypes } from 'react';

export default function SearchBox({ heading, id, clickAction, textAction,
    clickValue }) {
    const submitButton = clickAction ?
        (<span className="input-group-btn">
            <input
                key={clickValue}
                className="btn btn-default"
                type="submit"
                value={clickValue}
            />
        </span>) : null;
    return (
        <div className="panel panel-primary">
            <div className="panel-heading">
                {heading}
            </div>
            <form
                id={id}
                onSubmit={clickAction}
            >
                <div className="input-group">
                    {submitButton}
                    <input
                        className="form-control"
                        type="search"
                        id={id}
                        onChange={(e) => textAction(e)}
                    />
                </div>
            </form>
        </div>
    );
}

SearchBox.propTypes = {
    heading: PropTypes.string.isRequired,
    id: PropTypes.string.isRequired,
    textAction: PropTypes.func.isRequired,
    clickAction: PropTypes.func,
    clickValue: PropTypes.string,
};
