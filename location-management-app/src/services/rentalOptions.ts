import { RentalOption } from '../pages/Location/types';

const rentalOptions: RentalOption[] = [];

export const addRentalOption = (option: RentalOption): void => {
    rentalOptions.push(option);
};

export const getRentalOptions = (): RentalOption[] => {
    return rentalOptions;
};