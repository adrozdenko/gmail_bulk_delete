# Gmail Bulk Delete Tool – Development Roadmap

This document outlines the development roadmap for the Gmail Bulk Delete tool, organized into epics and tracked via GitHub Projects.

## 📊 **Project Board**

**GitHub Project**: [Gmail Bulk Delete - Development Roadmap](https://github.com/users/adrozdenko/projects/2)

All development tasks are organized in a kanban board with the following columns:
- **Backlog**: New issues start here
- **To Do**: Ready for development  
- **In Progress**: Currently being worked on
- **Done**: Completed tasks

## 🎯 **Development Epics**

### **Epic 1: OAuth 2.0 "Sign in with Google"** [#1](https://github.com/adrozdenko/gmail_bulk_delete/issues/1)
**Goal**: Eliminate manual JSON credential setup and implement secure OAuth flow

**Tasks**:
- [#14](https://github.com/adrozdenko/gmail_bulk_delete/issues/14) Register Google Cloud project & enable Gmail API
- [#15](https://github.com/adrozdenko/gmail_bulk_delete/issues/15) Implement OAuth browser flow & token exchange  
- [#16](https://github.com/adrozdenko/gmail_bulk_delete/issues/16) Add token-revocation helper & docs section
- [#17](https://github.com/adrozdenko/gmail_bulk_delete/issues/17) Smoke-test OAuth flow on personal + Workspace accounts

**Success Criteria**: Connect Gmail in < 60s, no JSON manual steps

---

### **Epic 2: Single-Binary CLI Release** [#2](https://github.com/adrozdenko/gmail_bulk_delete/issues/2)
**Goal**: Create standalone binary releases for all platforms

**Key Features**:
- Cross-platform binaries (macOS/Linux/Windows)
- Automated CI/CD release pipeline
- Package manager distribution (Homebrew, WinGet)
- One-liner installation

---

### **Epic 3: Daily Digest E-mail** [#3](https://github.com/adrozdenko/gmail_bulk_delete/issues/3)
**Goal**: Provide deletion summary reports with restore functionality

**Key Features**:
- HTML digest templates
- Restore links for deleted emails
- Configurable digest delivery
- Summary statistics

---

### **Epic 4: Snooze / Reminders** [#4](https://github.com/adrozdenko/gmail_bulk_delete/issues/4)
**Goal**: Implement email snooze functionality

**Key Features**:
- Snooze rule type in JSON schema
- Date-based labeling system
- Scheduled email return
- Accurate timing guarantees

---

### **Epic 5: Dashboard MVP** [#5](https://github.com/adrozdenko/gmail_bulk_delete/issues/5)
**Goal**: Create interactive user interface

**Key Features**:
- Web or TUI interface options
- Real-time statistics
- Preset triggers
- Self-hosted deployment

---

### **Epic 6: BlackHole / One-Click Unsubscribe** [#6](https://github.com/adrozdenko/gmail_bulk_delete/issues/6)
**Goal**: Automated email blocking and cleanup

**Key Features**:
- Sender blacklist management
- Automated nightly cleanup
- CLI commands for blackhole management
- Visual workflow documentation

---

### **Epic 7: Attachment Off-Load** [#7](https://github.com/adrozdenko/gmail_bulk_delete/issues/7)
**Goal**: Cloud storage integration for large attachments

**Key Features**:
- Google Drive integration
- Attachment replacement with share links
- Storage savings metrics
- RFC 822 email editing

---

### **Epic 8: Pause Inbox / Do-Not-Disturb** [#8](https://github.com/adrozdenko/gmail_bulk_delete/issues/8)
**Goal**: Inbox pause/resume functionality

**Key Features**:
- Inbox pause filters
- Zero email loss guarantee
- Simple toggle interface
- Reliable state management

---

### **Epic 9: Docker & Headless Mode** [#9](https://github.com/adrozdenko/gmail_bulk_delete/issues/9)
**Goal**: Containerization and automation support

**Key Features**:
- Minimal Alpine Docker container
- Scheduled operation support
- Helm charts and docker-compose
- Headless automation

---

### **Epic 10: Telemetry (Opt-in)** [#10](https://github.com/adrozdenko/gmail_bulk_delete/issues/10)
**Goal**: Usage analytics with privacy respect

**Key Features**:
- Anonymous metrics collection
- Opt-out capability
- Grafana analytics dashboard
- Privacy-first approach

---

### **Epic 11: Preset Marketplace** [#11](https://github.com/adrozdenko/gmail_bulk_delete/issues/11)
**Goal**: Community preset sharing platform

**Key Features**:
- GitHub-based preset repository
- CLI preset installation
- Community contribution guidelines
- Standardized preset format

---

### **Epic 12: UI Dark-Mode Polish** [#12](https://github.com/adrozdenko/gmail_bulk_delete/issues/12)
**Goal**: Enhanced UI theming

**Key Features**:
- Dark mode support
- OS theme detection
- Consistent theme variables
- Enhanced visual experience

---

### **Epic 13: Internationalization (i18n)** [#13](https://github.com/adrozdenko/gmail_bulk_delete/issues/13)
**Goal**: Multi-language support

**Key Features**:
- Support for English, Spanish, French
- CLI language flags
- Translated documentation
- Locale-based string extraction

## 🏷️ **Labels Used**

- `epic`: Large feature collections spanning multiple tasks
- `task`: Individual development tasks within epics  
- `roadmap`: Development roadmap items
- `enhancement`: Feature improvements
- `bug`: Bug fixes and issues
- `documentation`: Documentation updates

## 📈 **Priority Guidelines**

**High Priority Epics** (Next 3-6 months):
1. **Epic 1**: OAuth 2.0 (eliminates setup friction)
2. **Epic 2**: Binary releases (improves distribution)
3. **Epic 5**: Dashboard MVP (enhances user experience)

**Medium Priority Epics** (6-12 months):
4. **Epic 3**: Daily digest
5. **Epic 6**: BlackHole functionality  
6. **Epic 9**: Docker support

**Future Epics** (12+ months):
7. **Epic 4**: Snooze/reminders
8. **Epic 7**: Attachment off-load
9. **Epic 8**: Pause inbox
10. **Epic 10**: Telemetry
11. **Epic 11**: Preset marketplace
12. **Epic 12**: Dark mode
13. **Epic 13**: Internationalization

## 🔄 **Development Workflow**

1. **Issues start in Backlog** column
2. **Move to To Do** when ready for development
3. **Move to In Progress** when actively working
4. **Move to Done** when completed and tested
5. **Link related issues** to their parent epic
6. **Update issue descriptions** with progress notes

## 📋 **Contributing**

To contribute to the roadmap:
1. Check the [project board](https://github.com/users/adrozdenko/projects/2) for current status
2. Look for issues labeled `good first issue` or `help wanted`
3. Comment on issues to discuss approach before starting
4. Reference issue numbers in pull requests
5. Update project board status when working on issues

## 📊 **Current Status**

- **Total Epics**: 13
- **Total Tasks Defined**: 17+ (expanding as epics are broken down)
- **Current Focus**: Epic 1 (OAuth 2.0 implementation)
- **Project Board**: Active and maintained

This roadmap represents the evolution from a high-performance deletion tool to a comprehensive Gmail management platform with enterprise-grade features and user experience.