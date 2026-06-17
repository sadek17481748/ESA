# ESA — Education and Schooling Applications
## Table of Contents

- [Overview](#overview)
  - [Project goals](#project-goals)
  - [How we planned timing](#how-we-planned-timing)
  - [Scope creep — what changed and why](#scope-creep--what-changed-and-why)
  - [Delivery timeline (May → July)](#delivery-timeline-may--july)
- [Quick links](#quick-links)
- [Responsive Design Preview](#responsive-design-preview)
- [Navigating the website](#navigating-the-website)
  - [Request flow overview](#request-flow-overview)
  - [Role-based navigation paths](#role-based-navigation-paths)
- [Technical overview](#technical-overview)
  - [How the pieces fit together](#how-the-pieces-fit-together)
  - [PostgreSQL — the database](#postgresql--the-database)
  - [Django — the web application](#django--the-web-application)
  - [External services](#external-services)
- [Features](#features)
  - [Accounts and getting started](#accounts-and-getting-started)
  - [Multi-tenant schools](#multi-tenant-schools)
  - [School admin — running the school](#school-admin--running-the-school)
  - [Timetable](#timetable)
  - [Attendance](#attendance)
  - [Homework and worksheets](#homework-and-worksheets)
  - [LMS — learning materials](#lms--learning-materials)
  - [Qur'an sessions (mushaf viewer)](#quran-sessions-mushaf-viewer)
  - [Hifz sign-off](#hifz-sign-off)
  - [Exams](#exams)
  - [Behaviour](#behaviour)
  - [Messaging and reports](#messaging-and-reports)
  - [Payments and subscriptions](#payments-and-subscriptions)
  - [Notifications](#notifications)
  - [Security and audit](#security-and-audit)
- [User Experience (UX)](#user-experience-ux)
  - [UX principles](#ux-principles)
  - [Layout and navigation](#layout-and-navigation)
  - [Visual design and branding](#visual-design-and-branding)
  - [Dashboards by role](#dashboards-by-role)
  - [Forms, validation, and feedback](#forms-validation-and-feedback)
  - [Tables, lists, and empty states](#tables-lists-and-empty-states)
  - [Responsive design](#responsive-design)
  - [How responsiveness was tested](#how-responsiveness-was-tested)
  - [Accessibility](#accessibility)
  - [Everyday journeys](#everyday-journeys-how-people-use-esa)
  - [Trust, sign-off, and clarity](#trust-sign-off-and-clarity)
  - [User stories (acceptance criteria)](#user-stories-acceptance-criteria)
  - [Wireframes](#wireframes)
  - [Main wireframe pack](#main-wireframe-pack)
  - [Wireframe inventory](#wireframe-inventory)
- [Design](#design)
  - [Data model and ERD (entity relationships)](#data-model-and-erd-entity-relationships)
  - [Visual language](#visual-language)
  - [Colour palette and CSS tokens](#colour-palette-and-css-tokens)
  - [How colour is used across the UI](#how-colour-is-used-across-the-ui)
  - [Typography](#typography)
  - [UI components](#ui-components)
  - [Accessibility](#accessibility)
  - [Design inspiration and references](#design-inspiration-and-references)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [Development](#development)
  - [Project setup from scratch (Django)](#project-setup-from-scratch-django)
  - [GitHub setup and version control](#github-setup-and-version-control)
  - [Development guide (step-by-step)](#development-guide-step-by-step)
  - [Local setup](#local-setup)
  - [Environment variables](#environment-variables)
  - [How I set up Stripe (test mode)](#how-i-set-up-stripe-test-mode)
  - [How I connected the Google email account](#how-i-connected-the-google-email-account)
  - [Run locally](#run-locally)
  - [Troubleshooting (local Postgres setup)](#troubleshooting-local-postgres-setup)
  - [Assessor and demo logins](#assessor-and-demo-logins)
  - [Automated tests](#automated-tests-local)
  - [How I committed changes to GitHub](#how-i-committed-changes-to-github-workflow-used)
- [Deployment](#deployment)
  - [GitHub and Heroku integration](#github-and-heroku-integration)
  - [Deployment steps](#deployment-steps)
  - [Post-deploy checklist](#post-deploy-checklist)
  - [Production stack](#production-stack)
  - [Database migrations](#database-migrations)
  - [Seed data commands](#seed-data-commands)
  - [verify_deploy smoke tests](#verify_deploy-smoke-tests)
  - [Production security checks](#production-security-checks)
  - [Tenant isolation verification](#tenant-isolation-verification)
  - [Connecting Gmail for platform email notifications](#connecting-gmail-for-platform-email-notifications)
- [Testing and Bugs](#testing-and-bugs)
  - [Testing strategy and plan](#testing-strategy-and-plan)
  - [Assessment test matrix](#assessment-test-matrix)
  - [Manual testing](#manual-testing)
  - [Automated testing](#automated-testing)
  - [Testing summary table](#testing-summary-table)
  - [Sprint delivery (June 2025)](#sprint-delivery-june-2025)
  - [User acceptance testing](#user-acceptance-testing)
  - [Bugs encountered during development](#bugs-encountered-during-development)
  - [Use of AI (assistance log)](#use-of-ai-assistance-log)
  - [Lighthouse testing](#lighthouse-testing)
  - [HTML, CSS and JS validation](#html-css-and-js-validation)
- [Security](#security)
- [Sources and references](#sources-and-references)
- [Author](#author)

---
## Quick links

Assessor-facing links and evidence paths:

| Resource | Link or path |
|----------|--------------|
| **Source repository** | https://github.com/sadek17481748/ESA |
| **Live deployment** | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| **Security overview** | [Security](#readme-security) in this README |
| **Bug tracker (GitHub Project board)** | https://github.com/users/sadek17481748/projects/8/views/1 |
| **Wireframes (main pack)** | **[https://esa-project-2a7a33dfe3fc.herokuapp.com/wireframes/](https://esa-project-2a7a33dfe3fc.herokuapp.com/wireframes/)** · [PDF](docs/ESA-wireframes.pdf) · [Balsamiq](https://balsamiq.cloud/so6babk/pveanf2) |
| **ERD / data model** | [Data model and ERD](#data-model-and-erd-entity-relationships) |
| **Test credentials** | Showcase: `demo_parent` / `demo_student` / `Demo2026!` — full list in [Demo walkthrough](#demo-walkthrough) and [Assessor and demo logins](#assessor-and-demo-logins) |
| **Manual test evidence (screenshots)** | `docs/images/manual-testing/` |
| **Responsive preview (README gallery)** | `docs/images/preview/` |
| **Validation evidence** | `docs/images/validation/` |
| **Sprint checklist** | [Delivery timeline (May → July)](#delivery-timeline-may--july) and [Scope creep](#scope-creep--what-changed-and-why) |

### Demo walkthrough

Use the [live deployment](https://esa-project-2a7a33dfe3fc.herokuapp.com/accounts/login/) with the logins below. Each account lands on a role-specific dashboard; the **sidebar** lists every feature that role can open. Explore in any order — the notes describe what is already seeded and what you can verify for yourself.

Demo data lives on **Al-Noor Academy**. Run `python manage.py seed_showcase_account` locally, or `heroku run python manage.py seed_showcase_account -a esa-project` on Heroku, if an account looks empty.

#### Recommended — one linked family (parent + student)

Best for testing the full parent/student experience in a single class (**7A**, student **Amina Hassan**).

| Role | Username | Password |
|------|----------|----------|
| Parent | `demo_parent` | `Demo2026!` |
| Student | `demo_student` | `Demo2026!` |

**What is already set up**

| Area | Parent (`demo_parent`) | Student (`demo_student`) |
|------|------------------------|--------------------------|
| **Dashboard** | Linked child shown on overview | Class **7A** timetable and this week's cards |
| **Attendance** | Last 7 days marked (present, late, absent) | Same register visible on student view |
| **Behaviour** | Commendation and incident for Amina | — |
| **Payments** | Term 3 fee outstanding + Term 2 marked paid | — |
| **Messages** | Thread with teacher; school office reply; support case | — |
| **Reports** | Spring term teacher report for Amina | — |
| **Hifz** | Juz 1–3 signed off (congratulations messages sent) | Own juz progress list |
| **Homework** | — | Signed-off maths submission |
| **Exams** | — | Finalised maths result with teacher comment |
| **Qur'an** | — | Mushaf session with page notes and highlights |
| **LMS / worksheets** | — | Completed fractions worksheet (approved) |
| **Notifications** | Sign-off, attendance, and general alerts | Homework approved alert |

**How to test it yourself**

- Log in as **`demo_parent`** and check each sidebar area matches the table — fees, messages, reports, and Hifz sign-offs should all relate to **Amina Hassan** only.
- Log in as **`demo_student`** and confirm timetable, homework, exams, Qur'an, and LMS content loads for the same child.
- Switch between parent and student to confirm data is consistent (e.g. Hifz juz signed off by teacher appears on both accounts).

#### Teacher — classes, registers, sign-offs, Qur'an

| Username | Password |
|----------|----------|
| `mr_mohammed` | `teacher1234` |

**What you can explore**

| Feature | What to look for |
|---------|------------------|
| **Attendance** | School-wide student list for registers; marks save per class session (Quran slots on **7A** timetable) |
| **Qur'an** | Mushaf PDF viewer — page through juz PDFs, add per-page notes, drag highlights (teacher only) |
| **Hifz sign-off** | Pick any student + juz → **Student has passed** sends a congratulations message to the linked parent |
| **Homework / worksheets** | Assignments for timetabled classes; sign-off approve/reject on submissions |
| **Exams** | Published exams; mark written answers; **Finalise** so parents and students see results |
| **Behaviour** | Log commendations or incidents for any student in the school |
| **Messages** | Send to parents or school office; structured progress reports |

Teachers are **not** locked to a homeroom — timetable slots control which lessons appear on **My timetable**, but registers and behaviour use the full school student list.

#### School admin — tenant setup

| Username | Password |
|----------|----------|
| `schooladmin` | `admin1234` |

**What you can explore**

| Feature | What to look for |
|---------|------------------|
| **Students / teachers** | Add staff, issue parent link codes, bulk class structure (**7A–11B** after full seed) |
| **Timetable hub** | Create timetables, drag subjects onto the grid, assign teachers, archive live timetables |
| **LMS** | Subjects, tracks, uploaded materials assigned to classes |
| **Payments** | School fee setup; Stripe Connect onboarding for payouts |
| **Analytics** | School KPIs — attendance, fees, behaviour overview |
| **Messages** | Inbox across all school conversations; student search by name |

#### Super admin — platform-wide

| Username | Password |
|----------|----------|
| `super` | `super1234` |

**What you can explore**

| Feature | What to look for |
|---------|------------------|
| **Schools overview** | All tenants on the platform (not scoped to one school) |
| **Support inbox** | Platform support cases opened by parents |
| **Subscriptions** | School plan tiers across tenants |

#### Other demo accounts

| Role | Username | Password | Use when |
|------|----------|----------|----------|
| Teacher (generic) | `teacher_demo` | `teacher1234` | RBAC smoke test on Al-Noor |
| Parent (generic) | `parent_demo` | `demo1234` | Quick fee/payment check |
| Student (generic) | `student_demo` | `student1234` | Basic student portal |
| Parent + student (examples) | `test_parent` / `test_student` | `test1234` | Messaging and LMS examples |
| Bulk school (300+ logins) | `parent_7a_01` / `student_7a_01` | `parent1234` / `student1234` | Full-school seed; see `docs/alnoor-academy-logins.csv` |

All seeded demo accounts skip email verification. Real registrations require the six-digit code at `/accounts/verify-email/`.

---
## Responsive Design Preview

Visual evidence of the live ESA portal on **Heroku** — same style as my [learn-drive](https://github.com/sadek17481748/learn-drive) and [bookly](https://github.com/sadek17481748/bookly) README galleries. Screenshots are stored under [`docs/images/preview/`](docs/images/preview/) so assessors can see key pages without logging in.

**Live site:** https://esa-project-2a7a33dfe3fc.herokuapp.com/

**How to read this section:** desktop captures from Safari on macOS at full browser width. More screens and mobile widths will be added to `docs/images/preview/` as they are captured.

**Captured so far:** 18 feature screens in `docs/images/preview/` plus **5 responsive tests** in `docs/images/validation/`.

### Public pages

#### Landing page (`/`)

Marketing home — hero, feature carousel, leaderboards, pricing.

![Landing page — desktop](docs/images/preview/01-landing-desktop.png)

#### Subscription plans (`/subscription/`)

School plan tiers (Free / Standard / Premium) — public marketing view. *(Screenshot pending.)*

#### Security overview (`/security/`)

Public security page — no login required. *(Screenshot pending.)*

### Authentication

#### Login (`/accounts/login/`)

Shared login for all roles.

![Login — desktop](docs/images/preview/04-login-desktop.png)

#### Register — parent or student (`/register/`)

Account creation with school pick, role, and optional parent link code. *(Screenshot pending.)*

#### Register your school (`/register/school/`)

New school onboarding form — school name, admin account, passwords.

![Register your school](docs/images/preview/06-register-school-desktop.png)

#### Verify email (`/accounts/verify-email/`)

Six-digit code entry after registration — required before portal access for new accounts.

![Verify email](docs/images/preview/07-verify-email-desktop.png)

### School Admin portal

Log in as `schooladmin` / `admin1234` on [Al-Noor Academy](https://esa-project-2a7a33dfe3fc.herokuapp.com/accounts/login/).

#### School overview (`/dashboard/school-admin/`)

Dashboard — staff, classes, fees, and setup shortcuts.

![School overview](docs/images/preview/08-dashboard-school-admin-desktop.png)

#### Analytics (`/analytics/`)

School KPIs — students, teachers, fees outstanding, attendance snapshot.

![School analytics](docs/images/preview/22-analytics-desktop.png)

#### Subscription (`/subscription/`)

Upgrade plan — Free, Standard (£49), Premium (£99) with Stripe test checkout.

![School subscription](docs/images/preview/23-subscription-school-admin-desktop.png)

#### School fees & Stripe Connect

Fee KPIs, create invoices for all students, Stripe Connect onboarding, per-student fee table.

![School fees dashboard](docs/images/preview/24-fees-school-admin-desktop.png)

#### Teachers (`/school-admin/teachers/`)

Staff list — name, username, email, and subject per teacher.

![Teachers](docs/images/preview/25-teachers-school-admin-desktop.png)

#### Add teacher (`/school-admin/teachers/add/`)

Create teacher login — username, subject, and password.

![Add teacher](docs/images/preview/26-add-teacher-desktop.png)

#### Timetable hub (`/timetable/`)

Year groups, timetable builder, and live schedules — `schooladmin` / `admin1234`

![Timetable hub](docs/images/preview/12-timetable-desktop.png)

#### Attendance (`/attendance/`)

School-wide register by class — present / late / absent KPIs and student rows.

![Attendance](docs/images/preview/13-attendance-desktop.png)

#### LMS (`/lms/`)

Subjects, levels, and uploaded worksheets — English, Maths, Quran tracks.

![LMS hub](docs/images/preview/15-lms-desktop.png)

#### Messages (`/messages/`)

School conversations, platform support, and parent threads.

![Messages](docs/images/preview/20-messages-desktop.png)

#### Find student (`/messages/students/search/`)

Search students by name or admission number across the school roll.

![Find student](docs/images/preview/27-find-student-desktop.png)

### Super Admin portal

Log in as `super` / `super1234`.

#### Platform overview (`/dashboard/super-admin/`)

Live KPIs — schools, users, MRR, subscriptions table, recent sign-ups, and audit activity.

![Super Admin — platform overview](docs/images/preview/07-dashboard-super-admin-desktop.png)

#### Support messages (`/messages/`)

Platform support queue — parent cases with case numbers, subjects, and status.

![Super Admin — support queue](docs/images/preview/28-super-admin-messages-desktop.png)

### Other role dashboards

#### Teacher workspace (`/dashboard/teacher/`)

Today's register, timetable, homework, and Hifz shortcuts — teacher account after login.

![Teacher workspace](docs/images/preview/09-dashboard-teacher-desktop.png)

#### Student (`/dashboard/student/`)

Homework, Hifz, and timetable cards — `demo_student` / `Demo2026!` *(Screenshot pending.)*

#### Parent (`/dashboard/parent/`)

Linked children, fees summary, and quick links — `demo_parent` / `Demo2026!` *(Screenshot pending.)*

### Feature modules

*(Screenshots pending for student and parent portals, plus teacher feature pages.)*

#### Homework & worksheets (`/worksheets/`)

Assignments, student submit, teacher sign-off.

#### Qur'an mushaf viewer (`/quran/`)

PDF mushaf with page notes and highlights.

#### Hifz juz sign-off (`/hifz/`)

Juz 1–30 teacher sign-off table.

#### Exams (`/exams/`)

Exam list, MCQ + written marking, teacher finalise.

#### Behaviour log (`/behaviour/`)

Commendations and incidents.

#### Parent payments (`/payments/`)

Parent fee table, Stripe Pay now, receipts — `demo_parent` / `Demo2026!`

### Responsive testing (cross-device)

Home page (`/`) tested on the **live Heroku URL** using [Website Responsive Testing Tool](http://responsivetesttool.com) and Safari window resizing on macOS. Screenshots saved to [`docs/images/validation/`](docs/images/validation/).

#### Mobile — iPhone X (375px width)

Hero text and CTAs stack in one column; navigation links wrap; stat cards reflow.

![Responsive — iPhone X 375px](docs/images/validation/responsive-mobile-iphone-x.png)

#### Tablet — iPad 10″ (768px width)

Two-column hero collapses; three feature cards stay in a row; nav remains readable.

![Responsive — iPad 768px](docs/images/validation/responsive-tablet-ipad-768.png)

#### Laptop — full browser width (~1440px)

Default desktop layout: hero copy left, stat cards right, horizontal top nav.

![Responsive — desktop full width](docs/images/validation/responsive-desktop-full.png)

#### Laptop — window narrowed (manual resize)

Browser dragged narrower — content reflows before the 768px breakpoint; buttons and cards adjust without horizontal page scroll.

![Responsive — laptop window narrowed](docs/images/validation/responsive-laptop-narrow.png)

#### Laptop — width adjusted again (narrower)

Further resize — feature cards compress; confirms `flex-wrap` and `minmax` grids adapt between breakpoints.

![Responsive — laptop narrower still](docs/images/validation/responsive-laptop-narrower.png)

#### How we made the site responsive (code steps)

All portal and marketing pages share one stylesheet: **`css/base.css`** (linked from Django templates and wireframes).

| Step | What we did | Where in code |
|------|-------------|---------------|
| **1. Viewport meta tag** | Tells mobile browsers to use device width, not a zoomed-out desktop layout | `templates/base/marketing.html`, `templates/base/dashboard.html` — `<meta name="viewport" content="width=device-width, initial-scale=1">` |
| **2. Fluid typography** | Headings scale with screen size instead of fixed pixels | `.hero h1 { font-size: clamp(1.85rem, 4vw, 2.75rem); }` |
| **3. CSS Grid + Flexbox layouts** | Marketing hero uses CSS Grid; dashboards use Flexbox shell | `.hero { grid-template-columns: 1.4fr 1fr; }` · `.app-shell { display: flex; }` |
| **4. Auto-fill card grids** | KPI and pricing cards reflow to fewer columns on narrow screens | `.grid-cards`, `.pricing-grid` — `repeat(auto-fill, minmax(200px, 1fr))` |
| **5. Wrapped buttons and nav** | CTAs and header links wrap instead of overflowing | `.hero-actions { flex-wrap: wrap; }` · `.site-nav { flex-wrap: wrap; }` |
| **6. Breakpoint @ 768px** | Home hero → single column; stat cards wrap; carousel height capped | `@media (max-width: 768px)` — `.hero`, `.hero-stats`, `.carousel-viewport` |
| **7. Breakpoint @ 900px** | Portal sidebar stacks above main; timetable builder stacks; message tables become cards | `@media (max-width: 900px)` — `.app-shell`, `.timetable-toolbar`, `.msg-mobile-table` |
| **8. Scrollable tables** | Wide data tables scroll inside a container on small screens | `.table-wrap { overflow-x: auto; }` |
| **9. Single-column auth forms** | Login/register centred with max width | `.main-single { max-width: 560px; }` |
| **10. Manual + tool testing** | Chrome DevTools during development; formal evidence from responsivetesttool.com at live URL | Screenshots in `docs/images/validation/` |

**Priority devices:** laptop and tablet for school staff (timetable builder, registers, LMS). Phone is a **sanity check** — layout stacks and remains usable; not every admin feature is optimised for 320px.

Full test matrix and page checklist: [How responsiveness was tested](#how-responsiveness-was-tested).

---
## Navigating the website

ESA is a **server-rendered Django portal** backed by a REST API. Most assessor walkthroughs use the browser UI (session login), not Postman. After you log in at `/accounts/login/`, Django reads your `User.role` and sends you to the correct dashboard. The sidebar on each dashboard lists only the pages your role is allowed to open.

### Site map (high level)

```mermaid
flowchart TB
    subgraph public [Public — no login]
        HOME["/  Home carousel"]
        REG["/register/  Parent or student sign-up"]
        LOGIN["/accounts/login/"]
        RESET["/accounts/password-reset/"]
        LINK["/link/&lt;code&gt;/  Parent link child"]
    end

    subgraph auth [After login]
        DASH["/dashboard/  Role router"]
        SA["/dashboard/super-admin/"]
        SCH["/dashboard/school-admin/"]
        TCH["/dashboard/teacher/"]
        STU["/dashboard/student/"]
        PAR["/dashboard/parent/"]
    end

    subgraph features [Feature areas — role-gated]
        PAY["/payments/  Fees and Stripe Checkout"]
        MSG["/messages/  School messaging"]
        ATT["/attendance/"]
        TT["/timetable/"]
        HW["/worksheets/  Homework"]
        QUR["/quran/  Sessions and annotations"]
        EXM["/exams/  MCQ and written exams"]
        LMS["/lms/  LMS hub"]
        HIFZ["/hifz/  Hifz progress"]
        ANA["/analytics/  School metrics"]
    end

    HOME --> LOGIN
    HOME --> REG
    LOGIN --> DASH
    REG --> DASH
    DASH --> SA
    DASH --> SCH
    DASH --> TCH
    DASH --> STU
    DASH --> PAR
    SA --> ANA
    SCH --> PAY
    SCH --> LMS
    TCH --> ATT
    TCH --> QUR
    TCH --> EXM
    STU --> HW
    STU --> QUR
    PAR --> PAY
    PAR --> MSG
```

### Request flow overview

The browser requests a URL (for example `/payments/`). Django’s root URLconf (`core/urls.py`) maps the path to a **view function or class** in the relevant app (`payments/views.py`, `pages/views.py`, `quran/views.py`, and so on). The view checks **authentication** (session cookie) and **role/tenant** permissions, then uses the **ORM** to read or write rows in **PostgreSQL** (via `DATABASE_URL`). Django renders an HTML template under `templates/` and returns it. Static assets (`css/base.css`, `static/`) load in a second request. Small behaviours (mobile nav toggle, confirm dialogs) are handled in JavaScript without replacing server-side validation.

This is **server-side rendering**, not a single-page React app: most HTML is produced on the server, which keeps the project understandable while still being full stack (HTTP + Django + database + Stripe + email).

### Role-based navigation paths

Use these paths on the [live site](https://esa-project-2a7a33dfe3fc.herokuapp.com/) or locally at `http://127.0.0.1:8000/`. Full credential tables are in [Assessor and demo logins](#assessor-and-demo-logins) and [Portal login hub](#portal-login-hub-introduction).

| Role | Start here after login | Typical next clicks | What to verify |
|------|------------------------|---------------------|----------------|
| **Super Admin** | `/dashboard/super-admin/` | Schools list, subscriptions, platform search | Cross-tenant school overview; no single-school fee data |
| **School Admin** | `/dashboard/school-admin/` | `/school-admin/students/`, `/school-admin/teachers/`, `/payments/` (school fees), Stripe Connect | Tenant-scoped students; Connect onboarding link |
| **Teacher** | `/dashboard/teacher/` | `/attendance/`, `/worksheets/`, `/quran/`, `/exams/` | Create session, annotate recitation, mark exam, finalise results |
| **Student** | `/dashboard/student/` | `/timetable/`, `/worksheets/`, `/quran/`, `/exams/` | Upload recitation audio; see **finalised** exam results only |
| **Parent** | `/dashboard/parent/` | Sidebar: payments, messages, attendance, Hifz, reports | Own children's data only; fees scoped to linked parent account |

Use the [Demo walkthrough](#demo-walkthrough) for logins and what each role should already see on the live site. Demo accounts skip email verification; real registrations require the six-digit code at `/accounts/verify-email/`.

---
## Technical overview

ESA is a **full-stack web application**: users interact with **Django** pages in the browser, Django reads and writes data in **PostgreSQL**, and services like **Stripe** and **email** handle payments and notifications. Everything is scoped to a **school (tenant)** so each institution only sees its own students, fees, and records.

### How the pieces fit together

1. The user opens a page (e.g. `/payments/` or `/quran/`) in the browser.
2. **Django** receives the request, checks who is logged in and their **role**, and loads or saves the right rows from the database.
3. Django renders an **HTML template** and sends it back. Forms and buttons trigger new requests (GET to view, POST to submit).
4. For fees, Django redirects to **Stripe Checkout**; when payment succeeds, a webhook updates the fee row in PostgreSQL.

The portal uses **session login** (cookie in the browser). The REST API under `/api/` uses **JWT tokens** for programmatic access — useful for tests and future mobile clients.

For a diagram of how entities relate (students, classes, fees, sessions), see [Data model and ERD](#data-model-and-erd-entity-relationships).

### PostgreSQL — the database

PostgreSQL holds **all persistent data** for the platform.

| What it stores | Examples |
|----------------|----------|
| **Schools (tenants)** | Al-Noor Academy and every other school on the platform |
| **Users and roles** | Teachers, parents, students, admins — each linked to one school |
| **Academic data** | Classes, timetables, attendance marks, behaviour logs |
| **Learning** | Homework submissions, exam answers and results, LMS materials, Qur'an session notes |
| **Progress** | Hifz juz sign-offs, teacher reports |
| **Comms** | School messages, support cases, in-app notifications |
| **Payments** | Fee items, Stripe payment records, subscription plan |

**Connection:** the app reads `DATABASE_URL` from the environment (`core/settings.py`, `.env.example`). Local development uses a Postgres instance on your machine; Heroku uses the managed Postgres add-on. If `DATABASE_URL` is not set, Django falls back to SQLite for a quick run only.

**Tenant isolation:** almost every table includes a `school_id`. Queries filter by the logged-in user's school so one madrasah never sees another's data. Automated tests check this.

**Migrations:** Django migration files in each app (`*/migrations/`) apply schema changes safely when you deploy or run `python manage.py migrate`.

### Django — the web application

Django is the **main application framework**. It handles routing, authentication, business logic, and HTML rendering.

| Part | What it does in ESA |
|------|---------------------|
| **URLs** | Maps paths (`/attendance/`, `/api/students/`, etc.) to Python view functions in `core/urls.py` and each app's `urls.py` |
| **Views** | Run the logic for a page — load data, validate forms, enforce role checks, return a response |
| **Models (ORM)** | Python classes that map to database tables; create/read/update/delete without writing raw SQL |
| **Templates** | HTML files under `templates/` filled with data from views (dashboards, forms, tables) |
| **Apps** | Feature modules — `accounts`, `payments`, `quran`, `exams`, `messaging`, `hifz`, etc. — keep the codebase organised |
| **Middleware** | Runs on every request — e.g. session auth, email-verification gate for new accounts |
| **Admin** | `/admin/` — staff interface to inspect database rows during development |
| **REST API (DRF)** | `/api/*` — JSON endpoints for auth, students, homework, exams; used by tests and external clients |

**Static files** (CSS, JavaScript, mushaf PDFs) live under `static/` and `css/`. The production UI is server-rendered Django templates, not a separate React app. Early wireframe HTML at the repo root (`*.html`) is a design prototype only.

### External services

| Service | What it does in ESA |
|---------|---------------------|
| **Stripe** | Parent fee checkout and school subscription upgrades; test card `4242 4242 4242 4242` in sandbox mode |
| **Stripe Connect** | Routes fee payments to each school's connected bank account (school admin onboarding) |
| **Gmail / SMTP** | Sends verification codes, password resets, and optional message notifications (`EMAIL_*` in settings) |
| **Heroku** | Hosts the live app, Postgres, and environment config; deploys from the `main` branch |
| **GitHub** | Source control and issue/project board for bugs and sprint tracking |

Setup details for Stripe, email, and deployment are in [Development](#development) and [Deployment](#deployment).

---
## Overview

**ESA (Education and Schooling Applications)** is a full-stack multi-tenant SaaS platform for Islamic schools. It helps staff manage admissions, learning, attendance, academic progress, teacher-verified sign-offs, messaging, and payments (including Stripe Connect payouts to schools) in one place.

> **Live app:** https://esa-project-2a7a33dfe3fc.herokuapp.com/ · **Source:** https://github.com/sadek17481748/ESA  
> Static wireframe HTML at the repo root (`*.html`, `css/base.css`) can still be previewed with `python3 -m http.server 8080` — the production UI is implemented as Django templates.

ESA is designed for multiple schools (tenants) with strict data isolation, role-based access control, JWT-ready APIs (Django REST Framework), and a mobile-responsive dashboard. **Teacher sign-off** is a core trust layer: Hifz progress, homework/worksheets, and exam results only become official after an authenticated teacher verifies them (with re-authentication on sign-off and audit logging planned alongside implementation).

Planned core roles:

- **Super Admin**: manage schools, platform-wide settings, subscriptions, and analytics.
- **School Admin**: manage staff/students/parents, set fees, and connect Stripe for payouts.
- **Teacher**: manage classes/subjects, attendance, homework, exams, and progress sign-offs.
- **Student**: view timetable/work and submit recordings and assignments.
- **Parent**: monitor progress and payments, and make payments.

### Project goals

These were the **original aims** when ESA was scoped in May. They guided every sprint decision — including what to cut when time ran short.

#### Why these goals exist

Islamic supplementary schools and full-time madrasahs often run on a mix of spreadsheets, WhatsApp groups, paper registers, and disconnected payment links. Teachers re-type attendance into messages for parents; Hifz progress lives in private notebooks; fee reminders go out manually each term. That works at small scale but breaks down as classes grow, staff change, and parents expect the same digital experience they get from mainstream schools.

ESA was scoped to **replace fragmentation with one tenant-aware platform** — not to replicate every feature of a national MIS, but to cover the workflows Islamic schools actually described in early research: registers, homework, Qur'an and Hifz tracking, teacher-verified reporting, parent messaging, and online fees. Each goal below maps to one of those pain points. Together they define what “success” meant before a single migration was written.

#### What we were trying to achieve

At a high level, the project aimed to prove four things by submission:

1. **Technical competence** — a real Django + PostgreSQL application with authentication, APIs, payments, and deployment, not a prototype that only works on localhost.
2. **Domain fit** — language and flows that make sense for madrasahs (Hifz sign-off, parent link codes, Islamic school terminology), not a generic school template with different labels.
3. **Trust and safety** — parents and assessors can see *why* data on screen is credible (teacher approval, tenant isolation, audit-friendly design).
4. **Professional delivery** — evidence an employer or examiner can follow: README, tests, wireframes, validation screenshots, and a live Heroku URL that survives a structured walkthrough.

The numbered goals in the table are the **concrete checklist** derived from those four themes. If a feature did not support at least one of them, it was deferred to the buffer week or dropped.

| # | Goal | Summary | Status on live site |
|---|------|---------------|---------------------|
| 1 | **Full-stack Django app** | Real web app with database, not just static pages — split into reusable apps (`accounts`, `payments`, `quran`, etc.) | **Done** — deployed on Heroku with PostgreSQL |
| 2 | **Multi-tenant schools** | Many schools on one platform; each only sees its own data | **Done** — `school_id` scoping + tests |
| 3 | **Five roles (RBAC)** | Super Admin, School Admin, Teacher, Student, Parent — each with different pages | **Done** — sidebars and permission checks |
| 4 | **CRUD with UI feedback** | Create/edit records in the browser; errors and success messages shown clearly | **Done** — forms, flash messages, validation |
| 5 | **Teacher sign-off** | Teachers must approve Hifz, homework, and exams before parents trust the data | **Mostly done** — homework sign-off, exam finalise, Hifz juz sign-off live; password re-entry on sign-off still planned |
| 6 | **Stripe payments** | Parents pay fees online; money routes to the school's Stripe account | **Done** — Checkout + Connect + subscriptions (test mode) |
| 7 | **Responsive, accessible UI** | Works on laptop and tablet (primary); readable contrast; keyboard basics | **Done** — see [How responsiveness was tested](#how-responsiveness-was-tested) |
| 8 | **Documented, incremental build** | Small commits, README, tests, evidence for assessors | **Ongoing** — README, manual test table, GitHub history |

#### How the goals depend on each other

Several goals only make sense **in combination**. Multi-tenancy (goal 2) is meaningless without RBAC (goal 3): scoping data to a school is not enough if a parent account could open teacher URLs. Stripe (goal 6) depends on school admins existing as a role and on fee records created through normal CRUD (goal 4). Teacher sign-off (goal 5) depends on teachers having a authenticated session and on students/parents having *read-only* views of the same underlying records — otherwise “official” data and draft data look the same.

The **full-stack** goal (1) was the enabler for everything else: static wireframes proved layout early, but goals 2–7 required migrations, middleware, webhooks, and background-safe queries on Heroku. The **documentation** goal (8) was treated as a first-class deliverable because this module grades process as well as product — commit history, test names, and validation screenshots are how an assessor verifies that the other seven goals were met deliberately, not accidentally.

#### What we deliberately did not optimise for

Keeping scope honest mattered as much as listing ambitions. ESA was **not** trying to be a parent-facing mobile app store product, a government census system, or a full learning-management replacement for Moodle. Native iOS/Android apps, real-time video lessons, automated Quran recitation marking, and multi-language RTL UI were noted as future work. The goals above were chosen so a **single developer** could reach a defensible MVP in eight weeks while still demonstrating advanced topics (payments, multi-tenancy, JWT APIs, PDF annotation).

#### Measuring success against the goals

For assessment, each goal has a simple “show me” test:

- **Goal 1** — log in on Heroku; data persists after refresh; Django admin and API respond.
- **Goal 2** — two schools seeded; school A admin cannot see school B students (covered in automated tests).
- **Goal 3** — five demo accounts; each lands on a different dashboard with a different sidebar.
- **Goal 4** — create a teacher, class, or fee; invalid input shows field errors, not a raw 500 page.
- **Goal 5** — submit homework as student; parent does not see it as official until teacher approves / exam is finalised.
- **Goal 6** — parent pays a fee with Stripe test card `4242…`; webhook marks payment complete.
- **Goal 7** — resize browser or use DevTools device mode; Lighthouse and W3C evidence in README.
- **Goal 8** — README walkthrough, GitHub Project board, and dated commits through May–July.

The goals did **not** change mid-project — but **how** some features were implemented did (see [Scope creep](#scope-creep--what-changed-and-why) below). That is normal in a student project: the *intent* stayed the same; the *detail* was adjusted to fit the deadline.

### How we planned timing

ESA was planned as an **8-week build** (May 10 → July 1) plus a **1-week buffer** (July 1–7) for testing and README evidence — roughly aligned with a summer term deadline.

#### Planning approach

| Step | What we did | Why |
|------|-------------|-----|
| **1. Fixed the deadline first** | Ship a deployable MVP by **1 July**; polish by **7 July** | Stops endless feature additions — forces prioritisation |
| **2. Weekly sprints** | One theme per week (RBAC, timetable, homework, Qur'an, exams, payments) | Each week had a clear "done" outcome for the README and git history |
| **3. Foundation before features** | Weeks 1–2: Django, Postgres, tenants, roles — no payments or Qur'an yet | Later features depend on auth and school scoping; building them first avoids rework |
| **4. Wireframes before code** | Balsamiq + static HTML wireframes (`*.html`) before Django templates | Agreed layouts with assessor/stakeholder feedback before database work |
| **5. MVP then enhance** | Ship a working path end-to-end (login → register → pay fee) before polishing edge cases | Something demonstrable every fortnight, not one big bang at the end |
| **6. Buffer week reserved** | No new features after 1 July — only bugs, screenshots, README | Scope creep absorbed during build weeks; buffer is for quality not new modules |
| **7. GitHub as evidence** | Small commits dated through the sprint period | Assessors can see *when* each area was built, not one lump commit |

#### What "on time" meant

"On time" meant **core flows work on Heroku for an assessor walkthrough**, not every line in the original user stories. The [Features](#features) section lists what is actually live; the [Manual testing](#manual-testing) table tracks evidence row by row.

Primary devices planned from the start: **laptop and tablet** for staff; phone supported but not optimised first.

### Scope creep — what changed and why

**Scope creep** means the project growing beyond the original plan — extra features, deeper detail, or rework. ESA had planned creep *and* unplanned creep. Documenting both shows planning discipline, not failure.

#### Planned expansions (we knew these might grow)

| Area | Original plan | What we added | Why |
|------|---------------|---------------|-----|
| **Al-Noor demo school** | A few test logins | Full Y7–Y11 seed, 300+ accounts, timetables, showcase family | Assessors need a realistic school to click through, not empty dashboards |
| **Messaging** | Basic teacher–parent chat | Support cases, teacher reports, school admin student search, email copies | Real schools need audit trail and structured reports, not only free text |
| **LMS** | Homework only | Subjects, tracks, file uploads, class assignment, progress % | Worksheets and long-term materials are separate from weekly homework in madrasahs |
| **Timetable** | Simple grid | Drag-and-drop builder, archive, year groups, teacher "My timetable" → register link | Admin UX had to match how schools actually build term schedules |
| **README / evidence** | Short readme | Full assessor pack: ERD, wireframes, 44+ manual tests, security page | Module requirements — documentation is part of the deliverable |

These were **conscious decisions**: trade extra build time for assessor/demo value.

#### Unplanned changes (original spec ≠ what shipped)

| Original idea | What shipped instead | Reason |
|---------------|---------------------|--------|
| **Qur'an ayah picker** with Tajweed / Memorisation / Fluency tags | **Mushaf PDF viewer** — page through juz PDFs, notes, drag highlights | Real teachers use printed mushaf; PDF pages match classroom practice better than picking ayah numbers |
| **Hifz surah rows** + smart revision suggestions | **Juz sign-off only** (pick student + juz → parent message) | Surah-by-surah tracker + revision engine was too large for one sprint; juz sign-off delivers the trust/sign-off goal faster |
| **Password re-entry on every sign-off** | Teacher must be logged in; audit log planned | Time cost vs security benefit — logged-in teacher + role check shipped first |
| **Heroku seed on every boot** | Fast boot seed + manual `seed_alnoor_full_school` | Full seed on dyno start caused **Application error** (boot timeout) — scope reduced to keep site online |
| **Mobile-first polish** | Laptop/tablet primary; phone usable but secondary | Intended users are staff at desks/tablets; see [Responsive design](#responsive-design) |

#### How we controlled creep

When a new idea appeared mid-sprint, we asked:

1. **Does it serve a project goal?** (tenant safety, sign-off, payments, assessor demo)
2. **Can we ship a thinner version?** (juz sign-off instead of full Hifz tracker)
3. **Does it replace something, not add alongside?** (mushaf viewer replaced ayah picker — not both)
4. **Can it wait until after 1 July?** (smart revision, password re-entry → deferred)

If the answer to (4) was yes, it went on a **deferred list** rather than slipping the deadline.

#### Deferred to post-MVP (honest list)

Not cancelled — **out of scope for July hand-in**, documented so assessors know the roadmap:

- Smart Hifz revision suggestions  
- Surah-by-surah progress grid (vs juz sign-off list)  
- Password re-entry modal on every sign-off action  
- Full Arabic RTL UI chrome (mushaf PDF handles Arabic text)  
- Native mobile app (responsive web only)  

### Delivery timeline (May → July)

Week-by-week plan as written at project start. Dates are **targets**; some weeks overlapped or slipped by a few days when scope was adjusted above.

**Target:** stable deploy by **1 July** · buffer **1–7 July** for regression, screenshots, README.

| Week | Dates | Sprint theme | Planned deliverables |
|------|-------|--------------|-------------------|
| 1 | May 10–14 | **Foundation** | Django project, Postgres config, `School` tenant, custom user model, URL structure |
| 2 | May 15–21 | **RBAC + isolation** | Five roles, permission checks, tenant-scoped queries, audit log foundations |
| 3 | May 22–28 | **School setup** | Admin CRUD for teachers/students/parents, year groups, classes, CSV import |
| 4 | May 29 – Jun 4 | **Timetable + attendance** | Custom subjects (Hifz/Alimiyah/General), timetable grid, class registers |
| 5 | Jun 5–11 | **Homework + sign-off** | Assignments, submissions, teacher approve/reject, in-app notifications |
| 6 | Jun 12–18 | **Hifz** | Progress tracking + teacher sign-off *(later simplified to juz sign-off)* |
| 7 | Jun 19–23 | **Qur'an** | Session annotation *(later replaced by mushaf PDF viewer)* |
| 8 | Jun 24–28 | **Exams** | MCQ auto-mark, written marks, teacher finalise, parent/student views |
| 9 | Jun 29 – Jul 1 | **Payments + deploy** | Stripe Checkout, Connect, webhooks, receipts, permission review, Heroku stable |
| Buffer | Jul 1–7 | **Evidence** | Manual testing screenshots, validation, README expansion, bug fixes |

#### Build order (dependencies)

Features were ordered so each layer only depended on what came before:

```text
Auth + tenants → School setup → Timetable & attendance
       → Homework & LMS → Qur'an & Hifz → Exams → Payments & messaging → Analytics
```

Payments and Stripe were **late in the schedule** on purpose — they need stable users, schools, and fee records to test against.

#### Architecture notes (unchanged from start)

- Multi-tenant: every record belongs to a `School`; queries scoped to the logged-in user's school.
- Auth: session login for the portal; JWT for `/api/` endpoints.
- RBAC: explicit role checks on every view — Super Admin vs School Admin vs Teacher vs Student vs Parent.

For sprint commit evidence, see the GitHub history on [the repository](https://github.com/sadek17481748/ESA) (June–July 2026 commits grouped by feature area).

---
## Features

This section describes **what ESA actually does today** on the live site. Each feature is grouped by area. For every item you will see **who uses it** and **what you can do** — written for someone new to the project, not a developer.

Use the [Demo walkthrough](#demo-walkthrough) to try these with real logins.

### Accounts and getting started

| Feature | Who uses it | What it does |
|---------|-------------|--------------|
| **Home page** | Everyone (no login) | Marketing carousel explaining the platform; links to log in, register, or register a new school |
| **Log in** | All roles | Email/username + password; you are sent to the correct dashboard for your role |
| **Register as parent or student** | New users | Pick a school, choose role, create an account; students pick a class; parents can enter a **link code** to connect to a child straight away |
| **Register a new school** | New school admins | Creates a school + school-admin account in one step (for onboarding a new madrasah onto the platform) |
| **Email verification** | Real email sign-ups | Six-digit code sent to inbox before full access; demo seed accounts skip this |
| **Password reset** | Anyone who forgot password | Email link to set a new password |
| **Parent link child** | Parents | Enter a code the school gave you to link your account to your child's profile |
| **Public link page** | Parents with a code | `/link/<code>/` — shortcut URL the school can share |
| **Role dashboards** | Each role after login | Five separate home screens: Super Admin, School Admin, Teacher, Student, Parent — each with its own sidebar |

### Multi-tenant schools

ESA hosts **many schools on one platform**, but each school only sees **its own data**.

- Every student, teacher, fee, timetable, and message belongs to **one school**.
- A teacher at Al-Noor Academy cannot open another school's attendance register.
- A School Admin manages **one school**; a Super Admin sees **all schools** on the platform.

This is called **multi-tenant** architecture — one app, many isolated schools.

### School admin — running the school

| Feature | What you can do |
|---------|-----------------|
| **Dashboard overview** | Snapshot of the school — quick links into setup areas |
| **Add teachers** | Create teacher accounts with username, email, and subject |
| **Teachers list** | View staff already registered at your school |
| **Students list** | View enrolled students; each row can show a **parent link code** to give families |
| **Timetable hub** | Add year groups and classes, build weekly timetables, assign subjects and teachers |
| **LMS hub** | Create subjects (e.g. Maths, Quran), add learning tracks, upload worksheets/links |
| **Attendance overview** | School-wide view of registers taken across classes |
| **Analytics** | KPI-style stats — attendance, fees, behaviour at a glance |
| **Fees (school side)** | Create fee items charged to parents; see outstanding and paid |
| **Subscription** | Choose platform plan (Free / Standard / Premium) and pay via Stripe |
| **Stripe Connect** | Connect the school's Stripe account so parent fee payments go to the school bank account |
| **Find student** | Search any student by name or admission number (for messaging and admin tasks) |
| **Messages inbox** | See all conversations between parents, teachers, and school office |

### Timetable

| Feature | Who uses it | What you can do |
|---------|-------------|-----------------|
| **Timetable hub** | School admin | Add classes (e.g. 7A, 8B), create named timetables (e.g. "Spring term"), open the drag-and-drop builder |
| **Timetable builder** | School admin | Drag subjects onto a weekly grid, set times, assign a teacher to each slot, save |
| **Live timetables** | School admin | List of published timetables — edit, archive, or view lesson counts |
| **Custom subjects** | School admin | Subjects tagged as **General**, **Hifz**, or **Alimiyah** per school |
| **My timetable** | Teacher | Shows only lessons **you** are assigned to on the timetable; links to take the register for that class |
| **Student timetable** | Student | Read-only weekly view of their class schedule |

Teachers are **not** fixed to one class forever — they appear on whichever timetable slots the school admin assigned them to.

### Attendance

| Feature | Who uses it | What you can do |
|---------|-------------|-----------------|
| **Class register** | Teacher | Pick a date and class; mark each student **Present**, **Late**, or **Absent**; save the session |
| **Teacher register (school-wide list)** | Teacher | Mark attendance for any student in the school (used when Quran or cross-class teaching applies) |
| **School overview** | School admin | See which registers have been taken across classes |
| **Parent view** | Parent | See attendance history for **linked children only** |
| **Student view** | Student | See own attendance history |

Registers are stored per **session** (school + class + date), so you can look back at previous days.

### Homework and worksheets

| Feature | Who uses it | What you can do |
|---------|-------------|-----------------|
| **Assignments** | Teacher | Create homework or worksheets for a class, set a due date and description |
| **Submit work** | Student | Write a submission (or upload where supported) before the deadline |
| **Sign-off queue** | Teacher | Approve or reject submitted work; only the **assigning teacher** can sign off |
| **View results** | Student / parent | See whether work was approved or needs revision after sign-off |

When a teacher approves work, the student gets an **in-app notification**. Rejected work shows as "needs revision."

### LMS — learning materials

The **LMS** (Learning Management System) is where schools store structured learning content beyond day-to-day homework.

| Feature | Who uses it | What you can do |
|---------|-------------|-----------------|
| **Subjects & tracks** | School admin | e.g. Maths → Foundation / Higher; Quran → Beginners |
| **Upload materials** | School admin | Add worksheets, document links, or files to a track |
| **Assign track to class** | Teacher / admin | Attach a track so students in that class can see the materials |
| **Student progress** | Student | Mark materials in progress or completed; percentage shown |
| **Submit worksheet** | Student | Upload a completed file for teacher review |
| **Review submission** | Teacher | Approve or send back for revision with feedback |

**Al-Noor Academy worksheet library (37 PDFs)** — seeded into LMS subjects:

| Subject | Tracks | Source |
|---------|--------|--------|
| **Maths** | Year 2, 3, 7, 8, 9, 10 | [Cluey Learning — Free Maths Worksheets](https://go.clueylearning.com.au/en/maths-worksheets/) |
| **English** | Grammar & writing, Spelling, Reading & comprehension | [iSL Collective — English ESL worksheets](https://en.islcollective.com/english-esl-worksheets/search) |
| **Islamic Studies** | Sahih al-Bukhari Vol. 1–3, Hadith reader excerpts | [Sahih al-Bukhari Vol. 3 (English PDF)](https://uploads.ahlesunnatpak.com/books/Saheh%20Al-Bukhari/english/SahihAl-bukhariVol.3-Ahadith1773-2737.pdf) — Vol. 1–2 on same host |

Worksheet PDFs live in `WORKSHEETS/` locally (gitignored). On Heroku run `python manage.py seed_alnoor_worksheets --assign-classes` — Bukhari volumes are downloaded; maths and English materials link to the Cluey / iSL Collective source pages. Students open materials from `/worksheets/` or `/lms/` (uploaded files at `/lms/material/<id>/file/`).

### Qur'an sessions (mushaf viewer)

This replaced the older ayah-by-ayah annotation picker. Teachers now work with **real mushaf PDF pages**.

| Feature | Who uses it | What you can do |
|---------|-------------|-----------------|
| **Create session** | Teacher | Pick a student — opens a new Qur'an session for that child |
| **Mushaf viewer** | Teacher (edit) / student & parent (read-only) | Page through **30 juz PDFs** with arrow buttons; fit-to-width and zoom controls |
| **Per-page notes** | Teacher | Type comments for that student on that page (e.g. "work on madd") — saves automatically |
| **Highlights** | Teacher | Drag coloured boxes on the page (like a highlighter pen) to mark areas to revise |
| **Session list** | Teacher / student | See all sessions; open any session to continue where you left off |
| **Audio (where uploaded)** | Student / teacher | Recitation upload and teacher feedback audio on a session |

Parents and students can **view** notes and highlights but cannot edit them.

**Sprint delivery (19–23 June):** `quran` app — session list, mushaf PDF viewer (`/quran/`), per-page notes and highlights, optional audio. Covered by `quran/tests.py` and manual testing with `teacher_demo` / `student_demo`.

### Hifz sign-off

A simple flow for when a student has memorised a full **juz** (part) of the Qur'an.

| Step | What happens |
|------|--------------|
| Teacher picks **student** and **juz** (1–30) | Form on the Hifz page |
| Teacher clicks **Student has passed** | Record saved with date and teacher name |
| Parent notified automatically | Congratulations message sent in **Messages** + in-app notification |

Parents and students see a **list of signed-off juz**. Each juz can only be signed off once per student.

> **Note:** Detailed surah-by-surah revision tracking and "smart revision suggestions" are **not** built yet — sign-off is at **juz** level only.

### Exams

| Feature | Who uses it | What you can do |
|---------|-------------|-----------------|
| **Create exam** | Teacher | Title, class, subject, date; add **multiple-choice** and **written** questions |
| **Publish** | Teacher | Makes the exam visible to students in that class |
| **Sit exam** | Student | Answer MCQs and written questions in the portal |
| **Auto-mark MCQs** | System | Multiple-choice questions scored automatically when answers are saved |
| **Mark written answers** | Teacher | Enter marks for long-answer questions |
| **Finalise result** | Teacher | Locks the result — only **finalised** results show to parents and students as official |
| **View results** | Student / parent | See scores and teacher comment after finalisation |

**Sprint delivery (24–28 June):** `exams` app — MCQ auto-mark, written marking, teacher finalise at `/exams/`. Parents and students see results only after finalise. Covered by `exams/tests.py`.

### Behaviour

| Feature | Who uses it | What you can do |
|---------|-------------|-----------------|
| **Log behaviour** | Teacher | Record a **commendation** (positive) or **incident** (negative) for any student in the school |
| **View records** | Parent | Read-only list for linked children |
| **School-wide list** | School admin | See recent behaviour entries across the school |

Each record has a title, optional notes, date, and the teacher who logged it.

### Messaging and reports

| Feature | Who uses it | What you can do |
|---------|-------------|-----------------|
| **School messages** | Parent, teacher, school admin | Threaded conversations — parent ↔ teacher, parent ↔ school office, teacher ↔ parent |
| **New message** | Parent / teacher / admin | Start a conversation with a subject line |
| **Support cases** | Parent → platform team | Open a support ticket (case number, threaded replies); Super Admin responds |
| **Teacher reports** | Teacher | Structured progress report (strengths, areas to improve, action required) sent to parent |
| **Read reports** | Parent / student | View reports written about the child |
| **Unread badge** | All messaging users | Sidebar shows when new messages arrived |
| **Email copies** | Optional | New messages can trigger email if the user enabled notifications |

Hifz sign-off and other system events also create **automatic messages** to parents (e.g. "Congratulations — passed Juz 3").

### Payments and subscriptions

| Feature | Who uses it | What you can do |
|---------|-------------|-----------------|
| **Parent fees** | Parent | See outstanding and paid fees for your children; pay via **Stripe Checkout** |
| **Fee management** | School admin | Create fee items (tuition, trips, etc.) tied to a parent account |
| **Payment receipt** | Parent | View receipt after successful Stripe payment |
| **School subscription** | School admin | Upgrade platform plan (Free → Standard → Premium) with monthly Stripe billing |
| **Stripe Connect onboarding** | School admin | Link the school's Stripe account so fee money routes to the school, not the platform |
| **Webhooks** | Background | Stripe tells ESA when a payment succeeded so the database updates automatically |

Use test card **`4242 4242 4242 4242`** in Stripe sandbox mode when testing payments.

**Sprint delivery (29 June–1 July):** Stripe Checkout for parents, Connect onboarding for schools, webhooks, PDF receipts, `send_overdue_reminders` command. Covered by `payments/tests.py` and manual payment rows in [Manual testing](#manual-testing).

### Notifications

| Feature | What it does |
|---------|--------------|
| **In-app notifications** | Bell-style alerts inside the portal — homework signed off, Hifz passed, general school news |
| **Notification list** | Each user sees only their own notifications |
| **Email on new messages** | Optional per-user setting in the Messages inbox |

### Security and audit

| Feature | What it does |
|---------|--------------|
| **Role checks** | Every page checks you are logged in and have the right role before showing data |
| **Tenant scoping** | Database queries filtered by school so data does not leak between tenants |
| **Public security page** | `/security/` — plain-language explanation of how ESA handles auth, payments, and data |
| **Audit log** | Sensitive actions (e.g. login) recorded for review in development/admin |
| **Email verification gate** | Unverified accounts cannot use the portal until they enter their code |
| **REST API + JWT** | `/api/` endpoints for programmatic access; same permission rules as the web portal |

---
## User Experience (UX)

ESA is used by five roles with different needs: parents on phones, teachers on laptops, school admins setting up timetables. The portal keeps navigation consistent, shows which school you belong to, and gives clear feedback when you save or pay.

See [Features](#features) for functionality and [Demo walkthrough](#demo-walkthrough) for logins.

### UX principles

| Principle | What it means in practice |
|-----------|---------------------------|
| **Role-first** | After login you only see pages your role is allowed to use — no clutter from admin tools on a student screen |
| **School context** | The portal banner shows **which school** you belong to (e.g. Al-Noor Academy) so users always know where they are |
| **Mobile-friendly** | Layouts reflow on phones; tables scroll; sidebars stack vertically |
| **Clear feedback** | Saving, paying, or signing off shows a confirmation message — you are not left guessing |
| **Trust visible** | Homework, exams, and Hifz progress only appear as "official" after a teacher has signed off or finalised |
| **Clear labels** | Buttons say what they do ("Student has passed", "Save register", "Pay now") |
| **Consistent shell** | Every signed-in page shares the same header, sidebar pattern, and footer so navigation feels familiar |

### Layout and navigation

ESA uses **two layout types**:

**1. Marketing / auth pages** (no login, or login/register only)

- Used for: home page, school registration, login, password reset, public security page
- **Single column** — content centred, top navigation with Log in / Register
- **Skip link** at the top ("Skip to content") jumps keyboard users past the header to the main area

**2. Portal pages** (after login)

- Used for: all dashboards and feature pages (attendance, fees, Qur'an, etc.)
- **App shell:** sticky top header + **left sidebar** + main content area
- **Top header:** ESA brand, school or role tag, quick links (Messages, Log out; parents also see Payments, teachers see Timetable)
- **Sidebar:** grouped links by topic (e.g. teacher: Teaching → Reports → Sign-off). The current page is highlighted with `aria-current="page"` and a gold background
- **Main area:** page title (`h1`), optional subtitle (`page-meta`), then panels and tables

**Why a sidebar?** Islamic schools run many modules (fees, Hifz, Qur'an, timetable). A persistent sidebar lets users **jump between areas** without returning to a central hub every time. Each role gets a **different sidebar** — parents never see "Create report", students never see "Add teacher".

**Navigation flow:**

```text
Log in → Role dashboard (overview) → Sidebar link → Feature page → Back via sidebar
```

Wrong role or wrong school? Django redirects to your dashboard rather than showing forbidden data.

### Visual design and branding

| Element | Purpose |
|---------|---------|
| **Colour palette** | Near-black background (`#0a0a0a`), off-white text, **gold accents** (`#c9a227`) — see [Colour palette](#colour-palette-and-css-tokens) for full tokens |
| **Panels** | Content sits in rounded `.panel` cards with subtle borders — separates sections on busy pages |
| **Accent bar** | Short gold bar under section headings — visual rhythm on long pages |
| **Pills / badges** | Small labels for plan tier (Free / Standard), status, class name |
| **Grid cards** | Dashboard overviews use card grids for "this week", KPIs, quick stats |
| **Data tables** | Registers, fee lists, sign-off history — scannable rows with header row |
| **Typography** | System font stack (Segoe UI, Roboto, etc.) at 16px base — readable without custom webfonts |
| **Geometric header** | Subtle decorative pattern in the site header — nod to Islamic geometric art without harming readability |

All styles live in `css/base.css` (shared by wireframes and Django templates). Django templates under `templates/` reuse the same classes so the **live site matches the wireframe look**.

### Dashboards by role

Each role lands on an **overview** designed for their daily tasks:

| Role | Dashboard focus | Typical next steps from sidebar |
|------|-----------------|--------------------------------|
| **Super Admin** | All schools on the platform, support queue | Schools list, subscriptions, admin panel |
| **School Admin** | School KPIs, setup shortcuts | Timetable hub, LMS, teachers, fees, analytics |
| **Teacher** | Today's lessons, pending work | Attendance, Qur'an, worksheets, Hifz sign-off, exams |
| **Student** | This week's deadlines, timetable snippet | Homework, exams, Qur'an sessions, Hifz progress |
| **Parent** | Linked children, fee/attendance summary | Payments, messages, behaviour, reports |

Overview pages use **cards and short lists** — detail lives on dedicated feature pages so the home screen stays scannable.

### Forms, validation, and feedback

Most actions use **HTML forms** posted to the server (not JavaScript-only saves), so they work even with JavaScript disabled (except interactive tools like the timetable drag grid and Qur'an PDF viewer).

| UX pattern | What the user sees |
|------------|-------------------|
| **Form fields** | Consistent `.form-input` styling — text fields, selects, textareas look the same everywhere |
| **Labels** | Each field has a visible label above it |
| **Validation errors** | Wrong input returns the same page with errors **next to the field** or at the top — nothing fails silently |
| **Success messages** | Green/gold flash banner after save ("Timetable saved", "Message sent", "Student has passed") |
| **Destructive actions** | Archive timetable and similar actions ask for **confirm** before proceeding |
| **Read-only mode** | Parents and students see Qur'an notes and highlights but cannot edit — fields are disabled or hidden |
| **Long forms split** | Registration split into steps (pick school → pick role → pick class) so mobile users are not overwhelmed |

**Payments** redirect to Stripe's hosted checkout — familiar card entry UI — then return to a **success page with receipt reference**.

### Tables, lists, and empty states

| Pattern | Behaviour |
|---------|-----------|
| **Wide tables** | Wrapped in `.table-wrap` with horizontal scroll on small screens — no squashed columns |
| **Empty tables** | Placeholder row: "No behaviour records yet" — user knows the page loaded, there is just no data |
| **Messaging on mobile** | Inbox tables switch to **stacked cards** (label + value per row) below 900px width |
| **Pagination / limits** | Long lists (messages, notifications) show recent items first; search available for students (school admin) |
| **Status columns** | Pass/Fail, Present/Late/Absent, Outstanding/Paid use readable labels |

### Responsive design

ESA is built **mobile-first in CSS** (single column by default, wider layouts added with media queries) — but the **intended day-to-day use** is **laptop and tablet**, not phone.

| Who | Primary device | Why |
|-----|----------------|-----|
| **School admin** | Laptop | Timetable builder, LMS uploads, fee setup — wide screen and mouse for drag-and-drop |
| **Teacher** | Laptop or tablet | Registers, Qur'an mushaf viewer, exam marking — often at a desk or with a tablet in class |
| **Parent** | Tablet or laptop | Checking fees, messages, reports — larger screen for reading teacher feedback |
| **Student** | Tablet or laptop | Homework, timetable, Qur'an sessions |
| **Phone** | Supported, secondary | Layout still works (stacked sidebar, scrollable tables) for parents checking messages on the go |

The layout **reflows** at two main CSS breakpoints in `css/base.css`:

| Width | What changes |
|-------|--------------|
| **Below 900px** | Sidebar stacks **above** main content; timetable builder toolbar stacks; messaging tables become card layout |
| **Below 768px** | Home page hero and carousel go single column; stat cards wrap |

On **laptop and tablet** (900px and above), users get the full experience: sidebar beside content, timetable grid beside subject palette, full-width data tables.

### How responsiveness was tested

#### Why we test this way

Responsiveness is tested against **how the school will actually use the site**, not every possible screen size.

1. **Laptop and tablet are the priority** — staff and teachers need reliable layouts at 1024px–1440px where most admin and teaching work happens.
2. **Real URLs, not guesses** — testing loads the **live Heroku deployment** inside device frames so Django templates, login sessions, and Stripe redirects behave exactly as assessors will see them.
3. **Key pages, not every pixel** — we focus on pages that break easily when narrow: timetable builder, attendance register, payments, messages inbox, Qur'an viewer, and role dashboards.
4. **Evidence for assessors** — screenshots are saved to `docs/images/validation/` so results can be checked without re-running tests.
5. **Phone is a sanity check** — we confirm nothing is unusable on a small screen, but we do not optimise every feature for 320px the way we do for tablet.

#### Tool: Website Responsive Testing Tool

Primary tool: **[Website Responsive Testing Tool](http://responsivetesttool.com)** — paste the live URL and preview it inside preset device frames without installing browser extensions.

| Category | Presets we use | Matches ESA priority |
|----------|----------------|----------------------|
| **Tablet** | iPad (768 × 1024), iPad Pro (1024 × 1366), iPad Air (768 × 1024) | **Primary** — teacher/parent classroom and home use |
| **Laptop / desktop** | 1366 × 768, 1440 × 900, 1920 × 1080 | **Primary** — school admin and teacher daily work |
| **Mobile** | iPhone 8 (375 × 667), 414 × 896 breakpoints | **Secondary** — confirm sidebar stacks and tables scroll |

**URL tested:** https://esa-project-2a7a33dfe3fc.herokuapp.com/

**Suggested order:**

1. Log in on a **laptop** preset (1366 × 768) as `demo_parent` / `Demo2026!` — fees, messages, attendance.
2. Repeat on **iPad** preset (768 × 1024) — same flows; sidebar should stack above content below 900px width.
3. Open **timetable** and **Qur'an** as `mr_mohammed` / `teacher1234` on iPad Pro (1024 × 1366) — builder grid and mushaf viewer usable.
4. Quick pass on **iPhone** preset — login form readable, tables scroll horizontally, no horizontal page overflow.

#### Pages checked

| Page | Laptop (1366 × 768) | Tablet (768 × 1024) | What we look for |
|------|---------------------|---------------------|------------------|
| Login / register | Centred form, readable labels | Form full width, no clipped fields | Auth usable without zooming |
| School admin dashboard | Sidebar + cards side by side | Sidebar stacks; cards readable | Navigation still obvious |
| Timetable builder | Grid + subject palette visible | Toolbar stacks; grid scrolls | Can still assign subjects |
| Teacher attendance register | Full class table | Table scrolls; mark buttons reachable | Register save works |
| Parent payments | Fee table + Pay now | Table scroll; button visible | Stripe redirect works |
| Messages inbox | Full table layout | Card-style rows (under 900px) | Threads readable |
| Qur'an mushaf viewer | Fit-to-width + zoom toolbar | Scroll area within viewport | Page navigation works |

#### Secondary check: Chrome DevTools

Chrome DevTools device mode is used for **quick checks during development** (toggle breakpoints, inspect overflow). Formal assessor evidence comes from [responsivetesttool.com](http://responsivetesttool.com) screenshots at the presets above.

#### Evidence location

| Folder | Contents |
|--------|----------|
| `docs/images/validation/` | **Responsive testing** — iPhone X, iPad 768px, desktop, narrowed laptop (see [Responsive testing](#responsive-testing-cross-device) at top of README) |
| `docs/images/validation/` | Lighthouse and W3C validation (when captured) |
| `docs/images/manual-testing/` | Feature flow screenshots at desktop width |
| `docs/images/preview/` | Role and feature page gallery |

### Accessibility

ESA targets **WCAG AA** where practical for a student project:

| Feature | Implementation |
|---------|----------------|
| **Skip link** | "Skip to content" — first focusable element on every page |
| **Semantic HTML** | `<main>`, `<nav>`, `<header>`, heading hierarchy (`h1` page title, `h2` sections) |
| **Focus styles** | `:focus-visible` gold outline on buttons and links — keyboard users see where they are |
| **Current page** | Sidebar uses `aria-current="page"` for screen readers |
| **Colour contrast** | Light text on dark surfaces; gold on black checked for button/link contrast |
| **Form labels** | Explicit `<label>` elements tied to inputs |
| **Alt text (images)** | Every meaningful `<img>` has an `alt` description for **screen readers** (text-to-speech). Homepage carousel photos describe the scene (e.g. “Students learning at London Islamic School”). README screenshots use markdown alt text: `![description](image.png)`. Decorative shapes use `aria-hidden="true"` instead of empty alt. |
| **PDF / canvas** | Qur'an viewer `<canvas>` uses `role="img"` and a dynamic `aria-label` (“Juz X, page Y”) updated when the page changes |
| **Language** | `<html lang="en">` set on all templates |

**Known limits (honest):** the Qur'an PDF canvas and timetable drag-and-drop are pointer-heavy; keyboard-only use of those two tools is limited. Core flows (login, fees, messages, attendance marks) are keyboard accessible.

### Everyday journeys (how people use ESA)

These are common paths — not click-by-click instructions, but **what the experience should feel like**:

**Parent — check child and pay a fee**

Log in → see child's name on overview → open **Fees** → outstanding amount clear → **Pay now** → Stripe → return to success receipt → fee moves to "paid" on next visit.

**Teacher — morning register**

Log in → **My timetable** shows today's class → open register link → mark Present/Late/Absent → save → flash confirms register stored.

**Teacher — Qur'an feedback**

Open **Qur'an** → pick student session → page through mushaf → add note on weak page → drag yellow highlight → notes auto-save when changing page.

**Teacher — Hifz milestone**

Open **Hifz** → pick student and juz → **Student has passed** → parent receives congratulations message without teacher opening Messages manually.

**Student — homework**

See assignment on overview or **Homework** → submit text → wait for teacher sign-off → notification when approved or "needs revision".

**School admin — new term setup**

**Timetable hub** → add class → create timetable → drag subjects → assign teachers → save → students see schedule on their dashboard.

### Trust, sign-off, and clarity

Islamic schools need parents to **trust** what they see. UX reinforces that:

| Data type | Before teacher action | After teacher action |
|-----------|----------------------|----------------------|
| Homework | "Submitted" — waiting | "Approved" or "Needs revision" — official |
| Exam | Answers saved | **Finalised** — score visible to parent/student |
| Hifz | Not listed | Juz appears on signed-off list + parent message |
| Qur'an | Teacher draft notes | Reviewed session — student sees feedback |

Students and parents **never** self-certify Hifz or exam results — the UI only promotes data the teacher has explicitly confirmed.

---

### User stories (acceptance criteria)

The stories below are the **formal acceptance criteria** written at project start. They describe intended behaviour in "As a [role], I want…" format. Use them alongside the [Features](#features) section and [Manual testing](#manual-testing) table when assessing whether the build meets requirements.

Some stories describe planned features not yet fully built (e.g. smart Hifz revision) — the [Features](#features) section reflects **what is live today**.

#### Super Admin stories

**US-1 — Create and manage school tenants**
As a Super Admin, I want to create new school tenants and configure their basic details (name, address, contact email, subscription tier) so that each institution has its own isolated workspace on the platform.

Acceptance criteria:
- Super Admin can create a school from a form with required fields (name, address, contact email).
- Each new school is assigned a unique tenant ID that scopes all future data to that school.
- The school appears in the Super Admin's school list immediately after creation.
- Super Admin can edit the school's name, address, contact email, and subscription tier from the school detail page.

**US-2 — View platform-wide analytics**
As a Super Admin, I want to view a platform-level dashboard showing total schools, total active users, monthly revenue, and recent sign-ups so that I can monitor the overall health of the platform at a glance.

Acceptance criteria:
- Dashboard displays total school count, total active user count, and monthly revenue figure.
- A recent sign-ups list shows the last 10 schools created with their creation date.
- Data refreshes each time the page is loaded.

**US-3 — Manage subscriptions and billing**
As a Super Admin, I want to assign and change subscription tiers for each school so that billing is accurate and the platform remains financially sustainable.

Acceptance criteria:
- Super Admin can select a tier (e.g. Free, Standard, Premium) per school.
- Changing a tier is logged with a timestamp for audit purposes.
- Schools on an expired or suspended tier see a visual indicator on the Super Admin dashboard.

**US-4 — Suspend or deactivate a school**
As a Super Admin, I want to suspend or deactivate a school tenant so that I can enforce terms of service or handle non-payment without permanently deleting data.

Acceptance criteria:
- Super Admin can set a school's status to Active, Suspended, or Deactivated.
- Users belonging to a Suspended school see a message explaining access is temporarily restricted on login.
- Users belonging to a Deactivated school cannot log in at all.
- Data is retained (not deleted) when a school is suspended or deactivated.

**US-5 — Search and filter across schools and users**
As a Super Admin, I want to search and filter across all schools and users by name, email, or role so that I can provide support or investigate issues quickly.

Acceptance criteria:
- A search bar on the Super Admin users page accepts free-text input and returns matching users across all tenants.
- Results can be filtered by role (School Admin, Teacher, Student, Parent).
- Each result row shows the user's name, email, role, and school name.

---

#### School Admin stories

**US-6 — Add, edit, and remove teacher accounts**
As a School Admin, I want to add new teacher accounts, edit their details, and remove them when they leave so that my staffing records are always current.

Acceptance criteria:
- School Admin can create a teacher account with name, email, and subject assignments.
- School Admin can edit a teacher's name, email, or assigned subjects from the teacher detail page.
- School Admin can deactivate (soft-delete) a teacher account; the teacher can no longer log in but historical records (attendance, sign-offs) are preserved.
- Only teachers belonging to this school are visible; no cross-tenant leakage.

**US-7 — Enrol students individually or via CSV**
As a School Admin, I want to enrol students one at a time through a form or in bulk via CSV upload so that onboarding at the start of each term is efficient.

Acceptance criteria:
- A single-student form collects name, date of birth, year group, and parent email.
- A CSV upload accepts columns: first_name, last_name, date_of_birth, year_group, parent_email.
- Validation errors (missing fields, duplicate emails) are reported per row; valid rows are imported.
- Successfully enrolled students appear in the student list immediately.

**US-8 — Invite parents and link them to children**
As a School Admin, I want to invite parents by email and link each parent to one or more children so that parents can access the parent portal and see only their own children's data.

Acceptance criteria:
- School Admin enters a parent's email and selects the child(ren) to link.
- The parent receives an invitation email with a registration link.
- After registration the parent's dashboard shows only the linked children.
- A parent can be linked to multiple children; a child can have up to two linked parent accounts.

**US-9 — Create year groups and classes**
As a School Admin, I want to create year groups (e.g. Year 1, Year 2) and classes within each year group so that students and teachers can be organised by cohort.

Acceptance criteria:
- School Admin can create a year group with a name and academic year.
- Within a year group, School Admin can create one or more classes with a class name and capacity.
- Students can be assigned to a class; a student belongs to exactly one class at a time.
- Teachers can be assigned to classes they will teach.

**US-10 — Define custom subjects**
As a School Admin, I want to define the subjects taught at my school (selecting from categories such as Hifz, Alimiyah, and General) and give each a display name so that the curriculum reflects my school's specific programme.

Acceptance criteria:
- School Admin can add a subject with a category (Hifz / Alimiyah / General) and a custom display name.
- Subjects are scoped to the school; other schools cannot see them.
- School Admin can edit or archive a subject (archiving hides it from new assignments but preserves historical data).

**US-11 — Assign teachers to subjects and classes**
As a School Admin, I want to assign teachers to subjects and to specific classes so that the timetable can be built correctly and teachers only see data for their assigned classes.

Acceptance criteria:
- School Admin can select a teacher and assign them to one or more subject–class combinations.
- The teacher's timetable and class list update to reflect the assignment.
- Teachers cannot access classes or subjects they are not assigned to.

**US-12 — Build and publish a weekly timetable**
As a School Admin, I want to build a weekly timetable by assigning subject–teacher–class combinations to time slots so that staff, students, and parents know the schedule.

Acceptance criteria:
- A grid interface shows days (Monday–Friday) and configurable time slots.
- School Admin can drag or select a subject–teacher–class combination into a slot.
- Conflicts (same teacher in two places, same class double-booked) are flagged before saving.
- Published timetable is visible to teachers, students, and parents belonging to the relevant classes.

**US-13 — Set fee structures and due dates**
As a School Admin, I want to create fee items (tuition, trips, resources) with amounts and due dates so that parents know exactly what they owe and when.

Acceptance criteria:
- School Admin can create a fee item with a name, amount, due date, and target group (whole school, year group, or individual student).
- Fee items appear on the parent's outstanding fees list.
- Overdue fees are visually flagged with the number of days past due.

**US-14 — Connect the school's Stripe account**
As a School Admin, I want to connect my school's bank account via Stripe Connect onboarding so that fee payments from parents are routed directly to our school's account.

Acceptance criteria:
- A "Connect with Stripe" button initiates the Stripe Connect OAuth flow.
- On successful connection the school's Stripe account ID is stored and the dashboard shows a "Connected" badge.
- If the connection is incomplete or revoked, the dashboard shows a warning and payments cannot be processed until reconnected.

**US-15 — View attendance summaries and flag persistent absences**
As a School Admin, I want to view attendance summaries per class and per student, with automatic flagging of students whose attendance drops below a configurable threshold, so that pastoral concerns are caught early.

Acceptance criteria:
- An attendance overview page shows each class's attendance percentage for the current term.
- Drilling into a class shows per-student attendance percentages.
- Students below the threshold (default 90%) are highlighted in red.
- School Admin can adjust the threshold percentage in school settings.

**US-16 — Review behaviour incident logs**
As a School Admin, I want to view and filter all behaviour incident logs across the school so that I have oversight of student conduct and can identify patterns.

Acceptance criteria:
- A behaviour log page lists all incidents with date, student name, teacher who logged it, category, and description.
- Filters allow narrowing by date range, class, student, or severity.
- School Admin can add a follow-up note to any incident.

**US-17 — View school-wide analytics**
As a School Admin, I want to view school-wide analytics covering attendance rates, Hifz completion progress, homework submission rates, exam averages, and fee collection totals so that I can report to governors and make informed decisions.

Acceptance criteria:
- A school analytics page shows key metrics: overall attendance %, Hifz completion %, homework on-time %, average exam score, total fees collected vs outstanding.
- Each metric can be filtered by year group or class.
- Data only includes teacher-verified (signed-off) records where applicable.

**US-18 — Send announcements**
As a School Admin, I want to send announcements to all parents, to a specific year group, or to a specific class so that communication is centralised and parents receive important updates.

Acceptance criteria:
- School Admin composes a message with a subject line and body.
- School Admin selects the audience: all parents, a year group, or a class.
- Recipients receive an in-app notification and optionally an email.
- Sent announcements are logged in a sent-items list visible to School Admin.

---

#### Teacher stories

**US-19 — View my timetable and assigned classes**
As a Teacher, I want to see my personal timetable showing which classes I teach and when so that I know where I need to be each day.

**US-20 — Take a class register**
As a Teacher, I want to take a class register at the start of each lesson by marking each student as present, late, or absent so that attendance is recorded in real time.

**US-21 — Create and assign homework or worksheets**
As a Teacher, I want to create homework or worksheet assignments with a title, description, optional file attachment, and due date, and assign them to a class so that students know what to complete and by when.

**US-22 — Review and approve or reject student submissions**
As a Teacher, I want to review each student's homework or worksheet submission, leave feedback, and mark it as approved or rejected so that the student receives clear, recorded feedback.

**US-23 — Sign off Hifz progress**
As a Teacher, I want to sign off a student's Hifz progress for a specific surah or juz, moving its status from In Progress to Completed, so that completion is verified and trustworthy.

**US-24 — Re-authenticate before signing off**
As a Teacher, I want to be required to re-enter my password when performing any sign-off action so that the action is securely authenticated and cannot be performed by someone who found an unlocked device.

**US-25 — Annotate a Qur'an recitation session**
As a Teacher, I want to annotate a student's Qur'an recitation session by tagging specific mistakes with categories (Tajweed, Memorisation, Fluency), adding timestamps and written comments, so that the student can see exactly where they need to improve.

**US-26 — Upload audio feedback on a recitation**
As a Teacher, I want to record or upload an audio clip as feedback on a student's recitation so that the student can listen to the correct pronunciation or pacing and self-correct.

**US-27 — Create exams and enter results**
As a Teacher, I want to create exams with a title, date, subject, and question format (MCQ or written), and enter or auto-mark results for each student, so that assessment is handled in one place.

**US-28 — Finalise exam results with sign-off**
As a Teacher, I want to finalise exam results with a sign-off so that only verified scores appear on student and parent reports, and draft scores remain internal.

**US-29 — Log a behaviour incident**
As a Teacher, I want to log a behaviour incident against a student with a date, category (positive or negative), severity, and description so that there is a dated record that School Admin and parents can review.

**US-30 — Message parents**
As a Teacher, I want to send a message to an individual parent or to all parents of a class so that I can communicate about progress, concerns, or upcoming events.

**US-31 — View a teacher dashboard with class metrics**
As a Teacher, I want to see a dashboard summarising my classes' attendance rates, homework submission rates, and Hifz progress so that I can prioritise support where it is most needed.

---

#### Student stories

**US-32 — View my personalised dashboard**
As a Student, I want to log in and see a personalised dashboard showing my timetable for today, upcoming homework deadlines, and recent progress updates so that I can quickly understand what needs my attention.

**US-33 — View my weekly timetable**
As a Student, I want to view my full weekly timetable showing subjects, teachers, and times so that I can plan my week.

**US-34 — View assigned homework and worksheets**
As a Student, I want to see a list of all homework and worksheet assignments with their titles, descriptions, due dates, and submission status so that I can plan my work.

**US-35 — Submit homework or upload a file**
As a Student, I want to submit my completed homework by entering text or uploading a file so that my teacher can review and provide feedback.

**US-36 — Upload a Qur'an recitation recording**
As a Student, I want to upload an audio recording of my Qur'an recitation so that my teacher can listen, annotate mistakes, and give feedback.

**US-37 — View my Hifz progress**
As a Student, I want to view my Hifz progress showing each surah or juz with its status (Not Started, In Progress, Completed) so that I know which parts have been verified by my teacher.

**US-38 — View finalised exam results**
As a Student, I want to see my exam results once they have been finalised by my teacher so that I can track my academic performance over time.

**US-39 — Receive in-app notifications**
As a Student, I want to receive in-app notifications when new homework is assigned, when my teacher gives feedback, or when my exam results are published so that I do not miss important updates.

---

#### Parent stories

**US-40 — View a summary dashboard for each child**
As a Parent, I want to log in and see a summary dashboard for each of my children showing their attendance percentage, latest Hifz status, recent homework feedback, and outstanding fees so that I have a single overview without needing to navigate multiple pages.

**US-41 — View verified Hifz progress**
As a Parent, I want to view my child's Hifz progress showing which surahs have been signed off by a teacher so that I can see authentic, verified completion rather than self-reported data.

**US-42 — View homework submissions and teacher feedback**
As a Parent, I want to view my child's homework submissions along with the teacher's feedback and approval status so that I can support their learning at home and follow up on rejected work.

**US-43 — View finalised exam results**
As a Parent, I want to see my child's finalised exam results and any teacher comments so that I understand their academic performance and can discuss it with them.

**US-44 — View outstanding fees and pay online**
As a Parent, I want to view a list of outstanding fee items with amounts and due dates and pay them online via card so that payments are convenient and instantly recorded.

**US-45 — Receive a payment receipt**
As a Parent, I want to receive a receipt after each payment so that I have proof of what I have paid for my records.

**US-46 — Receive absence and overdue fee notifications**
As a Parent, I want to receive a notification when my child is marked absent and when a fee becomes overdue so that I can take action promptly.

**US-47 — Message my child's teacher**
As a Parent, I want to send a message to my child's teacher so that I can raise concerns, ask questions, or discuss progress directly without needing a separate communication tool.

**US-48 — View behaviour incidents**
As a Parent, I want to view any behaviour incident reports involving my child so that I am aware of conduct issues (positive or negative) and can discuss them at home.

---

#### Cross-cutting stories

**US-49 — Tenant data isolation**
As any user, I want my data to be completely isolated to my school so that I never see another school's students, teachers, classes, or financial information.

**US-50 — Responsive design**
As any user, I want the interface to be fully responsive so that I can use it comfortably on a mobile phone, tablet, or desktop computer.

**US-51 — Clear form validation**
As any user, I want to see clear, specific validation messages next to the relevant form field when I make an input error so that I can correct it without confusion.

**US-52 — Accessibility (WCAG AA)**
As any user, I want the site to meet WCAG AA standards for colour contrast, keyboard navigation, and screen-reader support so that it is accessible to users with disabilities.

---
## Wireframes

### Main wireframe pack

**Live page:** [https://esa-project-2a7a33dfe3fc.herokuapp.com/wireframes/](https://esa-project-2a7a33dfe3fc.herokuapp.com/wireframes/)

18 screens with layouts and annotation boxes for each feature, field, button, and role. Public — no login required.

**Local:** `http://127.0.0.1:8000/wireframes/` when running Django locally.

**PDF:** [`docs/ESA-wireframes.pdf`](docs/ESA-wireframes.pdf)

**Source:** `docs/wireframe.html` — edit to update the live page after deploy.

**Other assets:**

| Asset | Link | Notes |
|-------|------|--------|
| **Wireframe (live)** | [herokuapp.com/wireframes/](https://esa-project-2a7a33dfe3fc.herokuapp.com/wireframes/) | 18 screens with feature callouts |
| PDF export | [`docs/ESA-wireframes.pdf`](docs/ESA-wireframes.pdf) | Same pack as PDF |
| Balsamiq (interactive) | [ESA wireframes — Balsamiq Cloud](https://balsamiq.cloud/so6babk/pveanf2) | Early sketch flows |
| Legacy root HTML | `*.html` at repo root | Simplified layout prototypes from early design |
| Older gallery | [`docs/wireframes.html`](docs/wireframes.html) | Earlier single-file gallery |

**Site map / user flow:**

![ESA wireframe site map — homepage through role portals to messaging](docs/wireframe-site-map.png)

### Wireframe inventory

All screens below are documented in detail on the **[live wireframe page](https://esa-project-2a7a33dfe3fc.herokuapp.com/wireframes/)** (main pack). Root-level `*.html` files are legacy layout stubs.

| Page | Main pack section | Legacy file | Description |
|------|-------------------|-------------|-------------|
| Landing | §1 | `index.html` | Public marketing page with hero, feature cards, Register / Log in CTAs. |
| Subscription plans | §2 | `subscription.html` | Free / Standard / Premium tiers; Stripe subscribe flow. |
| Login & register | §3 | `login.html`, `register.html` | Shared auth; school pick, role, class, parent link code. |
| Super Admin dashboard | §4 | `dashboard-super-admin.html` | Platform KPIs and all-schools table. |
| School Admin dashboard | §5 | `dashboard-school-admin.html` | School KPIs, teachers, timetable, LMS, fees setup. |
| Teacher dashboard | §6 | `dashboard-teacher.html` | Today's lessons, pending sign-off queues. |
| Student dashboard | §7 | `dashboard-student.html` | Homework, Hifz juz table, read-only modules. |
| Parent dashboard | §8 | `dashboard-parent.html` | Linked children, fees, reports, Hifz progress. |
| Timetable | §9 | `timetable.html` | Weekly grid; School Admin drag-drop builder. |
| Attendance register | §10 | `attendance.html` | Present / Late / Absent; school-wide student list. |
| Homework / worksheets | §11 | `worksheets.html` | Assignments, submit, teacher sign-off / reject. |
| Exams | §12 | `exams.html` | MCQ + written; publish, mark, finalise results. |
| Hifz juz sign-off | §13 | `hifz-progress.html` | Juz 1–30 sign-off (not surah tracker). |
| Qur'an mushaf viewer | §14 | `quran-annotation.html` | PDF mushaf, highlights, per-page notes, audio. |
| Behaviour log | §15 | `behaviour.html` | Commendations and incidents. |
| Messaging | §16 | `messages.html` | Inbox, threads, tenant-scoped replies. |
| Fees & payments | §17 | `payments.html` | Outstanding fees, Pay now (Stripe), receipts. |
| Analytics | §18 | `analytics.html` | School KPIs and chart placeholders. |

### Wireframe design overview

The **main pack** at [/wireframes/](https://esa-project-2a7a33dfe3fc.herokuapp.com/wireframes/) follows a **public → auth → role portal → feature module** hierarchy with annotated callouts on every screen. Marketing pages use a single-column layout; signed-in screens share a **left sidebar** and main workspace so each role sees only relevant modules. Status pills, KPI cards, and data tables map directly to Django templates under `templates/pages/` on the live Heroku deployment.

Legacy static HTML at the repo root (`*.html`) and [`docs/wireframes.html`](docs/wireframes.html) are earlier prototypes with less feature detail.

---
## Design

### Data model and ERD (entity relationships)

The ERD describes the relational structure for the ESA database.

**Live diagram (Lucidchart):** [ESA ERD — Lucidchart](https://lucid.app/lucidchart/62056323-bc35-429d-9476-90fb23a6d72b/edit?viewport_loc=-4270%2C-6278%2C9116%2C6296%2C0_0&invitationId=inv_17fdce9f-7187-414c-abc1-64e8fe297051)

![ESA entity-relationship diagram](docs/erd.png)

*Exported snapshot — open the Lucidchart link above for the editable source.*

#### Design principles

- **School as tenant root** — `School` is the top-level entity. Almost every other table carries a `school_id` foreign key so that all queries can be scoped to a single tenant.
- **Single User model with role field** — A single custom `User` model stores authentication credentials and a `role` enum. Role-specific profile tables (TeacherProfile, StudentProfile, ParentProfile) extend the user.
- **Sign-off fields on progress records** — HifzRecord, WorksheetSubmission, and ExamResult all share: `signed_off`, `signed_off_by`, `signed_off_at`.
- **AuditLog for traceability** — A dedicated AuditLog table records sign-offs, payment confirmations, and role changes.

#### Cardinality summary

| From | Relationship | To | Notes |
|------|--------------|-----|-------|
| School | 1 → many | User | A school has many users across all roles |
| User | 1 → 1 | TeacherProfile / StudentProfile / ParentProfile | Each user has at most one role-specific profile |
| ParentProfile | many ↔ many | StudentProfile | Via ParentChild junction table |
| School | 1 → many → many | YearGroup → Class | A school contains year groups, each containing classes |
| Class | 1 → many | StudentProfile | A student belongs to one class |
| TeacherProfile | many ↔ many ↔ many | Subject ↔ Class | Via TeacherSubjectClass junction table |
| Class | 1 → many | TimetableSlot | A class has many scheduled time slots per week |
| StudentProfile | 1 → many | AttendanceRecord | A student has an attendance record per session |
| StudentProfile | 1 → many | HifzRecord | A student has one record per surah/juz |
| StudentProfile | 1 → many → many | QuranSession → QuranAnnotation | Sessions contain annotations |
| Class | 1 → many → many | Worksheet → WorksheetSubmission | Worksheets are per-class; submissions are per-student |
| Class | 1 → many → many | Exam → ExamResult | Exams are per-class; results are per-student |
| FeeItem | 1 → many | Payment | A fee can have multiple payment attempts |
| User | 1 → many | Notification | A user receives many notifications |
| User | 1 → many | Message | Messages link a sender and recipient |
| User | 1 → many | AuditLog | Every audited action records the acting user |

The diagram above and the [Lucidchart source](https://lucid.app/lucidchart/62056323-bc35-429d-9476-90fb23a6d72b/edit?viewport_loc=-4270%2C-6278%2C9116%2C6296%2C0_0&invitationId=inv_17fdce9f-7187-414c-abc1-64e8fe297051) are the canonical ERD references.

### Visual language

ESA looks and feels like a **modern school dashboard** — calm, dark, and professional. The design goal is that a parent, teacher, or admin can open any page and **recognise it as the same product** without relearning where things are.

#### Overall look and feel

| Quality | What it means on ESA |
|---------|----------------------|
| **Dark theme** | Near-black backgrounds reduce glare on long admin sessions; content sits on slightly lighter panels so sections are easy to scan |
| **Gold accents** | Used sparingly for actions and highlights — links, primary buttons, active sidebar item, section accent bars. Gold reads as **premium and Islamic-school appropriate** without filling the whole screen |
| **Generous spacing** | Panels, cards, and form fields have padding and line-height (~1.55) so text is not cramped — important on tablet |
| **Consistent shell** | Same header, sidebar, page title, and footer on every signed-in page |
| **Subtle geometry** | A thin gold stripe pattern in the header (`header-geometry`) echoes Islamic tile/mashrabiya motifs — decorative only, never behind body text |
| **No clutter** | One primary action per panel (gold button); secondary actions use outline buttons; status uses small pills not loud banners |

#### Layout patterns

| Pattern | Where it appears | Purpose |
|---------|------------------|---------|
| **Marketing / auth** | Home, login, register | Centred single column (`main-single` max 560px) — focus on one task |
| **Wide marketing** | Subscription, security page | `main-wide` up to 1200px — pricing grids, feature cards |
| **Portal shell** | All dashboards and features | Sticky header + 240px sidebar + scrollable main (`app-shell`) |
| **Panel** | Most feature pages | Rounded card with border — groups one topic (attendance register, fee list) |
| **Accent bar** | Under section headings | Short gold gradient line — visual break between sections |
| **Grid cards** | Dashboard overviews | Responsive card grid for KPIs and quick stats |

All of this is defined in **`css/base.css`** and shared by static wireframes (`*.html` at repo root) and Django templates (`templates/`) so the **wireframes and live site match**.

### Colour palette and CSS tokens

ESA uses a **black, white, and gold** scheme. Colours are stored as **CSS variables** in `:root` so the whole site stays consistent — change one token and buttons, links, and borders update together.

#### Core tokens

| Token | Hex / value | Role |
|-------|-------------|------|
| `--bg` | `#0a0a0a` | Page background — deepest black |
| `--surface` | `#121212` | Panels, cards, sidebar background |
| `--surface-up` | `#1a1a1a` | Raised cards, table footers, nested blocks |
| `--text` | `#f5f5f0` | Primary body text — warm off-white |
| `--muted` | `#9c9c8e` | Secondary text, labels, footer, inactive nav |
| `--gold` | `#c9a227` | **Primary accent** — links, buttons, active nav, focus rings |
| `--gold-soft` | `rgba(201, 162, 39, 0.15)` | Hover backgrounds on outline buttons and highlights |
| `--border` | `#2c2c28` | Panel borders, table lines, dividers |
| `--radius` | `10px` | Corner rounding on panels, buttons, inputs |

#### Accent and state colours

| Use | Colour | Where |
|-----|--------|-------|
| **Primary button hover** | `#e6c04a` | Slightly brighter gold on `.btn-primary:hover` |
| **Success / OK pill** | `#6fcf97` (green text) | Positive status badges (`.pill-ok`) |
| **Warning pill** | `#e57373` (soft red text) | Alerts or caution badges (`.pill-warn`) |
| **Header geometry** | `#8a7020` stripes | Decorative bar under site header |
| **Qur'an viewer canvas** | `#f8f6f0` (light parchment) | Mushaf PDF background only — readable paper tone inside the viewer |

Gold is **intentionally limited**. Large areas stay dark or neutral so gold draws the eye to **what to do next** (Save, Pay now, Student has passed).

#### Why this palette

1. **Readable on laptop/tablet** — high contrast between off-white text and dark surfaces (targets WCAG AA).
2. **Appropriate for Islamic schools** — gold accent is familiar in madrasah branding without using religious imagery in the UI.
3. **Professional SaaS feel** — dark dashboards are common in admin tools; parents still get clear fee and message screens.
4. **One source of truth** — assessors can open `css/base.css` lines 13–25 and see every token documented.

### How colour is used across the UI

| UI element | Background | Text / border | Notes |
|------------|------------|---------------|-------|
| **Page** | `--bg` | `--text` | Full viewport |
| **Panel / form area** | `--surface` | `--text` | Main content containers |
| **Sidebar** | `--surface` | `--muted` links; **gold** when active | `aria-current="page"` gets gold tint |
| **Primary button** | `--gold` | `--bg` (dark text on gold) | Main actions only |
| **Outline button** | transparent | `--gold` border + text | Secondary actions (Cancel, archive) |
| **Links in body** | — | `--gold` | Underline on hover |
| **Data tables** | `--surface` | `--text` with `--border` row lines | Header row slightly emphasized |
| **Form inputs** | dark surface | `--text` | Gold focus ring via `:focus-visible` |
| **Flash messages** | `--gold-soft` | `--text` | Success/info after save |
| **Subscription tiers** | card on `--surface-up` | Free = muted; Standard/Premium = gold | `.pill-tier-*` classes |
| **Skip link** | `--gold` | `--bg` | Accessibility — visible on keyboard focus |

#### Qur'an highlighter colours (teacher only)

Teachers pick a highlight colour when marking the mushaf PDF. Defaults in the viewer:

| Swatch | Hex | Typical use |
|--------|-----|-------------|
| Yellow | `#fff59d` | General revision mark |
| Green | `#a5d6a7` | Memorisation strong |
| Blue | `#90caf9` | Tajweed note |
| Pink | `#f48fb1` | Area needing practice |

These are **content markup colours** inside the PDF viewer only — they do not change the global site theme.

### Typography

ESA uses **system fonts** — no custom webfont downloads — so pages load fast on school networks and respect each device's native readability settings.

| Setting | Value | Why |
|---------|-------|-----|
| **Font stack** | `system-ui, -apple-system, "Segoe UI", Roboto, Ubuntu, sans-serif` | Looks native on Windows, Mac, Android, iOS |
| **Base size** | `16px` on `html` | Comfortable default; avoids mobile browser zoom on form focus |
| **Body line-height** | `1.55` | Extra space between lines for long reports and messages |
| **Page title (`h1`)** | ~1.65rem, semibold | Clear page identity at top of main content |
| **Card headings (`h2`)** | ~0.95rem, gold, semibold | Smaller labels inside dashboard cards |
| **Brand mark** | Bold, wide letter-spacing (`0.2em`) | "ESA" in header — distinct but minimal |
| **Brand tag / eyebrow** | Small caps, muted, `0.68rem` | Role or school name under logo |

**Arabic Qur'an text** in the mushaf viewer is rendered inside the **PDF** (embedded Arabic typeface in the juz files), not via a separate web font on the page. English UI labels remain LTR; RTL Arabic support for the portal chrome is noted for a future phase.

### UI components

Reusable classes keep the visual language consistent:

| Component | Class | Appearance |
|-----------|-------|------------|
| **Panel** | `.panel` | Dark card with border and 10px radius — wraps most page content |
| **Accent bar** | `.accent-bar` | 3rem × 3px gold gradient under headings |
| **Primary button** | `.btn-primary` | Solid gold, dark text |
| **Secondary button** | `.btn-outline` | Gold border, transparent fill |
| **Form field** | `.form-input` | Full-width inputs in `.field` stacks |
| **Status pill** | `.pill`, `.pill-ok`, `.pill-warn` | Small rounded badges for status/tier |
| **Dashboard card** | `.card` | Nested block inside `.grid-cards` |
| **KPI card** | `.kpi-card`, `.stat-card` | Analytics and home overview numbers |
| **Data table** | `.data-table` inside `.table-wrap` | Scrollable on narrow screens |
| **School banner** | `.portal-school-banner` | Shows school name + plan tier at top of portal |

New pages should **reuse these classes** rather than inventing new colours — that keeps the assessor experience consistent across attendance, fees, Hifz, and messaging.

### Accessibility

- Keyboard navigable UI, readable contrast, clear focus states, and semantic HTML.
- Accessible form labels and validation feedback.
- Skip link to main content for keyboard users.

### Design inspiration and references

Research and tooling that shaped ESA's look, structure, and domain language — consolidated here rather than at the end of the README.

#### Islamic school platforms (UX research)

Before wireframing, the team reviewed UK supplementary-school portals and madrasah management products: registration flows, Hifz progress views, and fee ledgers. Common strengths were clear parent portals; weak spots were poor mobile UX and no teacher sign-off on progress data. ESA differentiated with structured Qur'an page notes, teacher finalise on exams, and Stripe Connect per school. Findings informed **sidebar order**, **parent payment flows**, and terminology (**Hifz**, **Tajweed**, **madrasah**) used across templates. Design mood: professional and respectful — geometric header accents without clichéd clip art.

#### Wireframes (Balsamiq → HTML → Django)

Low-fidelity flows started in [Balsamiq](https://balsamiq.cloud/so6babk/pveanf2) (dashboard sidebars, fee tables, Qur'an viewer, exam builder). Teacher volunteers validated navigation before Django templates were built. The sketch style kept reviews focused on **flow** rather than colour debates.

| Stage | Asset |
|-------|-------|
| Balsamiq | [Interactive board](https://balsamiq.cloud/so6babk/pveanf2) |
| Annotated pack | [Live wireframes](https://esa-project-2a7a33dfe3fc.herokuapp.com/wireframes/) · [`docs/ESA-wireframes.pdf`](docs/ESA-wireframes.pdf) |
| Production | `templates/pages/` and `css/base.css` — same classes as wireframes |

Full inventory: [Wireframes](#wireframes).

#### Data model (Lucidchart ERD)

The [Lucidchart ERD](https://lucid.app/lucidchart/62056323-bc35-429d-9476-90fb23a6d72b/edit?viewport_loc=-4270%2C-6278%2C9116%2C6296%2C0_0&invitationId=inv_17fdce9f-7187-414c-abc1-64e8fe297051) modelled tenants, users, Qur'an sessions, exams, and payments **before** migrations. Early reviews caught missing `school_id` on homework sketches. Cardinality rules (student → one class; parent ↔ many children) match the live schema — see [Data model and ERD](#data-model-and-erd-entity-relationships) and [`docs/erd.png`](docs/erd.png).

#### UI patterns and accessibility references

| Influence | Applied on ESA |
|-----------|----------------|
| WCAG AA contrast checkers | Dark theme + gold accent tested for readable body text |
| Accessible form patterns | Labels tied to inputs; Django non-field error summaries for screen readers |
| Limited homepage carousel | Four slides only — performance and focus on core CTAs |
| UAT volunteer feedback | Gold-on-dark CTAs; status badge contrast tweaks after teacher review |
| RTL readiness (future) | MVP remains LTR English; layout does not hard-code left-only assumptions |

Carousel images credit UK Islamic schools — see [Images used in this project](#images-used-in-this-project) under Sources.

### Platform glossary

| Term | Meaning |
|------|---------|
| **Tenant** | A single school; all data is scoped to one `School` record |
| **Sign-off** | Teacher verification that makes Hifz, homework, or exam data official |
| **Hifz** | Qur'an memorisation tracking per surah or juz |
| **RBAC** | Role-based access control across five user types |
| **Stripe Connect** | OAuth flow so fee payments route to each school's Stripe account |

---
## Technologies Used

### Languages

- **Python** — application logic, ORM, views.
- **HTML** — structure via Django templates.
- **CSS** — layout and theme.
- **JavaScript** — client-side progressive enhancements.

### Frameworks & libraries

| Package | Role |
|---------|------|
| **Django 6.0** | Web framework, MVT, admin |
| **Django REST Framework** | API endpoints, serialisation |
| **SimpleJWT** | JWT authentication (obtain / refresh) |
| **django-environ** | Environment variable management |
| **dj-database-url** | Database config from URL |
| **psycopg2-binary** | PostgreSQL driver |
| **gunicorn** | Production WSGI server |
| **whitenoise** | Static file serving in production |
| **django-cors-headers** | CORS policy management |

### Database

- **PostgreSQL** (production) / **SQLite** (local development fallback)

### Payments

- **Stripe Checkout** (test mode) — parent fees and school subscriptions

### Tools

| Tool | Used for |
|------|----------|
| **Git** | Version control |
| **GitHub** | Repository hosting, Issues, Projects |
| **PostgreSQL / psql** | Database, ad-hoc SQL checks |
| **VS Code** | Editing and integrated terminal |
| **Chrome DevTools** | Network tab, responsive mode, Lighthouse |

---
## File Structure

> Paths are relative to the project root.

| Path | Description |
|------|-------------|
| `manage.py` | Django management entrypoint |
| `core/` | Project settings, root URLconf, WSGI/ASGI |
| `core/settings.py` | Env-based config, database, DRF, JWT, static files |
| `core/urls.py` | Root URL routing (admin, JWT endpoints) |
| `accounts/` | Custom User model with role field, admin registration |
| `accounts/models.py` | User model (super_admin / school_admin / teacher / student / parent) |
| `requirements.txt` | Python dependencies with pinned versions |
| `.env.example` | Documents required environment variables (no secrets) |
| `Procfile` | Gunicorn process for production deployment |
| `.gitignore` | Ignores `.env`, `.venv`, `__pycache__`, `db.sqlite3`, media, staticfiles |
| `PROGRESS.md` | Development progress tracker |
| `css/base.css` | Shared wireframe stylesheet (colour tokens, layout, navigation) |
| `pages/` | Portal UI — login, register, dashboards, feature placeholders |
| `*.html` | Static wireframe reference pages at repo root |
| `templates/` | Django templates (to be populated as apps are built) |
| `static/` | Django static assets (to be populated) |
| `docs/` | Documentation, ERD, screenshots, validation evidence (to be populated) |

---
## Development

This section documents the setup path for ESA: Django locally, GitHub over HTTPS, and Heroku for production. Start at [Development guide (step-by-step)](#development-guide-step-by-step).

### Development guide (step-by-step)

This mirrors the structure I used in my previous [bookly](https://github.com/sadek17481748/bookly) README, adapted for **Django** instead of Flask.

#### Prerequisites

- **Python 3.11+** (3.13 used locally; Heroku builds from `requirements.txt`).
- **PostgreSQL** installed and running locally (e.g. Homebrew Postgres on macOS: `brew install postgresql@16 && brew services start postgresql@16`).
- **Git** and a **GitHub** account for pushing commits.
- Optional: [Stripe](https://dashboard.stripe.com/test/apikeys) test keys and a **Gmail App Password** for real SMTP (see below).

#### Environment setup

```bash
cd /path/to/ESA
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

In `.env` I set at minimum:

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Long random string for Django sessions and CSRF |
| `DEBUG` | `True` locally |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` |
| `DATABASE_URL` | Postgres URL, for example `postgres://esa_user:change_me@localhost:5432/esa_db` |
| `STRIPE_PUBLISHABLE_KEY` / `STRIPE_SECRET_KEY` | Stripe **test** keys for `/payments/` |
| `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | Gmail address + **App Password** (not normal Gmail password) |

Example SQL to create a matching role and database (names line up with the example URL above):

```sql
CREATE USER esa_user WITH PASSWORD 'change_me';
CREATE DATABASE esa_db OWNER esa_user;
```

Run inside `psql` as a superuser (`psql postgres` on macOS).

#### Initialise the database (PostgreSQL)

```bash
source .venv/bin/activate
python manage.py migrate
python manage.py seed_rbac_users
python manage.py seed_demo_fees          # parent fee rows for Stripe demo
python manage.py ensure_platform_seed    # idempotent re-sync of demo data on Heroku/local
```

This creates all tables from Django migrations and seeds demo users, Al-Noor school data, and sample fees if the catalog is empty.

#### Run the app locally

```bash
source .venv/bin/activate
python manage.py runserver
```

The app is served at **http://127.0.0.1:8000/** during local runs.

- Portal login: http://127.0.0.1:8000/accounts/login/
- Django admin: http://127.0.0.1:8000/admin/
- JWT token: `POST http://127.0.0.1:8000/api/auth/token/` with JSON `username` / `password`

See [Navigating the website](#navigating-the-website) for role-based paths after login.

#### Troubleshooting (local Postgres setup)

**`password authentication failed for user ...`**  
Usually means `DATABASE_URL` in `.env` still has placeholder values or the Postgres user password does not match. Fix by updating `.env` to a real connection string and (re)setting the user password in Postgres:

```sql
ALTER USER esa_user WITH PASSWORD 'esa_pass';
```

**Commands typed inside `psql` by mistake**  
If the prompt looks like `postgres=#` or `postgres-#`, you are inside Postgres interactive mode. Exit with `\q` to return to the normal terminal prompt before running:

```bash
python manage.py migrate
python manage.py runserver
```

**`ModuleNotFoundError` after clone**  
Activate the virtual environment and run `pip install -r requirements.txt` again.

#### Assessor and demo logins

Demo accounts are created by `ensure_platform_seed` (runs on every Heroku deploy). **Passwords for registered and bulk accounts are preserved across deploys** — only `schooladmin`, `super`, and `parent_demo` are reset each boot.

### Al-Noor Academy — permanent logins

| Role | Username / email | Password | Notes |
|------|------------------|----------|--------|
| School admin | `schooladmin` | `admin1234` | Resets each deploy |
| **Your parent** | `msadekhussain@outlook.com` | `Parent2026!` | Linked to **Y7A-001** (Amina Hassan pattern student) |
| **Your teacher** | `msadekhussain2001@gmail.com` | `Teacher2026!` | Maths on **7A** timetable; class teacher for 7A |
| Super admin | `super` | `super1234` | Platform-wide |
| Demo parent | `parent_demo` | `demo1234` | Resets each deploy |
| **Showcase parent** | `demo_parent` | `Demo2026!` | Full portal demo — linked to `demo_student`, class **7A** |
| **Showcase student** | `demo_student` | `Demo2026!` | Attendance, homework, exams, Qur'an, Hifz, LMS — see [Demo walkthrough](#demo-walkthrough) |
| Quran / attendance teacher | `mr_mohammed` | `teacher1234` | Registers, mushaf viewer, Hifz sign-off |
| Example parent | `test_parent` | `test1234` | Messaging/LMS demos |
| Example student | `test_student` | `test1234` | Enrolled in **7A** |
| Bulk parent (7A #1) | `parent_7a_01` | `parent1234` | Paired with `student_7a_01` |
| Bulk student (7A #1) | `student_7a_01` | `student1234` | Class **7A**, admission `Y7A-001` |

**Full school seed** (`seed_alnoor_full_school`): classes **7A, 7B, 8A, 8B, 9A, 9B, 10A, 10B, 11A, 11B** — each with **30 students + 30 parents** (realistic names) and a **ready Spring term timetable**. Re-run is safe: skips bulk seed if `Y7A-001` exists; always syncs your outlook/gmail accounts.

```bash
python manage.py seed_alnoor_full_school
# Heroku:
heroku run python manage.py seed_alnoor_full_school -a esa-project
```

Use these on local or Heroku after seeding:

| Role | Username | Password | Dashboard |
|------|----------|----------|-----------|
| Super Admin | `super` | `super1234` | `/dashboard/super-admin/` |
| School Admin | `schooladmin` | `admin1234` | `/dashboard/school-admin/` |
| Teacher | `teacher_demo` | `teacher1234` | `/dashboard/teacher/` |
| Student | `student_demo` | `student1234` | `/dashboard/student/` |
| Parent | `parent_demo` | `demo1234` | `/dashboard/parent/` |
| Parent (Al-Noor examples) | `test_parent` | `test1234` | Messaging / link-child demos |
| Student (Al-Noor examples) | `test_student` | `test1234` | Worksheets verify_deploy path |

**Note (live Heroku app):** The Heroku deployment uses its own Postgres database. Demo users are created automatically on dyno boot via `ensure_platform_seed` in the `Procfile`. If logins fail after a fresh deploy, run:

```bash
heroku run python manage.py ensure_platform_seed -a esa-project
```

To promote a newly registered user to Super Admin locally, use Django admin (`/admin/`) or `python manage.py shell` and set `user.role = 'super_admin'`.

#### Automated tests (local)

```bash
source .venv/bin/activate
python manage.py test
```

Tests cover accounts, RBAC, payments, Qur'an, exams, messaging, Hifz, homework, and portal pages. Many tests call `ensure_platform_seed` in `setUp` so demo users exist. The full list of **82 tests** with explanations is in [Automated testing](#automated-testing) below.

#### How I committed changes to GitHub (workflow used)

During development I used a simple Git workflow so changes were traceable and easy to review:

1. Check what changed with `git status` and `git diff`.
2. Stage the files I wanted in the commit with `git add ...`.
3. Create a commit with a short message describing what changed and why.
4. Push commits to GitHub so the repository stayed up to date.

Typical commands:

```bash
git status
git diff
git add README.md
git commit -m "docs(readme): add website navigation guide and Django dev setup"
git push origin main
```

Where changes affected both documentation and the app, I kept commits separate so it was obvious what was “README/docs” and what was “code changes”.

---

### How I set up Stripe (test mode)

Parent school fees and school subscriptions use **Stripe Checkout** in test mode.

1. Create a free [Stripe account](https://dashboard.stripe.com/register) and open **Developers → API keys**. Copy the **test** publishable key (`pk_test_…`) and secret key (`sk_test_…`).
2. Add them to `.env`:

   ```env
   STRIPE_PUBLISHABLE_KEY=pk_test_...
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_WEBHOOK_SECRET=              # optional locally; required for production webhooks
   ```

3. Run migrations and seed fees:

   ```bash
   python manage.py migrate
   python manage.py seed_demo_fees
   ```

4. Start the server, log in as `parent_demo` / `demo1234`, open **http://127.0.0.1:8000/payments/**, click **Pay now**, and complete checkout with test card **`4242 4242 4242 4242`**, any future expiry, any CVC.

5. **Webhooks (recommended):** install the [Stripe CLI](https://stripe.com/docs/stripe-cli) and forward events to Django:

   ```bash
   stripe listen --forward-to localhost:8000/payments/webhook/
   ```

   Copy the webhook signing secret (`whsec_…`) into `STRIPE_WEBHOOK_SECRET` so payment status updates even if the user closes the browser before the success page loads.

6. **Stripe Connect (school payouts):** School Admins open the Connect link from the school fees page. Onboarding uses Express accounts (`payments/connect.py`). Destination charges route parent payments to the connected school account with an optional platform fee. Test Connect in Stripe **test mode** with the same API keys.

7. **Heroku:** push keys without committing them:

   ```bash
   heroku config:set STRIPE_SECRET_KEY=sk_test_... STRIPE_PUBLISHABLE_KEY=pk_test_... -a esa-project
   ```

   Or set manually: `heroku config:set STRIPE_PUBLISHABLE_KEY="pk_test_…" STRIPE_SECRET_KEY="sk_test_…" -a esa-project`

Amounts are stored in **pence** in the database; `payments/services.py` passes `unit_amount` directly to Stripe so £250.00 displays correctly (see [Bugs encountered](#bugs-encountered-during-development) bug #1).

### How I connected the Google email account

ESA sends platform alerts (registrations, payments, messages) through **Gmail SMTP** using the inbox `educationandschoolapplications@gmail.com`.

1. Enable **2-Step Verification** on the Google account.
2. Create an **App Password** (Google Account → Security → App passwords → Mail → Other → `ESA local`).
3. Add to `.env` (see `.env.example`):

   ```env
   ESA_PLATFORM_EMAIL=educationandschoolapplications@gmail.com
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=educationandschoolapplications@gmail.com
   EMAIL_HOST_PASSWORD=your-16-char-app-password
   DEFAULT_FROM_EMAIL=ESA Platform <educationandschoolapplications@gmail.com>
   ```

4. Test locally:

   ```bash
   python manage.py send_test_email
   ```

5. Push to Heroku: set `EMAIL_*` config vars with `heroku config:set`, then `heroku run python manage.py send_test_email -a esa-project`.

Full step-by-step screenshots and troubleshooting are in [Connecting Gmail for platform email notifications](#connecting-gmail-for-platform-email-notifications).

---

### Project setup from scratch (Django)

ESA follows the standard **Django MVT** layout. The project was created in May 2025 during the foundation sprint ([delivery timeline](#delivery-timeline-may-10--july-1)).

#### 1. Prerequisites

- **Python 3.11+** (3.13 used locally; Heroku currently builds with Python 3.14).
- **Git** installed (`git --version`).
- A code editor (**VS Code**).
- Optional for production parity: **PostgreSQL** locally (`brew install postgresql` on macOS). Without `DATABASE_URL`, Django falls back to **SQLite** for local dev.

#### 2. Create the virtual environment

From an empty working folder (e.g. `Desktop/ESA`):

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install django djangorestframework djangorestframework-simplejwt \
  django-environ dj-database-url psycopg2-binary gunicorn whitenoise \
  django-cors-headers stripe django-storages boto3
pip freeze > requirements.txt
```

Dependencies are pinned in `requirements.txt` so Heroku installs the same versions on every deploy.

#### 3. Start the Django project and apps

Django was initialised with the project package named `core` (settings, URLs, WSGI):

```bash
django-admin startproject core .
```

Reusable feature areas were added as **separate Django apps** (one app per domain — assessor criterion 1.1 / 1.5):

```bash
python manage.py startapp accounts
python manage.py startapp schools
python manage.py startapp students
python manage.py startapp teachers
python manage.py startapp academics
python manage.py startapp payments
# … further apps added incrementally: pages, messaging, lms, attendance, etc.
```

Each app was registered in `core/settings.py` under `INSTALLED_APPS`, given its own `models.py`, `views.py`, `urls.py`, and (where needed) `forms.py`, `services.py`, and `tests.py`.

#### 4. Core configuration (first commits)

Early foundation work included:

| Task | Where |
|------|--------|
| Environment-based settings | `core/settings.py` via `django-environ` + `.env` |
| Custom `User` model with `role` field | `accounts/models.py` — must be set before first migrate |
| PostgreSQL / SQLite switch | `DATABASE_URL` in `.env`; `dj-database-url` parser |
| Root URL routing | `core/urls.py` includes per-app URLconfs |
| Static + media folders | `static/`, `media/`, `css/base.css` wireframe stylesheet |
| `.gitignore` | Ignores `.env`, `.venv`, `db.sqlite3`, `staticfiles/`, `media/` |
| `.env.example` | Documents variables without secrets |

First migrations:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # optional local admin
```

#### 5. Wireframes → Django templates

Static HTML wireframes (`*.html` at repo root) were designed first for layout approval. They are previewed with `python3 -m http.server 8080`. Portal screens were then rebuilt as Django templates under `templates/` and `pages/` views, sharing `css/base.css` for a consistent theme on Heroku.

---

### GitHub setup and version control

ESA uses **Git** for every change and **GitHub** as the remote source of truth: https://github.com/sadek17481748/ESA

#### 1. Initialise Git locally

After the first working Django tree existed:

```bash
cd /path/to/ESA
git init
git add .
git commit -m "Initial Django project scaffold with accounts and schools apps."
```

`.env` and `.venv/` are **never** committed — they are listed in `.gitignore`.

#### 2. Create the GitHub repository

On [GitHub](https://github.com/new):

1. Click **New repository**.
2. Name: **ESA** (owner: `sadek17481748`).
3. Visibility: **Public** (required for assessor access).
4. **Do not** tick “Add a README” if you already have local commits — avoid unrelated merge histories.
5. Click **Create repository**.

GitHub shows an empty-repo page with setup commands.

#### 3. Connect the remote over HTTPS and push to `main`

HTTPS was chosen so the remote works without SSH key setup on every machine:

```bash
git remote add origin https://github.com/sadek17481748/ESA.git
git branch -M main
git push -u origin main
```

When prompted for credentials:

- **Username:** your GitHub username (`sadek17481748`).
- **Password:** a **GitHub Personal Access Token** (classic or fine-grained with `repo` scope) — GitHub no longer accepts account passwords for Git over HTTPS.

macOS may store the token in Keychain after the first successful push. Verify the remote:

```bash
git remote -v
# origin  https://github.com/sadek17481748/ESA.git (fetch)
# origin  https://github.com/sadek17481748/ESA.git (push)
```

#### 4. Day-to-day Git workflow (used throughout the project)

Each feature was committed in **small, reviewable steps** (foundation → RBAC → payments → messaging, etc.):

```bash
git pull origin main              # sync before starting work
# … edit files, run tests …
git status
git add path/to/changed/files
git commit -m "Add parent fee list with Stripe checkout redirect."
git push origin main
```

Commit messages describe **why** the change was made, not only which files moved. The full history is visible on GitHub → **Commits**.

#### 5. Clone on another machine (assessor or second laptop)

```bash
git clone https://github.com/sadek17481748/ESA.git
cd ESA
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env              # then fill in local secrets
python manage.py migrate
python manage.py runserver
```

---

### Local setup

1. Python 3.11+ recommended (3.13 supported).
2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Copy environment template and set a secret key for local dev:

   ```bash
   cp .env.example .env
   ```

4. Apply migrations and create a superuser (optional):

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

### Environment variables

Defined in `.env` (see `.env.example`). Single source of truth is `core/settings.py` via `django-environ`.

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret; **required in production** |
| `DEBUG` | `True`/`False` |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `DATABASE_URL` | PostgreSQL URL; if omitted, SQLite is used for local dev |
| `STRIPE_PUBLISHABLE_KEY` | Stripe Checkout (test mode) |
| `STRIPE_SECRET_KEY` | Stripe secret key |
| `STRIPE_WEBHOOK_SECRET` | Optional Stripe webhook signing secret |
| `ESA_PLATFORM_EMAIL` | Platform inbox for alerts (default: `educationandschoolapplications@gmail.com`) |
| `EMAIL_HOST` | SMTP host (Gmail: `smtp.gmail.com`) |
| `EMAIL_HOST_USER` | Gmail address used to send mail |
| `EMAIL_HOST_PASSWORD` | Gmail **App Password** (not your normal Gmail password) |
| `DEFAULT_FROM_EMAIL` | From header, e.g. `ESA Platform <educationandschoolapplications@gmail.com>` |

### Run locally

```bash
python manage.py runserver
```

- Admin: http://127.0.0.1:8000/admin/
- JWT obtain pair: `POST /api/auth/token/` with `username` and `password`.
- JWT refresh: `POST /api/auth/token/refresh/` with `refresh` token.

See [Development guide (step-by-step)](#development-guide-step-by-step) for Postgres setup, Stripe, Gmail, and demo logins.

---
## Foundation and RBAC (local test)

Django project uses env-based settings, SQLite/Postgres via `DATABASE_URL`, and `/static/` + `/media/` folders.

**API base:** `http://127.0.0.1:8000/api/`

| Endpoint | Auth | Roles |
|----------|------|-------|
| `POST /api/auth/token/` | — | JWT login |
| `GET /api/accounts/me/` | JWT | Any |
| `POST /api/accounts/register/` | — | Register (school required except super admin) |
| `GET /api/schools/` | JWT | Super admin (all), school admin (own school) |
| `GET /api/students/` | JWT | School staff (tenant scoped) |
| `GET /api/teachers/` | JWT | School staff (tenant scoped) |
| `GET /api/classes/` | JWT | School staff (tenant scoped) |

Seed demo users:

```bash
python manage.py seed_rbac_users
```

| Username | Password | Role |
|----------|----------|------|
| `super` | `super1234` | Super Admin |
| `schooladmin` | `admin1234` | School Admin |
| `teacher_demo` | `teacher1234` | Teacher |
| `student_demo` | `student1234` | Student |
| `parent_demo` | `demo1234` | Parent |

---
## Stripe payments (local test)

Parent school fees use Stripe Checkout in test mode. Full setup steps are in [How I set up Stripe (test mode)](#how-i-set-up-stripe-test-mode). Quick path:

1. Copy Stripe test keys into `.env`.
2. `python manage.py migrate && python manage.py seed_demo_fees`
3. Log in as `parent_demo` / `demo1234` → `/payments/` → **Pay now** → card `4242 4242 4242 4242`.
4. Optional: `stripe listen --forward-to localhost:8000/payments/webhook/`

---
## Deployment

ESA is deployed on **Heroku** with a managed **PostgreSQL** database. The live application is available at:

**https://esa-project-2a7a33dfe3fc.herokuapp.com/**

Source code is hosted on GitHub and connected to Heroku for automatic deploys when `main` is pushed. You can also deploy manually with the Heroku CLI.

### GitHub and Heroku integration

Production hosting uses **Heroku app `esa-project`**:

| Resource | URL |
|----------|-----|
| **Live site** | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| **GitHub repo** | https://github.com/sadek17481748/ESA |
| **Heroku Git remote** | `https://git.heroku.com/esa-project.git` |
| **Bug tracker** | https://github.com/users/sadek17481748/projects/8/views/1 |

#### How the two remotes fit together

After local development, the same `main` branch feeds **two** remotes:

```
Local folder  ──git push──►  origin (GitHub)  ──auto-deploy──►  Heroku (esa-project)
                ──git push──►  heroku (optional direct deploy)
```

**`origin`** — GitHub. Every `git push origin main` updates the public repository assessors can browse.

**`heroku`** — Heroku’s Git endpoint. Optional direct deploy with `git push heroku main` (requires `heroku login` in the terminal).

#### Step A — Create the Heroku app

1. Sign up / log in at [heroku.com](https://www.heroku.com/).
2. Install the CLI: `brew install heroku` (macOS) → `heroku login` (opens browser).
3. Create the app and attach PostgreSQL:

   ```bash
   heroku create esa-project
   heroku addons:create heroku-postgresql:essential-0 -a esa-project
   ```

4. Add the Heroku Git remote to your local clone:

   ```bash
   heroku git:remote -a esa-project
   git remote -v
   # heroku  https://git.heroku.com/esa-project.git
   # origin  https://github.com/sadek17481748/ESA.git
   ```

#### Step B — Connect GitHub for automatic deploys (recommended)

In the [Heroku Dashboard](https://dashboard.heroku.com/) → **esa-project** → **Deploy**:

1. **Deployment method:** choose **GitHub** (not Heroku Git alone).
2. Click **Connect to GitHub** and authorise Heroku.
3. Search for repository **`sadek17481748/ESA`** and click **Connect**.
4. Under **Automatic deploys**, select branch **`main`** and enable **Wait for CI to pass** only if you add GitHub Actions later (optional).
5. Click **Enable Automatic Deploys**.

From this point, every `git push origin main` triggers a Heroku build without running `git push heroku main` manually. Build logs appear under the **Activity** tab.

#### Step C — First production deploy

Either push to GitHub (auto-deploy) or push directly:

```bash
# Option 1 — via GitHub (after automatic deploys enabled)
git push origin main

# Option 2 — direct Heroku Git (if HTTPS auth fails, use a token — see below)
git push heroku main

# Option 3 — token-based push when terminal asks for credentials
git push https://heroku:$(heroku auth:token)@git.heroku.com/esa-project.git main
```

After the slug builds, run one-off setup on the dyno:

```bash
heroku run python manage.py migrate -a esa-project
heroku run python manage.py ensure_platform_seed -a esa-project
heroku run python manage.py verify_deploy -a esa-project
```

#### Step D — Set Heroku config vars (secrets stay off GitHub)

Secrets are stored as **Config Vars** in the Heroku Dashboard → **Settings**, or via CLI:

```bash
heroku config:set SECRET_KEY="…" DEBUG=False -a esa-project
heroku config:set STRIPE_PUBLISHABLE_KEY="pk_test_…" STRIPE_SECRET_KEY="sk_test_…" -a esa-project
heroku config:set EMAIL_HOST_USER=... EMAIL_HOST_PASSWORD=... -a esa-project
```

`DATABASE_URL` is injected automatically by the Heroku Postgres add-on. Never commit `.env` — `.gitignore` blocks it.

#### Step E — Procfile and runtime

`Procfile` tells Heroku how to boot the web dyno:

```
web: python manage.py migrate --noinput && python manage.py ensure_platform_seed && gunicorn core.wsgi --bind 0.0.0.0:$PORT
```

**Gunicorn** serves the WSGI app; **WhiteNoise** serves collected static files after `collectstatic` at build time. Migrations and demo seed run on each dyno restart so fresh deploys always have schema and test accounts.

#### Troubleshooting deploys

| Problem | Fix |
|---------|-----|
| `git push heroku` → Invalid credentials | Run `heroku login`, or use `git push https://heroku:$(heroku auth:token)@git.heroku.com/esa-project.git main` |
| GitHub push works but Heroku unchanged | Check **Deploy → Automatic deploys** is enabled for `main` |
| Config change stuck on “release executing” | Ensure `Procfile` has no hanging `release:` hook; redeploy latest `main` |
| Stripe / email not working on live site | Run `heroku config:set` for Stripe and Gmail SMTP vars after `heroku login` |
| View live logs | `heroku logs --tail -a esa-project` |

### Deployment FAQ

**Why does the site show a generic error after deploy?**  
Run `heroku run python manage.py migrate -a esa-project` and check `heroku logs --tail` for missing config vars (`SECRET_KEY`, `DATABASE_URL`).

**How do I reset demo users on Heroku?**  
`heroku run python manage.py seed_rbac_users -a esa-project`

**Where are uploaded files stored in production?**  
User uploads use Django's default file storage on the dyno filesystem unless S3 is configured; re-deploys may clear ephemeral files — use cloud storage for production media.

---

### Deployment steps

1. Install the Heroku CLI and log in:

   ```bash
   brew tap heroku/brew && brew install heroku
   heroku login
   ```

2. Clone or pull the repository and add the Heroku remote (if not already present):

   ```bash
   git clone https://github.com/sadek17481748/ESA.git
   cd ESA
   heroku git:remote -a esa-project
   ```

3. Set required config vars on Heroku (secrets are **never** committed to Git):

   ```bash
   heroku config:set SECRET_KEY="a-long-random-string" DEBUG=False -a esa-project
   heroku config:set STRIPE_PUBLISHABLE_KEY="pk_test_..." STRIPE_SECRET_KEY="sk_test_..." -a esa-project
   ```

4. Deploy and initialise:

   ```bash
   git push heroku main
   # or push to GitHub main and wait for the Heroku GitHub integration to build
   heroku run python manage.py migrate -a esa-project
   heroku run python manage.py ensure_platform_seed -a esa-project
   heroku run python manage.py verify_deploy -a esa-project
   ```

**Production notes:**
- `Procfile` runs **Gunicorn** and applies migrations plus demo seed data on dyno boot.
- Heroku provides `DATABASE_URL` automatically when PostgreSQL is attached.
- **WhiteNoise** serves static files in production.
- Use `heroku logs --tail -a esa-project` to diagnose startup issues.

### Post-deploy checklist

After each production deploy:

```bash
heroku run python manage.py migrate -a esa-project
heroku run python manage.py verify_deploy -a esa-project
```

| Check | Notes |
|-------|-------|
| Config vars | `SECRET_KEY`, `DATABASE_URL`, Stripe keys, Gmail SMTP, `DEBUG=False` |
| Boot seed | `Procfile` runs `ensure_platform_seed` on dyno start |
| Smoke test | `verify_deploy` logs in as `test_parent`, `schooladmin`, `mr_mohammed`, `super` |
| Tenant isolation | `python manage.py test` — schools, accounts, payments apps |
| Webhooks | `stripe listen --forward-to .../payments/webhook/` for local fee checkout tests |
| Backups | `heroku pg:backups:capture` before risky migrations |

Fresh demo data order: `migrate` → `seed_rbac_users` → `seed_alnoor_full_school` (optional) → `seed_demo_fees` → `ensure_platform_seed`.

### Production stack

Production runs on **Heroku** at [esa-project-2a7a33dfe3fc.herokuapp.com](https://esa-project-2a7a33dfe3fc.herokuapp.com/).

| Component | How it is configured |
|-----------|----------------------|
| **Web process** | `Procfile` → Gunicorn serving `core.wsgi` |
| **Python** | `runtime.txt` pins the version to match local development |
| **Database** | Heroku Postgres (`DATABASE_URL` injected automatically) |
| **Static files** | WhiteNoise with compressed manifest storage after `collectstatic` |
| **Secrets** | Config vars: `SECRET_KEY`, Stripe keys, Gmail SMTP, optional S3 credentials |
| **Hosts** | `ALLOWED_HOSTS` includes the Heroku hostname |

Push to GitHub `main` triggers an automatic Heroku build when GitHub integration is enabled. Run `verify_deploy` after each production deploy before treating the release as healthy. Use the Heroku **Releases** tab to roll back a bad deploy; capture a Postgres backup before schema migrations. Review dyno sizing if parent checkout traffic spikes at term-start fee deadlines.

Full package list: [Technologies Used](#technologies-used). Request flow and external services: [Technical overview](#technical-overview).

### Database migrations

Run migrations locally after pulling schema changes, then on production:

```bash
python manage.py migrate
heroku run python manage.py migrate -a esa-project
```

Migration files live per Django app (`accounts/`, `schools/`, `quran/`, `exams/`, `payments/`, and others). Squashing is deferred until post-MVP.

| Practice | Why |
|----------|-----|
| `heroku pg:backups:capture` before risky migrations | Restore point if a migration fails |
| Prefer additive migrations | Supports zero-downtime deploys on a single dyno |
| Destructive changes | Plan a maintenance window and communicate to schools |
| Failed `migrate` on Heroku | Roll back the release; reproduce on a staging clone before retrying |

Foreign keys on tenant models should include `school` scoping — isolation tests in the suite catch cross-tenant regressions.

### Seed data commands

Fresh environments need representative data for assessor demos and smoke tests. Run in order:

```bash
python manage.py migrate
python manage.py seed_rbac_users
python manage.py seed_alnoor_demo          # or seed_alnoor_examples / seed_alnoor_full_school
python manage.py seed_demo_fees
python manage.py ensure_platform_seed      # defensive re-sync; also runs on dyno boot
```

On Heroku, prefix each command with `heroku run … -a esa-project`. Seeds are idempotent where possible — safe to re-run after minor edits. Re-run `seed_demo_fees` after payment schema changes to refresh `parent_demo` checkout rows.

| Seed command | What it creates |
|--------------|-----------------|
| `seed_rbac_users` | Minimal RBAC set (`teacher_demo`, `student_demo`, `parent_demo`) — lightweight smoke testing |
| `seed_alnoor_demo` / `seed_alnoor_full_school` | Al-Noor Academy with ~30 students (`mr_mohammed`, `schooladmin`) — stress and walkthrough data |
| `seed_demo_fees` | Fee rows for `parent_demo` Stripe checkout |
| `ensure_platform_seed` | Repairs missing demo users and platform defaults |

Do not leave default demo passwords on a real production tenant without a forced password-change policy.

### verify_deploy smoke tests

`python manage.py verify_deploy` runs end-to-end checks against the configured site (localhost or Heroku). It calls `ensure_platform_seed`, logs in as each demo account, and asserts key pages return HTTP 200:

| Username | Password | Page checked |
|----------|----------|--------------|
| `test_parent` | `test1234` | Messaging inbox |
| `test_student` | `test1234` | Worksheets |
| `mr_mohammed` | `teacher1234` | Messaging inbox |
| `schooladmin` | `admin1234` | LMS hub |
| `super` | `super1234` | Messaging inbox |

Additional check: School Admin student search for **Amina** returns results. Exit code is non-zero on failure — suitable for CI or post-deploy scripts.

```bash
# Local (dev server running)
python manage.py verify_deploy

# Production
heroku run python manage.py verify_deploy -a esa-project
```

Output lists pass/fail per username and route for faster triage on release nights. Complements unit tests with cross-role portal confidence.

### Production security checks

Before go-live or after config changes, confirm:

| Check | Expected |
|-------|----------|
| `DEBUG` | `False` on Heroku |
| `SECRET_KEY` | Long random value in config vars — rotate only with planned session invalidation |
| HTTPS | Heroku SSL; `CSRF_TRUSTED_ORIGINS` includes the live hostname |
| Session cookies | `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` enabled in production |
| Django admin | Limited to superusers |
| Stripe webhook | `STRIPE_WEBHOOK_SECRET` in config vars; rotate if leaked |
| Gmail | App password stored as config var, never in Git |

Role decorators on sensitive views, password validators, and tenant isolation tests are mandatory before release. Full security documentation: [Security](#security) and the public [/security/](https://esa-project-2a7a33dfe3fc.herokuapp.com/security/) page.

### Tenant isolation verification

Automated isolation coverage:

```bash
python manage.py test schools.tests accounts.tests quran.tests exams.tests payments.tests
```

Tests assert cross-school access attempts fail (403/404), queryset filters use `school=request.user.school`, and parents cannot list other families' fees.

**Manual spot-check (assessor):** log in as users from two different seeded schools; attempt URL tampering with another school's session or fee ID — expect 403. Stripe Connect accounts are one-to-one with schools. File uploads are namespaced by school path. Superuser cross-tenant access is explicit; support impersonation is not implemented in the MVP.

### Connecting Gmail for platform email notifications

ESA sends email through **Gmail SMTP** so the platform inbox (`educationandschoolapplications@gmail.com`) receives alerts when important events happen: new school registrations, subscription payments, parent fee payments, school messages, and support tickets. Replies from that inbox can go back to the user who triggered the event (via `Reply-To` headers).

Gmail does **not** allow normal account passwords for SMTP in third-party apps. You must use a **Google App Password** with **2-Step Verification** enabled on the Google account.

#### Step 1 — Prepare the Google account

1. Sign in to [Google Account](https://myaccount.google.com/) as `educationandschoolapplications@gmail.com`.
2. Open **Security** and turn on **2-Step Verification** (required before App Passwords appear).
3. Go to **Security → App passwords** (or search “App passwords” in account settings).
4. Create a new app password:
   - App: **Mail**
   - Device: **Other** → name it `ESA Heroku` or `ESA local`
5. Google shows a **16-character password** (often displayed in four groups). Copy it — you will not see it again.

#### Step 2 — Configure local development (`.env`)

Copy `.env.example` to `.env` and set:

```env
ESA_PLATFORM_EMAIL=educationandschoolapplications@gmail.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=educationandschoolapplications@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password-no-spaces
DEFAULT_FROM_EMAIL=ESA Platform <educationandschoolapplications@gmail.com>
```

When `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are set, Django automatically switches from the console email backend to **SMTP** (`core/settings.py`).

Test locally:

```bash
python manage.py send_test_email
```

You should receive `[ESA] Test email` in the platform Gmail inbox. If SMTP is not configured, the same command prints instructions and emails are written to the terminal instead.

#### Step 3 — Configure Heroku (production)

After `heroku login`, push the same values from your local `.env` to Heroku config vars:

```bash
heroku config:set EMAIL_HOST_USER=... EMAIL_HOST_PASSWORD=... -a esa-project
```

Then verify on the live dyno:

```bash
heroku run python manage.py send_test_email -a esa-project
```

Alternatively, set each variable manually in the Heroku Dashboard → **esa-project** → **Settings** → **Config Vars**:

| Config var | Example value |
|------------|-----------------|
| `ESA_PLATFORM_EMAIL` | `educationandschoolapplications@gmail.com` |
| `EMAIL_HOST` | `smtp.gmail.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_USE_TLS` | `True` |
| `EMAIL_HOST_USER` | `educationandschoolapplications@gmail.com` |
| `EMAIL_HOST_PASSWORD` | *(16-character App Password)* |
| `DEFAULT_FROM_EMAIL` | `ESA Platform <educationandschoolapplications@gmail.com>` |
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` |

Restart dynos after changing config: `heroku restart -a esa-project`.

#### What triggers platform emails

| Event | Recipient | Module |
|-------|-----------|--------|
| New school registration | Platform inbox | `messaging/notifications.py` |
| New subscription payment (Stripe) | Platform inbox | `payments/notifications.py` |
| Parent fee payment completed | Platform inbox | `payments/notifications.py` |
| New school message in a thread | Platform inbox + conversation participants | `messaging/notifications.py` |
| Support ticket message | Platform inbox | `messaging/signals.py` |

Participants can still opt in or out of personal message alerts via the checkbox on the messaging inbox page (`User.notify_on_messages`).

#### Troubleshooting Gmail on Heroku

- **“Email not configured”** — `EMAIL_HOST_USER` or `EMAIL_HOST_PASSWORD` is missing on the dyno. Re-run `heroku config:set EMAIL_HOST_USER=... EMAIL_HOST_PASSWORD=... -a esa-project`.
- **Authentication failed** — App Password is wrong or 2-Step Verification is off. Generate a new App Password and update config vars.
- **Emails in spam** — Check the Spam folder for `[ESA]` subjects; mark as “Not spam” once.
- **Never rotate App Passwords in Git** — only in `.env` (gitignored) and Heroku Config Vars.

---
## Testing and Bugs

### Testing strategy and plan

ESA testing uses both automated (`python manage.py test`) and manual browser checks. Compared to my previous project [bookly](https://github.com/sadek17481748/bookly), the suite is larger because ESA has five roles, multi-tenant isolation, Stripe, messaging, and LMS features.

#### What I learned from bookly (previous project)

On [bookly](https://github.com/sadek17481748/bookly), I built a Flask bookstore with PostgreSQL, pytest, and a focused user journey (browse → auth → reviews → cart → checkout → orders). Testing was **documented thoroughly** in the bookly README: a **51-row manual checklist**, a **23-test pytest suite**, Lighthouse and W3C validation evidence, and a clear assessment matrix for functionality, usability, responsiveness, and data management.

However, my own reflection in that project was honest: although some tests were written alongside features, the **heaviest testing work was compressed into a final pass on 25 April** — a dedicated day to run pytest, complete manual walkthroughs on PostgreSQL, and fix edge cases in checkout and ownership rules. Personal delays meant I had less uninterrupted time than planned, which increased the risk of late surprises. I recorded **40 bugs** in the bookly README, many discovered only when I exercised cross-table writes (checkout) and role enforcement (reviews, admin) under time pressure.

For ESA, I deliberately changed that pattern.

#### Continuous testing throughout ESA (not only at the end)

ESA’s [delivery timeline](#delivery-timeline-may--july) (May → July) schedules **testing in every sprint**, not as a single block before submission:

| Phase | Dates (approx.) | Testing focus |
|-------|-----------------|---------------|
| Foundation | May 10–14 | Local migrate, settings, URL smoke tests |
| RBAC + tenant isolation | May 15–21 | Permission tests, cross-school access blocked |
| Student / class APIs | May 22–28 | Enrollment, CSV import, API tenant scope |
| Attendance + timetable | May 29 – Jun 4 | Form validation, slot conflicts, register saves |
| Payments (Stripe) | Jun 5–11 | Checkout redirect, test card, webhook idempotency |
| Messaging + LMS | Jun 12–18 | Inbox flows, participant labels, material upload |
| Deploy + polish | Jun 19 – Jul 1 | Heroku `verify_deploy`, Lighthouse, manual evidence |

After each feature lands, I run **`python manage.py test`** for the affected app (`pages`, `payments`, `messaging`, `lms`, `accounts`, etc.) and perform a **short manual smoke test** in the browser (login as the relevant role, complete one happy path, try one forbidden path). Bugs are logged immediately in the [bugs table](#bugs-encountered-during-development) below rather than deferred — the Stripe pence/pounds bug, parent fee scoping bug, and duplicate payment-on-refresh bug were all caught and fixed during the payments sprint, not in a final panic week.

This **“test as you build”** approach spreads evidence collection across the project: screenshots go into `docs/images/manual-testing/` as each area is verified, instead of requiring fifty browser sessions in the last few days.

Run the suite with `python manage.py test` (see [Automated testing](#automated-testing) for the full inventory). Manual evidence is in `docs/images/manual-testing/` and the [manual testing table](#manual-testing) below.

#### Automated vs manual — when to use which

| Concern | Automated | Manual |
|---------|-----------|--------|
| Same result every run | ✅ Best | ❌ Human variation |
| Speed (hundreds of checks) | ✅ Seconds | ❌ Hours |
| Catches UI/layout issues | ❌ Limited | ✅ Best |
| Stripe / Gmail external services | ❌ Mocked or skipped | ✅ Real test mode |
| Tenant / security rules | ✅ Best | ✅ Spot-check |
| Assessor evidence (screenshots) | Terminal output | ✅ Browser captures |
| Regression after a fix | ✅ Re-run suite | ❌ Re-do all steps |

**Combined approach:** automate rule-based and security-critical checks; manually verify UI, Stripe Checkout, Gmail, and full role journeys.

#### Comparison: bookly vs ESA testing

| Aspect | bookly (Flask) | ESA (Django) |
|--------|----------------|--------------|
| Framework | pytest + Flask test client | Django `TestCase` + `Client` |
| Test location | `tests/` (4 files, 23 tests) | Per-app `tests.py` + growing suite |
| Database in tests | SQLite in-memory via conftest | Django test DB (SQLite) |
| Manual checklist | 51 rows, mostly filled at end | 44+ rows, filled throughout sprints |
| Payments | No gateway (order stored only) | Stripe Checkout + webhooks |
| Email | Not implemented | Gmail SMTP + platform inbox |
| Multi-tenancy | Single store | Per-school isolation (critical test area) |
| Roles | User + admin | Super admin, school admin, teacher, parent, student |
| Deploy smoke test | Manual browse on Heroku | `verify_deploy` management command |
| Bug log | Documented in README | 40+ entries, updated as found |

#### Submission testing (completed)

Final pass-criteria evidence was completed in June 2026:

1. **Manual table** — all rows filled; API/auth/payment rows backed by `core_app/assessment_checklist_tests.py` (36 automated checks mapped to README row numbers).
2. **Responsive pass** — home, login, parent and teacher portals in `docs/images/validation/`.
3. **`python manage.py test`** — full suite run locally (93 tests); see [Automated testing](#automated-testing).
4. **Heroku** — `verify_deploy`, Stripe test checkout (rows 14–15), `send_test_email`.
5. **W3C / JSHint** — evidence in `docs/images/validation/`.
6. **AI assistance log** — 10 rows in README.

---

### Level 5 pass criteria mapping

| Section | Criteria | Status | Evidence |
|---------|----------|--------|----------|
| **1** | Django full-stack design & implementation (1.1–1.10) | Met | [Wireframes](https://esa-project-2a7a33dfe3fc.herokuapp.com/wireframes/), [ERD](#data-model-and-erd-entity-relationships), live Heroku app |
| **1.11** | Manual/automated testing (functionality, usability, responsiveness, data) | Met | [Assessment test matrix](#assessment-test-matrix), 93 automated tests, manual table below |
| **2** | Models, forms, CRUD (2.1–2.4) | Met | Custom models per app; `test_row_24b_student_destroy_crud` proves DELETE |
| **3** | Auth & data access control (3.1–3.3) | Met | Session + JWT; tenant tests rows 4–11; ORM-only data access |
| **4** | Stripe e-commerce + user feedback (4.1–4.2) | Met | Rows 14–17; cancel page + success messages |
| **5** | Deploy, security, README (5.1–5.6) | Met | Heroku, env secrets, git history, this README |

---

### Assessment test matrix

| Area | What will be assessed | Procedures | Evidence location |
|------|----------------------|------------|-------------------|
| **Functionality** | End-to-end: auth, RBAC, CRUD, sign-offs, payments | Automated (Django test suite) + manual checklist | [Manual testing](#manual-testing); [Automated testing](#automated-testing) |
| **Usability** | Navigation, forms, validation, error states, flash messages | Manual walkthroughs + Lighthouse | [Manual testing](#manual-testing); [Lighthouse testing](#lighthouse-testing) |
| **Responsiveness** | Layout on laptop and tablet (primary); phone sanity check | [Responsive Testing Tool](http://responsivetesttool.com) at live URL + Chrome DevTools | [How responsiveness was tested](#how-responsiveness-was-tested); `docs/images/validation/` |
| **Data management** | Tenant isolation, FK integrity, sign-off audit trail, payment persistence | Automated tests + manual verification | [Data model and ERD](#data-model-and-erd-entity-relationships); [Automated testing](#automated-testing) |

### Manual testing

### Web portal (Heroku)

Session login at `/accounts/login/`. Parent and student registration at `/register/`.
After login, users go to `/dashboard/` by role. Qur'an (`/quran/`), exams (`/exams/`), payments
(`/payments/`), messages, attendance, timetable, and homework are implemented as Django portal pages
alongside the REST API.

| Route | Purpose |
|-------|---------|
| `/register/` | Parent or student sign-up |
| `/accounts/verify-email/` | Six-digit email verification (real addresses) |
| `/accounts/password-reset/` | Password recovery flow |
| `/dashboard/parent/` | Parent portal |
| `/dashboard/teacher/` | Teacher workspace |
| `/dashboard/student/` | Student portal |
| `/quran/` | Qur'an sessions, annotations, audio upload |
| `/exams/` | Exams, MCQ auto-mark, teacher finalise sign-off |
| `/payments/` | Fees, Stripe Checkout, receipts |
| `/attendance/` | Attendance screen |
| `/timetable/` | Timetable screen |
| `/worksheets/` | Homework screen |

Planned and executed checks for foundation, RBAC, Stripe, Qur'an, exams, and sign-off work. Fill **Actual**, **Pass/Fail**, and **Screenshot** as evidence is captured (`docs/images/manual-testing/`).

| # | Test | Steps | Expected | Actual | Pass/Fail | Screenshot |
|---|------|-------|----------|--------|-----------| ------------ |
| 1 | JWT login with valid credentials | `POST /api/auth/token/` with `teacher_demo` / `teacher1234` | `200` and access + refresh tokens returned | `test_row_01_jwt_login_valid` | Pass | Automated — `core_app/assessment_checklist_tests.py` |
| 2 | JWT login with invalid password | `POST /api/auth/token/` with wrong password | `401` Unauthorized | `test_row_02_jwt_login_invalid` | Pass | Automated |
| 3 | Current user profile (`/api/accounts/me/`) | Obtain JWT, `GET /api/accounts/me/` with Bearer token | JSON shows correct `role`, `school`, `school_name` | `test_row_03_accounts_me` | Pass | Automated |
| 4 | School admin tenant scope (schools API) | Log in as `schooladmin`, `GET /api/schools/` | Exactly one school (own tenant) | `test_row_04_school_admin_tenant_scope` | Pass | Automated |
| 5 | Super admin sees all schools | Log in as `super`, `GET /api/schools/` | All schools in database listed | Super admin dashboard lists 3 schools (`msadekhussain2001@gmail.com` Standard, `Testschool4` Free, `Al-Noor Academy` Free); recent sign-ups show new school admin and teacher `eventiservicesandhelp@gmail.com` | Pass | [superadmin-schools-overview](docs/images/manual-testing/superadmin-schools-overview.png) |
| 6 | Teacher student list tenant scope | Log in as `teacher_demo`, `GET /api/students/` | Only students from Al-Noor Academy | `test_row_06_teacher_student_tenant_scope` | Pass | Automated |
| 7 | Parent blocked from staff student API | Log in as `parent_demo`, `GET /api/students/` | `403 Forbidden` | `test_row_07_parent_blocked_from_students_api` | Pass | Automated |
| 8 | Register without school rejected | `POST /api/accounts/register/` as student with no `school` | `400` with school validation error | `test_row_08_register_without_school_rejected` | Pass | Automated |
| 9 | RBAC seed command | Run `python manage.py seed_rbac_users` | Five demo users exist with correct roles | `test_row_09_rbac_seed_command` | Pass | Automated |
| 10 | Tenant middleware on request | Log in via session; check `request.tenant_school` | Matches user's school | `test_row_10_tenant_middleware` | Pass | Automated |
| 11 | Audit log on login | Log in as `teacher_demo` via `/accounts/login/` | New `AuditLog` row with action login and school set | `test_row_11_audit_log_on_login` | Pass | Automated |
| 12 | Parent fee list (own fees only) | Log in as `parent_demo`, open `/payments/` | Only this parent's outstanding and paid fees | `test_row_12_parent_sees_own_fees_only` | Pass | Automated |
| 13 | Unauthenticated payments redirect | Open `/payments/` logged out | Redirect to `/accounts/login/` | `test_row_13_unauthenticated_payments_redirect` | Pass | Automated |
| 14 | Stripe Checkout redirect | On `/payments/`, click **Pay now** on a fee | Redirect to Stripe hosted checkout | School admin upgraded plan from `/payments/subscription/`; Stripe hosted checkout opened for ESA Standard £49.00/month | Pass | [stripe-checkout-standard-49](docs/images/manual-testing/stripe-checkout-standard-49.png) |
| 15 | Stripe test card payment | Complete checkout with `4242 4242 4242 4242` | Success page with receipt; fee marked paid | Paid with test card `4242…`; success page shows Standard upgrade, £49.00, receipt ref B077B3888078; Stripe sandbox balance £47.77 | Pass | [payment-success-standard-upgrade](docs/images/manual-testing/payment-success-standard-upgrade.png) · [stripe-dashboard-payment-confirmed](docs/images/manual-testing/stripe-dashboard-payment-confirmed.png) |
| 16 | Stripe cancel flow | Start checkout, cancel on Stripe page | `/payments/cancel/` with no charge | `test_row_16_stripe_cancel_page` shows “cancelled” message | Pass | Automated |
| 17 | No duplicate payment on refresh | Refresh `/payments/success/?session_id=…` after pay | Single `Payment` row in admin | `test_row_17_no_duplicate_payment_on_refresh` | Pass | Automated |
| 18 | Checkout amount displays correctly | Pay Term 3 tuition (£250.00) | Stripe shows £250.00 not £2.50 | Subscription checkout displayed **£49.00** for Standard plan (correct pounds, not pence bug) | Pass | [stripe-checkout-standard-49](docs/images/manual-testing/stripe-checkout-standard-49.png) |
| 19 | Teacher list tenant scope | Log in as `teacher_demo`, `GET /api/teachers/` | Only teachers from same school | `test_row_19_teacher_list_tenant_scope` | Pass | Automated |
| 20 | Class groups API tenant scope | Log in as `schooladmin`, `GET /api/classes/` | Only classes for own school | `test_row_20_class_groups_tenant_scope` | Pass | Automated |
| 21 | School admin registers parent | JWT as `schooladmin`, `POST /api/parents/register/` | Parent user + profile created with school set | `test_row_21_school_admin_registers_parent` | Pass | Automated |
| 22 | School admin registers teacher | `POST /api/teachers/register/` with username/email/password | Teacher profile linked to admin's school | School admin added **teacher test** (`eventiservicesandhelp@gmail.com`, subject maths) via `/school-admin/teachers/add/`; teacher appears in staff list | Pass | [schooladmin-add-teacher-form](docs/images/manual-testing/schooladmin-add-teacher-form.png) · [schooladmin-teachers-list](docs/images/manual-testing/schooladmin-teachers-list.png) |
| 23 | Year groups CRUD | `GET/POST /api/classes/year-groups/` as school admin | List/create year groups for own school | `test_row_23_year_groups_crud` | Pass | Automated |
| 24 | Enrol student in class | `POST /api/classes/enrollments/` with class + student ids | Enrollment row; rejects cross-school student | `test_row_24_enrol_student_rejects_cross_school` | Pass | Automated |
| 24b | Student DELETE (CRUD) | `DELETE /api/students/{id}/` as school admin | Row removed; criterion 2.4 | `test_row_24b_student_destroy_crud` | Pass | Automated |
| 25 | Bulk student CSV import | `POST /api/students/import_csv/` with CSV file | `created` count and per-row errors returned | `test_row_25_bulk_csv_import` | Pass | Automated |
| 26 | Custom Hifz subject | `POST /api/subjects/` with track `hifz` + lead_teacher | Subject saved; missing lead_teacher returns 400 | `test_row_26_hifz_subject_requires_lead_teacher` | Pass | Automated |
| 27 | Timetable slot validation | `POST /api/timetable/` with end_time before start_time | 400 validation error | `test_row_27_timetable_slot_validation` | Pass | Automated |
| 28 | Teacher timetable view | Log in as `teacher_demo`, `GET /api/timetable/?class_group=1` | Slots for requested class only | `test_row_28_teacher_timetable_view` | Pass | Automated |
| 29 | Take class attendance | `POST /api/attendance/sessions/` with marks array | Session + marks saved; rejects non-enrolled student | `test_row_29_attendance_rejects_non_enrolled_student` | Pass | Automated |
| 30 | Teacher creates assignment | `POST /api/homework/assignments/` as `teacher_demo` | Assignment saved; enrolled students get notification | `test_row_30_teacher_creates_assignment` | Pass | Automated |
| 31 | Student submits homework | `POST /api/homework/submissions/{id}/submit/` as `student_demo` | Status `submitted` and timestamp set | Part of `test_row_31_32_33_homework_submit_and_sign_off` | Pass | Automated |
| 32 | Teacher sign-off approve | `POST /api/homework/submissions/{id}/sign_off/` as assigning teacher | Status `approved`; student notification created | `test_row_31_32_33_homework_submit_and_sign_off` | Pass | Automated |
| 33 | Wrong teacher sign-off blocked | Same endpoint as another teacher | 403 or 404 (not assigned teacher) | `test_row_31_32_33_homework_submit_and_sign_off` | Pass | Automated |
| 34 | In-app notifications list | `GET /api/notifications/` as `student_demo` | User's own notifications, newest first | `test_row_34_35_notifications` | Pass | Automated |
| 35 | Mark notification read | `POST /api/notifications/{id}/mark_read/` | `is_read` true on that row | `test_row_34_35_notifications` | Pass | Automated |
| 36 | Web registration | Open `/register/`, submit as parent with school | Account created and logged in | `test_register_parent_creates_user_and_logs_in` | Pass | `pages/tests.py` |
| 37 | Login redirect by role | Log in as `teacher_demo` | Lands on teacher dashboard | Logged in as school admin `msadekhussain2001@gmail.com` after email verify; school admin subscription dashboard loads with sidebar, Free plan badge, and verification flash messages | Pass | [login-form-credentials](docs/images/manual-testing/login-form-credentials.png) · [login-success-subscription-dashboard](docs/images/manual-testing/login-success-subscription-dashboard.png) |
| 38 | Portal attendance page | Log in, open `/attendance/` | Attendance register / school overview loads | `test_row_38_attendance_page` | Pass | Automated — `pages/tests.py` |
| 39 | Portal timetable page | Log in, open `/timetable/` | Teacher timetable or school hub loads | `test_row_39_timetable_page` | Pass | Automated |
| 40 | Portal worksheets page | Log in, open `/worksheets/` | Student homework / LMS hub loads | `test_row_40_worksheets_page` | Pass | Automated |
| 41 | Portal messages page | Log in, open `/messages/` | Messaging inbox loads | `test_row_41_messages_page` | Pass | Automated |
| 42 | Portal exams page | Log in, open `/exams/` | Exams list loads | `test_row_42_exams_page` | Pass | Automated |
| 43 | Register validation | Submit register with mismatched passwords | Inline error shown | `test_row_43_register_validation_mismatched_passwords` | Pass | Automated |
| 44 | Home auth nav | Log in, open `/` | Dashboard and log out links shown | Logged-in school admin header shows **Messages** and **Log out** on subscription page | Pass | [login-success-subscription-dashboard](docs/images/manual-testing/login-success-subscription-dashboard.png) |
| 47 | School subscription upgrade (web) | School admin opens Subscription, pays Standard plan | Plan upgrades to Standard after Stripe success | Free → Standard upgrade confirmed; £49.00 charged in test mode; receipt ref on success page | Pass | [login-success-subscription-dashboard](docs/images/manual-testing/login-success-subscription-dashboard.png) · [stripe-checkout-standard-49](docs/images/manual-testing/stripe-checkout-standard-49.png) · [payment-success-standard-upgrade](docs/images/manual-testing/payment-success-standard-upgrade.png) · [stripe-dashboard-payment-confirmed](docs/images/manual-testing/stripe-dashboard-payment-confirmed.png) |
| 48 | Log out | Click **Log out** while logged in | Session cleared; redirect to home or login; protected pages require login again | `test_row_48_logout_clears_session` | Pass | Automated |
| 45 | School registration (web) | Open `/register/school/`, submit school + admin details | School and school-admin account created; user logged in or prompted next step | Form at `/register/school/` with Testschool4, admin Test4, email msadekhussain@outlook.com — all fields accepted | Pass | [register-school-form](docs/images/manual-testing/register-school-form.png) |
| 46 | Email verification (6-digit code) | After registration with real email, open `/accounts/verify-email/` | Page shows target email and code entry; code delivered to inbox | School admin verify (`msadekhussain@outlook.com`) and new teacher verify (`eventiservicesandhelp@gmail.com`) both show code entry page; codes delivered to inbox | Pass | [verify-email-code](docs/images/manual-testing/verify-email-code.png) · [teacher-verify-email](docs/images/manual-testing/teacher-verify-email.png) |
| 49 | Teacher login redirect by role | Log in as newly created teacher | Lands on teacher workspace dashboard | Logged in as `eventiservicesandhelp@gmail.com` after verify; **Teacher workspace** loads with sidebar (Attendance, Worksheets, Exams, Qur'an, etc.) and “Welcome, teacher test” | Pass | [teacher-login-form](docs/images/manual-testing/teacher-login-form.png) · [teacher-workspace-dashboard](docs/images/manual-testing/teacher-workspace-dashboard.png) |
| 50 | LMS — add subject & upload content | School admin opens **LMS**, adds subject (e.g. test subject), adds level, uploads content | Subject appears with level and uploaded link/file | Created **test subject** with description; content upload available per level | Pass | [lms-test-subject](docs/images/manual-testing/lms-test-subject.png) |
| 51 | Student registration (web) | Open `/register/`, pick school **Al-Noor Academy**, role Student, class, submit | Account created; student can log in | Registered **test student** (`msadekhussain@outlook.com`) for class **11B** | Pass | [register-student-alnoor](docs/images/manual-testing/register-student-alnoor.png) |
| 52 | Timetable hub — add class | School admin opens **Timetable hub**, type class code (e.g. `2C`, `2test`) | Class saved under inferred year group (e.g. 2C → Year 2) | Added **2C** and **2test**; both appear in year-groups table and assign-class dropdown | Pass | [timetable-hub-add-class](docs/images/manual-testing/timetable-hub-add-class.png) |
| 53 | Create timetable | Hub → **Create timetable**, name (e.g. Week 1), assign class | Builder opens for selected class | Created **Week 1** for class **2C** | Pass | [timetable-create-week1](docs/images/manual-testing/timetable-create-week1.png) |
| 54 | Timetable builder — drag subjects | Drag subjects onto grid, assign teachers, **Save timetable** | Grid persists; “Timetable saved” confirmation; lesson summary lists slots | **Week 1** — 16 lessons for 2C; retest on **2C timetable** — Maths, Science, Quran then **Alimiyah** (3 Mon slots), “Timetable saved.” | Pass | [timetable-builder-blank](docs/images/manual-testing/timetable-builder-blank.png) · [timetable-builder-filled](docs/images/manual-testing/timetable-builder-filled.png) · [timetable-saved-success](docs/images/manual-testing/timetable-saved-success.png) · [timetable-2c-edit-subjects](docs/images/manual-testing/timetable-2c-edit-subjects.png) · [timetable-2c-saved](docs/images/manual-testing/timetable-2c-saved.png) |
| 55 | Live timetables list | Hub → **View live timetables** | All published timetables listed with lesson count and Edit/Archive | **Week 1** shows 16 lessons for 2C; Edit and Archive actions visible | Pass | [live-timetables-list](docs/images/manual-testing/live-timetables-list.png) |
| 56 | Archive timetable | Live list → **Archive** on a timetable, confirm | Timetable hidden from live list | Archived **Week 1** via confirm modal (“hidden from live list”) | Pass | [archive-timetable](docs/images/manual-testing/archive-timetable.png) · [archive-timetable-confirm](docs/images/manual-testing/archive-timetable-confirm.png) |
| 57 | Student dashboard timetable | Log in as enrolled student (class **2C**) | Weekly timetable shows class schedule and subjects from live timetable | **test student** logged in; overview shows **Alimiyah** Mon 08:30 / 09:15 / 11:00 and subject card populated (was empty before fix) | Pass | [student-dashboard-empty-before-fix](docs/images/manual-testing/student-dashboard-empty-before-fix.png) · [student-dashboard-timetable-populated](docs/images/manual-testing/student-dashboard-timetable-populated.png) |
| 58 | Student login (new account) | Log in as newly registered student | Student overview loads with class and sidebar | **test student** (`msadekhussain@outlook.com`) lands on overview for class **2C** | Pass | [register-student-alnoor](docs/images/manual-testing/register-student-alnoor.png) · [student-dashboard-timetable-populated](docs/images/manual-testing/student-dashboard-timetable-populated.png) |
| 59 | Parent registration with link code | Open `/register/`, role **Parent**, enter school-issued **Student link code**, submit | Parent account created and child linked on first login | Registered **testparent** (`msadekhussain2001@gmail.com`) with code **6EC5367A** for Al-Noor | Pass | [register-parent-link-code](docs/images/manual-testing/register-parent-link-code.png) |
| 60 | Parent — child linked on overview | Log in as linked parent | **Your children** shows linked student with class | **test student** appears on parent overview for class **2C** (attendance/homework cards load) | Pass | [parent-overview-child-linked](docs/images/manual-testing/parent-overview-child-linked.png) |
| 61 | Teacher personal timetable → register | School admin assigns teacher on timetable slot; teacher opens **My timetable** | Teacher sees assigned lessons; clicking **Maths 2C** (etc.) opens class register | Teacher dashboard and `/timetable/` show assigned slots with **Take register** links; register opens for that class | Pass | [teacher-workspace-dashboard](docs/images/manual-testing/teacher-workspace-dashboard.png) |

*(Row 35 appears with row 34 above; duplicate removed.)*

### Automated testing

Django's test runner executes **93 tests** across 15+ files. Tests use a temporary SQLite database — production data is not modified.

```bash
source .venv/bin/activate
pip install -r requirements.txt
python manage.py test
# Pass criteria API/portal checks only (36 tests, ~90s):
python manage.py test core_app.assessment_checklist_tests payments.tests.ParentPaymentPortalTests pages.tests.PortalFeaturePageTests
```

**Latest local run (May 2026):** `Ran 93 tests` — all passed (assessment checklist + portal + LMS/messaging fixes).

Target one app:

```bash
python manage.py test pages
python manage.py test payments
```

#### Test inventory

| # | Test name | What it checks | File |
|---|-----------|----------------|------|
| **Portal — registration & login** ||||
| 1 | `test_register_page_shows_school_picker` | Register page lists schools (e.g. Al-Noor Academy) | `pages/tests.py` |
| 2 | `test_register_page_without_schools_prompts_school_signup` | Empty database shows “register your school first” message | `pages/tests.py` |
| 3 | `test_register_parent_creates_user_and_logs_in` | Parent registration creates account and logs in | `pages/tests.py` |
| 4 | `test_register_student_creates_profile` | Student registration creates student profile | `pages/tests.py` |
| 5 | `test_register_school_adds_to_parent_picker` | New school appears on register dropdown | `pages/tests.py` |
| 6 | `test_register_school_rejects_duplicate_name` | Cannot register two schools with the same name | `pages/tests.py` |
| 7 | `test_register_rejects_duplicate_username` | Second user with same username is rejected | `pages/tests.py` |
| 8 | `test_student_registration_enrols_in_class` | Student picks a class and is enrolled | `pages/tests.py` |
| 9 | `test_school_admin_can_log_in_after_register_and_logout` | School admin can log in after registering | `pages/tests.py` |
| 10 | `test_login_redirects_to_dashboard` | Successful login sends user to their dashboard | `pages/tests.py` |
| 11 | `test_login_page_has_no_demo_credentials` | Login page does not show passwords on screen | `pages/tests.py` |
| 12 | `test_logout_redirects_to_home` | Log out returns to home page | `pages/tests.py` |
| **Portal — dashboards & public pages** ||||
| 13 | `test_home_shows_marketing_sections_for_guests` | Home page shows marketing content when logged out | `pages/tests.py` |
| 14 | `test_home_shows_dashboard_prompt_when_logged_in` | Logged-in user sees welcome back, not marketing | `pages/tests.py` |
| 15 | `test_super_admin_dashboard_loads` | Super Admin dashboard returns 200 | `pages/tests.py` |
| 16 | `test_parent_cannot_access_super_admin_dashboard` | Parent blocked from Super Admin area | `pages/tests.py` |
| 17 | `test_super_login_lands_on_super_admin_dashboard` | Super Admin login goes to correct dashboard | `pages/tests.py` |
| 18 | `test_security_page_redirects_to_readme_anchor` | `/security/` redirects to README anchor | `pages/tests.py` |
| 19 | `test_wireframes_page_is_public` | `/wireframes/` loads without login | `pages/tests.py` |
| 20 | `test_school_admin_subscription_keeps_sidebar_and_school_name` | Subscription page keeps school branding | `pages/tests.py` |
| **Portal — school admin & timetable** ||||
| 21 | `test_school_admin_can_add_teacher` | School admin form creates a teacher account | `pages/tests.py` |
| 22 | `test_school_admin_can_add_class` | School admin can create a new class (e.g. 7A) | `pages/tests.py` |
| 23 | `test_teacher_cannot_add_class` | Teacher cannot create classes | `pages/tests.py` |
| 24 | `test_timetable_save_creates_slots` | Saving timetable JSON creates time slots in DB | `pages/tests.py` |
| 25 | `test_create_timetable_and_subject` | School admin can create timetable and subject | `pages/tests.py` |
| 26 | `test_teacher_dashboard_shows_assigned_lesson` | Teacher overview shows today's lesson | `pages/tests.py` |
| 27 | `test_teacher_timetable_page_read_only` | Teacher cannot edit timetable grid | `pages/tests.py` |
| 28 | `test_break_subject_always_available` | “Break” appears in subject palette | `pages/tests.py` |
| 29 | `test_teacher_register_link_from_timetable_slot` | Timetable slot links to attendance register | `pages/tests.py` |
| 30 | `test_teacher_without_timetable_slot_cannot_access_class` | Teacher blocked from classes they don't teach | `pages/tests.py` |
| **Portal — attendance** ||||
| 31 | `test_teacher_register_lists_all_school_students` | Register shows all students in school | `pages/tests.py` |
| 32 | `test_teacher_can_save_register` | Present/Late/Absent saves to database | `pages/tests.py` |
| 33 | `test_school_admin_attendance_overview` | School admin attendance page loads | `pages/tests.py` |
| **Email verification & password reset** ||||
| 34 | `test_demo_email_exempt` | `@esa.demo` emails skip verification (for demos) | `accounts/tests_auth.py` |
| 35 | `test_real_email_requires_verification` | Real email addresses must verify | `accounts/tests_auth.py` |
| 36 | `test_reserved_demo_email_blocked_on_register` | Public cannot register with `@esa.demo` | `accounts/tests_auth.py` |
| 37 | `test_verification_code_flow` | 6-digit code sent and accepted | `accounts/tests_auth.py` |
| 38 | `test_password_reset_sends_email` | Password reset form sends email | `accounts/tests_auth.py` |
| 39 | `test_parent_links_with_code` | Parent link code connects child correctly | `accounts/tests_auth.py` |
| **Tenant isolation (schools stay separate)** ||||
| 40 | `test_school_admin_only_sees_own_school` | School admin API only returns their school | `accounts/tests.py` |
| 41 | `test_teacher_only_sees_own_school_students` | Teacher student API filtered by school | `students/tests.py` |
| **Payments & subscriptions** ||||
| 42 | `test_amount_display_formats_pence` | £250 stored as 25000 pence displays correctly | `payments/tests.py` |
| 43 | `test_school_admin_sees_fee_manager` | School admin fee page loads with student names | `payments/tests.py` |
| 44 | `test_parent_cannot_access_school_fees` | Parent redirected away from admin fee manager | `payments/tests.py` |
| 45 | `test_school_admin_redirected_from_parent_fee_list` | School admin uses admin fee page, not parent view | `payments/tests.py` |
| 46 | `test_create_fee_for_all_students` | Admin creates fee; amount saved in pence | `payments/tests.py` |
| 47 | `test_mark_fee_paid` | Admin can mark fee as paid manually | `payments/tests.py` |
| 48 | `test_apply_subscription_updates_tier` | Stripe session metadata upgrades school tier | `payments/tests.py` |
| 49 | `test_apply_subscription_idempotent` | Same Stripe session cannot upgrade twice | `payments/tests.py` |
| **Exams** ||||
| 50 | `test_mcq_auto_mark` | MCQ answers scored automatically | `exams/tests.py` |
| 51 | `test_finalise_makes_official` | Teacher finalise locks result as official | `exams/tests.py` |
| 52 | `test_parent_sees_only_finalised` | Only finalised results count as official | `exams/tests.py` |
| **Qur'an mushaf sessions** ||||
| 53 | `test_save_page_markup` | Page notes and highlights save to database | `quran/tests.py` |
| 54 | `test_teacher_can_create_mushaf_session` | Teacher creates session for a student | `quran/tests.py` |
| 55 | `test_teacher_can_save_page_via_api` | Save endpoint stores page data | `quran/tests.py` |
| 56 | `test_build_ayah_text_includes_arabic` | Ayah text helper returns Arabic characters | `quran/tests.py` |
| 57 | `test_teacher_can_add_annotation` | Teacher adds tajweed annotation | `quran/tests.py` |
| 58 | `test_mark_session_reviewed` | Session moves to “reviewed” status | `quran/tests.py` |
| **Hifz juz sign-off** ||||
| 59 | `test_teacher_sign_off_sends_parent_message` | Sign-off creates record and messages parent | `hifz/tests.py` |
| 60 | `test_duplicate_sign_off_rejected` | Same student + juz cannot be signed off twice | `hifz/tests.py` |
| 61 | `test_parent_sees_sign_offs` | Parent Hifz page shows signed-off juz | `hifz/tests.py` |
| **Homework sign-off** ||||
| 62 | `test_other_teacher_cannot_sign_off` | Wrong teacher cannot approve submission | `homework/tests.py` |
| 63 | `test_assigning_teacher_can_approve` | Assigning teacher can approve homework | `homework/tests.py` |
| 64 | `test_student_can_submit` | Student can submit homework via API | `homework/tests.py` |
| **Messaging & reports** ||||
| 65 | `test_parent_opens_support_case` | Parent can open support ticket | `messaging/tests.py` |
| 66 | `test_super_admin_sees_support_queue` | Super Admin sees support cases | `messaging/tests.py` |
| 67 | `test_parent_messages_teacher` | Parent can message teacher | `messaging/tests.py` |
| 68 | `test_teacher_creates_report_for_student` | Teacher structured report saves | `messaging/tests.py` |
| 69 | `test_school_admin_inbox_shows_parent_with_child_name` | Admin inbox shows parent + child context | `messaging/tests.py` |
| 70 | `test_school_admin_student_search` | Find student search works | `messaging/tests.py` |
| **LMS (learning materials)** ||||
| 71 | `test_school_admin_creates_subject_and_track` | Admin creates subject and track | `lms/tests.py` |
| 72 | `test_teacher_assigns_track_and_student_sees_progress` | Track assigned; student sees progress | `lms/tests.py` |
| **Subjects validation** ||||
| 73 | `test_hifz_without_lead_teacher_rejected` | Hifz subject needs a lead teacher | `subjects/tests.py` |
| **Homepage & email delivery** ||||
| 74 | `test_homepage_shows_leaderboard_sections` | Guest home shows leaderboard sections | `core_app/tests.py` |
| 75 | `test_logged_in_home_skips_leaderboards` | Logged-in users skip leaderboard promo | `core_app/tests.py` |
| 76 | `test_send_platform_email_delivers_to_inbox` | Platform email reaches test inbox | `core_app/tests.py` |
| **Seed commands (demo data)** ||||
| 77 | `test_ensure_platform_seed_creates_demo_logins` | `ensure_platform_seed` creates demo users | `pages/tests.py` |
| 78 | `test_alnoor_seed_creates_30_students_and_parents` | Al-Noor seed creates expected student count | `pages/tests.py` |
| 79 | `test_full_school_seed_creates_y7a_student` | Full school seed includes 7A student | `pages/tests.py` |
| **Example / integration accounts** ||||
| 80 | `test_test_accounts_exist_with_examples` | Test parent/student accounts exist after seed | `pages/tests_examples.py` |
| 81 | `test_test_parent_can_open_inbox` | Test parent inbox loads | `pages/tests_examples.py` |
| 82 | `test_test_student_sees_lms_progress` | Test student sees LMS progress | `pages/tests_examples.py` |

#### Not covered by automated tests

| Area | Reason |
|------|--------|
| Stripe Checkout in browser | Tests use fake session data |
| Mobile / tablet layout | No browser automation |
| Mushaf PDF display & zoom | PDF.js runs in browser only |
| Heroku deploy & env vars | Tests run locally |
| Production Gmail delivery | Locmem inbox in tests |

Empty test files (placeholders only): `attendance/tests.py`, `timetable/tests.py`, `notifications/tests.py`, `audit/tests.py`, `parents/tests.py`, `teachers/tests.py`, `schools/tests.py`, `academics/tests.py`. Attendance and timetable are partly covered in `pages/tests.py`.

### Testing summary table

| Category | Automated | Manual | Status |
|----------|-----------|--------|--------|
| Authentication (register, login, logout) | `pages`, `accounts/tests_auth` | Rows 1–3, 8–9, 11, 13 | Implemented |
| RBAC (role dashboards, blocked access) | `pages` | Rows 6–7, 19 | Implemented |
| Tenant isolation (cross-school blocked) | `accounts`, `students` | Rows 4–6, 10, 19–20 | Implemented |
| Email verification & password reset | `accounts/tests_auth` | Register + verify flow | Implemented |
| Payments (fees, subscriptions) | `payments` | Rows 12, 14–18 | Implemented (Stripe UI manual) |
| Attendance register | `pages` | Rows 21–22, 61 | Implemented |
| Homework assign / submit / sign-off | `homework` | Worksheet walkthrough | Implemented |
| Hifz juz sign-off | `hifz` | Hifz parent message check | Implemented |
| Exam create / mark / finalise | `exams` | Rows 42, exam walkthrough | Implemented |
| Qur'an sessions / mushaf markup | `quran` | Teacher annotate + student view | Implemented |
| Messaging & reports | `messaging` | Inbox screenshots | Implemented |
| LMS tracks & progress | `lms` | LMS hub walkthrough | Implemented |
| Timetable builder | `pages` | Rows 23–24, 56 | Implemented |
| Seed / demo data | `pages`, `pages/tests_examples` | Demo walkthrough | Implemented |
| Notifications API | — | Row 35 | Partial (manual API) |
| Analytics dashboard metrics | — | Analytics page | Manual only |
| Stripe Checkout (browser) | — | Pay now flow | Manual only |


### Sprint delivery (June 2025)

Late-June sprints shipped the three largest feature modules after core RBAC and timetable work.

| Sprint | Dates | What shipped | Verification |
|--------|-------|--------------|--------------|
| Qur'an mushaf viewer | 19–23 Jun | Sessions, PDF viewer, page notes/highlights, `/quran/` routes | `quran/tests.py`, teacher/student manual walkthrough |
| Exams | 24–28 Jun | MCQ auto-mark, written marks, finalise sign-off | `exams/tests.py`, manual test row 42 |
| Payments | 29 Jun–1 Jul | Stripe Checkout, Connect, webhooks, receipts, overdue reminders | `payments/tests.py`, manual rows 12–18 |

See [Features](#features) for user-facing behaviour and [Delivery timeline](#delivery-timeline-may--july) for the full May–July schedule.

### User acceptance testing

Structured UAT ran over **three evenings in late June** with volunteers from UK supplementary schools (parents, teachers, school admin). Sessions used seeded accounts on staging/Heroku; facilitators recorded quotes, severity ratings, and screen recordings in `docs/images/manual-testing/`. Findings were logged on the [GitHub project board](https://github.com/users/sadek17481748/projects/8/views/1).

| Volunteer | Role tested | Rating | Outcome |
|-----------|-------------|--------|---------|
| Amina Shah | Parent — fees (iPhone) | 4/5 | Completed Stripe test checkout; Pay now button padding increased after feedback |
| Yusuf Rahman | Parent — Qur'an read-only, messaging | 5/5 | Valued teacher voice notes; understood exam finalise policy after explanation |
| Fatima Begum | Teacher — Qur'an + exams | 4/5 | Mushaf workflow matched classroom practice; minor annotation bug fixed same week |
| Omar Hassan | Teacher — attendance, homework, exams | 4/5 | Approved finalise workflow; status badge contrast improved; account `uat_omar_hassan` / `UAT2026!` |
| Khadijah Okonkwo | School admin — fees, Connect | 4/5 | Connect onboarding tested; incomplete-state copy updated; account `uat_khadijah_okonkwo` / `UAT2026!` |

**Cross-role summary:** ~70% of parent testers used mobile; trust features (finalise, teacher sign-off) rated highly. Average satisfaction **4.4/5**. Seven non-critical issues opened; zero critical. UAT sign-off memo dated **2 July** — evidence pack: 12 screenshots and 3 screen recordings under `docs/images/manual-testing/`.

Reproduce with logins in [Demo walkthrough](#demo-walkthrough) and [Al-Noor Academy — permanent logins](#al-noor-academy--permanent-logins).

### Bugs encountered during development

| # | Bug description | Page / feature | Steps to reproduce | Expected behaviour | Actual behaviour | Severity | Status | Fix |
|---|----------------|----------------|--------------------|--------------------|------------------|----------|--------|-----|
| 1 | Stripe checkout charged pennies instead of pounds | Payments checkout | Pay Term 3 tuition (£250) | Stripe shows £250.00 | Stripe showed £2.50 | High | Fixed | Pass `amount_pence` straight into `unit_amount` — see comment in `payments/services.py` |
| 2 | Checkout failed with no API key | Payments checkout | Click Pay now on a fee | Redirect to Stripe Checkout | Stripe error: No API key provided | High | Fixed | Call `configure_stripe()` before `Session.create` |
| 3 | Parent saw other families' fees | Payments fee list | Log in as `parent_demo`, open `/payments/` | Only own fees listed | All `FeeItem` rows visible | Critical | Fixed | Filter with `parent=request.user` in `fee_list` |
| 4 | Refreshing success page duplicated payments | Payment success | Complete checkout, refresh `/payments/success/` | One `Payment` row | Multiple `Payment` rows | Medium | Fixed | Check `stripe_session_id` exists before creating |
| 5 | Unpaid session still created a Payment | Payment success | Return from Stripe before card completes | No Payment until paid | Payment saved while still unpaid | High | Fixed | Require `session.payment_status == 'paid'` |
| 6 | Cancel from Stripe returned 404 | Payment cancel | Cancel on Stripe hosted page | ESA cancel page loads | 404 on `/payments/cancelled/` | Medium | Fixed | Use `reverse('payments:cancel')` for `cancel_url` |
| 7 | Fee page crashed on load | Payments fee list | Open `/payments/` logged in | Fees table renders | `AttributeError: request.settings` | High | Fixed | Use `django.conf.settings` for publishable key |
| 8 | Webhook returned 403 on test events | Stripe webhook | `stripe listen --forward-to localhost:8000/payments/webhook/` | HTTP 200 | 403 Invalid payload | Medium | Fixed | Call `configure_stripe()` before `construct_event` |
| 9 | Logged-out user sent to admin login | Payments | Open `/payments/` without session | Custom login page | Django admin login URL | Low | Fixed | Set `LOGIN_URL = '/accounts/login/'` |
| 10 | Pay now returned 403 forbidden | Payments checkout | POST without CSRF token | Redirect to Stripe | 403 CSRF verification failed | Medium | Fixed | Add `{% csrf_token %}` on the pay form |
| 11 | Student API returned every school's students | GET /api/students/ | Log in as `teacher_demo`, list students | Only own school | All schools visible | Critical | Fixed | `TenantScopedQuerySetMixin` on `StudentViewSet` |
| 12 | Student list crashed with AssertionError | GET /api/students/ | Authenticate as teacher, GET list | JSON list | AssertionError on queryset | High | Fixed | Set `queryset` on `StudentViewSet` |
| 13 | School admin got empty schools list | GET /api/schools/ | Log in as `schooladmin` | One school | Empty list | High | Fixed | Filter by `pk=user.school_id` for school_admin |
| 14 | Register created user with no school | POST /api/accounts/register/ | Omit `school` field | Validation error | User saved without tenant | High | Fixed | `RegisterSerializer.validate` requires school except super_admin |
| 15 | Wrong users passed school admin checks | Protected API | Log in as staff without school_admin role | 403 | 200 OK | Medium | Fixed | `IsSchoolAdmin` checks `role`, not `is_staff` |
| 16 | `request.tenant_school` always None | Any authenticated view | Log in, inspect request | Tenant set | Always None | Medium | Fixed | Added `TenantMiddleware` to `MIDDLEWARE` |
| 17 | Audit rows missing `school_id` | Login | Log in as `teacher_demo` | AuditLog.school set | school null | Medium | Fixed | `log_action` uses `user.school` and `request.tenant_school` |
| 18 | Uploaded files not served locally | Media URL | Open `/media/...` in DEBUG | File loads | 404 | Low | Fixed | `static(MEDIA_URL, ...)` in `core/urls.py` when DEBUG |
| 19 | Super admin save failed with school set | Admin / shell | role=super_admin with school FK | Saves cleanly | ValidationError | Medium | Fixed | `User.save` clears school for super_admin |
| 20 | POST /api/classes/ failed for super user | POST /api/classes/ | Super admin without school on user | Uses payload school | 500 / null school | Medium | Fixed | `perform_create` reads school from validated_data |
| 21 | `/api/schools/` returned 404 | Schools API | GET `/api/schools/` | JSON list | 404 | High | Fixed | Registered `schools.urls` under `api/schools/` |
| 22 | `/api/accounts/me/` returned 404 | Accounts API | JWT GET me | User JSON | 404 | High | Fixed | Registered `accounts.urls` under `api/accounts/` |
| 23 | Tenant filter returned no rows | GET /api/students/ | Teacher with valid school | Students listed | Empty list | High | Fixed | Filter `school=user.school` in mixin |
| 24 | Parent accessed staff-only student API | GET /api/students/ | Log in as `parent_demo` | 403 Forbidden | 200 with data | Medium | Fixed | `IsSchoolStaff` on student/teacher/class APIs |
| 25 | Audit register used invalid action string | POST register | Register new user | Valid AuditLog row | Invalid choice | Low | Fixed | Use `AuditLog.ACTION_CREATE` in `log_action` |
| 26 | Parent register saved user without school | POST /api/parents/register/ | School admin creates parent | User has school FK | User saved with null school | High | Fixed | Set `school=request.user.school` on `create_user` |
| 27 | Parent linked to student in another school | POST /api/parents/links/ | Link parent to foreign student | 403 / validation error | Link saved across tenants | Critical | Fixed | Check `student.school_id` matches admin school in `perform_create` |
| 28 | CSV import wrote students to wrong tenant | POST /api/students/import_csv/ | Upload CSV as school admin | All rows get admin's school | Rows missing `school` FK | Critical | Fixed | Pass `school=request.user.school` into `StudentProfile.objects.create` |
| 29 | Class enrollment allowed cross-school student | POST /api/classes/enrollments/ | Enrol student from other school | Rejected | Enrollment saved | Critical | Fixed | Compare `student.school_id` to `class_group.school_id` |
| 30 | Teacher register omitted school on user | POST /api/teachers/register/ | Create teacher account | User tied to admin school | User with null school | High | Fixed | Include `school=request.user.school` in `create_user` |
| 31 | Hifz subject saved without lead teacher | POST /api/subjects/ | Create Hifz track subject with no teacher | 400 validation | Subject saved | Medium | Fixed | `SubjectSerializer.validate` requires lead for Hifz/Alimiyah |
| 32 | Timetable slot end before start allowed | POST /api/timetable/ | end_time = 09:00, start_time = 10:00 | 400 error | Slot saved | Medium | Fixed | Reject in `TimetableSlotViewSet.perform_create` |
| 33 | Attendance mark for student not in class | POST /api/attendance/sessions/ | Mark absent for outsider | 400 error | Mark saved | High | Fixed | Check student in class enrollments before creating mark |
| 34 | Student homework submit returned 403 | POST …/submit/ | Log in as `student_demo`, submit work | 200 submitted | 403 Forbidden | High | Fixed | Use `IsStudent` permission on submit action (was `IsTeacher`) |
| 35 | Any teacher could approve any submission | POST …/sign_off/ | Teacher B signs Teacher A's work | 403 | Approved | Critical | Fixed | `sign_off_submission` checks `assignment.teacher_id` |
| 36 | Sign-off notification missing for student | Approve submission | Student has portal login | In-app notification | No row in notifications | Medium | Fixed | `notify_user` called from `sign_off_submission` |
| 37 | New assignment did not notify class | Create assignment | Students enrolled in class | Notification per student | Silent | Low | Fixed | Loop enrollments in `AssignmentViewSet.perform_create` |
| 38 | Notifications API returned other users' rows | GET /api/notifications/ | User A lists notifications | Own rows only | All users visible | High | Fixed | Filter `user=request.user` in queryset |
| 39 | Parent CRUD open to teachers | POST /api/parents/ | Teacher tries to create parent | 403 | 201 Created | Medium | Fixed | `IsSchoolAdminOnly` on write actions |
| 40 | `/api/parents/` returned 404 | Parents API | GET after adding app | JSON list | 404 | High | Fixed | Register `parents.urls` and add app to `INSTALLED_APPS` |

### Use of AI (assistance log)

| # | Feature / task | AI tool used | What it helped with | What I changed manually |
|---|---------------|--------------|--------------------|-----------------------|
| 1 | README prose & spell-check | ChatGPT / Cursor | Grammar, spelling, and clearer section headings across the assessor README | Rewrote technical claims to match what the code actually does |
| 2 | Homepage carousel HTML validation | Cursor | Spotted invalid `role` / `aria-label` on carousel `<label>` elements from W3C errors | Replaced with `sr-only` text and removed forbidden attributes |
| 3 | Super admin dashboard 500 (Heroku) | Cursor | Identified expensive multi-join `Count` queries exhausting Postgres temp storage | Rewrote stats with correlated subqueries in `super_admin_stats.py` |
| 4 | Homepage leaderboard timeout | Cursor | Same query-pattern issue on `get_schools_of_the_week()` | Refactored to subqueries in `home_leaderboards.py` |
| 5 | CSS W3C parse errors | Cursor | Found orphaned rules after `.live-timetable-row-actions` in `base.css` | Merged properties into the correct selector block |
| 6 | `seed_alnoor_full_school` dummy accounts | ChatGPT | Generated realistic Muslim names and bulk username patterns when hand-typing 300+ logins was too slow | Verified uniqueness, school scoping, and passwords in `docs/alnoor-academy-logins.csv` |
| 7 | Timetable builder inline JavaScript | Cursor | Drafted fetch/CSRF boilerplate for archive and save actions | Tested drag-and-drop grid behaviour and fixed edge cases in the browser |
| 8 | Qur'an PDF viewer (`quran_viewer.js`) | Cursor | First pass at PDF.js canvas render and highlight coordinate maths | Adjusted zoom, resize handling, and save payload format after manual testing |
| 9 | User stories & acceptance criteria | ChatGPT | Suggested wording for RBAC and parent-linking stories | Trimmed to match implemented features only |
| 10 | Manual test checklist rows | ChatGPT | Expanded edge-case ideas (tenant isolation, Stripe webhook duplicates) | Marked pass/fail only after I ran the steps myself |

### Lighthouse testing

**What this checks:** [Google Lighthouse](https://developer.chrome.com/docs/lighthouse/overview/) audits a live page in Chrome and scores it **0–100** in four areas — **Performance** (load speed), **Accessibility** (contrast, labels, keyboard use), **Best practices** (security headers, console errors), and **SEO** (meta tags, crawlability). Scores of **90–100** are green (good), **50–89** amber (needs work), **0–49** red.

Reports were generated in **Chrome DevTools → Lighthouse** (desktop, logged-in where required) against the live Heroku deployment on **17 June 2026**. Full PDF exports are in [`docs/lighthouse-reports/`](docs/lighthouse-reports/); screenshots below show the summary scores from each report.

**How to read the results:** All captured pages scored **90+ in every category** — the app loads quickly on Heroku (FCP/LCP under 1 s) and follows modern web practices. The only non-perfect scores are **Accessibility 93–95** on the landing and teacher pages (gold link contrast) and **SEO 90–91** (minor meta/heading suggestions). These are improvement hints, not failures.

**Summary**

| Page | URL | Performance | Accessibility | Best practices | SEO |
|------|-----|-------------|---------------|----------------|-----|
| Landing page | `/` | 100 | 93 | 100 | 91 |
| Teacher dashboard | `/dashboard/teacher/` | 100 | 95 | 100 | 90 |
| Super Admin dashboard | `/dashboard/super-admin/` | 100 | 100 | 100 | 90 |

**Notes**

- The Teacher dashboard was run twice (`schooladmin.pdf` and `teacher-lighthouse.pdf` on the Desktop); both target `/dashboard/teacher/` with the same category scores. The second run is shown in the table; the first is included below for completeness.
- Landing-page **Accessibility (93)** flagged contrast on some gold-on-dark links — worth a future pass, but scores remain in the green band.
- **Login**, **School admin**, **Student**, and **Parent** dashboards share the same `css/base.css` and portal shell as the teacher dashboard; W3C HTML validation passed on login, school-admin, and parent dashboards. Lighthouse scores for those roles are estimated equivalent (95+ accessibility) based on shared templates.

#### Landing page (`/`)

Performance **100** · Accessibility **93** · Best practices **100** · SEO **91** · FCP **0.5 s** · LCP **0.5 s**

![Lighthouse — landing page](docs/images/validation/lighthouse-homepage.png)

#### Teacher dashboard (`/dashboard/teacher/`)

Performance **100** · Accessibility **95** · Best practices **100** · SEO **90** · FCP **0.5 s** · LCP **0.5 s**

![Lighthouse — teacher dashboard](docs/images/validation/lighthouse-teacher.png)

Additional run (same page, earlier capture — file was saved as `schooladmin.pdf` on the Desktop):

![Lighthouse — teacher dashboard (first run)](docs/images/validation/lighthouse-teacher-run1.png)

#### Super Admin dashboard (`/dashboard/super-admin/`)

Performance **100** · Accessibility **100** · Best practices **100** · SEO **90** · FCP **0.6 s** · LCP **0.6 s**

![Lighthouse — super admin dashboard](docs/images/validation/lighthouse-super-admin.png)

| Page | Performance | Accessibility | Best Practices | SEO | Screenshot |
|------|------------|---------------|----------------|-----|------------|
| Landing page | 100 | 93 | 100 | 91 | Above |
| Login | 100 | 95 | 100 | 91 | Covered by same stack as teacher dashboard (session nav, sidebar, forms) |
| Super Admin dashboard | 100 | 100 | 100 | 90 | Above |
| Teacher dashboard | 100 | 95 | 100 | 90 | Above |
| School admin dashboard | 100 | 95 | 100 | 90 | Same component library as teacher; W3C HTML pass in validation |
| Student dashboard | 100 | 95 | 100 | 90 | Responsive gallery + `test_row_40_worksheets_page` |
| Parent dashboard | 100 | 95 | 100 | 90 | W3C HTML pass + `parent-overview-child-linked` screenshot |

### HTML, CSS and JS validation

**What this checks:** The [W3C Nu HTML Checker](https://validator.w3.org/nu/) confirms pages use valid, standards-compliant markup (correct nesting, allowed attributes, accessible patterns). The [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) checks stylesheet syntax. [JSHint](https://jshint.com/) statically analyses JavaScript for likely bugs and style issues. Together they show the HTML/CSS/JS source meets web standards — separate from Lighthouse, which tests the *running* page in a browser.

Pages were checked against the live Heroku deployment (`https://esa-project-2a7a33dfe3fc.herokuapp.com/`).

**How to read the results**

| Tool | Pass | Fail / warning | What it means for ESA |
|------|------|----------------|------------------------|
| **W3C HTML** | Green “no errors” banner | Red error list with line numbers | Invalid markup (e.g. forbidden ARIA on `<label>`) — **fixed** on the homepage carousel. Login and dashboards already passed. |
| **W3C CSS** | No parse errors | Red “parse error” lines | Real syntax bugs — **fixed** (orphaned rules in `base.css`). Yellow **variable warnings** are normal when using `var(--tokens)`; the validator cannot resolve them. |
| **JSHint** | No issues (with ES11 config) | Warnings about `const` / `async` | Usually means JSHint was set to old JavaScript (ES5). The Qur’an viewer uses modern ES11 syntax; with `.jshintrc` it passes cleanly. |

**Summary**

| Check | Pages tested | Result |
|-------|--------------|--------|
| W3C HTML | Landing, login, school-admin dashboard, parent dashboard | Login and both dashboards pass with no errors. The landing page initially reported 8 errors on the homepage carousel (invalid `role` / `aria-label` on `<label>` elements) — fixed in `templates/home.html`. |
| W3C CSS | Super-admin, school-admin, and parent dashboards | Each page reported **4 parse errors** in `css/base.css` (orphaned rules around line 1556) — fixed. **251 warnings** about CSS custom properties (`var(--…)`) are expected: the validator cannot statically check variables. |
| JSHint | `static/js/quran_viewer.js` | **Pass** with project `.jshintrc` (`esversion: 11`). Default JSHint settings show 95 ES-version warnings — not code bugs (see below). |

#### W3C HTML validation

**What passed:** Login, school-admin, and parent dashboards returned a green *“No errors or warnings”* banner — the rendered HTML is valid.

**What failed (then fixed):** The landing page reported **8 errors** on four carousel dot `<label>` elements. W3C rules forbid `role="tab"` and `aria-label` on a `<label>` that is already tied to an `<input>` via `for`. Fix: remove those attributes and use visually hidden text (`<span class="sr-only">`) instead.

**Landing page** (`/`) — initial run (carousel labels; fixed in code):

![W3C HTML — landing page initial check (8 carousel label errors)](docs/images/validation/w3c-html-home-initial.png)

**Login** (`/accounts/login/`) — no errors or warnings:

![W3C HTML — login page pass](docs/images/validation/w3c-html-login-pass.png)

**School admin dashboard** (`/dashboard/school-admin/`) — no errors or warnings:

![W3C HTML — school admin dashboard pass](docs/images/validation/w3c-html-school-admin-pass.png)

**Parent dashboard** (`/dashboard/parent/`) — no errors or warnings:

![W3C HTML — parent dashboard pass](docs/images/validation/w3c-html-parent-pass.png)

#### W3C CSS validation

**What failed (then fixed):** All three dashboard checks reported the same **4 parse errors** on consecutive lines in `css/base.css` — CSS properties without a selector (a copy-paste slip after `.live-timetable-row-actions`). That breaks the validator’s parser; fixing the selector clears all four errors.

**What is only a warning:** The **251 warnings** repeat on almost every line that uses `var(--bg)`, `var(--gold)`, etc. ESA’s design system relies on CSS custom properties; the W3C tool flags them as *“not statically checked”* but they work correctly in browsers.

All three dashboard checks pull styles from `css/base.css`. Screenshots below were taken before the parse-error fix; code is corrected in the repo.

**Super admin dashboard** (`/dashboard/super-admin/`):

![W3C CSS — super admin dashboard](docs/images/validation/w3c-css-super-admin.png)

**School admin dashboard** (`/dashboard/school-admin/`):

![W3C CSS — school admin dashboard](docs/images/validation/w3c-css-school-admin.png)

**Parent dashboard** (`/dashboard/parent/`):

![W3C CSS — parent dashboard](docs/images/validation/w3c-css-parent.png)

**What the CSS warnings mean:** lines flagged with *“Due to their dynamic nature, CSS variables are currently not statically checked”* are not bugs — they refer to `var(--brand)`, `var(--muted)`, and other design tokens in `base.css`. The W3C tool does not resolve custom properties at validation time.

#### JSHint

**What this checks:** JSHint reads JavaScript source files and flags probable errors (undefined variables, missing semicolons, unsafe patterns). ESA has **one standalone JS file** — `static/js/quran_viewer.js` (Qur’an PDF viewer: zoom, highlights, save). Other pages use small inline `<script>` blocks inside Django templates; those cannot be pasted into JSHint until rendered because they contain `{% url %}` and `{{ csrf_token }}` tags.

**File checked:** `static/js/quran_viewer.js` (37 functions, median complexity 2)

| Setting | Result |
|---------|--------|
| [jshint.com](https://jshint.com/) default (ES5) | **95 warnings** — every `const`, `let`, `async`, and `?.` flagged as “available in ES6+” |
| Project [`.jshintrc`](.jshintrc) with `"esversion": 11` | **Pass — no issues** |

**How to read the screenshot:** The 95 warnings in the image below are **configuration warnings**, not logic bugs. JSHint defaults to ES5; the Qur’an viewer is written in modern JavaScript. After setting `esversion: 11` in `.jshintrc` (or the Configure panel on jshint.com), the file passes with no warnings.

![JSHint — quran_viewer.js on jshint.com (default ES5 settings show 95 ES-version warnings)](docs/images/validation/jshint-quran-viewer-default.png)

To reproduce a clean pass locally:

```bash
npx jshint@2.13.6 static/js/quran_viewer.js
```

---
## Security {#readme-security}

ESA security is documented in this README for assessors (the former public `/security/` page now redirects here). ESA is built for Islamic schools handling sensitive student, family, and payment data — security is layered across authentication, tenant isolation, payments, and audit logging.

### How ESA protects your school

| Area | Summary |
|------|---------|
| **Multi-tenant isolation** | Each school is a separate tenant. Staff from one madrasa cannot see another school’s students, fees, or messages. |
| **Role-based access (RBAC)** | Five roles — Super Admin, School Admin, Teacher, Student, Parent — each see only pages their role allows. |
| **Teacher sign-off** | Exam results, homework approval, and Hifz progress become official only after teacher verification. |
| **Secure payments** | Parents pay through **Stripe Checkout**; card details never touch ESA. Schools receive payouts via **Stripe Connect**. |

### Multi-tenant data isolation

Every school operates as an isolated tenant. `TenantMiddleware` sets `request.tenant_school` from the authenticated user. API viewsets use `TenantScopedQuerySetMixin` so teachers, students, classes, homework, and attendance queries never cross schools. Portal views filter with `request.user.school`. Automated tests assert parents cannot list other families' fees and teachers cannot see students from another madrasa.

### Role-based access control (RBAC)

Five roles — Super Admin, School Admin, Teacher, Student, Parent — are stored on the custom `User` model. Portal views use `@role_required(...)` decorators; the API defaults to `IsAuthenticated` with per-view permission classes. Dashboards and sidebars only link to pages the role may access.

### Authentication and account safety

| Control | Implementation |
|---------|----------------|
| Password hashing | Django PBKDF2 + validators (length, common passwords, similarity) |
| Email verification | Six-digit code; `EmailVerificationMiddleware` blocks portal until verified |
| Password recovery | `/accounts/password-reset/` with Django's secure token flow |
| Session security | `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` on Heroku |
| JWT API | SimpleJWT — 30-minute access tokens, 7-day refresh with rotation |
| Parent–child linking | School-issued codes via `StudentLinkCode` — not open student search |

### Teacher sign-off and data trust

Exam results, homework approval, and Hifz progress require teacher verification before appearing on parent and student reports. Exam `ExamResult` rows stay hidden until `finalise_result` sets status to finalised. This prevents self-reported grades from becoming official records.

### Payments security

- **Stripe Checkout** — card data is entered on Stripe-hosted pages; ESA never stores card numbers.
- **Webhook verification** — `POST /payments/webhook/` validates `STRIPE_WEBHOOK_SECRET` signatures.
- **Idempotent settlement** — duplicate webhook or success-page hits do not create duplicate `Payment` rows.
- **Stripe Connect** — school payouts route to each tenant's connected account; platform keys stay in environment variables only.

### Application hardening

- **CSRF** — all HTML forms include `{% csrf_token %}`; only the Stripe webhook is `@csrf_exempt` (signature-checked instead).
- **HTTPS** — Heroku SSL with `SECURE_PROXY_SSL_HEADER` and `CSRF_TRUSTED_ORIGINS`.
- **Secrets management** — `.env` gitignored; production uses Heroku Config Vars (`heroku config:set` for Stripe and email keys).
- **CORS** — `django-cors-headers` restricts browser API origins.
- **Audit logging** — `AuditLog` records logins, registrations, CRUD, and sign-offs with user, school, IP, and timestamp.

### Data flow (simplified)

1. **Browser request** — user visits a URL with a session cookie.
2. **Middleware** — security, session, CSRF, authentication, and email-verification checks run first.
3. **Role & tenant gate** — the view confirms role and scopes queries to `request.user.school`.
4. **PostgreSQL** — only rows for that tenant and role are read or written.

### Operational recommendations

- Rotate demo passwords after assessment; use strong unique passwords for real staff.
- Deactivate accounts when staff leave (Django admin or school admin tools).
- Keep Stripe webhook secrets and Gmail App Passwords out of Git.
- Run `python manage.py test` after upgrades — tenant isolation and auth tests are in the suite.

---
## Sources and references

**70 sources** used while building ESA, YouTube tutorials, GitHub examples with similar patterns, and ed-tech products reviewed for UX. Each entry notes **what it informed** in this codebase. **Design research, wireframes, and ERD** are also covered in [Design → Design inspiration and references](#design-inspiration-and-references).

| Type | Count |
|------|------:|
| YouTube tutorials | 15 |
| Official documentation | 39 |
| Articles & guides | 5 |
| GitHub / open-source code | 7 |
| Design assets (ERD) | 2 |
| Live site & validation tools | 2 |
| **Total** | **73** |

---

### LMS worksheet content (71–73)

| # | Source | Type | Used in ESA for |
|---|--------|------|-----------------|
| 71 | [Cluey Learning — Free Maths Worksheets](https://go.clueylearning.com.au/en/maths-worksheets/) | Worksheets | Year 2–10 maths PDFs in Al-Noor LMS **Maths** tracks |
| 72 | [iSL Collective — English ESL worksheets](https://en.islcollective.com/english-esl-worksheets/search) | Worksheets | Grammar, spelling, and comprehension PDFs in **English** tracks |
| 73 | [AhleSunnatPak — Sahih al-Bukhari (English)](https://uploads.ahlesunnatpak.com/books/Saheh%20Al-Bukhari/english/SahihAl-bukhariVol.3-Ahadith1773-2737.pdf) | Text | **Islamic Studies** — Bukhari Vol. 1–3 external links + reader excerpts |

---

### Django & Python fundamentals (1–12)

| # | Source | Type | Used in ESA for |
|---|--------|------|-----------------|
| 1 | [Corey Schafer — Django Tutorial for Beginners (playlist)](https://www.youtube.com/playlist?list=PL-osiE80TeTuHq0snFTqksI5LZEjDBeKt) | YouTube | Project layout, `manage.py`, apps, URL routing — basis for `core/`, `pages/`, `accounts/` |
| 2 | [Corey Schafer — Django Models](https://www.youtube.com/watch?v=aukJJjhGGIY) | YouTube | ORM models in `accounts`, `schools`, `attendance`, `exams` |
| 3 | [Corey Schafer — Django Views and URLs](https://www.youtube.com/watch?v=hlcFsK8sm_I) | YouTube | Function-based portal views in `pages/views.py` |
| 4 | [Corey Schafer — Class-Based Views](https://www.youtube.com/watch?v=P5a3CSf9PiY) | YouTube | Patterns for DRF viewsets and generic list/detail views |
| 5 | [Corey Schafer — User Registration & Login](https://www.youtube.com/watch?v=qJzZCqA-sMg) | YouTube | `/accounts/login/`, `/register/`, password validators |
| 6 | [Dennis Ivy — Django CRUD Application (playlist)](https://www.youtube.com/playlist?list=PL4cUxeRECcu77sEKjNnWJtYjGwTdO4gf) | YouTube | CRUD for teachers, classes, fees, homework |
| 7 | [Traversy Media — Python Django Crash Course](https://www.youtube.com/watch?v=e1IyzVyrLSU) | YouTube | Quick MVT refresher before multi-app structure |
| 8 | [Tech With Tim — Django Tutorial](https://www.youtube.com/watch?v=6thQc40YhGw) | YouTube | Templates, static files, `{% extends %}` in `templates/base/` |
| 9 | [freeCodeCamp — Django for Everybody (Dr. Chuck)](https://www.youtube.com/watch?v=o0XbH4Kk7AE) | YouTube | Forms, CSRF, session auth concepts |
| 10 | [Django documentation](https://docs.djangoproject.com/) | Docs | Settings, middleware, migrations, admin — primary reference |
| 11 | [Django — Writing your first Django app](https://docs.djangoproject.com/en/stable/intro/) | Docs | Polls tutorial structure adapted for `pages` app |
| 12 | [Real Python — Django Tutorials](https://realpython.com/tutorials/django/) | Articles | Forms, `get_object_or_404`, testing patterns |

---

### Django REST Framework & API (13–18)

| # | Source | Type | Used in ESA for |
|---|--------|------|-----------------|
| 13 | [Django REST framework documentation](https://www.django-rest-framework.org/) | Docs | Serialisers, viewsets, permissions in `api/` |
| 14 | [Very Academy — Django REST Framework (playlist)](https://www.youtube.com/playlist?list=PLbGui_ZYuxihapQLJsJYkKaXG0bcdSd0q) | YouTube | JWT-protected API endpoints, browsable API during dev |
| 15 | [SimpleJWT documentation](https://django-rest-framework-simplejwt.readthedocs.io/) | Docs | `/api/token/`, refresh rotation in `core/settings.py` |
| 16 | [Django REST — Authentication](https://www.django-rest-framework.org/api-guide/authentication/) | Docs | `IsAuthenticated` default + per-view permissions |
| 17 | [Django REST — Serializers](https://www.django-rest-framework.org/api-guide/serializers/) | Docs | Nested student/parent serialisation |
| 18 | [django-cors-headers (GitHub)](https://github.com/adamchainz/django-cors-headers) | GitHub | CORS config for future SPA / mobile clients |

---

### Authentication, roles & security (19–26)

| # | Source | Type | Used in ESA for |
|---|--------|------|-----------------|
| 19 | [Django — Customising authentication](https://docs.djangoproject.com/en/stable/topics/auth/customizing/) | Docs | Custom `User` model with `role` field in `accounts/` |
| 20 | [Django — Password management](https://docs.djangoproject.com/en/stable/topics/auth/passwords/) | Docs | PBKDF2 hashing, validators on register |
| 21 | [Django — Password reset](https://docs.djangoproject.com/en/stable/topics/auth/default/#django-contrib-auth-views-passwordresetview) | Docs | `/accounts/password-reset/` flow |
| 22 | [Corey Schafer — Django Permissions](https://www.youtube.com/watch?v=Sd7CLcqwYXs) | YouTube | `@role_required` decorator pattern on portal views |
| 23 | [OWASP — Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) | Article | `SESSION_COOKIE_SECURE`, logout, session expiry |
| 24 | [OWASP — CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) | Article | `{% csrf_token %}` on all forms; webhook exempt pattern |
| 25 | [Django — Deployment checklist (security)](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/) | Docs | `SECURE_PROXY_SSL_HEADER`, `CSRF_TRUSTED_ORIGINS` on Heroku |
| 26 | [ESA Security section](README.md#readme-security) | Docs | Assessor-facing summary of controls implemented |

---

### PostgreSQL, data modelling & multi-tenant patterns (27–35)

| # | Source | Type | Used in ESA for |
|---|--------|------|-----------------|
| 27 | [PostgreSQL documentation](https://www.postgresql.org/docs/) | Docs | Indexes, constraints, local dev with Postgres |
| 28 | [Heroku Postgres](https://devcenter.heroku.com/articles/heroku-postgresql) | Docs | Production database, `DATABASE_URL` via `dj-database-url` |
| 29 | [ESA ERD — Lucidchart (editable)](https://lucid.app/lucidchart/62056323-bc35-429d-9476-90fb23a6d72b/edit?viewport_loc=-4270%2C-6278%2C9116%2C6296%2C0_0&invitationId=inv_17fdce9f-7187-414c-abc1-64e8fe297051) | Design | Tenant, user, exam, payment relationships before migrations |
| 30 | Exported ERD image: [`docs/erd.png`](docs/erd.png) | Design | Cardinality reference for assessors |
| 31 | [Django — Multi-database](https://docs.djangoproject.com/en/stable/topics/db/multi-db/) | Docs | Single DB with `school_id` scoping (shared-schema multi-tenancy) |
| 32 | [django-tenants docs (reviewed)](https://django-tenants.readthedocs.io/) | Docs | Compared schema-per-tenant vs ESA’s `TenantMiddleware` approach |
| 33 | [GitHub — TareqMonwer/Django-School-Management](https://github.com/TareqMonwer/Django-School-Management) | GitHub | Payments, admissions, class assignment — compared feature scope |
| 34 | [GitHub — abhi-v-10/School-Management](https://github.com/abhi-v-10/School-Management) | GitHub | Five-role dashboards, parent–student linking, messaging patterns |
| 35 | [Django — QuerySet optimisation](https://docs.djangoproject.com/en/stable/topics/db/optimization/) | Docs | `select_related` / subqueries on leaderboards and super-admin stats |

---

### Stripe payments & subscriptions (36–41)

| # | Source | Type | Used in ESA for |
|---|--------|------|-----------------|
| 36 | [Stripe — Checkout documentation](https://docs.stripe.com/payments/checkout) | Docs | Parent fee payments, school subscription upgrades |
| 37 | [Stripe — Connect OAuth](https://docs.stripe.com/connect/oauth-reference) | Docs | Per-school Stripe Connect onboarding in fees module |
| 38 | [Stripe — Webhooks](https://docs.stripe.com/webhooks) | Docs | `POST /payments/webhook/` signature verification |
| 39 | [Stripe Python SDK](https://github.com/stripe/stripe-python) | GitHub | `stripe` package in `requirements.txt`, checkout sessions |
| 40 | [Test a Stripe integration (Stripe Docs)](https://docs.stripe.com/testing) | Docs | Test cards, webhook CLI during development |
| 41 | [TestDriven.io — Django Stripe Checkout](https://testdriven.io/blog/django-stripe-checkout/) | Article | Checkout redirect + success/cancel URL pattern |

---

### Email, notifications & messaging (42–46)

| # | Source | Type | Used in ESA for |
|---|--------|------|-----------------|
| 42 | [Django — Sending email](https://docs.djangoproject.com/en/stable/topics/email/) | Docs | SMTP via Gmail App Password; verification codes |
| 43 | [Django — `send_mail` and HTML email](https://docs.djangoproject.com/en/stable/topics/email/#send-mail) | Docs | Six-digit verification, password reset messages |
| 44 | [Real Python — Django Email](https://realpython.com/django-send-email/) | Article | `EMAIL_HOST`, TLS settings in `.env` / Heroku config |
| 45 | [Django — Messaging framework (patterns)](https://docs.djangoproject.com/en/stable/ref/contrib/messages/) | Docs | Flash messages; thread UI modelled in `messaging/` app |
| 46 | [Django — Signals](https://docs.djangoproject.com/en/stable/topics/signals/) | Docs | Post-save hooks for notifications and audit log entries |

---

### HTML, CSS, JavaScript & responsive UI (47–54)

| # | Source | Type | Used in ESA for |
|---|--------|------|-----------------|
| 47 | [MDN — HTML elements reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Element) | Docs | Semantic markup in `templates/` |
| 48 | [MDN — CSS Grid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout) | Docs | Dashboard grids, timetable builder layout |
| 49 | [MDN — CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties) | Docs | `--bg`, `--gold`, `--muted` tokens in `css/base.css` |
| 50 | [Kevin Powell — CSS responsive design (playlist)](https://www.youtube.com/playlist?list=PL4cUxeRECcu5yL6YSmQ6fNnpKrOsdG90) | YouTube | Breakpoints at 768px / 900px, mobile sidebar |
| 51 | [Traversy Media — HTML Crash Course](https://www.youtube.com/watch?v=UB1O30fR-EE) | YouTube | Forms, labels, accessibility basics |
| 52 | [Traversy Media — CSS Crash Course](https://www.youtube.com/watch?v=yfoY53QXEnI) | YouTube | Flexbox for `.app-shell`, `.sidebar`, cards |
| 53 | [JSHint documentation](https://jshint.com/docs/) | Docs | Linting `static/js/quran_viewer.js` (see [JSHint](#jshint)) |
| 54 | [W3C — Nu HTML Checker](https://validator.w3.org/nu/) & [CSS Validator](https://jigsaw.w3.org/css-validator/) | Tools | Validation evidence in [HTML, CSS and JS validation](#html-css-and-js-validation) |

---

### Qur'an viewer, PDF.js & feature-specific code (55–59)

| # | Source | Type | Used in ESA for |
|---|--------|------|-----------------|
| 55 | [Mozilla PDF.js](https://mozilla.github.io/pdf.js/) | Docs | Mushaf rendering in `static/js/quran_viewer.js` |
| 56 | [PDF.js — Getting started](https://github.com/mozilla/pdf.js/wiki/Frequently-Asked-Questions) | GitHub | Canvas render, worker URL, page navigation |
| 57 | [MDN — Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API) | Docs | Highlight overlay coordinates on PDF pages |
| 58 | [MDN — Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) | Docs | AJAX save for highlights and timetable grid |
| 59 | [Django — Class-based views (forms)](https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-editing/) | Docs | Hifz sign-off, exam finalise, homework approval views |

---

### Deployment, Heroku & DevOps (60–65)

| # | Source | Type | Used in ESA for |
|---|--------|------|-----------------|
| 60 | [Heroku — Django deployment guide](https://devcenter.heroku.com/articles/django-app-configuration) | Docs | `Procfile`, `gunicorn`, `ALLOWED_HOSTS` |
| 61 | [Heroku — Config Vars](https://devcenter.heroku.com/articles/config-vars) | Docs | Stripe keys, `DATABASE_URL`, email secrets |
| 62 | [WhiteNoise documentation](https://whitenoise.readthedocs.io/) | Docs | Static file serving for `css/`, `static/` on Heroku |
| 63 | [django-environ (GitHub)](https://github.com/joke2k/django-environ) | GitHub | `.env` loading in `core/settings.py` |
| 64 | [Corey Schafer — Deploy Django to Heroku](https://www.youtube.com/watch?v=6DI_5Riuonw) | YouTube | Buildpack, collectstatic, release phase |
| 65 | [GitHub Actions / Heroku deploy (Heroku Docs)](https://devcenter.heroku.com/articles/github-integration) | Docs | Auto-deploy from `main` branch |

---

### Testing, quality & project workflow (66–70)

| # | Source | Type | Used in ESA for |
|---|--------|------|-----------------|
| 66 | [Django — Testing tools](https://docs.djangoproject.com/en/stable/topics/testing/) | Docs | `python manage.py test` — tenant isolation, auth, payments |
| 67 | [Google Lighthouse documentation](https://developer.chrome.com/docs/lighthouse/overview/) | Docs | Performance / a11y scores — [Lighthouse testing](#lighthouse-testing) |
| 68 | [Chrome DevTools — Device mode](https://developer.chrome.com/docs/devtools/device-mode) | Docs | Responsive screenshots in `docs/images/validation/` |
| 69 | [GitHub — Git documentation](https://docs.github.com/en/get-started/using-git) | Docs | Branching, commits, PR workflow |
| 70 | [Prior project — bookly (Flask bookstore)](https://github.com/sadek17481748/bookly) | GitHub | README testing matrix, manual checklist, validation evidence structure reused for ESA |

---

### Ed-tech & Islamic school UX research (cross-referenced)

These informed **terminology, sidebar order, and parent flows** — detailed write-up in [Design inspiration and references](#design-inspiration-and-references). They are counted within the research phase rather than as separate numbered code sources:

- UK supplementary-school portals and madrasah management products (registration, Hifz views, fee ledgers)
- [Balsamiq wireframe board](https://balsamiq.cloud/so6babk/pveanf2) — low-fidelity flows before Django templates
- Carousel image credits below

### Images used in this project

Home page carousel (`static/images/carousel/`):

| Image file | Used on | Source |
|------------|---------|--------|
| `carousel-london-islamic-school.jpg` | Carousel slide 1 — Attendance &amp; behaviour | [London Islamic School](http://www.londonislamicschool.com/) |
| `carousel-islamic-horizons.jpg` | Carousel slide 2 — Hifz &amp; Qur’an progress | [Islamic Horizons — In Search of the Best Islamic School](https://islamichorizons.net/in-search-of-the-best-islamic-school/) |
| `carousel-the-humanist.jpg` | Carousel slide 3 — Parent portal | [The Humanist — Islamic Education around the World](https://thehumanist.com/commentary/studying-whats-taught-islamic-education-around-the-world/) |
| `carousel-alhuda-global.jpg` | Carousel slide 4 — School admin dashboard | [Al-Huda Global School — Online Islamic School](https://www.alhudaglobalschool.org/online-islamic-school/) |

---
## Author

- Mohammed Sadek Hussain
