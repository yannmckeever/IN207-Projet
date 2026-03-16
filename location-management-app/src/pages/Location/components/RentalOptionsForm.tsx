import React, { useState } from 'react';

const RentalOptionsForm = () => {
    const [optionName, setOptionName] = useState('');
    const [optionPrice, setOptionPrice] = useState('');
    const [optionDescription, setOptionDescription] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // Logic to handle form submission, e.g., sending data to the server
        console.log('Rental Option Submitted:', { optionName, optionPrice, optionDescription });
        // Reset form fields
        setOptionName('');
        setOptionPrice('');
        setOptionDescription('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="optionName">Option Name:</label>
                <input
                    type="text"
                    id="optionName"
                    value={optionName}
                    onChange={(e) => setOptionName(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="optionPrice">Option Price:</label>
                <input
                    type="number"
                    id="optionPrice"
                    value={optionPrice}
                    onChange={(e) => setOptionPrice(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="optionDescription">Option Description:</label>
                <textarea
                    id="optionDescription"
                    value={optionDescription}
                    onChange={(e) => setOptionDescription(e.target.value)}
                    required
                />
            </div>
            <button type="submit">Add Rental Option</button>
        </form>
    );
};

export default RentalOptionsForm;