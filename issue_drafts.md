# Feature Issue Drafts

## 1) Add 7-day weather forecast and trend chart

Title: Add 7-day weather forecast and trend chart

Body:
```
## Summary
Add a multi-day weather forecast view to the existing weather app so users can see upcoming conditions beyond the current temperature.

## Proposed functionality
- Show a 7-day forecast for the selected city
- Include daily high/low temperatures, precipitation chance, and weather icons
- Add a simple trend chart or compact cards for the next 24 hours
- Keep the existing current-weather panel intact

## Acceptance criteria
- User can search for a city and see current weather plus a forecast section
- Forecast data is fetched from Open-Meteo or an equivalent API
- The UI remains readable on desktop and mobile
- Unsupported or missing data is handled gracefully

## Notes
This feature builds directly on the current Flask weather dashboard and makes the app more useful for planning.
```

## 2) Add saved cities and recent search history

Title: Add saved cities and recent search history

Body:
```
## Summary
Let users save frequently used cities and quickly revisit previous searches without retyping them.

## Proposed functionality
- Add a favorites list with local persistence
- Save the last 5-10 searched cities in a recent history panel
- Allow users to click a saved city to reload weather immediately
- Include a clear/remove action for favorites and history

## Acceptance criteria
- Saved cities persist across page refreshes
- Recent searches are shown in a list with a clear action
- Search results update correctly when a favorite is selected
- The feature works without requiring a backend database

## Notes
This is a lightweight improvement that boosts usability and fits well with the weather app's current single-city workflow.
```

## 3) Add calculator history, memory, and scientific mode

Title: Add calculator history, memory, and scientific mode

Body:
```
## Summary
Improve the calculator experience with reusable history and a more capable calculation interface.

## Proposed functionality
- Keep a history of recent expressions and results
- Add memory buttons such as MC, MR, M+, M-
- Add a scientific mode with functions like sqrt, sin, cos, tan, and parentheses support
- Let users click previous entries to restore them into the expression box

## Acceptance criteria
- Recent evaluations remain visible after each calculation
- Memory operations work reliably for repeated calculations
- Scientific functions produce correct results for supported expressions
- Invalid expressions show helpful error messages

## Notes
This feature will make the calculator more useful for repeated tasks and align it with common desktop calculator behavior.
```
