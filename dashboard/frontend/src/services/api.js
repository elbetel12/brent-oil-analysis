import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchPrices = async () => {
  try {
    const response = await api.get('/prices');
    return response.data;
  } catch (error) {
    console.error('Error fetching prices:', error);
    throw error;
  }
};

export const fetchPricesByDate = async (startDate, endDate) => {
  try {
    const response = await api.get(`/prices/${startDate}/${endDate}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching prices by date:', error);
    throw error;
  }
};

export const fetchChangePoints = async () => {
  try {
    const response = await api.get('/change_points');
    return response.data;
  } catch (error) {
    console.error('Error fetching change points:', error);
    throw error;
  }
};

export const fetchEvents = async () => {
  try {
    const response = await api.get('/events');
    return response.data;
  } catch (error) {
    console.error('Error fetching events:', error);
    throw error;
  }
};

export const fetchEventCorrelation = async (eventId) => {
  try {
    const response = await api.get(`/event_correlation/${eventId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching event correlation:', error);
    throw error;
  }
};

export const fetchVolatility = async () => {
  try {
    const response = await api.get('/volatility');
    return response.data;
  } catch (error) {
    console.error('Error fetching volatility:', error);
    throw error;
  }
};

export const fetchSummaryStats = async () => {
  try {
    const response = await api.get('/summary_stats');
    return response.data;
  } catch (error) {
    console.error('Error fetching summary stats:', error);
    throw error;
  }
};

export const calculatePriceImpact = async (eventDate, windowDays = 30) => {
  try {
    const response = await api.post('/price_impact', {
      event_date: eventDate,
      window_days: windowDays
    });
    return response.data;
  } catch (error) {
    console.error('Error calculating price impact:', error);
    throw error;
  }
};