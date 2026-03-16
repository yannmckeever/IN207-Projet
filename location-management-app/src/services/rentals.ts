import { Rental } from '../pages/Location/types';

const rentals: Rental[] = [];

export const addRental = (rental: Rental): void => {
    rentals.push(rental);
};

export const getRentals = (): Rental[] => {
    return rentals;
};

export const updateRental = (id: number, updatedRental: Rental): void => {
    const index = rentals.findIndex(rental => rental.id === id);
    if (index !== -1) {
        rentals[index] = { ...rentals[index], ...updatedRental };
    }
};

export const deleteRental = (id: number): void => {
    const index = rentals.findIndex(rental => rental.id === id);
    if (index !== -1) {
        rentals.splice(index, 1);
    }
};