import React, { useState } from 'react';
import { Form, Row, Col, Button } from 'react-bootstrap';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

const Filters = ({ onFilterChange }) => {
  const [startDate, setStartDate] = useState(new Date('2010-01-01'));
  const [endDate, setEndDate] = useState(new Date('2023-12-31'));
  const [selectedEventTypes, setSelectedEventTypes] = useState(['all']);
  const [selectedRegions, setSelectedRegions] = useState(['all']);

  const eventTypes = [
    { value: 'all', label: 'All Types' },
    { value: 'political', label: 'Political' },
    { value: 'economic', label: 'Economic' },
    { value: 'policy', label: 'Policy' }
  ];

  const regions = [
    { value: 'all', label: 'All Regions' },
    { value: 'Middle East', label: 'Middle East' },
    { value: 'North America', label: 'North America' },
    { value: 'Europe', label: 'Europe' },
    { value: 'Global', label: 'Global' }
  ];

  const handleEventTypeChange = (event) => {
    const value = event.target.value;
    const isChecked = event.target.checked;
    
    let newSelection;
    if (value === 'all') {
      newSelection = isChecked ? ['all'] : [];
    } else {
      if (selectedEventTypes.includes('all')) {
        newSelection = [value];
      } else {
        newSelection = isChecked
          ? [...selectedEventTypes, value]
          : selectedEventTypes.filter(type => type !== value);
      }
      
      if (newSelection.length === 0) {
        newSelection = ['all'];
      }
    }
    
    setSelectedEventTypes(newSelection);
  };

  const handleRegionChange = (event) => {
    const value = event.target.value;
    const isChecked = event.target.checked;
    
    let newSelection;
    if (value === 'all') {
      newSelection = isChecked ? ['all'] : [];
    } else {
      if (selectedRegions.includes('all')) {
        newSelection = [value];
      } else {
        newSelection = isChecked
          ? [...selectedRegions, value]
          : selectedRegions.filter(region => region !== value);
      }
      
      if (newSelection.length === 0) {
        newSelection = ['all'];
      }
    }
    
    setSelectedRegions(newSelection);
  };

  const handleApplyFilters = () => {
    onFilterChange({
      startDate: startDate.toISOString().split('T')[0],
      endDate: endDate.toISOString().split('T')[0],
      eventTypes: selectedEventTypes,
      regions: selectedRegions
    });
  };

  const handleResetFilters = () => {
    setStartDate(new Date('2010-01-01'));
    setEndDate(new Date('2023-12-31'));
    setSelectedEventTypes(['all']);
    setSelectedRegions(['all']);
    
    onFilterChange({
      startDate: '2010-01-01',
      endDate: '2023-12-31',
      eventTypes: ['all'],
      regions: ['all']
    });
  };

  return (
    <div className="filter-section">
      <h4 className="mb-4">Filter Analysis</h4>
      <Form>
        <Row>
          <Col md={3}>
            <Form.Group className="mb-3">
              <Form.Label>Start Date</Form.Label>
              <DatePicker
                selected={startDate}
                onChange={setStartDate}
                selectsStart
                startDate={startDate}
                endDate={endDate}
                maxDate={endDate}
                className="form-control"
                dateFormat="yyyy-MM-dd"
              />
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group className="mb-3">
              <Form.Label>End Date</Form.Label>
              <DatePicker
                selected={endDate}
                onChange={setEndDate}
                selectsEnd
                startDate={startDate}
                endDate={endDate}
                minDate={startDate}
                maxDate={new Date()}
                className="form-control"
                dateFormat="yyyy-MM-dd"
              />
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group className="mb-3">
              <Form.Label>Event Types</Form.Label>
              <div className="filter-checkboxes">
                {eventTypes.map(type => (
                  <Form.Check
                    key={type.value}
                    type="checkbox"
                    id={`event-type-${type.value}`}
                    label={type.label}
                    value={type.value}
                    checked={selectedEventTypes.includes(type.value)}
                    onChange={handleEventTypeChange}
                  />
                ))}
              </div>
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group className="mb-3">
              <Form.Label>Regions</Form.Label>
              <div className="filter-checkboxes">
                {regions.map(region => (
                  <Form.Check
                    key={region.value}
                    type="checkbox"
                    id={`region-${region.value}`}
                    label={region.label}
                    value={region.value}
                    checked={selectedRegions.includes(region.value)}
                    onChange={handleRegionChange}
                  />
                ))}
              </div>
            </Form.Group>
          </Col>
        </Row>
        <Row>
          <Col className="text-end">
            <Button variant="outline-secondary" onClick={handleResetFilters} className="me-2">
              Reset Filters
            </Button>
            <Button variant="primary" onClick={handleApplyFilters}>
              Apply Filters
            </Button>
          </Col>
        </Row>
      </Form>
    </div>
  );
};

export default Filters;