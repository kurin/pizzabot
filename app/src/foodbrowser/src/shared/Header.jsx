import React from 'react';
import { Link } from 'react-router';

export default function Header() {
    return (
        <nav className="navbar navbar-inverse navbar-static-top">
            <a className="navbar-brand">foodbrowser</a>
            <div className="collapse navbar-collapse">
                <ul className="nav navbar-nav">
                    <li>
                        <Link to="#/search">
                            Search
                        </Link>
                    </li>
                    <li>
                        <Link to="#/chart">
                            Chart
                        </Link>
                    </li>
                </ul>
            </div>
        </nav>
    );
}
