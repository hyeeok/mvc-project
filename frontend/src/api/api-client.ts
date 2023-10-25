import axios from 'axios';

const apiEndpointLocal = 'http://localhost:8000';
const apiEndpoint = process.env.NEXT_PUBLIC_BASE_API;
export const baseUrl = apiEndpoint;

export const apiClient = () =>
  axios.create({
    baseURL: apiEndpointLocal,
    headers: {
      'Content-Type': 'application/json',
    },
  });
