import { Agency } from '../pages/Location/types';

const agencies: Agency[] = [];

export const addAgency = (agency: Agency): void => {
    agencies.push(agency);
};

export const getAgencies = (): Agency[] => {
    return agencies;
};