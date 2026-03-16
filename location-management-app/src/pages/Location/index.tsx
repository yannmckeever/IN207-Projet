import React from 'react';
import ClientForm from './components/ClientForm';
import RentalForm from './components/RentalForm';
import RentalOptionsForm from './components/RentalOptionsForm';
import AgencyForm from './components/AgencyForm';

const LocationPage: React.FC = () => {
    return (
        <div>
            <h1>Location Management</h1>
            <h2>Add Client</h2>
            <ClientForm />
            <h2>Add Rental</h2>
            <RentalForm />
            <h2>Add Rental Options</h2>
            <RentalOptionsForm />
            <h2>Add Agency</h2>
            <AgencyForm />
        </div>
    );
};

export default LocationPage;