import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import LocationPage from './pages/Location';

const App = () => {
    return (
        <Router>
            <Switch>
                <Route path="/" exact component={LocationPage} />
                {/* Add more routes here as needed */}
            </Switch>
        </Router>
    );
};

export default App;