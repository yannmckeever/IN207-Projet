import React, { useState } from 'react';

const RentalForm = () => {
    const [rentalDetails, setRentalDetails] = useState({
        propertyName: '',
        rentalPrice: '',
        rentalDuration: '',
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setRentalDetails({
            ...rentalDetails,
            [name]: value,
        });
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        // Logic to add rental to the database
        console.log('Rental added:', rentalDetails);
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>
                    Property Name:
                    <input
                        type="text"
                        name="propertyName"
                        value={rentalDetails.propertyName}
                        onChange={handleChange}
                        required
                    />
                </label>
            </div>
            <div>
                <label>
                    Rental Price:
                    <input
                        type="number"
                        name="rentalPrice"
                        value={rentalDetails.rentalPrice}
                        onChange={handleChange}
                        required
                    />
                </label>
            </div>
            <div>
                <label>
                    Rental Duration:
                    <input
                        type="text"
                        name="rentalDuration"
                        value={rentalDetails.rentalDuration}
                        onChange={handleChange}
                        required
                    />
                </label>
            </div>
            <button type="submit">Add Rental</button>
        </form>
    );
};

export default RentalForm;