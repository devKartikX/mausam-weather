import React, {
  useState,
  useEffect,
  useRef,
  useCallback,
  useId,
} from 'react';
import { MapPin, Loader2, SearchX, WifiOff } from 'lucide-react';
import { searchLocations } from '../../services/locationClient';

/**
 * LocationAutocomplete — Debounced location search with dropdown (Step 25).
 *
 * Props:
 *   value          {string}   Current input display text
 *   onInputChange  {fn}       Called with raw typed text (for controlled input)
 *   onSelect       {fn}       Called with canonical LocationResult object on selection
 *   inputId        {string}   id for the <input> element (for <label> association)
 *   placeholder    {string}   Input placeholder text
 *   className      {string}   Extra CSS class for the root wrapper
 */
export default function LocationAutocomplete({
  value = '',
  onInputChange,
  onSelect,
  inputId = 'location-autocomplete-input',
  placeholder = 'Enter your city',
  className = '',
}) {
  const [inputText, setInputText] = useState(value);
  const [suggestions, setSuggestions] = useState([]);
  const [status, setStatus] = useState('idle'); // 'idle' | 'loading' | 'empty' | 'error' | 'done'
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);

  const debounceRef = useRef(null);
  const abortRef = useRef(null);
  const containerRef = useRef(null);
  const listboxId = useId();

  // Sync controlled value → internal text when parent changes it (e.g. selecting from dropdown)
  useEffect(() => {
    setInputText(value);
  }, [value]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleOutsideClick = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setIsOpen(false);
        setActiveIndex(-1);
      }
    };
    document.addEventListener('mousedown', handleOutsideClick);
    return () => document.removeEventListener('mousedown', handleOutsideClick);
  }, []);

  const runSearch = useCallback(async (query) => {
    // Cancel any in-flight request
    if (abortRef.current) {
      abortRef.current.abort();
    }
    const controller = new AbortController();
    abortRef.current = controller;

    setStatus('loading');
    setSuggestions([]);
    setActiveIndex(-1);

    try {
      const results = await searchLocations(query, controller.signal);
      // Guard against results arriving after a newer search was triggered
      if (controller.signal.aborted) return;

      setSuggestions(results);
      setStatus(results.length > 0 ? 'done' : 'empty');
      setIsOpen(true);
    } catch (err) {
      if (err && err.name === 'AbortError') return;
      setStatus('error');
      setIsOpen(true);
    }
  }, []);

  const handleInputChange = (e) => {
    const text = e.target.value;
    setInputText(text);
    if (onInputChange) onInputChange(text);

    // Clear debounce timer
    if (debounceRef.current) clearTimeout(debounceRef.current);

    if (!text.trim()) {
      // Empty input — close dropdown, cancel any in-flight request
      if (abortRef.current) abortRef.current.abort();
      setSuggestions([]);
      setStatus('idle');
      setIsOpen(false);
      return;
    }

    // Debounce ~300ms before firing request
    debounceRef.current = setTimeout(() => {
      runSearch(text.trim());
    }, 300);
  };

  const handleSelect = useCallback(
    (result) => {
      // Cancel pending debounce + in-flight requests
      if (debounceRef.current) clearTimeout(debounceRef.current);
      if (abortRef.current) abortRef.current.abort();

      const displayText = result.displayName || result.city || '';
      setInputText(displayText);
      setSuggestions([]);
      setStatus('idle');
      setIsOpen(false);
      setActiveIndex(-1);

      if (onInputChange) onInputChange(displayText);
      if (onSelect) onSelect(result);
    },
    [onInputChange, onSelect]
  );

  const handleKeyDown = (e) => {
    if (!isOpen) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveIndex((prev) => Math.min(prev + 1, suggestions.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveIndex((prev) => Math.max(prev - 1, -1));
        break;
      case 'Enter':
        if (activeIndex >= 0 && suggestions[activeIndex]) {
          e.preventDefault();
          handleSelect(suggestions[activeIndex]);
        }
        break;
      case 'Escape':
        setIsOpen(false);
        setActiveIndex(-1);
        break;
      default:
        break;
    }
  };

  const handleInputFocus = () => {
    // Re-open if we already have results
    if (suggestions.length > 0 || status === 'empty' || status === 'error') {
      setIsOpen(true);
    }
  };

  const isExpanded = isOpen && (status !== 'idle');

  return (
    <div
      ref={containerRef}
      className={`location-autocomplete ${className}`}
      role="combobox"
      aria-expanded={isExpanded}
      aria-haspopup="listbox"
      aria-owns={listboxId}
    >
      {/* Input */}
      <div className="location-input-wrapper">
        <MapPin
          size={16}
          className="location-input-icon"
          aria-hidden="true"
        />
        <input
          id={inputId}
          type="text"
          className="text-input location-input-field"
          value={inputText}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onFocus={handleInputFocus}
          placeholder={placeholder}
          autoComplete="off"
          aria-label="Location search"
          aria-autocomplete="list"
          aria-controls={listboxId}
          aria-activedescendant={
            activeIndex >= 0 ? `${listboxId}-option-${activeIndex}` : undefined
          }
        />
        {status === 'loading' && (
          <Loader2
            size={16}
            className="location-input-spinner"
            aria-label="Searching locations"
          />
        )}
      </div>

      {/* Dropdown */}
      {isExpanded && (
        <div
          id={listboxId}
          role="listbox"
          aria-label="Location suggestions"
          className="location-dropdown"
        >
          {/* Loading */}
          {status === 'loading' && (
            <div className="location-dropdown-state" role="status">
              <Loader2 size={15} className="dropdown-state-spinner" />
              <span>Searching locations…</span>
            </div>
          )}

          {/* No results */}
          {status === 'empty' && (
            <div className="location-dropdown-state location-dropdown-state--empty">
              <SearchX size={15} aria-hidden="true" />
              <span>No matching cities found</span>
            </div>
          )}

          {/* Network / backend error */}
          {status === 'error' && (
            <div className="location-dropdown-state location-dropdown-state--error">
              <WifiOff size={15} aria-hidden="true" />
              <span>Couldn't search locations. Try again.</span>
            </div>
          )}

          {/* Suggestions */}
          {status === 'done' && suggestions.length > 0 && (
            <ul className="location-suggestions-list" role="group">
              {suggestions.map((result, idx) => {
                const subline = [result.state, result.country]
                  .filter(Boolean)
                  .join(', ');

                return (
                  <li
                    key={`${result.city}-${result.state}-${result.country}-${idx}`}
                    id={`${listboxId}-option-${idx}`}
                    role="option"
                    aria-selected={idx === activeIndex}
                    className={`location-suggestion-item ${
                      idx === activeIndex ? 'location-suggestion-item--active' : ''
                    }`}
                    onMouseDown={(e) => {
                      // Prevent input blur before click fires
                      e.preventDefault();
                      handleSelect(result);
                    }}
                    onMouseEnter={() => setActiveIndex(idx)}
                    onMouseLeave={() => setActiveIndex(-1)}
                  >
                    <MapPin
                      size={13}
                      className="suggestion-icon"
                      aria-hidden="true"
                    />
                    <span className="suggestion-text">
                      <span className="suggestion-city">{result.city}</span>
                      {subline && (
                        <span className="suggestion-region">{subline}</span>
                      )}
                    </span>
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
