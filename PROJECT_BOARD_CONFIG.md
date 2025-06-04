# GitHub Project Board Configuration

This document outlines the desired configuration for the Gmail Bulk Delete development project board.

## 🎯 **Project Information**
- **Project URL**: https://github.com/users/adrozdenko/projects/2
- **Title**: Gmail Bulk Delete - Development Roadmap
- **Description**: Development roadmap with kanban workflow: Backlog → Ready → In Progress → In Review → Done

## 📋 **Column Configuration (Status Field)**

The Status field should have these options:

| Column | Color | Description | Purpose |
|--------|--------|-------------|---------|
| **Backlog** | Gray | Items ready to be worked on | All new issues start here |
| **Ready** | Yellow | Items prioritized and ready to start | Groomed and ready for development |
| **In Progress** | Blue | Items currently being worked on | Active development |
| **In Review** | Purple | Items under review | Code review, testing phase |
| **Done** | Green | Completed items | Finished and deployed |

## 🏷️ **Additional Fields**

### **Priority Field** (Single Select)
- **P0**: Critical/Urgent
- **P1**: High Priority  
- **P2**: Medium Priority
- **P3**: Low Priority

### **Size Field** (Single Select)
- **XS**: < 1 day
- **S**: 1-2 days
- **M**: 3-5 days
- **L**: 1-2 weeks
- **XL**: > 2 weeks

### **Standard GitHub Fields**
- Title
- Assignees
- Labels
- Linked pull requests
- Milestone
- Repository
- Reviewers

## 📊 **Current Item Organization**

### **Epics (High Level)**
Move these to **Backlog** initially:
- Epic 1: OAuth 2.0 Sign in with Google (#1)
- Epic 2: Single-Binary CLI Release (#2)  
- Epic 3: Daily Digest E-mail (#3)
- Epic 4: Snooze / Reminders (#4)
- Epic 5: Dashboard MVP (#5)

### **Tasks (Ready for Development)**
Move these to **Ready**:
- Register Google Cloud project & enable Gmail API (#14)
- Implement OAuth browser flow & token exchange (#15)
- Add token-revocation helper & docs section (#16)
- Smoke-test OAuth flow on personal + Workspace accounts (#17)

## 🔧 **Manual Configuration Steps**

Since the GitHub Projects V2 API has limited mutation capabilities, here are the manual steps to configure the board:

### Step 1: Update Status Field Options
1. Go to https://github.com/users/adrozdenko/projects/2
2. Click on the Status field dropdown
3. Edit field options:
   - Rename "Todo" to "Backlog" (Gray)
   - Add "Ready" option (Yellow) 
   - Keep "In Progress" (Blue)
   - Add "In Review" option (Purple)
   - Keep "Done" (Green)

### Step 2: Add Priority Field
1. Click "+ Add field" button
2. Select "Single select"
3. Name: "Priority"
4. Add options: P0, P1, P2, P3

### Step 3: Add Size Field  
1. Click "+ Add field" button
2. Select "Single select"
3. Name: "Size"
4. Add options: XS, S, M, L, XL

### Step 4: Organize Items
1. Move all Epic issues to "Backlog" column
2. Move specific task issues (#14-17) to "Ready" column
3. Set Priority levels (P0 for OAuth tasks, P1 for binary release, etc.)
4. Set Size estimates for each task

## 🎯 **Board Views**

Create these custom views:

### **1. Kanban Board** (Default)
- Group by: Status
- Sort by: Priority, then Creation date

### **2. Epic Overview**
- Filter: Label = "epic"
- Group by: Priority
- Sort by: Issue number

### **3. Current Sprint**
- Filter: Status = "Ready" OR Status = "In Progress" OR Status = "In Review"
- Group by: Assignee
- Sort by: Priority

### **4. Completed Work**
- Filter: Status = "Done"
- Group by: Milestone
- Sort by: Completion date

## 📈 **Workflow Guidelines**

1. **New Issues**: Always start in "Backlog"
2. **Grooming**: Move to "Ready" when fully defined and prioritized
3. **Development**: Move to "In Progress" when work begins
4. **Review**: Move to "In Review" for code review/testing
5. **Completion**: Move to "Done" when merged and deployed

## 🔄 **Automation Rules** (if available)

- Auto-move to "In Progress" when PR is created
- Auto-move to "In Review" when PR is ready for review
- Auto-move to "Done" when PR is merged
- Auto-assign priority based on labels

## 📋 **Current Status**

- ✅ Project created with basic structure
- ✅ 13 Epic issues created and added
- ✅ 4 detailed task issues for Epic 1 added
- ⏳ Status field options need manual update
- ⏳ Priority and Size fields need to be added
- ⏳ Items need to be organized into appropriate columns

## 🗑️ **Cleanup Task**

After project 2 is fully configured:
- Delete project 1 (https://github.com/users/adrozdenko/projects/1) as it's no longer needed
- Verify all issues are properly organized in project 2
- Test the kanban workflow with a sample task