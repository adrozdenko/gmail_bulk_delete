# Gmail Bulk Delete Tool - Development Timeline & Story Points

## 📊 **Story Point System**

**Story Points Scale** (Fibonacci sequence):
- **1 Point**: Trivial (< 4 hours) - Simple config changes, documentation updates
- **2 Points**: Small (0.5-1 day) - Minor features, bug fixes
- **3 Points**: Medium (1-2 days) - Standard features with testing
- **5 Points**: Large (3-5 days) - Complex features, API integrations
- **8 Points**: Extra Large (1-2 weeks) - Major features, architectural changes
- **13 Points**: Epic (2-4 weeks) - Large subsystems, complex integrations
- **21 Points**: Mega (1-2 months) - Major platform features

**Time Breakdown Include**:
- Development: 60%
- Testing & QA: 25%
- Documentation: 10%
- Code Review: 5%

## 🗓️ **Development Timeline**

### **Q1 2025 (Jan-Mar) - Foundation Phase**

#### **Epic 1: OAuth 2.0 "Sign in with Google"** - **21 Points** (6 weeks)
**Start**: January 6, 2025 | **End**: February 14, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| [#14] Register Google Cloud project & enable Gmail API | 2 | 1 day | Jan 6 | Jan 6 |
| [#15] Implement OAuth browser flow & token exchange | 13 | 3 weeks | Jan 7 | Jan 27 |
| [#16] Add token-revocation helper & docs section | 3 | 2 days | Jan 28 | Jan 29 |
| [#17] Smoke-test OAuth flow on accounts | 3 | 2 days | Jan 30 | Feb 14* |

*Includes comprehensive testing across different account types and edge cases

#### **Epic 2: Single-Binary CLI Release** - **13 Points** (3 weeks)
**Start**: February 17, 2025 | **End**: March 7, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Research PyInstaller vs Nuitka vs Shiv | 3 | 2 days | Feb 17 | Feb 18 |
| Create CI job (GitHub Actions) to build artifacts | 5 | 1 week | Feb 19 | Feb 25 |
| Publish Homebrew tap & WinGet manifest | 3 | 2 days | Feb 26 | Feb 27 |
| Update README with one-liner install instructions | 2 | 1 day | Feb 28 | Mar 7* |

*Includes extensive testing on multiple platforms and package managers

---

### **Q2 2025 (Apr-Jun) - User Experience Phase**

#### **Epic 5: Dashboard MVP** - **21 Points** (6 weeks)
**Start**: March 10, 2025 | **End**: April 18, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Decide TUI (rich) vs Web (Flask + HTMX) | 2 | 1 day | Mar 10 | Mar 10 |
| Build preset trigger / JSON upload interface | 8 | 2 weeks | Mar 11 | Mar 21 |
| Wire up websocket (or polling) for live stats | 8 | 2 weeks | Mar 24 | Apr 4 |
| Ship Dockerfile for self-hosted dashboard | 3 | 2 days | Apr 7 | Apr 18* |

*Includes UI/UX testing, responsive design verification, and deployment testing

#### **Epic 3: Daily Digest E-mail** - **13 Points** (3 weeks)
**Start**: April 21, 2025 | **End**: May 9, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Design digest JSON → HTML Jinja template | 3 | 2 days | Apr 21 | Apr 22 |
| Integrate digest send step at run completion | 5 | 1 week | Apr 23 | Apr 29 |
| Unit-test restore link flow | 3 | 2 days | Apr 30 | May 1 |
| Add docs & screenshot to README | 2 | 1 day | May 2 | May 9* |

*Includes email template testing across different clients and restore flow validation

#### **Epic 6: BlackHole / One-Click Unsubscribe** - **13 Points** (3 weeks)
**Start**: May 12, 2025 | **End**: May 30, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Implement --blackhole alias & YAML sender list | 5 | 1 week | May 12 | May 16 |
| Nightly job: purge messages matching list | 5 | 1 week | May 19 | May 23 |
| CLI command blackhole add <email\|domain> | 2 | 1 day | May 26 | May 26 |
| Docs: quick video gif showing workflow | 1 | 4 hours | May 27 | May 30* |

*Includes automation testing and workflow documentation

---

### **Q3 2025 (Jul-Sep) - Advanced Features Phase**

#### **Epic 9: Docker & Headless Mode** - **8 Points** (2 weeks)
**Start**: June 2, 2025 | **End**: June 13, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Write minimal Alpine-based Dockerfile | 3 | 2 days | Jun 2 | Jun 3 |
| Implement looped scheduler entrypoint | 3 | 2 days | Jun 4 | Jun 5 |
| Add Helm chart / docker-compose example | 2 | 1 day | Jun 6 | Jun 13* |

*Includes container security testing and orchestration validation

#### **Epic 4: Snooze / Reminders** - **21 Points** (6 weeks)
**Start**: June 16, 2025 | **End**: July 25, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Add snooze rule type to JSON schema | 2 | 1 day | Jun 16 | Jun 16 |
| Create Label/Snooze/YYYY-MM-DD labelling logic | 8 | 2 weeks | Jun 17 | Jun 27 |
| Implement scheduler (cron or Cloud Function) | 8 | 2 weeks | Jun 30 | Jul 11 |
| End-to-end test: message returns on time | 3 | 2 days | Jul 14 | Jul 25* |

*Includes extensive timing accuracy testing and edge case validation

#### **Epic 7: Attachment Off-Load** - **21 Points** (6 weeks)
**Start**: July 28, 2025 | **End**: September 5, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| List messages ≥ config min_mb & parse attachments | 5 | 1 week | Jul 28 | Aug 1 |
| Integrate Google Drive upload + share-link retrieval | 8 | 2 weeks | Aug 4 | Aug 15 |
| Replace attachment with share-URL note (RFC 822) | 5 | 1 week | Aug 18 | Aug 22 |
| Metrics: show MB freed after run | 3 | 2 days | Aug 25 | Sep 5* |

*Includes file integrity testing and Google Drive API integration validation

---

### **Q4 2025 (Oct-Dec) - Polish & Extensions Phase**

#### **Epic 8: Pause Inbox / Do-Not-Disturb** - **13 Points** (3 weeks)
**Start**: September 8, 2025 | **End**: September 26, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Create Pause filter (all incoming → @Paused) | 5 | 1 week | Sep 8 | Sep 12 |
| Add CLI/Web toggle pause / resume | 5 | 1 week | Sep 15 | Sep 19 |
| Verify zero missed e-mails after resume | 3 | 2 days | Sep 22 | Sep 26* |

*Includes comprehensive email flow testing and reliability validation

#### **Epic 10: Telemetry (Opt-in)** - **8 Points** (2 weeks)
**Start**: September 29, 2025 | **End**: October 10, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Define anonymous metrics payload & endpoint | 3 | 2 days | Sep 29 | Sep 30 |
| Add --analytics off CLI flag / config | 2 | 1 day | Oct 1 | Oct 1 |
| Grafana dashboard for live deletion stats | 3 | 2 days | Oct 2 | Oct 10* |

*Includes privacy compliance testing and dashboard functionality validation

#### **Epic 11: Preset Marketplace** - **13 Points** (3 weeks)
**Start**: October 13, 2025 | **End**: October 31, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Create GitHub repo folder presets/ & JSON schema | 3 | 2 days | Oct 13 | Oct 14 |
| CLI preset install <name> command | 5 | 1 week | Oct 15 | Oct 21 |
| Community guidelines CONTRIBUTING.md | 5 | 1 week | Oct 22 | Oct 31* |

*Includes community workflow testing and preset validation systems

---

### **Q1 2026 (Jan-Mar) - Internationalization & Final Polish**

#### **Epic 12: UI Dark-Mode Polish** - **5 Points** (1 week)
**Start**: November 3, 2025 | **End**: November 7, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Add theme variables (Rich style or CSS vars) | 3 | 2 days | Nov 3 | Nov 4 |
| Toggle based on OS prefers-color-scheme | 2 | 1 day | Nov 5 | Nov 7* |

*Includes cross-platform theme testing and accessibility validation

#### **Epic 13: Internationalization (i18n)** - **21 Points** (6 weeks)
**Start**: November 10, 2025 | **End**: December 19, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Extract CLI/UI strings to locale JSONs (en,es,fr) | 8 | 2 weeks | Nov 10 | Nov 21 |
| Add --lang CLI flag and Accept-Language handling | 8 | 2 weeks | Nov 24 | Dec 5 |
| Translate docs snippets (README badges) | 5 | 1 week | Dec 8 | Dec 19* |

*Includes translation accuracy testing and locale-specific functionality validation

## 📈 **Timeline Summary**

### **Total Development Time**: 12 months (Jan 2025 - Dec 2025)
### **Total Story Points**: 155 points

### **Quarterly Breakdown**:

| Quarter | Epics | Story Points | Key Deliverables |
|---------|-------|-------------|------------------|
| **Q1 2025** | Epic 1, 2 | 34 points | OAuth flow, Binary releases |
| **Q2 2025** | Epic 3, 5, 6 | 47 points | Dashboard, Digest, BlackHole |
| **Q3 2025** | Epic 4, 7, 9 | 50 points | Snooze, Attachments, Docker |
| **Q4 2025** | Epic 8, 10, 11, 12 | 39 points | Pause, Telemetry, Marketplace, UI |
| **Q1 2026** | Epic 13 | 21 points | Internationalization |

### **Velocity Assumptions**:
- **Team Size**: 1-2 developers
- **Sprint Length**: 2 weeks
- **Velocity**: 10-15 story points per sprint
- **Buffer Time**: 20% added for unforeseen complexity
- **Testing**: Comprehensive testing included in each estimate

### **Risk Mitigation**:
- **Google API Changes**: 2-week buffer in OAuth epic
- **Package Manager Approval**: Extended timeline for binary releases
- **Third-party Dependencies**: Conservative estimates for integrations
- **User Feedback**: Iterative development with feedback loops

### **Success Metrics**:
- **OAuth Success Rate**: >95% first-time setup success
- **Binary Install Time**: <30 seconds average
- **Dashboard Response Time**: <500ms for all operations
- **Test Coverage**: >90% for all new features
- **Documentation Quality**: Complete setup guides for all features

This timeline provides a realistic roadmap while maintaining optimistic development pace with proper testing and quality assurance built into each epic.