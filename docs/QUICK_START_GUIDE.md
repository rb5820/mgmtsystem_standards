# ⚡ Quick Start Guide - Management System Standards Module

**Version**: 18.0.1.0.5 | **Setup Time**: 15-30 minutes | **Target**: New Users, Administrators

## 🚀 Installation & Prerequisites

### System Requirements
- Odoo 18.0 Enterprise
- Required modules: `base`, `mail`, `mgmtsystem`, `document_page`, `product`
- Optional (recommended): `mgmtsystem_audit_workflow` for enhanced tracking

### Installation Steps
1. **Install Module**: Apps → Search "Management System Standards" → Install
2. **Verify Dependencies**: Ensure all required modules are active
3. **Refresh Browser**: Clear cache and refresh for menu updates
4. **Check Permissions**: Assign users to appropriate security groups

## Initial Setup

### Step 1: Define Standard Categories
1. Go to Management System > Standards > Standard Categories
2. Create categories for your standards (e.g., Quality, Environmental, Security)
3. Organize them in a hierarchy if needed

### Step 2: Add Standards
1. Go to Management System > Standards > Standards
2. Click Create to add a new standard
3. Fill in the details:
   - Standard Code (e.g., ISO 9001:2015)
   - Name
   - Version
   - Category
   - Publication/Effective dates
4. Save the record

### Step 3: Define Requirements
1. Open the standard you created
2. Go to the Requirements tab
3. Add the main clauses of the standard
4. For each clause, you can add sub-clauses by setting a parent
5. Set the compliance status for each requirement

### Step 4: Create Audit Questions
1. Open a requirement record
2. Go to the Audit Questions tab
3. Add questions that would verify compliance
4. Specify the expected evidence

## Daily Usage

### Tracking Compliance
1. Go to Management System > Standards > Requirements
2. Filter by compliance status to see non-compliant items
3. Use grouping options to analyze by standard or category

### Preparing for Audits
1. Go to Management System > Standards > Requirements
2. Select requirements to be verified
3. Review the audit questions and expected evidence
4. Update compliance status based on findings

### Standard Updates
When a standard is updated to a new version:
1. Create the new standard version
2. Set the old standard to "Superseded" status
3. Link the old standard to the new one using the "Superseded By" field
4. Create requirements for the new standard version

## Tips & Tricks
- Use color coding to highlight important standards
- Assign priorities to critical requirements
- Link actual evidence documents to requirements
- Use the search filters to quickly find specific requirements
- Create custom dashboards to monitor compliance status

## Need Help?
Contact your system administrator or the support team at vorsselmansphilip@gmail.com