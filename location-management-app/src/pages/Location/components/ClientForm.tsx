import React, { useState } from 'react';

const ClientForm = () => {
    const [clientName, setClientName] = useState('');
    const [clientEmail, setClientEmail] = useState('');
    const [clientPhone, setClientPhone] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Logic to add client to the database goes here
        console.log('Client added:', { clientName, clientEmail, clientPhone });
        // Reset form fields
        setClientName('');
        setClientEmail('');
        setClientPhone('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="clientName">Name:</label>
                <input
                    type="text"
                    id="clientName"
                    value={clientName}
                    onChange={(e) => setClientName(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="clientEmail">Email:</label>
                <input
                    type="email"
                    id="clientEmail"
                    value={clientEmail}
                    onChange={(e) => setClientEmail(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="clientPhone">Phone:</label>
                <input
                    type="tel"
                    id="clientPhone"
                    value={clientPhone}
                    onChange={(e) => setClientPhone(e.target.value)}
                    required
                />
            </div>
            <button type="submit">Add Client</button>
        </form>
    );
};

export default ClientForm;