/**
 * App.jsx — Mausam root component (Step 25 update).
 *
 * State shape:
 *   formData = { name: string, location: string, selectedInterests: string[] }
 *   canonicalLocation = LocationResult | null
 *
 * localStorage key: "mausam_user_profile"
 * Stored shape (v2):
 *   {
 *     name: string,
 *     location: string | { city, state, country, latitude, longitude, timezone, displayName },
 *     selectedInterests: string[],
 *     canonicalLocation: LocationResult | null
 *   }
 *
 * Backward compatibility:
 *   Old profiles stored { name, location: "Jaipur", selectedInterests }.
 *   These are loaded without canonicalLocation; the dashboard falls back to the
 *   raw location string for weather queries (which still works).
 */

import React, { useState, useEffect } from 'react';
import PersonalizationScreen from './components/onboarding/PersonalizationScreen';
import Dashboard from './components/dashboard/Dashboard';
import './styles/App.css';

const STORAGE_KEY = 'mausam_user_profile';

// ─── Storage helpers ────────────────────────────────────────────────────────

function loadProfile() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    // Validate minimal shape to avoid crashes on corrupted data
    if (typeof parsed !== 'object' || parsed === null) return null;
    return parsed;
  } catch {
    return null;
  }
}

function saveProfile(formData, canonicalLocation) {
  try {
    const payload = {
      name: formData.name,
      location: formData.location,
      selectedInterests: formData.selectedInterests,
      canonicalLocation: canonicalLocation,
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  } catch {
    // Ignore storage quota errors — state still works in-memory
  }
}

// ─── Default form state ──────────────────────────────────────────────────────

function defaultFormData() {
  return { name: '', location: '', selectedInterests: [] };
}

// ─── App ─────────────────────────────────────────────────────────────────────

export default function App() {
  // ── Initialize from localStorage (or fresh defaults) ────────────────────
  const [formData, setFormData] = useState(() => {
    const saved = loadProfile();
    if (!saved) return defaultFormData();
    return {
      name: saved.name || '',
      location: typeof saved.location === 'string'
        ? saved.location
        : (saved.location?.displayName || saved.location?.city || ''),
      selectedInterests: Array.isArray(saved.selectedInterests)
        ? saved.selectedInterests
        : [],
    };
  });

  // canonicalLocation: null means no canonical object yet (legacy user)
  const [canonicalLocation, setCanonicalLocation] = useState(() => {
    const saved = loadProfile();
    if (!saved) return null;
    // Validate that it's a proper canonical object before using it
    if (
      saved.canonicalLocation &&
      typeof saved.canonicalLocation === 'object' &&
      saved.canonicalLocation.city &&
      typeof saved.canonicalLocation.latitude === 'number'
    ) {
      return saved.canonicalLocation;
    }
    return null;
  });

  const [isSubmitted, setIsSubmitted] = useState(() => {
    const saved = loadProfile();
    if (!saved) return false;
    // Auto-restore dashboard if profile has name + some location
    return (
      !!saved.name &&
      !!(saved.location || saved.canonicalLocation?.city)
    );
  });

  // ── Persist to localStorage whenever state changes ───────────────────────
  useEffect(() => {
    if (isSubmitted) {
      saveProfile(formData, canonicalLocation);
    }
  }, [formData, canonicalLocation, isSubmitted]);

  // ── Handlers ─────────────────────────────────────────────────────────────

  const handleFieldChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));

    // If user manually edits the location text field after a canonical selection,
    // clear the canonical object so a new selection is required for full fidelity.
    if (field === 'location') {
      setCanonicalLocation((prev) => {
        if (!prev) return null;
        // Only clear if the text diverges from the canonical displayName
        const canonical = prev.displayName || prev.city || '';
        return value === canonical ? prev : null;
      });
    }
  };

  const handleToggleInterest = (interestId) => {
    setFormData((prev) => {
      const exists = prev.selectedInterests.includes(interestId);
      return {
        ...prev,
        selectedInterests: exists
          ? prev.selectedInterests.filter((id) => id !== interestId)
          : [...prev.selectedInterests, interestId],
      };
    });
  };

  const handleLocationSelect = (locationResult) => {
    // Store canonical object
    setCanonicalLocation(locationResult);
    // Update location text to displayName for form display
    setFormData((prev) => ({
      ...prev,
      location: locationResult.displayName || locationResult.city || '',
    }));
  };

  const handleSubmit = () => {
    setIsSubmitted(true);
    saveProfile(formData, canonicalLocation);
  };

  const handleEditPreferences = () => {
    setIsSubmitted(false);
  };

  // ── Determine weather query location ─────────────────────────────────────
  // Dashboard receives the full canonical object if available,
  // otherwise falls back to the raw location string (backward compat).
  const dashboardLocation = canonicalLocation
    ? canonicalLocation.city
    : formData.location;

  return (
    <div className="app-viewport">
      <main className="app-shell">
        {!isSubmitted ? (
          <PersonalizationScreen
            formData={formData}
            canonicalLocation={canonicalLocation}
            onChange={handleFieldChange}
            onLocationSelect={handleLocationSelect}
            onToggleInterest={handleToggleInterest}
            onSubmit={handleSubmit}
          />
        ) : (
          <Dashboard
            userProfile={{
              ...formData,
              // Pass city name for weather query + display
              location: dashboardLocation,
              // Pass full canonical object for richer display (displayName, timezone, etc.)
              canonicalLocation: canonicalLocation,
            }}
            onEditPreferences={handleEditPreferences}
          />
        )}
      </main>
    </div>
  );
}
