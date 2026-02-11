import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { fetchPricesByDate, fetchEvents } from '../services/api';

const PriceChart = ({ filters }) => {
  const [priceData, setPriceData] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, [filters]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [prices, eventData] = await Promise.all([
        fetchPricesByDate(filters.startDate, filters.endDate),
        fetchEvents()
      ]);
      
      // Filter events based on selected types and regions
      const filteredEvents = eventData.filter(event => {
        if (filters.eventTypes[0] !== 'all' && !filters.eventTypes.includes(event.type)) {
          return false;
        }
        if (filters.regions[0] !== 'all' && !filters.regions.includes(event.region)) {
          return false;
        }
        return true;
      });

      setPriceData(prices);
      setEvents(filteredEvents);
    } catch (error) {
      console.error('Error loading price data:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const event = events.find(e => e.date === label);
      return (
        <div className="custom-tooltip">
          <p className="date">{formatDate(label)}</p>
          <p className="price">Price: ${payload[0].value.toFixed(2)}</p>
          {event && (
            <div className="event-info">
              <p className="event-name">{event.name}</p>
              <p className="event-type">{event.type}</p>
            </div>
          )}
        </div>
      );
    }
    return null;
  };

  if (loading) {
    return (
      <div className="chart-container">
        <div className="text-center py-5">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <h3 className="chart-title">Brent Oil Price Trend with Event Markers</h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart
          data={priceData}
          margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey="date"
            tickFormatter={formatDate}
            interval="preserveStartEnd"
            minTickGap={50}
          />
          <YAxis
            label={{ value: 'Price (USD)', angle: -90, position: 'insideLeft' }}
            domain={['auto', 'auto']}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Line
            type="monotone"
            dataKey="price"
            stroke="#667eea"
            strokeWidth={2}
            dot={false}
            name="Brent Oil Price"
            activeDot={{ r: 6 }}
          />
          {events.map(event => {
            const eventDataPoint = priceData.find(p => p.date === event.date);
            if (eventDataPoint) {
              return (
                <g key={event.id}>
                  <circle
                    cx={(priceData.findIndex(p => p.date === event.date) / priceData.length * 100) + '%'}
                    cy={eventDataPoint.price}
                    r={6}
                    fill={event.type === 'political' ? '#dc3545' : event.type === 'economic' ? '#28a745' : '#007bff'}
                    stroke="#fff"
                    strokeWidth={2}
                  />
                </g>
              );
            }
            return null;
          })}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PriceChart;