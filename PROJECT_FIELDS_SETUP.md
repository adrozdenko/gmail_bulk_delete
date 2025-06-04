# GitHub Project Fields Setup Guide

## 🎯 **Required Additional Fields**

This document provides step-by-step instructions to add Priority and Size fields to the GitHub project board.

## 📋 **Field Configurations**

### **Priority Field (Single Select)**
- **Field Name**: Priority
- **Field Type**: Single select
- **Description**: Task priority level for development planning

| Option | Color | Description |
|--------|-------|-------------|
| **P0** | Red (`#F44336`) | Critical/Urgent - Drop everything |
| **P1** | Orange (`#FF9800`) | High Priority - Next sprint |
| **P2** | Yellow (`#FDD835`) | Medium Priority - Planned work |
| **P3** | Green (`#4CAF50`) | Low Priority - Backlog |

### **Size Field (Single Select)**
- **Field Name**: Size
- **Field Type**: Single select  
- **Description**: Estimated development effort

| Option | Color | Description |
|--------|-------|-------------|
| **XS** | Light Blue (`#E3F2FD`) | < 1 day - Quick fixes |
| **S** | Blue (`#BBDEFB`) | 1-2 days - Small features |
| **M** | Medium Blue (`#64B5F6`) | 3-5 days - Standard features |
| **L** | Dark Blue (`#1976D2`) | 1-2 weeks - Large features |
| **XL** | Navy (`#0D47A1`) | > 2 weeks - Epic features |

## 🔧 **Manual Setup Instructions**

Since GitHub Projects V2 API has limited field creation capabilities, follow these steps:

### **Step 1: Access Project Settings**
1. Go to https://github.com/users/adrozdenko/projects/2
2. Click the "Settings" icon (gear) in the top right
3. Select "Fields" from the left sidebar

### **Step 2: Add Priority Field**
1. Click "Add field" button
2. Select "Single select" field type
3. Enter field details:
   - **Name**: `Priority`
   - **Description**: `Task priority level for development planning`
4. Add options one by one:
   - **P0**: Red color, "Critical/Urgent - Drop everything"
   - **P1**: Orange color, "High Priority - Next sprint"  
   - **P2**: Yellow color, "Medium Priority - Planned work"
   - **P3**: Green color, "Low Priority - Backlog"
5. Click "Save field"

### **Step 3: Add Size Field**
1. Click "Add field" button again
2. Select "Single select" field type
3. Enter field details:
   - **Name**: `Size`
   - **Description**: `Estimated development effort`
4. Add options one by one:
   - **XS**: Light Blue, "< 1 day - Quick fixes"
   - **S**: Blue, "1-2 days - Small features"
   - **M**: Medium Blue, "3-5 days - Standard features"
   - **L**: Dark Blue, "1-2 weeks - Large features"
   - **XL**: Navy, "> 2 weeks - Epic features"
5. Click "Save field"

## 📊 **Field Assignment Guidelines**

### **Priority Assignment**
Based on roadmap timeline and business impact:

| Epic/Task | Priority | Reasoning |
|-----------|----------|-----------|
| Epic 1: OAuth 2.0 | P0 | Critical for user adoption |
| Epic 2: Binary CLI | P1 | High impact on distribution |
| Epic 5: Dashboard | P1 | Major UX improvement |
| Epic 3: Daily Digest | P2 | Nice-to-have feature |
| Epic 6: BlackHole | P2 | Power user feature |
| Epic 9: Docker | P2 | DevOps improvement |
| Epic 4: Snooze | P3 | Advanced feature |
| Epic 7: Attachments | P3 | Storage optimization |
| Epic 8: Pause Inbox | P3 | Niche feature |
| Epic 10: Telemetry | P3 | Analytics feature |
| Epic 11: Marketplace | P3 | Community feature |
| Epic 12: Dark Mode | P3 | UI polish |
| Epic 13: i18n | P3 | Accessibility feature |

### **Size Assignment**
Based on story points and complexity:

| Story Points | Size | Examples |
|--------------|------|----------|
| 1-2 points | XS | Simple config, docs |
| 3 points | S | Basic features, bug fixes |
| 5 points | M | Standard API integrations |
| 8 points | L | Complex features |
| 13+ points | XL | Major subsystems |

## 🎯 **Recommended Field Values for Current Issues**

### **Epic Issues**
| Issue | Title | Priority | Size |
|-------|-------|----------|------|
| #1 | Epic 1: OAuth 2.0 | P0 | XL |
| #2 | Epic 2: Binary CLI | P1 | L |
| #3 | Epic 3: Daily Digest | P2 | L |
| #4 | Epic 4: Snooze | P3 | XL |
| #5 | Epic 5: Dashboard | P1 | XL |
| #6 | Epic 6: BlackHole | P2 | L |
| #7 | Epic 7: Attachments | P3 | XL |
| #8 | Epic 8: Pause Inbox | P3 | L |
| #9 | Epic 9: Docker | P2 | M |
| #10 | Epic 10: Telemetry | P3 | M |
| #11 | Epic 11: Marketplace | P3 | L |
| #12 | Epic 12: Dark Mode | P3 | S |
| #13 | Epic 13: i18n | P3 | XL |

### **Task Issues**
| Issue | Title | Priority | Size |
|-------|-------|----------|------|
| #14 | Register Google Cloud project | P0 | XS |
| #15 | Implement OAuth flow | P0 | L |
| #16 | Token revocation helper | P0 | S |
| #17 | Smoke-test OAuth | P0 | S |
| #18 | Research binary packaging | P1 | S |
| #19 | Create CI/CD pipeline | P1 | M |
| #20 | Choose dashboard tech | P1 | XS |

## 📈 **Field Usage Best Practices**

### **Priority Guidelines**
- **P0**: Only use for critical bugs or foundational features
- **P1**: Features required for major milestones
- **P2**: Planned features for current quarter
- **P3**: Backlog items and future enhancements

### **Size Guidelines**
- **XS**: Configuration changes, documentation updates
- **S**: Bug fixes, minor features with clear requirements
- **M**: Standard features requiring design and testing
- **L**: Complex features with multiple components
- **XL**: Major features requiring architectural changes

### **Field Maintenance**
- **Review Quarterly**: Reassess priorities based on user feedback
- **Update Sizes**: Adjust based on actual implementation complexity
- **Cross-Reference**: Ensure Size aligns with Story Points
- **Document Changes**: Track reasoning for priority/size adjustments

## 🔄 **Automation Opportunities**

Once fields are created, consider these automation rules:

### **Auto-Assignment Rules**
- New issues default to P3 priority
- Issues in milestones auto-assign to appropriate priority
- Epic issues automatically get XL size
- Task issues default to M size

### **Workflow Triggers**
- Move P0 issues directly to "Ready" column
- Notify team when P0/P1 issues are created
- Auto-assign based on issue labels
- Update priority when moved to "In Progress"

## ✅ **Verification Steps**

After setting up fields:

1. **Test Field Creation**: Verify both Priority and Size fields appear
2. **Test Option Selection**: Confirm all options are selectable
3. **Color Verification**: Check that colors display correctly
4. **Bulk Assignment**: Test assigning values to multiple issues
5. **Filter Testing**: Verify filtering by Priority and Size works
6. **View Configuration**: Set up custom views using new fields

## 📊 **Custom Views to Create**

Once fields are set up, create these useful views:

### **1. Priority Dashboard**
- Group by: Priority
- Sort by: Story Points (descending)
- Filter: Status ≠ Done

### **2. Size Planning**
- Group by: Size  
- Sort by: Priority
- Show: All issues

### **3. Current Sprint**
- Filter: Priority = P0 OR P1
- Filter: Status = Ready OR In Progress
- Group by: Assignee

### **4. Backlog Grooming**
- Filter: Priority = P3
- Filter: Size = Not set
- Sort by: Creation date

This field setup will provide comprehensive project management capabilities aligned with the development roadmap and story point system.