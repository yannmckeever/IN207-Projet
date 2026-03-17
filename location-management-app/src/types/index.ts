export interface Client {
    id: number;
    name: string;
    email: string;
    phone: string;
}

export interface Rental {
    id: number;
    clientId: number;
    agencyId: number;
    startDate: Date;
    endDate: Date;
    totalCost: number;
}

export interface RentalOption {
    id: number;
    rentalId: number;
    optionName: string;
    optionCost: number;
}

export interface Agency {
    id: number;
    name: string;
    address: string;
    phone: string;
}