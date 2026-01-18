# Management System Standards - Multi-Employer Security Model

## 🔐 Security Architecture Overview

The Management System Standards module implements a comprehensive multi-employer security architecture with eleven hierarchical access levels, ensuring proper data isolation and role-based access control. The employer serves as the final approver for all compliance activities.

**Non-Employer Users**: Viewer < Editor < Reviewer < Approver < Certified Auditor < Multi-Employer Manager  
**Employer Users (Final Approvers)**: Employer Viewer < Employer Editor < Employer Reviewer < Employer Approver < Employer Certified Auditor

## 🏢 Multi-Employer Compliance

### Employer Isolation Strategy
- **Record Rules**: All models implement multi-employer access rules using `company_ids` filtering
- **Domain Pattern**: `['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]`
- **Global Records**: Records with `company_id = False` are visible across all employers
- **Employer-Specific**: Records with specific `company_id` are isolated per employer (final approver)

### Supported Models
All core models implement multi-employer isolation with final approval by employer:
- `mgmtsystem.standard` - Management System Standards
- `mgmtsystem.standard.category` - Standard Categories
- `mgmtsystem.standard.requirement` - Requirements
- `mgmtsystem.standard.control` - Controls
- `mgmtsystem.standard.domain` - Domains
- `mgmtsystem.standard.zone` - Security Zones
- `mgmtsystem.standard.certification` - Certifications
- `mgmtsystem.standard.control.assessment.tool` - Assessment Tools
- `mgmtsystem.standard.audit.question` - Audit Questions

## 👥 Security Group Hierarchy

### Non-Employer Users (Subject to Employer Approval)

### Level 1: Standards Viewer (`group_standard_viewer`)
**Role**: Read-only Observer
- **Access**: Read-only access to all standards data
- **Permissions**: View standards, requirements, controls, compliance status
- **Restrictions**: Cannot modify any data
- **Multi-Employer**: Employer-isolated viewing
- **Use Case**: Executives, auditors requiring oversight without modification rights

### Level 2: Standards Editor (`group_standard_editor`)
**Role**: Content Creator/Editor
- **Access**: Create, Read, Update (no delete)
- **Permissions**: Manage standards data within employer scope (subject to employer approval)
- **Restrictions**: Cannot delete records
- **Multi-Employer**: Employer-isolated operations
- **Use Case**: Standards managers, compliance officers

### Level 3: Standards Reviewer (`group_standard_reviewer`)
**Role**: Assessment Reviewer
- **Access**: Enhanced Editor permissions + review capabilities
- **Permissions**: Review test results, validate assessments, provide feedback
- **Restrictions**: Cannot delete core standards data
- **Multi-Employer**: Employer-isolated reviewing
- **Use Case**: Senior compliance officers, review managers

### Level 4: Standards Approver (`group_standard_approver`)
**Role**: Compliance Approver
- **Access**: Enhanced Reviewer permissions + approval capabilities
- **Permissions**: Approve compliance status changes, validate final assessments (pending employer approval)
- **Restrictions**: Cannot delete core standards data
- **Multi-Employer**: Employer-isolated approving
- **Use Case**: Senior compliance officers, approval managers

### Level 5: Standards Certified Auditor (`group_standard_certified_auditor`)
**Role**: Internal Auditor
- **Access**: Full read/write/create/delete within employer
- **Permissions**: Conduct formal audits, provide independent audit opinions
- **Restrictions**: Limited to assigned employer
- **Multi-Employer**: Employer-isolated auditing
- **Use Case**: Internal auditors, certification managers

### Level 6: Multi-Employer Manager (`group_standard_multi_company_manager`)
**Role**: Enterprise Administrator
- **Access**: Full administrative access across all employers
- **Permissions**: Manage standards data for all employers in system (ultimate authority)
- **Restrictions**: None (subject to system administrator oversight)
- **Multi-Employer**: Cross-employer management capabilities
- **Use Case**: Enterprise compliance directors, system administrators

### Employer Users (Final Approval Authority)

### Level 7: Employer Viewer (`group_employer_viewer`)
**Role**: Employer Observer
- **Access**: Read-only access with employer oversight authority
- **Permissions**: View all standards data with final approval oversight
- **Restrictions**: Cannot modify data directly
- **Multi-Employer**: Employer-specific viewing with authority
- **Use Case**: Employer executives, oversight personnel

### Level 8: Employer Editor (`group_employer_editor`)
**Role**: Employer Content Manager
- **Access**: Create, Read, Update with direct approval authority
- **Permissions**: Manage standards data with immediate approval capability
- **Restrictions**: Cannot delete records (preservation of audit trail)
- **Multi-Employer**: Employer-specific operations with authority
- **Use Case**: Employer compliance managers, authorized representatives

### Level 9: Employer Reviewer (`group_employer_reviewer`)
**Role**: Employer Compliance Reviewer
- **Access**: Enhanced Editor permissions + direct review authority
- **Permissions**: Review and validate assessments with immediate approval
- **Restrictions**: Cannot delete core standards data
- **Multi-Employer**: Employer-specific reviewing with authority
- **Use Case**: Employer senior compliance officers, authorized reviewers

### Level 10: Employer Approver (`group_employer_approver`)
**Role**: Employer Final Approver
- **Access**: Full read/write/create/delete with final approval authority
- **Permissions**: Final approval for compliance status changes and certifications
- **Restrictions**: None within employer scope
- **Multi-Employer**: Employer-specific final approval authority
- **Use Case**: Employer directors, final approval authorities

### Level 11: Employer Certified Auditor (`group_employer_certified_auditor`)
**Role**: Employer Authorized Auditor
- **Access**: Full audit authority with delete permissions
- **Permissions**: Complete audit oversight and final approval as employer representative
- **Restrictions**: None within employer scope
- **Multi-Employer**: Employer-authorized audit authority
- **Use Case**: Employer-authorized certified auditors, ultimate compliance authorities



## 🛡️ Access Rights Matrix

### Non-Employer Users (Subject to Employer Approval)
| Model | Viewer | Editor | Reviewer | Approver | Certified Auditor | Multi-Employer |
|-------|--------|--------|----------|----------|------------------|----------------|
| Standards | R | RWC | RWC | RWC | RWCD | RWCD |
| Categories | R | RWC | RWC | RWC | RWCD | RWCD |
| Requirements | R | RWC | RWC | RWC | RWCD | RWCD |
| Controls | R | RWC | RWC | RWC | RWCD | RWCD |
| Domains | R | RWC | RWC | RWC | RWCD | RWCD |
| Zones | R | RWC | RWC | RWC | RWCD | RWCD |
| Certifications | R | RWC | RWC | RWC | RWCD | RWCD |
| Assessment Tools | R | RWC | RWC | RWC | RWCD | RWCD |
| Audit Questions | R | RWC | RWC | RWC | RWCD | RWCD |

### Employer Users (Final Approval Authority)
| Model | Emp Viewer | Emp Editor | Emp Reviewer | Emp Approver | Emp Certified Auditor |
|-------|------------|------------|--------------|--------------|----------------------|
| Standards | R | RWC | RWC | RWCD | RWCD |
| Categories | R | RWC | RWC | RWCD | RWCD |
| Requirements | R | RWC | RWC | RWCD | RWCD |
| Controls | R | RWC | RWC | RWCD | RWCD |
| Domains | R | RWC | RWC | RWCD | RWCD |
| Zones | R | RWC | RWC | RWCD | RWCD |
| Certifications | R | RWC | RWC | RWCD | RWCD |
| Assessment Tools | R | RWC | RWC | RWCD | RWCD |
| Audit Questions | R | RWC | RWC | RWCD | RWCD |

**Legend**: R=Read, W=Write, C=Create, D=Delete

## 🔒 Record Rules Implementation

### Multi-Employer Domain Pattern
```python
['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]
```

### Global vs Employer-Specific Records
- **Global Records** (`company_id = False`): Visible to all employers
  - Standard templates, base categories, reference data
- **Employer Records** (`company_id != False`): Employer-isolated with final approval authority
  - Employer-specific implementations, assessments, certifications

### Security Rule Examples

#### Standards Access Rule
```xml
<record id="mgmtsystem_standard_comp_rule" model="ir.rule">
    <field name="name">Standards: Multi-Employer Rule</field>
    <field name="model_id" ref="model_mgmtsystem_standard"/>
    <field name="domain_force">['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]</field>
</record>
```

## 🚀 Implementation Guidelines

### For Developers

1. **Model Security**: Always implement multi-employer record rules for new models
2. **Employer Field**: Add `company_id` field to all business models (employer as final approver)
3. **Default Values**: Set appropriate employer defaults in model creation
4. **Access Rights**: Define access rights for all security levels (both non-employer and employer tracks)
5. **Testing**: Verify multi-employer isolation and dual-track approval workflows in tests
6. **Dual Track Design**: Ensure clear separation between non-employer user capabilities and employer final approval authority

### For Administrators

1. **Group Assignment**: Assign users to appropriate security groups based on roles and employer status
2. **Employer Setup**: Ensure proper employer configuration for multi-tenant setups with final approval designation
3. **Data Migration**: Consider employer assignment and approval authority during data imports
4. **Monitoring**: Regularly audit user access and group memberships for both tracks
5. **Approval Workflows**: Configure clear escalation paths from non-employer users to employer approvers

## 📋 Security Checklist

### Pre-Deployment Verification
- [ ] All models have multi-employer record rules
- [ ] Security groups properly configured with dual-track hierarchy
- [ ] Access rights defined for all user levels (both non-employer and employer)
- [ ] Employer isolation tested and verified
- [ ] Admin user assigned to multi-employer manager group
- [ ] Standard users assigned to appropriate employer-specific groups
- [ ] Employer approval workflows properly configured
- [ ] Clear separation between non-employer and employer user capabilities
- [ ] Employer final approval authority properly designated

### Post-Deployment Validation
- [ ] Cross-employer data leakage prevention verified
- [ ] User access permissions functioning correctly for both tracks
- [ ] Employer-specific data properly isolated
- [ ] Global data accessible across employers
- [ ] Security group inheritance working as expected for both hierarchies
- [ ] Employer approval authority properly enforced
- [ ] Non-employer to employer escalation workflows functioning

## 🔧 Troubleshooting

### Common Issues

#### Users Cannot See Data
**Symptom**: Users with appropriate groups cannot access records
**Solution**: 
1. Verify employer assignment on user record
2. Check record company_id values (employer ID)
3. Validate multi-employer record rules are active

#### Cross-Employer Data Leakage
**Symptom**: Users see data from other employers
**Solution**:
1. Review record rule domain expressions
2. Ensure company_id fields are properly set with correct employer
3. Verify user employer assignments

#### Permission Denied Errors
**Symptom**: Access denied despite proper group membership
**Solution**:
1. Check access rights CSV for group permissions
2. Verify security group hierarchy (implied_ids)
3. Validate user active status and group assignments

## 📚 Related Documentation

- [Multi-Employer Setup Guide](MULTI_EMPLOYER_SETUP.md)
- [User Management Guide](USER_MANAGEMENT.md)
- [Security Configuration](SECURITY_CONFIG.md)
- [Access Rights Reference](ACCESS_RIGHTS.md)
- [Employer Approval Workflows](EMPLOYER_APPROVAL.md)

---

**Version**: 18.0.1.0.1  
**Last Updated**: 2025-01-28  
**Author**: RB5820 Development Team  
**Status**: Production Ready ✅