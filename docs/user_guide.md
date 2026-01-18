# 👤 User Guide - Management System Standards

**Version**: 18.0.1.0.5 | **Target**: Business Users, Compliance Teams, Auditors

## 🎯 Overview

The Management System Standards module provides comprehensive tools for managing compliance frameworks (ISO 9001/14001/27001, CIS Controls, IEC 62443) with advanced cost tracking, multi-company support, and workflow integration.

## 🧭 Navigation & Access

### Main Menu Structure
Access via: **Apps → Management System → Standards** 

```
📋 Standards          # Main compliance frameworks
├── 🏗️ Domains        # Security/compliance domains with filtering
├── 📝 Controls       # Individual controls with cost tracking
├── 📋 Requirements   # Detailed framework requirements  
├── 🏆 Certifications # Assessment and certification tracking
├── 📂 Categories     # Framework organization
├── 🔧 Zones          # Logical control groupings
├── 📊 Assessment Tools # External tool integration
└── ❓ Audit Questions # Structured audit support
```

### Security Groups & Access Levels
- **👁️ Viewer**: Read-only access to standards and controls
- **👤 User**: Basic editing of controls and requirements
- **🧪 Tester**: Assessment and testing capabilities
- **👀 Reviewer**: Review and approval functions
- **👑 Manager**: Full administrative access and cost configuration

## 💰 Cost Management & ROI Analysis

### Setting Up Cost Tracking

1. **Configure Base Parameters**
   - Navigate to any control record
   - Go to "💰 Cost Information" tab  
   - Set **Hourly Rate** (default: $100.00/hour)
   - Define **Implementation Time** (minutes for initial setup)
   - Set **Maintenance Time** (minutes for ongoing testing/maintenance)

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