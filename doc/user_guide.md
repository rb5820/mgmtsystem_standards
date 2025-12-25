# User Guide - Management Systems Standards

## Overview

The Management Systems Standards module provides comprehensive tools for managing compliance frameworks with advanced cost tracking capabilities.

## Navigation

### Main Menus
- **Standards**: Manage compliance frameworks (ISO 27001, NIST, CIS Controls)
- **Domains**: Organize controls into logical categories
- **Controls**: Individual security/compliance requirements with cost tracking

## Cost Management Features

### Setting Up Cost Tracking

1. **Configure Hourly Rates**
   - Navigate to a control record
   - Go to "💰 Cost Information" tab
   - Set appropriate hourly rate (default: $100.00)

2. **Set Test Timing**
   - **Manual Test Timing**: Time required for manual testing (default: 7.5 minutes)
   - **Automated Test Timing**: Time for automated assessment (default: 3 seconds)
   - **Test Frequency**: How often testing occurs (Monthly, Quarterly, Semi-Annual, Annual)

### Understanding Cost Calculations

#### Annual Maintenance Costs
- **Manual Only**: `(manual_time × frequency) ÷ 60 × hourly_rate`
- **Combined**: Uses automated time when available, otherwise manual time
  ```
  if automated_assessment_enabled:
      time = automated_test_timing ÷ 60
  else:
      time = manual_test_timing
  
  cost = (time × frequency) ÷ 60 × hourly_rate
  ```

#### Example Calculation
```
Control: Quarterly Password Policy Review
- Manual Test Timing: 15 minutes
- Automated Test Timing: 5 seconds = 0.083 minutes
- Test Frequency: Quarterly (4×/year)
- Hourly Rate: $100/hour
- Automated Assessment: Enabled

Manual Cost = (15 × 4) ÷ 60 × $100 = $100.00/year
Combined Cost = (0.083 × 4) ÷ 60 × $100 = $0.55/year
Automation Savings = $99.45/year (99.4% reduction)
```

### Cost Information Pages

#### Control Level
- Access cost details in the "💰 Cost Information" tab
- View both manual and combined cost projections
- See efficiency metrics like cost-per-minute

#### Domain Level  
- Navigate to domain record → "💰 Cost Information" tab
- View aggregated costs for all controls in the domain
- Compare manual vs automated cost implications

#### Standard Level
- Open standard record → "💰 Cost Information" tab
- See total costs across all domains and controls
- Use for executive reporting and budget planning

## Best Practices

### Time Estimation Guidelines
- **Simple checks**: 2-5 minutes
- **Configuration reviews**: 5-15 minutes  
- **Documentation audits**: 15-30 minutes
- **Complex assessments**: 30+ minutes

### Frequency Selection
- **Critical controls**: Monthly or Quarterly
- **Standard controls**: Quarterly or Semi-Annual
- **Low-risk controls**: Annual

### Cost Analysis Workflow
1. Set up controls with realistic time estimates
2. Choose appropriate test frequencies based on risk
3. Review domain-level cost summaries
4. Use standard-level totals for budget planning
5. Compare manual vs automated costs for ROI decisions

## Troubleshooting

### Common Issues
- **Zero costs showing**: Check that hourly rate is set and > 0
- **Unexpected totals**: Verify test frequency and time estimates
- **Missing cost information**: Ensure cost information tabs are accessible

### Support
For technical issues or questions, refer to the detailed implementation guide in `/doc/cost_enhancement_guide.md`.