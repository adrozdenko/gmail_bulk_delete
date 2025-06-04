# Gmail Bulk Delete Tool - Updated Development Timeline & Story Points

## 📊 **Story Point System** (Unchanged)

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

## 🗓️ **Updated Development Timeline** (Starting June 4, 2025)

### **Q2 2025 (Jun-Aug) - Foundation Phase**

#### **Epic 1: OAuth 2.0 "Sign in with Google"** - **21 Points** (6 weeks)
**Start**: June 4, 2025 | **End**: July 15, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| [#14] Register Google Cloud project & enable Gmail API | 2 | 1 day | Jun 4 | Jun 4 |
| [#15] Implement OAuth browser flow & token exchange | 13 | 3 weeks | Jun 5 | Jun 25 |
| [#16] Add token-revocation helper & docs section | 3 | 2 days | Jun 26 | Jun 27 |
| [#17] Smoke-test OAuth flow on accounts | 3 | 2 weeks | Jun 30 | Jul 15* |

*Includes comprehensive testing across different account types and edge cases

#### **Epic 2: Single-Binary CLI Release** - **13 Points** (3 weeks)
**Start**: July 16, 2025 | **End**: August 5, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| [#18] Research PyInstaller vs Nuitka vs Shiv | 3 | 2 days | Jul 16 | Jul 17 |
| [#19] Create CI job (GitHub Actions) to build artifacts | 5 | 1 week | Jul 18 | Jul 25 |
| Publish Homebrew tap & WinGet manifest | 3 | 2 days | Jul 28 | Jul 29 |
| Update README with one-liner install instructions | 2 | 1 day | Jul 30 | Aug 5* |

*Includes extensive testing on multiple platforms and package managers

---

### **Q3 2025 (Sep-Nov) - User Experience Phase**

#### **Epic 5: Dashboard MVP** - **21 Points** (6 weeks)
**Start**: August 6, 2025 | **End**: September 16, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| [#20] Decide TUI (rich) vs Web (Flask + HTMX) | 2 | 1 day | Aug 6 | Aug 6 |
| Build preset trigger / JSON upload interface | 8 | 2 weeks | Aug 7 | Aug 20 |
| Wire up websocket (or polling) for live stats | 8 | 2 weeks | Aug 21 | Sep 3 |
| Ship Dockerfile for self-hosted dashboard | 3 | 2 weeks | Sep 4 | Sep 16* |

*Includes UI/UX testing, responsive design verification, and deployment testing

#### **Epic 3: Daily Digest E-mail** - **13 Points** (3 weeks)
**Start**: September 17, 2025 | **End**: October 7, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Design digest JSON → HTML Jinja template | 3 | 2 days | Sep 17 | Sep 18 |
| Integrate digest send step at run completion | 5 | 1 week | Sep 19 | Sep 26 |
| Unit-test restore link flow | 3 | 2 days | Sep 29 | Sep 30 |
| Add docs & screenshot to README | 2 | 1 week | Oct 1 | Oct 7* |

*Includes email template testing across different clients and restore flow validation

#### **Epic 6: BlackHole / One-Click Unsubscribe** - **13 Points** (3 weeks)
**Start**: October 8, 2025 | **End**: October 28, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Implement --blackhole alias & YAML sender list | 5 | 1 week | Oct 8 | Oct 14 |
| Nightly job: purge messages matching list | 5 | 1 week | Oct 15 | Oct 21 |
| CLI command blackhole add <email\|domain> | 2 | 1 day | Oct 22 | Oct 22 |
| Docs: quick video gif showing workflow | 1 | 1 week | Oct 23 | Oct 28* |

*Includes automation testing and workflow documentation

---

### **Q4 2025 (Nov-Dec) - Advanced Features Phase**

#### **Epic 9: Docker & Headless Mode** - **8 Points** (2 weeks)
**Start**: October 29, 2025 | **End**: November 11, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Write minimal Alpine-based Dockerfile | 3 | 2 days | Oct 29 | Oct 30 |
| Implement looped scheduler entrypoint | 3 | 2 days | Oct 31 | Nov 3 |
| Add Helm chart / docker-compose example | 2 | 1 week | Nov 4 | Nov 11* |

*Includes container security testing and orchestration validation

#### **Epic 4: Snooze / Reminders** - **21 Points** (6 weeks)
**Start**: November 12, 2025 | **End**: December 23, 2025

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Add snooze rule type to JSON schema | 2 | 1 day | Nov 12 | Nov 12 |
| Create Label/Snooze/YYYY-MM-DD labelling logic | 8 | 2 weeks | Nov 13 | Nov 26 |
| Implement scheduler (cron or Cloud Function) | 8 | 2 weeks | Nov 27 | Dec 10 |
| End-to-end test: message returns on time | 3 | 2 weeks | Dec 11 | Dec 23* |

*Includes extensive timing accuracy testing and edge case validation

---

### **Q1 2026 (Jan-Mar) - Storage & Enterprise Phase**

#### **Epic 7: Attachment Off-Load** - **21 Points** (6 weeks)
**Start**: January 6, 2026 | **End**: February 17, 2026

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| List messages ≥ config min_mb & parse attachments | 5 | 1 week | Jan 6 | Jan 10 |
| Integrate Google Drive upload + share-link retrieval | 8 | 2 weeks | Jan 13 | Jan 24 |
| Replace attachment with share-URL note (RFC 822) | 5 | 1 week | Jan 27 | Jan 31 |
| Metrics: show MB freed after run | 3 | 2 weeks | Feb 3 | Feb 17* |

*Includes file integrity testing and Google Drive API integration validation

#### **Epic 8: Pause Inbox / Do-Not-Disturb** - **13 Points** (3 weeks)
**Start**: February 18, 2026 | **End**: March 10, 2026

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Create Pause filter (all incoming → @Paused) | 5 | 1 week | Feb 18 | Feb 24 |
| Add CLI/Web toggle pause / resume | 5 | 1 week | Feb 25 | Mar 3 |
| Verify zero missed e-mails after resume | 3 | 1 week | Mar 4 | Mar 10* |

*Includes comprehensive email flow testing and reliability validation

---

### **Q2 2026 (Apr-Jun) - Polish & Community Phase**

#### **Epic 10: Telemetry (Opt-in)** - **8 Points** (2 weeks)
**Start**: March 11, 2026 | **End**: March 24, 2026

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Define anonymous metrics payload & endpoint | 3 | 2 days | Mar 11 | Mar 12 |
| Add --analytics off CLI flag / config | 2 | 1 day | Mar 13 | Mar 13 |
| Grafana dashboard for live deletion stats | 3 | 1.5 weeks | Mar 16 | Mar 24* |

*Includes privacy compliance testing and dashboard functionality validation

#### **Epic 11: Preset Marketplace** - **13 Points** (3 weeks)
**Start**: March 25, 2026 | **End**: April 14, 2026

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Create GitHub repo folder presets/ & JSON schema | 3 | 2 days | Mar 25 | Mar 26 |
| CLI preset install <name> command | 5 | 1 week | Mar 27 | Apr 2 |
| Community guidelines CONTRIBUTING.md | 5 | 1.5 weeks | Apr 3 | Apr 14* |

*Includes community workflow testing and preset validation systems

#### **Epic 12: UI Dark-Mode Polish** - **5 Points** (1 week)
**Start**: April 15, 2026 | **End**: April 21, 2026

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Add theme variables (Rich style or CSS vars) | 3 | 2 days | Apr 15 | Apr 16 |
| Toggle based on OS prefers-color-scheme | 2 | 3 days | Apr 17 | Apr 21* |

*Includes cross-platform theme testing and accessibility validation

#### **Epic 13: Internationalization (i18n)** - **21 Points** (6 weeks)
**Start**: April 22, 2026 | **End**: June 2, 2026

| Task | Story Points | Duration | Start Date | End Date |
|------|-------------|----------|------------|----------|
| Extract CLI/UI strings to locale JSONs (en,es,fr) | 8 | 2 weeks | Apr 22 | May 5 |
| Add --lang CLI flag and Accept-Language handling | 8 | 2 weeks | May 6 | May 19 |
| Translate docs snippets (README badges) | 5 | 2 weeks | May 20 | Jun 2* |

*Includes translation accuracy testing and locale-specific functionality validation

## 📈 **Updated Timeline Summary**

### **Total Development Time**: 12 months (June 2025 - June 2026)
### **Total Story Points**: 155 points

### **Quarterly Breakdown**:

| Quarter | Epics | Story Points | Key Deliverables |
|---------|-------|-------------|------------------|
| **Q2 2025** | Epic 1, 2 | 34 points | OAuth flow, Binary releases |
| **Q3 2025** | Epic 3, 5, 6 | 47 points | Dashboard, Digest, BlackHole |
| **Q4 2025** | Epic 4, 9 | 29 points | Snooze, Docker |
| **Q1 2026** | Epic 7, 8 | 34 points | Attachments, Pause Inbox |
| **Q2 2026** | Epic 10, 11, 12, 13 | 47 points | Telemetry, Marketplace, UI, i18n |

### **Adjusted Velocity Assumptions**:
- **Team Size**: 1-2 developers
- **Sprint Length**: 2 weeks
- **Velocity**: 10-15 story points per sprint
- **Buffer Time**: 20% added for unforeseen complexity
- **Testing**: Comprehensive testing included in each estimate

### **Critical Path Updated**:
- **Q2 2025**: Foundation establishment (OAuth + Binary)
- **Q3 2025**: User experience enhancement (Dashboard + Features)
- **Q4 2025**: Advanced functionality (Snooze + Docker)
- **Q1 2026**: Enterprise features (Storage + Inbox management)
- **Q2 2026**: Polish and community (UI + i18n + Marketplace)

### **Risk Mitigation (Updated)**:
- **Summer 2025**: Focus on core OAuth implementation during peak productivity
- **Holiday Season**: Lighter workload with Docker and beginning of Snooze
- **Q1 2026**: Complex attachment handling during fresh start of year
- **Q2 2026**: Community features and polish during final quarter

### **Success Metrics (Unchanged)**:
- **OAuth Success Rate**: >95% first-time setup success
- **Binary Install Time**: <30 seconds average
- **Dashboard Response Time**: <500ms for all operations
- **Test Coverage**: >90% for all new features
- **Documentation Quality**: Complete setup guides for all features

This updated timeline provides a realistic roadmap starting from today (June 4, 2025) with proper scheduling and no overdue dates.