import React, { useState, useEffect } from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Table, Badge } from 'react-bootstrap';
import { fetchChangePoints, fetchEvents } from '../services/api';

const ChangePoints = ({ filters }) => {
  const [changePoints, setChangePoints] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, [filters]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [changePointsData, eventsData] = await Promise.all([
        fetchChangePoints(),
        fetchEvents()
      ]);

      // Filter events based on selected types and regions
      const filteredEvents = eventsData.filter(event => {
        if (filters.eventTypes[0] !== 'all' && !filters.eventTypes.includes(event.type)) {
          return false;
        }
        if (filters.regions[0] !== 'all' && !filters.regions.includes(event.region)) {
          return false;
        }
        return true;
      });

      // Filter change points that have associated filtered events
      const filteredChangePoints = changePointsData.filter(cp => {
        if (cp.associated_events) {
          return cp.associated_events.some(eventId => 
            filteredEvents.some(e => e.id === eventId)
          );
        }
        return true;
      });

      setChangePoints(filteredChangePoints);
      setEvents(filteredEvents);
    } catch (error) {
      console.error('Error loading change points:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatProbability = (prob) => {
    return (prob * 100).toFixed(1) + '%';
  };

  const getChangeBadge = (change) => {
    if (change > 0) {
      return <Badge bg="success">+{change.toFixed(1)}%</Badge>;
    } else {
      return <Badge bg="danger">{change.toFixed(1)}%</Badge>;
    }
  };

  const getProbabilityColor = (prob) => {
    if (prob > 0.9) return '#28a745';
    if (prob > 0.8) return '#ffc107';
    return '#dc3545';
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
      <h3 className="chart-title">Change Point Analysis Results</h3>
      
      {/* Scatter Plot */}
      <div className="mb-4">
        <ResponsiveContainer width="100%" height={300}>
          <ScatterChart
            margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              name="Date"
              tickFormatter={(date) => new Date(date).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}
            />
            <YAxis 
              dataKey="change_percentage" 
              name="Change %"
              label={{ value: 'Price Change %', angle: -90, position: 'insideLeft' }}
            />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const data = payload[0].payload;
                  return (
                    <div className="custom-tooltip">
                      <p className="date">{new Date(data.date).toLocaleDateString()}</p>
                      <p className="change">{getChangeBadge(data.change_percentage)}</p>
                      <p className="probability">Probability: {formatProbability(data.probability)}</p>
                      <p className="price">Before: ${data.before_mean.toFixed(2)}</p>
                      <p className="price">After: ${data.after_mean.toFixed(2)}</p>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Scatter
              data={changePoints}
              fill="#667eea"
              shape={(props) => {
                const { cx, cy, payload } = props;
                return (
                  <circle
                    cx={cx}
                    cy={cy}
                    r={payload.probability * 10}
                    fill={getProbabilityColor(payload.probability)}
                    stroke="#fff"
                    strokeWidth={2}
                  />
                );
              }}
            />
          </ScatterChart>
        </ResponsiveContainer>
      </div>

      {/* Table View */}
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Date</th>
            <th>Probability</th>
            <th>Before Event</th>
            <th>After Event</th>
            <th>Change</th>
            <th>Associated Events</th>
          </tr>
        </thead>
        <tbody>
          {changePoints.map((cp, index) => {
            const associatedEvents = events.filter(e => 
              cp.associated_events?.includes(e.id)
            );
            
            return (
              <tr key={index}>
                <td>{new Date(cp.date).toLocaleDateString()}</td>
                <td>
                  <Badge bg={cp.probability > 0.9 ? "success" : cp.probability > 0.8 ? "warning" : "danger"}>
                    {formatProbability(cp.probability)}
                  </Badge>
                </td>
                <td>${cp.before_mean.toFixed(2)}</td>
                <td>${cp.after_mean.toFixed(2)}</td>
                <td>{getChangeBadge(cp.change_percentage)}</td>
                <td>
                  {associatedEvents.map(event => (
                    <div key={event.id} className="mb-1">
                      <small>{event.name}</small>
                    </div>
                  ))}
                </td>
              </tr>
            );
          })}
        </tbody>
      </Table>
    </div>
  );
};

export default ChangePoints;