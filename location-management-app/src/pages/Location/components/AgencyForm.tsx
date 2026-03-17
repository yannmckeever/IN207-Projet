import React, { useState } from 'react';

const AgencyForm = () => {
    const [agencyName, setAgencyName] = useState('');
    const [agencyAddress, setAgencyAddress] = useState('');
    const [agencyPhone, setAgencyPhone] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Logic to add agency to the database goes here
        console.log('Agency added:', { agencyName, agencyAddress, agencyPhone });
        // Reset form fields
        setAgencyName('');
        setAgencyAddress('');
        setAgencyPhone('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="agencyName">Agency Name:</label>
                <input
                    type="text"
                    id="agencyName"
                    value={agencyName}
                    onChange={(e) => setAgencyName(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="agencyAddress">Agency Address:</label>
                <input
                    type="text"
                    id="agencyAddress"
                    value={agencyAddress}
                    onChange={(e) => setAgencyAddress(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="agencyPhone">Agency Phone:</label>
                <input
                    type="tel"
                    id="agencyPhone"
                    value={agencyPhone}
                    onChange={(e) => setAgencyPhone(e.target.value)}
                    required
                />
            </div>
            <button type="submit">Add Agency</button>
        </form>
    );
};

export default AgencyForm;