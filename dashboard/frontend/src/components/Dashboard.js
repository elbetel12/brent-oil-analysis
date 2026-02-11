import React, { useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import Filters from './Filters';
import PriceChart from './PriceChart';
import EventCorrelation from './EventCorrelation';
import ChangePoints from './ChangePoints';
import './Dashboard.css';

const Dashboard = () => {
  const [filters, setFilters] = useState({
    startDate: '2010-01-01',
    endDate: '2023-12-31',
    eventTypes: ['all'],
    regions: ['all']
  });

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  return (
    <Container fluid className="dashboard">
      <Row>
        <Col>
          <Filters onFilterChange={handleFilterChange} />
        </Col>
      </Row>
      <Row>
        <Col lg={12}>
          <PriceChart filters={filters} />
        </Col>
      </Row>
      <Row>
        <Col lg={12}>
          <EventCorrelation filters={filters} />
        </Col>
      </Row>
      <Row>
        <Col lg={12}>
          <ChangePoints filters={filters} />
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;
