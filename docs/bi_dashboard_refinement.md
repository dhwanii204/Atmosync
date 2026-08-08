# AtmoSync BI Dashboard Refinement

## Interactive Container Filtering

The AtmoSync Logistics Control Tower dashboard was refined with a native Container ID filter.

The filter allows operations users to select an individual shipment container and dynamically update the relevant dashboard views.

### Filter Configuration

- Filter type: Values
- Dataset: Shipment Analysis
- Column: `container_id`
- Multiple selections: Disabled
- Default value: None
- Required value: No

### Applied Views

The Container ID filter is scoped to:

- Shipment Risk Distribution
- Spoilage Risk Distribution
- Container Journey Progress
- Critical Shipment Watchlist

### Business Purpose

The filter enables users to move from an overall logistics view to container-specific monitoring.

For example, selecting a container such as `C002` allows the user to investigate its shipment risk, spoilage risk, journey progress, and critical monitoring status without manually inspecting individual records.

This improves the dashboard's usability for operational monitoring and decision-making.