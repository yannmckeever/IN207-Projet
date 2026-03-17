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
    vehicleType: string;
}

export interface RentalOption {
    id: number;
    rentalId: number;
    optionName: string;
    optionValue: string;
}

export interface Agency {
    id: number;
    name: string;
    address: string;
    phone: string;
}