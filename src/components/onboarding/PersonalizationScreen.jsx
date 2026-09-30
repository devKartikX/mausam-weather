import React from 'react';
import { CloudSun, User, Sparkles, ArrowRight } from 'lucide-react';
import { INTERESTS } from '../../data/interests';
import InterestChip from './InterestChip';
import LocationAutocomplete from './LocationAutocomplete';
import '../../styles/Personalization.css';

/**
 * PersonalizationScreen — Onboarding form (Step 25 update).
 *
 * Props:
 *   formData           { name, location, selectedInterests }
 *   canonicalLocation  LocationResult | null  (the resolved canonical object)
 *   onChange           (field, value) => void  (for name / raw location text)
 *   onLocationSelect   (LocationResult) => void  (called on autocomplete pick)
 *   onToggleInterest   (interestId) => void
 *   onSubmit           () => void
 */
export default function PersonalizationScreen({
  formData,
  canonicalLocation,
  onChange,
  onLocationSelect,
  onToggleInterest,
  onSubmit,
}) {
  const { name, location, selectedInterests } = formData;

  // Form is valid when:
  //   1. name is non-empty
  //   2. a canonical location has been selected (or legacy string location present)
  //   3. at least one interest selected
  const hasLocation = canonicalLocation !== null
    ? true
    : (typeof location === 'string' && location.trim().length > 0);

  const isFormValid =
    name.trim().length > 0 &&
    hasLocation &&
    selectedInterests.length > 0;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isFormValid) {
      onSubmit();
    }
  };

  // Display text for the autocomplete input:
  // When user is typing, formData.location reflects the current text.
  // When canonicalLocation exists and matches, or initial load, use displayName.
  const locationDisplayValue =
    typeof location === 'string'
      ? location
      : (canonicalLocation?.displayName || canonicalLocation?.city || '');

  return (
    <div className="personalization-container">
      {/* 1. Header / Branding */}
      <header className="onboarding-brand">
        <div className="brand-logo-badge">
          <CloudSun size={24} className="brand-logo-icon" />
          <span className="brand-name">Mausam</span>
        </div>
        <p className="brand-tagline">Your weather, your way.</p>
      </header>

      {/* 2. Welcome Section */}
      <section className="onboarding-welcome">
        <h1 className="welcome-heading">Personalized weather for your daily life.</h1>
        <p className="welcome-desc">
          Mausam delivers hyper-local forecasts and official safety alerts. Tell us your location
          and daily lifestyle interests so your homepage highlights the insights that matter most to you.
        </p>
      </section>

      {/* Form Area */}
      <form onSubmit={handleSubmit} className="onboarding-form">
        {/* 3. Name Input */}
        <div className="form-group">
          <label htmlFor="user-name-input" className="form-label">
            <User size={16} className="label-icon" />
            <span>What should we call you?</span>
            <span className="required-indicator">*</span>
          </label>
          <div className="input-wrapper">
            <input
              id="user-name-input"
              type="text"
              name="name"
              value={name}
              onChange={(e) => onChange('name', e.target.value)}
              placeholder="Enter your name"
              className="text-input"
              autoComplete="name"
              required
            />
          </div>
        </div>

        {/* 4. Location Autocomplete */}
        <div className="form-group">
          <label htmlFor="user-location-input" className="form-label">
            <Sparkles size={16} className="label-icon" />
            <span>Where are you?</span>
            <span className="required-indicator">*</span>
          </label>
          <LocationAutocomplete
            inputId="user-location-input"
            value={locationDisplayValue}
            onInputChange={(text) => onChange('location', text)}
            onSelect={onLocationSelect}
            placeholder="Search your city…"
          />
        </div>

        {/* 5. Interest Selection */}
        <div className="form-group">
          <div className="interests-header">
            <label className="form-label">
              <Sparkles size={16} className="label-icon" />
              <span>What weather information matters to you?</span>
              <span className="required-indicator">*</span>
            </label>
            <span className="interests-counter">
              {selectedInterests.length > 0
                ? `${selectedInterests.length} selected`
                : 'Choose at least 1'}
            </span>
          </div>
          <p className="interests-help-text">
            Select one or more categories that match your daily routine.
          </p>

          <div className="interests-grid">
            {INTERESTS.map((interest) => (
              <InterestChip
                key={interest.id}
                interest={interest}
                isSelected={selectedInterests.includes(interest.id)}
                onToggle={onToggleInterest}
              />
            ))}
          </div>
        </div>

        {/* 6. Continue Button */}
        <div className="form-action">
          <button
            type="submit"
            disabled={!isFormValid}
            className={`submit-btn ${isFormValid ? 'submit-btn--active' : 'submit-btn--disabled'}`}
            id="create-dashboard-btn"
          >
            <span>Create My Dashboard</span>
            <ArrowRight size={18} />
          </button>

          {!isFormValid && (
            <p className="form-validation-tip">
              Please enter your name, select a city from the suggestions, and pick at least one interest to continue.
            </p>
          )}
        </div>
      </form>
    </div>
  );
}
