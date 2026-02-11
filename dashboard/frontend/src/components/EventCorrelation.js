import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card, ListGroup, Badge, Row, Col } from 'react-bootstrap';
import { fetchEvents, fetchEventCorrelation } from '../services/api';

const EventCorrelation = ({ filters }) => {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [correlationData, setCorrelationData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadEvents();
  }, [filters]);

  const loadEvents = async () => {
    try {
      const eventData = await fetchEvents();
      
      const filteredEvents = eventData.filter(event => {
        if (filters.eventTypes[0] !== 'all' && !filters.eventTypes.includes(event.type)) {
          return false;
        }
        if (filters.regions[0] !== 'all' && !filters.regions.includes(event.region)) {
          return false;
        }
        return true;
      });

      setEvents(filteredEvents);
      if (filteredEvents.length > 0 && !selectedEvent) {
        handleEventSelect(filteredEvents[0]);
      }
    } catch (error) {
      console.error('Error loading events:', error);
    }
  };

  const handleEventSelect = async (event) => {
    setSelectedEvent(event);
    setLoading(true);
    try {
      const correlation = await fetchEventCorrelation(event.id);
      setCorrelationData(correlation);
    } catch (error) {
      console.error('Error loading event correlation:', error);
    } finally {
      setLoading(false);
    }
  };

  const getEventTypeBadge = (type) => {
    const colors = {
      political: 'danger',
      economic: 'success',
      policy: 'primary'
    };
    return <Badge bg={colors[type]}>{type}</Badge>;
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
      <h3 className="chart-title">Event Impact Analysis</h3>
      <Row>
        <Col md={4}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Geopolitical Events</h5>
            </Card.Header>
            <ListGroup variant="flush" style={{ maxHeight: '500px', overflowY: 'auto' }}>
              {events.map(event => (
                <ListGroup.Item
                  key={event.id}
                  action
                  active={selectedEvent?.id === event.id}
                  onClick={() => handleEventSelect(event)}
                  className="event-card"
                >
                  <div className="d-flex justify-content-between align-items-start">
                    <div>
                      <h6 className="mb-1">{event.name}</h6>
                      <p className="text-muted mb-1">{new Date(event.date).toLocaleDateString()}</p>
                      <div className="mb-1">{getEventTypeBadge(event.type)}</div>
                      <small className="text-muted">{event.region}</small>
                    </div>
                  </div>
                </ListGroup.Item>
              ))}
            </ListGroup>
          </Card>
        </Col>
        <Col md={8}>
          {selectedEvent && correlationData && (
            <>
              <Card className="mb-4">
                <Card.Body>
                  <Card.Title>{selectedEvent.name}</Card.Title>
                  <Card.Subtitle className="mb-2 text-muted">
                    {new Date(selectedEvent.date).toLocaleDateString()} | {selectedEvent.region}
                  </Card.Subtitle>
                  <Card.Text>{selectedEvent.description}</Card.Text>
                </Card.Body>
              </Card>

              {correlationData.change_point && (
                <Card className="mb-4">
                  <Card.Header>
                    <h5 className="mb-0">Change Point Analysis</h5>
                  </Card.Header>
                  <Card.Body>
                    <Row>
                      <Col md={6}>
                        <div className="metric-card">
                          <div className="metric-label">Before Event</div>
                          <div className="metric-value">
                            ${correlationData.change_point.before_mean.toFixed(2)}
                          </div>
                        </div>
                      </Col>
                      <Col md={6}>
                        <div className="metric-card">
                          <div className="metric-label">After Event</div>
                          <div className="metric-value">
                            ${correlationData.change_point.after_mean.toFixed(2)}
                          </div>
                        </div>
                      </Col>
                    </Row>
                    <div className="text-center mt-3">
                      <h4 className={correlationData.change_point.change_percentage > 0 ? 'text-success' : 'text-danger'}>
                        {correlationData.change_point.change_percentage > 0 ? '+' : ''}
                        {correlationData.change_point.change_percentage.toFixed(1)}%
                      </h4>
                      <p className="text-muted">Price Change</p>
                    </div>
                  </Card.Body>
                </Card>
              )}

              {correlationData.price_analysis && (
                <Card>
                  <Card.Header>
                    <h5 className="mb-0">Price Impact Timeline</h5>
                  </Card.Header>
                  <Card.Body>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart
                        data={[
                          {
                            period: 'Pre-Event',
                            price: correlationData.price_analysis.pre_event_mean
                          },
                          {
                            period: 'Post-Event',
                            price: correlationData.price_analysis.post_event_mean
                          }
                        ]}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="period" />
                        <YAxis label={{ value: 'Price (USD)', angle: -90, position: 'insideLeft' }} />
                        <Tooltip formatter={(value) => [`$${value.toFixed(2)}`, 'Average Price']} />
                        <Bar dataKey="price" fill="#667eea" name="Average Price" />
                      </BarChart>
                    </ResponsiveContainer>
                  </Card.Body>
                </Card>
              )}
            </>
          )}
        </Col>
      </Row>
    </div>
  );
};

export default EventCorrelation;