IMPLEMENT STEP 2 — PERSONALIZATION / WELCOME SCREEN ONLY

The project foundation from Step 1 is complete. Now implement ONLY the initial personalization screen for the Mausam prototype.

GOAL:
Create a polished first-screen experience where the user enters their name, selects their city/location, and chooses the weather interests that matter to them.

IMPORTANT:
Do NOT build the weather dashboard yet.
Do NOT build weather cards.
Do NOT build weather APIs.
Do NOT build backend/database/authentication.
Do NOT build the personalization engine yet.
Do NOT build the persona switcher.
Do NOT modify the existing project architecture unnecessarily.

SCREEN CONTENT:

1. Header / branding
- Show "Mausam" prominently.
- Add a short supporting line such as:
  "Your weather, your way."
- Keep branding clean and professional.

2. Welcome section
- Heading similar to:
  "Let's personalize your weather."
- Supporting text explaining that Mausam will prioritize weather information based on the user's interests.

3. Name input
- Label: "What should we call you?"
- Text input with a clean placeholder such as "Enter your name"
- Required field.

4. Location input
- Label: "Where are you?"
- Text input with placeholder such as "Enter your city"
- Required field.
- For this prototype, this is only a text input. Do NOT integrate geolocation or a weather API.

5. Interest selection
Display selectable interest chips/cards for:

- Health
- Fitness
- Travel
- Family
- Agriculture
- Commuting
- Events
- Beach & Surf

Each interest should have:
- Appropriate Lucide icon
- Short label
- Clear selected/unselected visual state

Allow MULTIPLE interests to be selected.

6. Continue button
- Button text: "Create My Dashboard"
- Keep it visually prominent.
- It should remain disabled until:
  - name is entered
  - location is entered
  - at least one interest is selected

BEHAVIOR:
- Store the entered name, location and selected interests in React state only.
- Do not add backend persistence yet.
- On clicking "Create My Dashboard", for now simply transition to a temporary placeholder state/page saying:
  "Your personalized dashboard is ready."
  Also display the entered name, location and selected interests so we can verify the state is being passed correctly.
- This is temporary and will be replaced by the real dashboard in the next step.

DESIGN:
- Use the existing design tokens from Step 1.
- Modern premium weather-app appearance.
- Mobile-first and responsive.
- Clean spacing and hierarchy.
- Rounded cards/chips.
- Subtle shadows.
- Use the existing atmospheric dark/blue theme.
- Avoid excessive gradients, glassmorphism, or animations.
- Make the interface feel like a real polished mobile weather application rather than a generic form.

FILE ORGANIZATION:
- Put onboarding-specific components inside:
  src/components/onboarding/
- Keep App.jsx responsible for the simple screen/state transition.
- Reuse common components only if genuinely useful.
- Do not create unnecessary abstractions.

VERIFICATION:
1. Run npm run build.
2. Run the dev server.
3. Verify the screen renders without console errors.
4. Test:
   - empty form → button disabled
   - name only → disabled
   - name + location but no interest → disabled
   - select multiple interests → selected states work
   - valid form → button becomes enabled
   - click button → temporary confirmation state displays entered data

STOP after this task.

REPORT:
- Files created/modified
- Components created
- State/interaction implemented
- Verification results
- Any issues

Do not proceed to the dashboard or any other feature.

REPORT BACK AFTER COMPLETION:

Before stopping, provide a concise implementation report containing:

1. WHAT YOU DID
- Describe exactly what was implemented/changed.

2. FILES CHANGED
- List every file created, modified, or deleted.
- For each file, briefly explain its purpose.

3. UI / BEHAVIOR CHANGES
- Describe what the user can now see and do.
- Mention important interactions and state changes.

4. TECHNICAL CHANGES
- Mention important components, state, functions, data structures, dependencies, or logic added.

5. VERIFICATION
- Report whether `npm run build` passed.
- Report whether the dev server was tested.
- Report whether browser/console testing was performed.
- Mention any errors or warnings found.

6. DEVIATIONS / ISSUES
- Explicitly mention anything that could not be implemented exactly as requested.
- Mention any assumptions or decisions you made.

7. CURRENT PROJECT STATE
- Briefly describe what is now working.
- Clearly state what remains intentionally unimplemented.

STOP HERE.
Do not continue to the next feature or make additional changes beyond this prompt.