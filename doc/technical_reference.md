# 🔧 Technical Reference Guide - Cost Enhancement Module

## 📋 Field Definitions

### Control Model (mgmtsystem.standard.control)

#### Time Tracking Fields
| Field Name | Type | Unit | Description | Default |
|------------|------|------|-------------|---------|
| `manual_implementation_timing` | Float | Minutes | Time to manually implement control | 15.0 |
| `manual_test_timing` | Float | Minutes | Time to manually test control | 7.5 |
| `automated_implementation_timing` | Float | Seconds | Time for automated implementation | 0.0 |
| `automated_test_timing` | Float | Seconds | Time for automated testing | 3.0 |

#### Computed Time Conversion Fields
| Field Name | Type | Compute Method | Description |
|------------|------|----------------|-------------|
| `manual_implementation_timing_hours` | Float | `_compute_manual_timing_hours` | Implementation time in hours |
| `manual_test_timing_hours` | Float | `_compute_manual_timing_hours` | Test time in hours |

#### Cost Calculation Fields
| Field Name | Type | Compute Method | Description |
|------------|------|----------------|-------------|
| `manual_annual_maintenance_cost` | Float | `_compute_maintenance_cost_manual` | Annual cost using manual timing only |
| `combined_annual_maintenance_cost` | Float | `_compute_maintenance_cost_combined` | Annual cost using automated when available |
| `implementation_cost` | Float | `_compute_implementation_cost` | One-time implementation cost |
| `cost_per_minute` | Float | `_compute_cost_per_minute` | Implementation efficiency metric |

#### Annual Time Aggregation Fields
| Field Name | Type | Compute Method | Unit | Description |
|------------|------|----------------|------|-------------|
| `total_annual_maintenance_time` | Float | `_compute_total_annual_times` | Minutes | Manual test time × frequency |
| `total_annual_maintenance_time_combined` | Float | `_compute_total_annual_times` | Minutes | Smart test time × frequency |
| `total_annual_maintenance_hours` | Float | `_compute_total_annual_times` | Hours | Manual time in hours |
| `total_annual_maintenance_hours_combined` | Float | `_compute_total_annual_times` | Hours | Smart time in hours |

### Domain Model (mgmtsystem.standard.domain)

#### Domain Cost Aggregation Fields
| Field Name | Type | Compute Method | Description |
|------------|------|----------------|-------------|
| `domain_total_maintenance_cost_manual` | Float | `_compute_domain_costs` | Sum of manual costs for all controls |
| `domain_total_maintenance_cost_combined` | Float | `_compute_domain_costs` | Sum of combined costs for all controls |
| `domain_total_implementation_cost` | Float | `_compute_domain_costs` | Sum of implementation costs |

#### Domain Time Aggregation Fields
| Field Name | Type | Unit | Description |
|------------|------|------|-------------|
| `domain_total_maintenance_time_manual` | Float | Minutes | Sum of manual maintenance time |
| `domain_total_maintenance_time_combined` | Float | Minutes | Sum of combined maintenance time |
| `domain_total_maintenance_hours_manual` | Float | Hours | Sum of manual maintenance hours |
| `domain_total_maintenance_hours_combined` | Float | Hours | Sum of combined maintenance hours |

### Standard Model (mgmtsystem.standard)

#### Standard Cost Aggregation Fields
| Field Name | Type | Compute Method | Description |
|------------|------|----------------|-------------|
| `standard_total_maintenance_cost_manual` | Float | `_compute_standard_costs` | Sum of all manual maintenance costs |
| `standard_total_maintenance_cost_combined` | Float | `_compute_standard_costs` | Sum of all combined maintenance costs |
| `standard_total_implementation_cost` | Float | `_compute_standard_costs` | Sum of all implementation costs |

#### Standard Time Aggregation Fields
| Field Name | Type | Unit | Description |
|------------|------|------|-------------|
| `standard_total_maintenance_time_manual` | Float | Minutes | Sum of all manual maintenance time |
| `standard_total_maintenance_time_combined` | Float | Minutes | Sum of all combined maintenance time |  
| `standard_total_maintenance_hours_manual` | Float | Hours | Sum of all manual maintenance hours |
| `standard_total_maintenance_hours_combined` | Float | Hours | Sum of all combined maintenance hours |

## 🧮 Calculation Methods

### Control Level Calculations

#### Manual Maintenance Cost
```python
@api.depends('manual_test_timing', 'test_frequency', 'company_id.hourly_rate')
def _compute_maintenance_cost_manual(self):
    for record in self:
        hourly_rate = record.company_id.hourly_rate or 100.0
        if record.test_frequency and record.manual_test_timing:
            time_hours = record.manual_test_timing / 60
            frequency_multiplier = self._get_frequency_multiplier(record.test_frequency)
            record.manual_annual_maintenance_cost = time_hours * frequency_multiplier * hourly_rate
        else:
            record.manual_annual_maintenance_cost = 0.0
```

#### Combined Maintenance Cost (Smart Logic)
```python
@api.depends('manual_test_timing', 'automated_test_timing', 'automated_assessment', 
             'test_frequency', 'company_id.hourly_rate')
def _compute_maintenance_cost_combined(self):
    for record in self:
        hourly_rate = record.company_id.hourly_rate or 100.0
        if record.test_frequency:
            # Use automated timing if available and enabled
            if record.automated_assessment and record.automated_test_timing:
                time_hours = record.automated_test_timing / 3600  # Convert seconds to hours
            elif record.manual_test_timing:
                time_hours = record.manual_test_timing / 60  # Convert minutes to hours
            else:
                time_hours = 0.0
            
            frequency_multiplier = self._get_frequency_multiplier(record.test_frequency)
            record.combined_annual_maintenance_cost = time_hours * frequency_multiplier * hourly_rate
        else:
            record.combined_annual_maintenance_cost = 0.0
```

### Frequency Multipliers

#### Test Frequency Conversion
```python
def _get_frequency_multiplier(self, frequency):
    """Convert test frequency to annual multiplier"""
    frequency_map = {
        'monthly': 12,
        'quarterly': 4,
        'semi_annual': 2,
        'annual': 1,
    }
    return frequency_map.get(frequency, 1)
```

### Domain Level Calculations

#### Domain Cost Aggregation
```python
@api.depends('control_ids.manual_annual_maintenance_cost',
             'control_ids.combined_annual_maintenance_cost',
             'control_ids.implementation_cost',
             'child_domain_ids.domain_total_maintenance_cost_manual',
             'child_domain_ids.domain_total_maintenance_cost_combined',
             'child_domain_ids.domain_total_implementation_cost')
def _compute_domain_costs(self):
    for record in self:
        # Direct control costs
        control_manual = sum(record.control_ids.mapped('manual_annual_maintenance_cost'))
        control_combined = sum(record.control_ids.mapped('combined_annual_maintenance_cost'))
        control_implementation = sum(record.control_ids.mapped('implementation_cost'))
        
        # Child domain costs (recursive)
        child_manual = sum(record.child_domain_ids.mapped('domain_total_maintenance_cost_manual'))
        child_combined = sum(record.child_domain_ids.mapped('domain_total_maintenance_cost_combined'))
        child_implementation = sum(record.child_domain_ids.mapped('domain_total_implementation_cost'))
        
        # Total aggregation
        record.domain_total_maintenance_cost_manual = control_manual + child_manual
        record.domain_total_maintenance_cost_combined = control_combined + child_combined
        record.domain_total_implementation_cost = control_implementation + child_implementation
```

## 🎨 View Structure

### Control Form View Sections

#### Cost Information Tab Layout
```xml
<page string="💰 Cost Information" name="cost_info">
    <group name="cost_implementation" string="Implementation">
        <field name="manual_implementation_timing"/>
        <field name="manual_implementation_timing_hours"/>
        <field name="implementation_cost"/>
        <field name="cost_per_minute"/>
    </group>
    
    <group name="cost_manual_only" string="Annual Maintenance (Manual Only)">
        <field name="total_annual_maintenance_time"/>
        <field name="total_annual_maintenance_hours"/>
        <field name="manual_annual_maintenance_cost"/>
    </group>
    
    <group name="cost_combined" string="Annual Maintenance (Combined)">
        <field name="total_annual_maintenance_time_combined"/>
        <field name="total_annual_maintenance_hours_combined"/>
        <field name="combined_annual_maintenance_cost"/>
    </group>
</page>
```

### Domain Form View Cost Tab
```xml
<page string="💰 Cost Information" name="cost_info">
    <group name="domain_implementation" string="Implementation Totals">
        <field name="domain_total_implementation_cost"/>
    </group>
    
    <group name="domain_manual_totals" string="Annual Maintenance (Manual Only)">
        <field name="domain_total_maintenance_time_manual"/>
        <field name="domain_total_maintenance_hours_manual"/>
        <field name="domain_total_maintenance_cost_manual"/>
    </group>
    
    <group name="domain_combined_totals" string="Annual Maintenance (Combined)">
        <field name="domain_total_maintenance_time_combined"/>
        <field name="domain_total_maintenance_hours_combined"/>
        <field name="domain_total_maintenance_cost_combined"/>
    </group>
</page>
```

## ⚙️ Configuration

### Company Settings
- **Hourly Rate**: Default $100.00 per hour
- **Location**: `res.company` model enhancement
- **Field**: `hourly_rate` (Float field)

### Default Values
- **Manual Implementation Time**: 15 minutes
- **Manual Test Time**: 7.5 minutes  
- **Automated Test Time**: 3 seconds
- **Test Frequency**: Annual

## 🔄 Dependencies

### Module Dependencies
- **mgmtsystem_standards**: Base compliance module
- **base**: Odoo core functionality

### Computed Field Dependencies
```python
# Example dependency chain
@api.depends('manual_test_timing', 'test_frequency', 'company_id.hourly_rate')
def _compute_maintenance_cost_manual(self):
    # Cost calculation depends on timing, frequency, and hourly rate
```

## 🐛 Troubleshooting

### Common Issues

#### Zero Costs Displayed
- **Check**: Hourly rate set at company level
- **Check**: Test frequency configured
- **Check**: Time values > 0

#### Incorrect Aggregation
- **Check**: Parent-child relationships properly configured
- **Check**: @api.depends includes all related fields
- **Solution**: Refresh computed fields or restart Odoo service

#### Performance Issues
- **Optimize**: Batch calculations using `@api.depends_context`
- **Cache**: Use `@api.model` for static calculations
- **Index**: Add database indexes for frequently queried fields

---
*Complete technical reference for cost enhancement implementation* 🔧