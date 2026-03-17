import axios from 'axios';
import { Client } from '../pages/Location/types';

const API_URL = 'http://localhost:3000/api/clients'; // Replace with your actual API URL

export const addClient = async (clientData: Client): Promise<Client> => {
    const response = await axios.post(API_URL, clientData);
    return response.data;
};

export const getClients = async (): Promise<Client[]> => {
    const response = await axios.get(API_URL);
    return response.data;
};

export const updateClient = async (clientId: string, clientData: Client): Promise<Client> => {
    const response = await axios.put(`${API_URL}/${clientId}`, clientData);
    return response.data;
};

export const deleteClient = async (clientId: string): Promise<void> => {
    await axios.delete(`${API_URL}/${clientId}`);
};