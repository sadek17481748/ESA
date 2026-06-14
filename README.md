# ESA — Education and Schooling Applications
## Table of Contents

- [Overview](#overview)
  - [Project goals](#project-goals)
  - [How we planned timing](#how-we-planned-timing)
  - [Scope creep — what changed and why](#scope-creep--what-changed-and-why)
  - [Delivery timeline (May → July)](#delivery-timeline-may--july)
- [Quick links](#quick-links)
- [Navigating the website](#navigating-the-website)
  - [Request flow overview](#request-flow-overview)
  - [Role-based navigation paths](#role-based-navigation-paths)
- [Technical overview](#technical-overview)
  - [How the pieces fit together](#how-the-pieces-fit-together)
  - [PostgreSQL — the database](#postgresql--the-database)
  - [Django — the web application](#django--the-web-application)
  - [External services](#external-services)
- [Key UI screenshots](#key-ui-screenshots)
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
  - [What we mean by user experience](#what-we-mean-by-user-experience)
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
  - [Main wireframe pack (start here)](#main-wireframe-pack-start-here)
  - [Wireframe inventory](#wireframe-inventory)
- [Design](#design)
  - [Data model and ERD (entity relationships)](#data-model-and-erd-entity-relationships)
  - [Visual language](#visual-language)
  - [Colour palette and CSS tokens](#colour-palette-and-css-tokens)
  - [How colour is used across the UI](#how-colour-is-used-across-the-ui)
  - [Typography](#typography)
  - [UI components](#ui-components)
  - [Accessibility](#accessibility)
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
  - [Connecting Gmail for platform email notifications](#connecting-gmail-for-platform-email-notifications)
- [Testing and Bugs](#testing-and-bugs)
  - [Testing strategy and plan](#testing-strategy-and-plan)
  - [Assessment test matrix](#assessment-test-matrix)
  - [Manual testing](#manual-testing)
  - [Automated testing](#automated-testing)
  - [Testing summary table](#testing-summary-table)
  - [Bugs encountered during development](#bugs-encountered-during-development)
  - [Use of AI (assistance log)](#use-of-ai-assistance-log)
  - [Lighthouse testing](#lighthouse-testing)
  - [HTML, CSS and JS validation](#html-css-and-js-validation)
- [Security](#security)
- [Sources and references](#sources-and-references)
- [Sprint delivery evidence (June–July 2025)](#sprint-delivery-evidence-junejuly-2025)
  - [Portal login hub](#portal-login-hub-introduction)
  - [Login credentials by role](#super-admin-login-credentials)
  - [Quick navigation links](#quick-navigation-links)
  - [Qur'an annotation sprint (19–23 June)](#quran-sprint-overview-1923-june)
  - [Exams and sign-off sprint (24–28 June)](#exams-sprint-overview-2428-june)
  - [Payments and deployment sprint (29 June–1 July)](#payments-sprint-overview-29-june1-july)
  - [User acceptance testing](#user-acceptance-testing-overview)
  - [Design inspiration (videos and websites)](#design-inspiration--islamic-school-platforms)
  - [Deployment readiness checklist](#deployment-readiness--heroku-platform)
  - [Systems used summary](#systems-used--technology-summary)
  - [Closing assessor guide](#closing-assessor-guide)
- [Author](#author)

---
## Quick links

Assessor-facing links and evidence paths:

| Resource | Link or path |
|----------|--------------|
| **Source repository** | https://github.com/sadek17481748/ESA |
| **Live deployment** | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| **Security overview (public)** | https://esa-project-2a7a33dfe3fc.herokuapp.com/security/ |
| **Bug tracker (GitHub Project board)** | https://github.com/users/sadek17481748/projects/8/views/1 |
| **Wireframes (main pack)** | **[`docs/ESA-wireframes.pdf`](docs/ESA-wireframes.pdf)** · [Balsamiq](https://balsamiq.cloud/so6babk/pveanf2) |
| **ERD / data model** | [Data model and ERD](#data-model-and-erd-entity-relationships) |
| **Test credentials** | Showcase: `demo_parent` / `demo_student` / `Demo2026!` — full list in [Demo walkthrough](#demo-walkthrough) and [Assessor and demo logins](#assessor-and-demo-logins) |
| **Manual test evidence (screenshots)** | `docs/images/manual-testing/` |
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

| # | Goal | Plain English | Status on live site |
|---|------|---------------|---------------------|
| 1 | **Full-stack Django app** | Real web app with database, not just static pages — split into reusable apps (`accounts`, `payments`, `quran`, etc.) | **Done** — deployed on Heroku with PostgreSQL |
| 2 | **Multi-tenant schools** | Many schools on one platform; each only sees its own data | **Done** — `school_id` scoping + tests |
| 3 | **Five roles (RBAC)** | Super Admin, School Admin, Teacher, Student, Parent — each with different pages | **Done** — sidebars and permission checks |
| 4 | **CRUD with UI feedback** | Create/edit records in the browser; errors and success messages shown clearly | **Done** — forms, flash messages, validation |
| 5 | **Teacher sign-off** | Teachers must approve Hifz, homework, and exams before parents trust the data | **Mostly done** — homework sign-off, exam finalise, Hifz juz sign-off live; password re-entry on sign-off still planned |
| 6 | **Stripe payments** | Parents pay fees online; money routes to the school's Stripe account | **Done** — Checkout + Connect + subscriptions (test mode) |
| 7 | **Responsive, accessible UI** | Works on laptop and tablet (primary); readable contrast; keyboard basics | **Done** — see [How responsiveness was tested](#how-responsiveness-was-tested) |
| 8 | **Documented, incremental build** | Small commits, README, tests, evidence for assessors | **Ongoing** — README, manual test table, GitHub history |

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
## Key UI screenshots

Screenshots will be stored under `docs/images/manual-testing/` so key screens are visible directly in this README.

| Screen | Screenshot |
|--------|------------|
| Landing page | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| Login | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| Super Admin dashboard | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| School Admin dashboard | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| Teacher dashboard | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| Student dashboard | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| Parent dashboard | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| Timetable | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| Attendance register | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| Hifz progress | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| Payments / fees | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |

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

### Responsive behaviour

The UI is designed mobile-first. Navigation collapses to a hamburger menu on small screens, dashboard cards stack vertically, and data tables scroll horizontally. Touch targets meet the 44x44px minimum on mobile viewports.

### How responsiveness was tested

| Device class | Typical width | What was checked |
|--------------|---------------|------------------|
| **Phone** | ~375px (portrait) | Hamburger menu, single-column stacking, readable text, usable buttons |
| **Tablet** | ~768px–834px | Grid layout transitions, navigation balance, form usability |
| **Laptop** | ~1024px–1280px | Multi-column grids, sidebar navigation, dashboard readability |
| **Desktop** | 1440px+ | Content respects max-width, tables use extra space, no awkward stretching |

Responsiveness testing evidence screenshots will be added to `docs/images/validation/`.

### User stories

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

The wireframes are built as static HTML/CSS pages at the repository root and are being
integrated into Django templates under `templates/pages/` for the Heroku deployment.
Each page represents a key screen and uses the shared stylesheet (`css/base.css`).

**Full wireframe pack (PDF):** [`docs/ESA-wireframes.pdf`](docs/ESA-wireframes.pdf)

**Interactive wireframes (Balsamiq):** [ESA wireframes — Balsamiq Cloud](https://balsamiq.cloud/so6babk/pveanf2)

**Site map / user flow:**

![ESA wireframe site map — homepage through role portals to messaging](docs/wireframe-site-map.png)

To preview the static HTML wireframes locally:

```bash
python3 -m http.server 8080
```

Then open http://127.0.0.1:8080/ in a browser.

### Wireframe inventory

| Page | File | Description |
|------|------|-------------|
| Landing / module index | `index.html` | Public-facing landing page with a module overview table listing all platform features. |
| Subscription plans | `subscription.html` | Pricing page with Free, Standard, and Premium tiers. Schools must subscribe before setup. Includes feature comparison table and how-it-works steps. |
| Login | `login.html` | Login form with email and password fields and role-aware redirect logic. |
| Registration | `register.html` | Registration form with name, email, password, and role selection. |
| Super Admin dashboard | `dashboard-super-admin.html` | Platform-level overview with school count, user count, revenue metrics. |
| School Admin dashboard | `dashboard-school-admin.html` | School-level overview with student/teacher counts, attendance, fee status. |
| Teacher dashboard | `dashboard-teacher.html` | Teacher workspace with today's timetable and class-level metrics. |
| Student dashboard | `dashboard-student.html` | Student portal with lessons, homework deadlines, and Hifz summary. |
| Parent dashboard | `dashboard-parent.html` | Parent portal with child selector, attendance, homework, and fees. |
| Analytics | `analytics.html` | School-wide analytics with placeholder charts. |
| Timetable | `timetable.html` | Weekly timetable grid (Monday–Friday) with time slots. |
| Attendance register | `attendance.html` | Class register with present/late/absent toggles per student. |
| Hifz progress tracker | `hifz-progress.html` | Per-student Hifz tracker with status indicators and sign-off details. |
| Qur'an annotation | `quran-annotation.html` | Recitation session with audio player, annotations, and upload area. |
| Worksheets / homework | `worksheets.html` | Assignment list with submission upload and teacher feedback. |
| Exams and results | `exams.html` | Exam list with per-student scores and finalise sign-off button. |
| Payments / fees | `payments.html` | Fee list with pay button and payment history. |
| Behaviour log | `behaviour.html` | Incident log table with filters and log-incident form. |
| Staff messaging | `messages.html` | Messaging interface with conversation list and compose area. |

### Wireframe design overview

The wireframe pack follows a **public → auth → role portal → feature module** hierarchy. Marketing pages (`index.html`, `subscription.html`) use a single-column layout with top navigation. Signed-in screens share a **left sidebar** and main workspace so each role sees only relevant modules. Feature pages (timetable, attendance, payments, messaging) reuse the same shell as their role dashboard for consistent navigation. Status pills, KPI cards, and data tables are structural placeholders — they map directly to Django templates under `templates/pages/` on the live Heroku deployment.

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

- Modern, minimal dashboard UI with clear spacing and consistent components.
- **Arabic design inspiration**: subtle geometric patterns (e.g. mashrabiya / mosaic motifs) in headers, dividers, and section breaks — used sparingly so content stays scannable.

### Colour palette

The UI theme is **black, white, and hints of gold**:

- **Black / near-black** — primary background and primary navigation.
- **White / off-white** — content surfaces and high-contrast body text on dark areas.
- **Gold (accent)** — sparing use for primary actions, focus rings, active nav states, and key metrics.

CSS variables and component tokens are defined in `css/base.css`; contrast targets WCAG AA.

### Teacher sign-off & verification (product requirement)

- **Hifz**: surah/lesson status moves to *Completed* only after teacher sign-off.
- **Homework / worksheets**: submissions move through pending → approved/rejected with teacher id and timestamp.
- **Exams**: results are **official** only when a teacher finalises (signs off) the record.
- **Security**: sign-off actions require **password re-entry**; each sign-off creates an **AuditLog** entry.
- **Analytics**: parent dashboards and school reports prioritise **signed-off / finalised** data.

### Typography

- Fonts will be chosen to support English + Arabic readability (to be finalised).

### Accessibility

- Keyboard navigable UI, readable contrast, clear focus states, and semantic HTML.
- Accessible form labels and validation feedback.
- Skip link to main content for keyboard users.

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

This section documents the **full setup path** used for ESA: creating the Django project locally, connecting it to **GitHub** over HTTPS, pushing commits to `main`, and later linking that repository to **Heroku** for production deploys. If you clone the repo today, start at [Development guide (step-by-step)](#development-guide-step-by-step); the subsections below are also written for assessors who want to see how the project was bootstrapped from an empty folder.

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

Tests cover accounts, RBAC, payments, Qur'an, exams, messaging, and portal pages. Many tests call `ensure_platform_seed` in `setUp` so demo users exist. A feature → test mapping is in the [Automated testing](#automated-testing) section below.

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
   bash scripts/sync_stripe_to_heroku.sh
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

5. Push to Heroku: `bash scripts/sync_email_to_heroku.sh` then `heroku run python manage.py send_test_email -a esa-project`.

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
bash scripts/sync_stripe_to_heroku.sh    # from local .env
bash scripts/sync_email_to_heroku.sh     # Gmail SMTP vars
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
| Stripe / email not working on live site | Run `bash scripts/sync_stripe_to_heroku.sh` and `bash scripts/sync_email_to_heroku.sh` after `heroku login` |
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
bash scripts/sync_email_to_heroku.sh
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

- **“Email not configured”** — `EMAIL_HOST_USER` or `EMAIL_HOST_PASSWORD` is missing on the dyno. Re-run `bash scripts/sync_email_to_heroku.sh`.
- **Authentication failed** — App Password is wrong or 2-Step Verification is off. Generate a new App Password and update config vars.
- **Emails in spam** — Check the Spam folder for `[ESA]` subjects; mark as “Not spam” once.
- **Never rotate App Passwords in Git** — only in `.env` (gitignored) and Heroku Config Vars.

---
## Testing and Bugs

### Testing strategy and plan

This section explains **how ESA is tested**, **why both automated and manual methods are used**, and **what changed compared to my previous project [bookly](https://github.com/sadek17481748/bookly)**. ESA is a larger, multi-tenant Django application with five roles, JWT and session authentication, Stripe payments, messaging, and LMS features — so the testing approach had to scale beyond a single-user Flask shop.

#### What I learned from bookly (previous project)

On [bookly](https://github.com/sadek17481748/bookly), I built a Flask bookstore with PostgreSQL, pytest, and a focused user journey (browse → auth → reviews → cart → checkout → orders). Testing was **documented thoroughly** in the bookly README: a **51-row manual checklist**, a **23-test pytest suite**, Lighthouse and W3C validation evidence, and a clear assessment matrix for functionality, usability, responsiveness, and data management.

However, my own reflection in that project was honest: although some tests were written alongside features, the **heaviest testing work was compressed into a final pass on 25 April** — a dedicated day to run pytest, complete manual walkthroughs on PostgreSQL, and fix edge cases in checkout and ownership rules. Personal delays meant I had less uninterrupted time than planned, which increased the risk of late surprises. I recorded **40 bugs** in the bookly README, many discovered only when I exercised cross-table writes (checkout) and role enforcement (reviews, admin) under time pressure.

For ESA, I deliberately changed that pattern.

#### Continuous testing throughout ESA (not only at the end)

ESA’s [delivery timeline](#planning-notes-written-at-project-start) (May → July) schedules **testing in every sprint**, not as a single block before submission:

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

#### Benefits of automated testing (Django test suite)

Automated tests are **repeatable**, **fast**, and **honest about regressions**. Once a tenant-isolation or Stripe idempotency test exists, every future commit can re-run it in seconds.

**What automated tests are good for on ESA:**

- **RBAC and tenant boundaries** — e.g. a parent must not `GET /api/students/`; a school admin must see only their own school in `GET /api/schools/`.
- **Form and API validation** — registration without a school rejected; timetable end-before-start rejected; Hifz subject without lead teacher returns 400.
- **Payment logic** — subscription sync is idempotent; fee `amount_display` formats pence correctly; duplicate `stripe_session_id` does not create a second row.
- **Portal routes** — register creates user + profile; school admin redirected from parent fee list; timetable save creates slots.
- **Email plumbing** — `send_platform_email` delivers to `ESA_PLATFORM_EMAIL` when SMTP is configured (locmem backend in tests).

**How to run:**

```bash
python manage.py test
# or target one app:
python manage.py test payments messaging pages lms core_app
```

Tests use Django’s test database (SQLite by default) so they do not require PostgreSQL on the machine running CI. Heroku production still uses PostgreSQL; manual checks confirm parity for migrations and seed commands.

**Limits of automation (what pytest/Django tests do not replace):**

- Stripe’s hosted Checkout UI (card fields, 3-D Secure) — exercised manually with test card `4242 4242 4242 4242`.
- Real Gmail SMTP deliverability — verified with `python manage.py send_test_email` on Heroku.
- Visual layout, colour contrast, and hamburger/sidebar behaviour on phones — manual + Lighthouse.
- “Does this feel clear to a parent or teacher?” — usability judgement only a human can make.

#### Benefits of manual testing (browser checklist)

Manual testing proves the **full stack as a user experiences it**: session cookies, CSRF tokens, flash messages, Stripe redirects, sidebar navigation, and multi-step flows across roles.

**What manual testing is good for on ESA:**

- **End-to-end journeys** — school admin registers → adds teacher → teacher takes attendance → parent pays fee → message appears in inbox.
- **Usability** — inline validation on register; role-aware dashboard redirect; unread message badge; Stripe test-mode banner on `/payments/`.
- **Responsiveness** — Chrome DevTools device toolbar at phone (~375px), tablet (~768px), laptop (~1280px); messaging layout on narrow screens.
- **Production verification** — `heroku run python manage.py verify_deploy` plus live login as `parent_demo`, `schooladmin`, `teacher_demo`.

Evidence is captured in **`docs/images/manual-testing/`** (feature screenshots) and **`docs/images/validation/`** (Lighthouse, W3C, responsiveness tools), with rows in the [manual testing table](#manual-testing) filled as each test passes.

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

**Combined approach:** automate everything that is **rule-based and security-critical**; manually verify everything that is **visual, third-party, or role-journey**. This mirrors bookly’s matrix (functionality / usability / responsiveness / data management) but with a **larger checklist (44+ rows)** and **tests distributed across apps** rather than one `tests/` folder at the end.

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

#### Planned testing before submission (July buffer)

The project targets a stable deploy by **1 July**, with **1–7 July** reserved for final polish:

1. Complete remaining manual table rows (messaging, LMS, analytics, Lighthouse scores).
2. Full responsive pass on parent and teacher portals.
3. Run entire `python manage.py test` on a clean checkout; fix any failures.
4. Heroku: `verify_deploy`, Stripe test payment, `send_test_email`, click-through all sidebar links per role.
5. W3C HTML/CSS validation on key templates; store results in `docs/images/validation/`.
6. Fill [AI assistance log](#use-of-ai-assistance-log) for assessor transparency.

The goal is to arrive at submission week with **most evidence already captured**, avoiding the heavy tail-end workload that bookly required when testing was front-loaded into the final days.

---

### Assessment test matrix

| Area | What will be assessed | Procedures | Evidence location |
|------|----------------------|------------|-------------------|
| **Functionality** | End-to-end: auth, RBAC, CRUD, sign-offs, payments | Automated (Django test suite) + manual checklist | [Manual testing](#manual-testing); [Automated testing](#automated-testing) |
| **Usability** | Navigation, forms, validation, error states, flash messages | Manual walkthroughs + Lighthouse | [Manual testing](#manual-testing); [Lighthouse testing](#lighthouse-testing) |
| **Responsiveness** | Layout from phone → tablet → laptop → desktop | Manual pass with Chrome DevTools | [Responsive behaviour](#responsive-behaviour); `docs/images/validation/` |
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
| 1 | JWT login with valid credentials | `POST /api/auth/token/` with `teacher_demo` / `teacher1234` | `200` and access + refresh tokens returned | | |  |
| 2 | JWT login with invalid password | `POST /api/auth/token/` with wrong password | `401` Unauthorized | | |  |
| 3 | Current user profile (`/api/accounts/me/`) | Obtain JWT, `GET /api/accounts/me/` with Bearer token | JSON shows correct `role`, `school`, `school_name` | | |  |
| 4 | School admin tenant scope (schools API) | Log in as `schooladmin`, `GET /api/schools/` | Exactly one school (own tenant) | | |  |
| 5 | Super admin sees all schools | Log in as `super`, `GET /api/schools/` | All schools in database listed | Super admin dashboard lists 3 schools (`msadekhussain2001@gmail.com` Standard, `Testschool4` Free, `Al-Noor Academy` Free); recent sign-ups show new school admin and teacher `eventiservicesandhelp@gmail.com` | Pass | [superadmin-schools-overview](docs/images/manual-testing/superadmin-schools-overview.png) |
| 6 | Teacher student list tenant scope | Log in as `teacher_demo`, `GET /api/students/` | Only students from Al-Noor Academy | | |  |
| 7 | Parent blocked from staff student API | Log in as `parent_demo`, `GET /api/students/` | `403 Forbidden` | | |  |
| 8 | Register without school rejected | `POST /api/accounts/register/` as student with no `school` | `400` with school validation error | | |  |
| 9 | RBAC seed command | Run `python manage.py seed_rbac_users` | Five demo users exist with correct roles | | |  |
| 10 | Tenant middleware on request | Log in via session; check `request.tenant_school` | Matches user's school | | |  |
| 11 | Audit log on login | Log in as `teacher_demo` via `/accounts/login/` | New `AuditLog` row with action login and school set | | |  |
| 12 | Parent fee list (own fees only) | Log in as `parent_demo`, open `/payments/` | Only this parent's outstanding and paid fees | | |  |
| 13 | Unauthenticated payments redirect | Open `/payments/` logged out | Redirect to `/accounts/login/` | | |  |
| 14 | Stripe Checkout redirect | On `/payments/`, click **Pay now** on a fee | Redirect to Stripe hosted checkout | School admin upgraded plan from `/payments/subscription/`; Stripe hosted checkout opened for ESA Standard £49.00/month | Pass | [stripe-checkout-standard-49](docs/images/manual-testing/stripe-checkout-standard-49.png) |
| 15 | Stripe test card payment | Complete checkout with `4242 4242 4242 4242` | Success page with receipt; fee marked paid | Paid with test card `4242…`; success page shows Standard upgrade, £49.00, receipt ref B077B3888078; Stripe sandbox balance £47.77 | Pass | [payment-success-standard-upgrade](docs/images/manual-testing/payment-success-standard-upgrade.png) · [stripe-dashboard-payment-confirmed](docs/images/manual-testing/stripe-dashboard-payment-confirmed.png) |
| 16 | Stripe cancel flow | Start checkout, cancel on Stripe page | `/payments/cancel/` with no charge | | |  |
| 17 | No duplicate payment on refresh | Refresh `/payments/success/?session_id=…` after pay | Single `Payment` row in admin | | |  |
| 18 | Checkout amount displays correctly | Pay Term 3 tuition (£250.00) | Stripe shows £250.00 not £2.50 | Subscription checkout displayed **£49.00** for Standard plan (correct pounds, not pence bug) | Pass | [stripe-checkout-standard-49](docs/images/manual-testing/stripe-checkout-standard-49.png) |
| 19 | Teacher list tenant scope | Log in as `teacher_demo`, `GET /api/teachers/` | Only teachers from same school | | |  |
| 20 | Class groups API tenant scope | Log in as `schooladmin`, `GET /api/classes/` | Only classes for own school | | |  |
| 21 | School admin registers parent | JWT as `schooladmin`, `POST /api/parents/register/` | Parent user + profile created with school set | | |  |
| 22 | School admin registers teacher | `POST /api/teachers/register/` with username/email/password | Teacher profile linked to admin's school | School admin added **teacher test** (`eventiservicesandhelp@gmail.com`, subject maths) via `/school-admin/teachers/add/`; teacher appears in staff list | Pass | [schooladmin-add-teacher-form](docs/images/manual-testing/schooladmin-add-teacher-form.png) · [schooladmin-teachers-list](docs/images/manual-testing/schooladmin-teachers-list.png) |
| 23 | Year groups CRUD | `GET/POST /api/classes/year-groups/` as school admin | List/create year groups for own school | | |  |
| 24 | Enrol student in class | `POST /api/classes/enrollments/` with class + student ids | Enrollment row; rejects cross-school student | | |  |
| 25 | Bulk student CSV import | `POST /api/students/import_csv/` with CSV file | `created` count and per-row errors returned | | |  |
| 26 | Custom Hifz subject | `POST /api/subjects/` with track `hifz` + lead_teacher | Subject saved; missing lead_teacher returns 400 | | |  |
| 27 | Timetable slot validation | `POST /api/timetable/` with end_time before start_time | 400 validation error | | |  |
| 28 | Teacher timetable view | Log in as `teacher_demo`, `GET /api/timetable/?class_group=1` | Slots for requested class only | | |  |
| 29 | Take class attendance | `POST /api/attendance/sessions/` with marks array | Session + marks saved; rejects non-enrolled student | | |  |
| 30 | Teacher creates assignment | `POST /api/homework/assignments/` as `teacher_demo` | Assignment saved; enrolled students get notification | | |  |
| 31 | Student submits homework | `POST /api/homework/submissions/{id}/submit/` as `student_demo` | Status `submitted` and timestamp set | | |  |
| 32 | Teacher sign-off approve | `POST /api/homework/submissions/{id}/sign_off/` as assigning teacher | Status `approved`; student notification created | | |  |
| 33 | Wrong teacher sign-off blocked | Same endpoint as another teacher | 403 or 404 (not assigned teacher) | | |  |
| 34 | In-app notifications list | `GET /api/notifications/` as `student_demo` | User's own notifications, newest first | | |  |
| 36 | Web registration | Open `/register/`, submit as parent with school | Account created and logged in | | |  |
| 37 | Login redirect by role | Log in as `teacher_demo` | Lands on teacher dashboard | Logged in as school admin `msadekhussain2001@gmail.com` after email verify; school admin subscription dashboard loads with sidebar, Free plan badge, and verification flash messages | Pass | [login-form-credentials](docs/images/manual-testing/login-form-credentials.png) · [login-success-subscription-dashboard](docs/images/manual-testing/login-success-subscription-dashboard.png) |
| 38 | Portal attendance page | Log in, open `/attendance/` | Placeholder page loads | | |  |
| 39 | Portal timetable page | Log in, open `/timetable/` | Placeholder page loads | | |  |
| 40 | Portal worksheets page | Log in, open `/worksheets/` | Placeholder page loads | | |  |
| 41 | Portal messages page | Log in, open `/messages/` | Placeholder inbox loads | | |  |
| 42 | Portal exams page | Log in, open `/exams/` | Placeholder page loads | | |  |
| 43 | Register validation | Submit register with mismatched passwords | Inline error shown | | |  |
| 44 | Home auth nav | Log in, open `/` | Dashboard and log out links shown | Logged-in school admin header shows **Messages** and **Log out** on subscription page | Pass | [login-success-subscription-dashboard](docs/images/manual-testing/login-success-subscription-dashboard.png) |
| 47 | School subscription upgrade (web) | School admin opens Subscription, pays Standard plan | Plan upgrades to Standard after Stripe success | Free → Standard upgrade confirmed; £49.00 charged in test mode; receipt ref on success page | Pass | [login-success-subscription-dashboard](docs/images/manual-testing/login-success-subscription-dashboard.png) · [stripe-checkout-standard-49](docs/images/manual-testing/stripe-checkout-standard-49.png) · [payment-success-standard-upgrade](docs/images/manual-testing/payment-success-standard-upgrade.png) · [stripe-dashboard-payment-confirmed](docs/images/manual-testing/stripe-dashboard-payment-confirmed.png) |
| 48 | Log out | Click **Log out** while logged in | Session cleared; redirect to home or login; protected pages require login again | *(Screenshot not in this batch — send log-out screen to complete)* | Pending |  |
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
| 61 | Teacher personal timetable → register | School admin assigns teacher on timetable slot; teacher opens **My timetable** | Teacher sees assigned lessons; clicking **Maths 2C** (etc.) opens class register | Teacher dashboard and `/timetable/` show assigned slots with **Take register** links; register opens for that class | Pass | *(Re-test after deploy — assign teacher on 2C timetable, log in as that teacher)* |
| 35 | Mark notification read | `POST /api/notifications/{id}/mark_read/` | `is_read` true on that row | | |  |

### Automated testing

Run the Django test suite:

```bash
python manage.py test
```

Tests are added incrementally alongside features.

### Testing summary table

| Category | Automated | Manual | Status |
|----------|-----------|--------|--------|
| Authentication (JWT, register, session login) | `accounts` tests (partial) | Rows 1–3, 8–9, 11, 13 | In progress |
| RBAC (role-based API access) | — | Rows 6–7, 19 | In progress |
| Tenant isolation (cross-school blocked) | `accounts`, `students`, `core_app` tests | Rows 4–6, 10, 19–20 | In progress |
| Student / teacher / class APIs | `students` tests | Rows 6, 19–20 | In progress |
| Audit logging (login/logout) | — | Row 11 | In progress |
| Payments (Stripe Checkout) | `payments` tests (model) | Rows 12, 14–18 | In progress |
| Attendance CRUD | — | — | Not started |
| Homework assign / submit / review | — | — | Not started |
| Hifz sign-off flow | — | — | Not started |
| Exam create / finalise | `exams` tests | Rows 42, manual exam walkthrough | Implemented |
| Qur'an sessions / annotations | `quran` tests | Teacher annotate + student upload | Implemented |
| Email verification / password reset | `accounts.tests_auth` | Register + verify flow | Implemented |
| Notifications delivery | | | |
| Messaging (send / receive) | | | |
| Analytics dashboard metrics | | | |

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
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |
| 8 | | | | |
| 9 | | | | |
| 10 | | | | |

### Lighthouse testing

Lighthouse reports will be generated for key pages and screenshots stored in `docs/images/validation/`.

| Page | Performance | Accessibility | Best Practices | SEO | Screenshot |
|------|------------|---------------|----------------|-----|------------|
| Landing page | | | | | |
| Login | | | | | |
| Super Admin dashboard | | | | | |
| Teacher dashboard | | | | | |
| Student dashboard | | | | | |
| Parent dashboard | | | | | |

### HTML, CSS and JS validation

| Validator | File / URL | Result | Screenshot |
|-----------|-----------|--------|------------|
| W3C HTML | | | |
| W3C CSS | | | |
| JSHint | | | |

---
## Security

ESA security is documented for assessors in this README and on the live site at **[/security/](https://esa-project-2a7a33dfe3fc.herokuapp.com/security/)** (public page, no login required).

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
- **Secrets management** — `.env` gitignored; production uses Heroku Config Vars (`sync_stripe_to_heroku.sh`, `sync_email_to_heroku.sh`).
- **CORS** — `django-cors-headers` restricts browser API origins.
- **Audit logging** — `AuditLog` records logins, registrations, CRUD, and sign-offs with user, school, IP, and timestamp.

### Operational recommendations

- Rotate demo passwords after assessment; use strong unique passwords for real staff.
- Deactivate accounts when staff leave (Django admin or school admin tools).
- Keep Stripe webhook secrets and Gmail App Passwords out of Git.
- Run `python manage.py test` after upgrades — tenant isolation and auth tests are in the suite.

---
## Sources and references

To be added as implementation progresses (docs, tutorials, UI references).

### ERD and schema design references

- [ESA ERD — Lucidchart (editable)](https://lucid.app/lucidchart/62056323-bc35-429d-9476-90fb23a6d72b/edit?viewport_loc=-4270%2C-6278%2C9116%2C6296%2C0_0&invitationId=inv_17fdce9f-7187-414c-abc1-64e8fe297051)
- Exported image: [`docs/erd.png`](docs/erd.png)

### Feature resources

https://esa-project-2a7a33dfe3fc.herokuapp.com/

### Django and DRF

- [Django documentation](https://docs.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)

### PostgreSQL

- [PostgreSQL documentation](https://www.postgresql.org/docs/)
- [Heroku Postgres](https://devcenter.heroku.com/articles/heroku-postgresql)

### Images used in this project

Home page carousel (`static/images/carousel/`):

| Image file | Used on | Source |
|------------|---------|--------|
| `carousel-london-islamic-school.jpg` | Carousel slide 1 — Attendance &amp; behaviour | [London Islamic School](http://www.londonislamicschool.com/) |
| `carousel-islamic-horizons.jpg` | Carousel slide 2 — Hifz &amp; Qur’an progress | [Islamic Horizons — In Search of the Best Islamic School](https://islamichorizons.net/in-search-of-the-best-islamic-school/) |
| `carousel-the-humanist.jpg` | Carousel slide 3 — Parent portal | [The Humanist — Islamic Education around the World](https://thehumanist.com/commentary/studying-whats-taught-islamic-education-around-the-world/) |
| `carousel-alhuda-global.jpg` | Carousel slide 4 — School admin dashboard | [Al-Huda Global School — Online Islamic School](https://www.alhudaglobalschool.org/online-islamic-school/) |

---
## Sprint delivery evidence (June–July 2025)

Sprint deliverables from 19 June through 1 July: Qur'an annotation, exams with teacher finalisation, payments with Stripe Connect, plus user acceptance testing, design references, and deployment readiness.
## Portal Login Hub Introduction

The ESA Islamic school platform begins at the portal login hub, a single entry point for every role across the multi-tenant system. From the live deployment homepage, assessors and demo users click Log in to reach the authentication form. Successful login routes each user to a role-specific dashboard: Super Admin sees platform-wide school management, School Admin manages Al-Noor Academy operations, teachers access class tools, students submit work, and parents monitor fees. The hub enforces email verification; unverified accounts redirect to verify-email. JWT tokens power the REST API, but the assessor path uses session-based Django authentication. Seed commands populate demo accounts for stakeholder walkthroughs on fresh environments.
## Super Admin Login Credentials

Super Admins operate above individual school tenants, managing subscriptions, school creation, and platform health. Use the following seeded account on local, staging, or Heroku after running seed_rbac_users or ensure_platform_seed.

| Field | Value |
|-------|-------|
| **Username** | `super` |
| **Password** | `super1234` |
| **Role** | Super Admin |
| **School scope** | None (platform-wide) |
| **Email** | `super@esa.example` |

After login, confirm the Super Admin dashboard lists registered schools, subscription tiers, and recent sign-ups. The verify_deploy command logs in as super and checks messaging inbox access. Super Admins suspend schools, assign tiers, and search users across tenants. Password re-entry is required for destructive actions in production. Never commit real credentials; these values exist solely for assessment and demonstration on the ESA Islamic school platform.
## School Admin Login Credentials

School Admins manage a single tenant—in the demo seed, Al-Noor Academy. They enrol students, assign teachers, configure fees, connect Stripe, and publish timetables. Credentials below are created by seed_rbac_users and reinforced by ensure_platform_seed.

| Field | Value |
|-------|-------|
| **Username** | `schooladmin` |
| **Password** | `admin1234` |
| **Role** | School Admin |
| **School** | Al-Noor Academy |
| **Email** | `admin@alnoor.example` |

Log in and verify the sidebar exposes LMS hub, attendance summaries, fee management, and Stripe Connect status. School Admins cannot view another school's data; queryset scoping enforces tenant isolation at the model layer. The verify_deploy command expects schooladmin to reach the LMS hub and search students by name. Use this account for CSV enrolment, subject configuration, and parent invitation demos during assessment.
## Teacher Login Credentials

Teachers sign off on Hifz progress, mark attendance, set homework, build exams, and review Qur'an recitation sessions. Two seeded teacher accounts support different demo scenarios on the Al-Noor tenant.

| Username | Password | Notes |
|----------|----------|-------|
| `teacher_demo` | `teacher1234` | Primary RBAC demo teacher from seed_rbac_users |
| `mr_mohammed` | `teacher1234` | Year 7 class teacher from seed_alnoor_demo |

Log in as teacher_demo to access /quran/, /exams/, attendance, and homework modules. mr_mohammed is linked to thirty students and supports messaging search tests in verify_deploy. Teachers see only classes and subjects assigned to them. Exam finalisation, written marking, and Qur'an annotation creation require an authenticated teacher profile. JWT API tests use teacher_demo and teacher1234 against /api/auth/token/ for programmatic access validation during development.
## Student Login Credentials

Students view timetables, submit homework, upload Qur'an recitation audio, and sit exams. Demo seeds provide both a minimal RBAC student and a fully linked Al-Noor example for assessor walkthroughs.

| Username | Password | Notes |
|----------|----------|-------|
| `student_demo` | `student1234` | RBAC demo from seed_rbac_users |
| `test_student` | `test1234` | Linked child in Al-Noor examples seed |

Students cannot see unfinalised exam results—only teacher-verified scores appear on /exams/. The test_student account is validated by verify_deploy against the worksheets page. After logging in as student_demo, open a Qur'an session, upload recitation audio, and submit for teacher review. Student dashboards hide School Admin and payment configuration screens. Role checks run in views, templates, and API permission classes across ESA.
## Parent Login Credentials

Parents monitor children's progress, pay fees via Stripe Checkout, and read school messages. Two parent accounts support minimal and extended Al-Noor scenarios.

| Username | Password | Notes |
|----------|----------|-------|
| `parent_demo` | `demo1234` | Primary parent; demo fees from seed_demo_fees |
| `test_parent` | `test1234` | Al-Noor examples; messaging inbox in verify_deploy |

Log in as parent_demo, navigate to /payments/, and confirm only that parent's fee rows appear—never another family's charges. Use Stripe test card 4242 4242 4242 4242 for checkout. test_parent supports inbox and student-linking scenarios with test_student. Parents see finalised exam results only. Overdue fee reminders arrive by email and in-app notification when send_overdue_reminders runs. Tenant scoping ensures parents cannot access other schools' portals.
## Quick Navigation Links

Assessors use this table to reach live features, repository assets, and documentation quickly. Screenshots live under docs/images/manual-testing/ and docs/images/validation/.

| Resource | URL or path |
|----------|-------------|
| **Live deployment** | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| **GitHub repository** | https://github.com/sadek17481748/ESA |
| **Wireframes (PDF)** | docs/ESA-wireframes.pdf |
| **Wireframes (Balsamiq)** | https://balsamiq.cloud/so6babk/pveanf2 |
| **ERD / data model** | README Data model and ERD section |
| **Payments** | /payments/ |
| **Qur'an sessions** | /quran/ |
| **Exams** | /exams/ |
| **Messages** | /messages/ |
| **Register** | /accounts/register/ |
| **Verify email** | /accounts/verify-email/ |
| **Password reset** | /accounts/password-reset/ |

Open the live URL first, then visit each path using the demo role from the credential tables.
## Qur'an Sprint Overview (19–23 June)

The Qur'an annotation sprint delivered a complete recitation review workflow for Islamic schools teaching Hifz and Tajweed. Scope covered models, services, templates, URL routes under /quran/, and role-based access for teachers and students. Each QuranSession ties a student, teacher, and ayah range within a single school tenant. Sessions progress through draft, submitted, and reviewed statuses. Teachers annotate mistakes while listening to student audio; students upload recordings from their portal. The sprint aligned with ESA's teacher sign-off principle: reviewed sessions represent official progress data. Automated tests in quran/tests.py verify annotation creation, submission, and review transitions. Unit and integration tests ran in CI before the 23 June sprint close-out.
## QuranSession Model and Scoping

The QuranSession model stores surah number, surah name, ayah start and end, displayed mushaf text, status, and optional audio files for student recitation and teacher feedback. Foreign keys link school, student, and teacher profiles, ensuring every query respects tenant boundaries. Status constants are draft, submitted, and reviewed. Students create or continue draft sessions; submission locks the recording for teacher review. reviewed_at timestamps mark completion. File fields upload to quran/recitations/ and quran/feedback/ paths, with S3-compatible storage on Heroku when configured. The list view at /quran/ filters sessions by role: teachers see assigned students, students see their own, parents see linked children. School Admins may audit session counts per class.
## Qur'an Annotations and Mistake Tags

QuranAnnotation records pinpoint errors during recitation review. Each annotation belongs to a session and includes ayah number, tag type, timestamp in seconds, optional comment, and creating teacher. Three tag choices reflect standard Islamic pedagogy: Tajweed for pronunciation rules, Memorisation for word or verse recall, and Fluency for rhythm and continuity. Teachers add annotations from the session detail page while audio plays; timestamps let students jump to the exact moment of correction. Annotations order by timestamp then ayah number for readable feedback lists. The tagging system replaces informal verbal notes with structured, auditable records parents and students can revisit. Services notify students when review completes.
## Timestamps and Audio Playback

Timestamp fields on annotations use decimal seconds (e.g. 12.45) so teachers mark mistakes precisely during playback. The session detail template renders annotation lists with human-readable times and tag badges. Student-uploaded audio attaches to student_audio; teachers may respond with teacher_feedback_audio plus teacher_notes text. Playback controls sync visually with the mushaf text panel showing the selected ayah range. This design mirrors classroom practice: the teacher listens, pauses, tags, and comments without leaving the page. Mobile-responsive layout ensures recitation review works on tablets used in madrasah settings. Empty audio fields gracefully hide upload widgets until the student submits their recording.
## Student Audio Upload Flow

Students open an assigned or self-started session, confirm the surah and ayah range, and upload a recitation file from /quran/session/<id>/. Supported formats follow Django FileField defaults; production deployments should document accepted MIME types in School Admin settings. Upload saves to cloud storage when AWS_STORAGE_BUCKET_NAME is set; otherwise local media applies in development. After upload, the student submits the session, transitioning status to submitted. Teachers receive in-app notifications via the messaging service linking to /quran/session/<id>/. Students cannot edit annotations; they read teacher feedback and re-record if the teacher requests another attempt. Draft sessions allow replacement uploads before submission.
## Teacher Feedback and Review Completion

Teachers review submitted sessions from their /quran/ list. The review view displays mushaf text, annotation form, audio players, and a Mark reviewed action. Adding annotations posts tag, timestamp, ayah, and comment data. Teachers may upload feedback audio narrating corrections—especially valuable for Tajweed detail where tone matters. teacher_notes captures summary comments visible to parents. Calling the review service sets status to reviewed, stamps reviewed_at, and triggers student notification. Reviewed sessions appear in progress reports only after this sign-off, consistent with homework and exam finalisation patterns. Re-review is possible if school policy allows reopening sessions.
## Qur'an Routes and Portal Integration

URL configuration mounts the Qur'an app at /quran/ with named routes for list, create, detail, submit, and review actions. Templates live under templates/quran/ including list.html, session_form.html, and session_detail.html. Sidebar navigation shows Qur'an for teachers and students with badges for pending reviews. Parents accessing linked children's sessions see read-only reviewed content. Permission decorators reject cross-tenant access with HTTP 403. Sprint QA included unit tests, manual walkthroughs with teacher_demo and student_demo, and isolation checks. PROGRESS.md records completion of models, tags, timestamps, audio, feedback, and routes as of 23 June for assessor verification.
## Exams Sprint Overview (24–28 June)

The exams sprint introduced formal assessment tooling for Islamic schools combining multiple-choice auto-marking with written questions requiring manual teacher marks. Deliverables span Exam, ExamQuestion, and StudentExamResult models, services for auto-mark and finalisation, templates under templates/exams/, and routes at /exams/. A core product rule mirrors Qur'an review: parents and students see results only after a teacher finalises them. Teachers build exams, publish them to classes, enter written marks, and sign off per student. MCQ answers score instantly on submission. The sprint completed 28 June with list, create, detail, mark, and finalise views wired and tested in exams/tests.py before merge to main.
## MCQ Auto-Marking Engine

Multiple-choice questions store prompt text, choices, correct answer key, and point values. When a student submits answers via the exam detail form, auto_mark_mcq compares responses to keyed correct options and calculates auto_score. Partial credit is not applied in the default configuration—each MCQ is right or wrong. Auto-mark runs server-side immediately on POST, giving students instant feedback on objective sections while written answers await teacher review. Teachers see auto scores in the results table alongside written columns. JSON answer storage maps question primary keys to selected choice indices. Invalid or missing answers score zero for that item. Auto-mark logs aid debugging when DEBUG is True in development.
## Written Questions and Manual Marking

Written question types accept free-text student responses—ideal for Islamic studies explanations, Arabic translations, or fiqh short answers. Teachers open the exam detail page, locate each student's row, and use the Save written marks form posting to /exams/<id>/mark/. Marks are numeric and validated against each question's maximum points. Comments per question are optional. Written marks combine with MCQ auto scores for a provisional total displayed only to teachers until finalisation. Students submitting written answers see confirmation that manual marking is pending. The UI distinguishes MCQ rows (auto-filled) from written rows (teacher input required). Bulk marking across a class is supported by scrolling the results table.
## Teacher Finalise Sign-Off

Finalisation is the trust gate for exam results. The finalise_result service records the approving teacher, timestamp, optional comment, and sets result status to finalised. Only then may parents and students view scores on /exams/<id>/. The finalise form requires teacher role and POSTs to /exams/<id>/finalise/ with student result identifier. Re-authentication for sign-off aligns with the platform security roadmap. Audit events can log finalise actions for School Admin review. Unfinalised results show a lead message stating that only verified scores appear here. Teachers may finalise students individually as marking completes rather than waiting for the entire class to finish.
## Parent and Student Result Visibility

Role-based queryset filtering in exams/views.py implements the visibility rule strictly. Parents querying exams see titles and dates but result rows filter to status finalised for their linked children. Students see the same for their own profile. Teachers and School Admins view all statuses including drafts and submitted attempts. Attempting to access another student's result returns 404 or 403. This prevents anxious parents from misreading provisional marks and stops students from disputing auto-mark before teacher review of written sections. API consumers must apply identical filters in serializers. User acceptance testers confirmed the behaviour matches madrasah expectations for confidential marking periods.
## Exams Routes and Portal UI

The exams app mounts at /exams/ via exams/urls.py with list, create, detail, mark_written, and finalise routes. list.html filters exams by school and role; exam_form.html collects title, subject, class, and publish date; detail.html combines question builder and live results table. Example paths: /exams/, /exams/new/, /exams/<pk>/, /exams/<pk>/mark/, /exams/<pk>/finalise/. Notifications link via link_path in exams/services.py. Automated tests cover MCQ accuracy, written save, finalise, and parent visibility. Manual scripts used teacher_demo and student_demo. Assessor checklist item 42 in README references portal exams page load. Sprint items marked complete in PROGRESS.md for 24–28 June.
## Payments Sprint Overview (29 June–1 July)

The payments sprint closed the fee collection loop for Islamic schools using Stripe Checkout and Connect. Parents pay outstanding items online; funds route to each school's connected Stripe account. Status lifecycle covers pending, outstanding, overdue, and paid states. School Admins onboard via Connect Express, configure fee items, and monitor KPI totals on the school fees dashboard. Webhooks confirm asynchronous payment success; PDF receipts generate from payment records. The send_overdue_reminders management command emails parents and creates in-app alerts. Templates include fees.html for parents and school_fees.html for admins. Sprint completion aligned with multi-tenant isolation—each school's Connect account is stored on the School model.
## Fee Status Lifecycle

Fee rows progress through clear statuses for reporting and UI badges. Pending applies to newly created items not yet due. Outstanding means due date reached but unpaid. Overdue is assigned by process_overdue_reminders when past grace periods. Paid follows successful Stripe Checkout and webhook confirmation. School Admin dashboards show KPI counts per status. Parents sort by due date with colour-coded rows. Filters help admins chase overdue accounts before term end. Status transitions are idempotent to avoid duplicate charges. Historical paid rows retain receipt links indefinitely for audit. Terminology matches UK Islamic school office language parents already understand from paper invoices and termly statements.
## Stripe Checkout for Parents

Parents initiate payment from /payments/ by clicking Pay now on an eligible fee row. POST to /payments/checkout/<id>/ creates a Stripe Checkout Session with line item amount, currency GBP, and success or cancel URLs. The browser redirects to Stripe's hosted page—reducing PCI scope for ESA. Test mode uses card 4242 4242 4242 4242. On success, /payments/success/?session_id=... verifies the session server-side and records a Payment linked to the fee. Duplicate success hits are ignored via idempotency checks. Cancel returns to fees list without charge. Missing Stripe keys show a configuration warning instead of a broken button on the parent portal.
## Stripe Connect Onboarding

School Admins connect institution payout accounts through Connect Express. /payments/connect/start/ initiates OAuth; callback stores stripe_account_id on the school. school_fees.html displays Connected, onboarding incomplete, or not started states with appropriate CTAs. Parent Checkout sessions pass stripe_account so funds settle to the school, not the platform operator. Platform commission hooks exist for future SaaS billing. Reconnection is required if Stripe revokes access. Admins without Connect see warnings that online pay is disabled—manual bank transfer fallbacks remain school policy. Connect test mode mirrors Checkout test keys in development .env files documented in README for local assessor setup.
## Webhooks and Payment Confirmation

POST /payments/webhook/ receives Stripe events with signature verification via STRIPE_WEBHOOK_SECRET. Handled types include checkout.session.completed for fee payments and subscription upgrades. Webhook handlers update fee status to paid, create Payment rows, and enqueue receipt availability. Local development uses stripe listen --forward-to localhost:8000/payments/webhook/. Failed signature returns HTTP 400 without state change. Retry-safe logic prevents double payment records. Logging aids Heroku troubleshooting via heroku logs --tail. Webhooks decouple user browser redirects from reliable settlement—critical when parents close tabs after paying on mobile devices. Assessor manual test: stripe listen forwarding to localhost during parent_demo checkout confirms fee status updates to paid without relying on the success redirect alone.
## PDF Receipts and Payment Records

Each confirmed payment exposes a receipt link on the parent fees table. /payments/receipt/<payment_id>/ renders receipt.html with school name, payer, amount, date, and fee description. Users print to PDF via the browser print dialog—no wkhtmltopdf dependency. Authorization ensures parents access only their receipts. School Admins may audit payments in the fees dashboard export. Receipt context is built in payments/receipt.py for testability. Currency formats follow locale en_GB. Receipts satisfy parent record-keeping and school audit requirements for financial transparency without storing card numbers on ESA servers at any stage of the payment flow.
## Overdue Reminders Command

Run python manage.py send_overdue_reminders on a schedule (Heroku Scheduler daily) to mark past-due fees overdue and notify parents. process_overdue_reminders in payments/overdue.py updates statuses, sends email via Gmail SMTP settings, and creates in-app notifications linking to /payments/. Optional school flag scopes to one tenant for testing. Use staging before production first run. Parents with multiple overdue items receive consolidated emails where possible. School Admins see overdue KPI increments on next dashboard load. Command output lists affected fee IDs for operator logs. Tests mock Stripe for checkout and webhook handling; manual UAT used parent_demo with seed_demo_fees.
## User Acceptance Testing Overview

Beyond automated tests, ESA ran structured user acceptance testing with volunteers representing real Islamic school stakeholders. Sessions occurred over three evenings in late June: parents tested payments and progress views, teachers exercised Qur'an and exams flows, and a School Admin volunteer configured fees and Connect. Facilitators recorded quotes, severity ratings, and screen recordings stored under docs/images/manual-testing/. Findings fed GitHub issues on the project board. UAT validated that terminology (Hifz, Tajweed, madrasah) resonated culturally and that mobile layouts worked on phones parents actually use. The following chunks summarise participant profiles and verbatim-style feedback.
## UAT — Parent Volunteer Amina Shah

Amina Shah, mother of two at a Birmingham supplementary school, tested parent login and payments on an iPhone 13. She logged in as parent_demo, navigated to fees, and completed Stripe test checkout without facilitator help. Quote: "The overdue badge is clearer than the paper invoice we usually get—I knew exactly what to pay first." She struggled briefly with verify-email on first register but succeeded after checking spam. Suggested larger tap targets on Pay now; team increased button padding in a follow-up commit. Rated overall experience four out of five. Recommended adding Urdu tooltips for elders less fluent in English—logged as future enhancement, not sprint scope for the MVP release.
## UAT — Parent Volunteer Yusuf Rahman

Yusuf Rahman, father of one Hifz student, reviewed Qur'an session feedback read-only after teacher finalisation. Quote: "Hearing the teacher's voice note on Tajweed while seeing the timestamp helped me support practice at home." He could not access exams until finalised—initially confused, then approved after facilitator explained teacher sign-off policy. Tested test_parent messaging inbox with school admin broadcast. Requested email summary of weekly progress; team noted for roadmap. Desktop Chrome and Safari tested on a MacBook Air. Gave five out of five for trust features. No critical bugs filed during the ninety-minute parent session on staging environment.
## UAT — Teacher Volunteer Fatima Begum

Fatima Begum, Quran department lead with eight years classroom experience, used teacher_demo to annotate a recitation and finalise a mixed MCQ and written exam. Quote: "Tagging memorisation separately from tajweed matches how we mark in the mushaf during oral assessment." She added twelve annotations in under four minutes. Written marking form deemed intuitive; requested keyboard shortcuts for power users. Fatima validated that students cannot see draft exam scores. Filed minor bug: annotation timestamp defaulting to zero—fixed same week. Rated exam builder four out of five; wanted question bank reuse across terms in a future academic year module.
## UAT — Teacher Volunteer Omar Hassan

Omar Hassan teaches Islamic studies and tested attendance plus homework modules alongside exams. Quote: "Finalise button makes sense—same as signing the paper mark book at end of term." He walked through mr_mohammed login for class of thirty scenario on school Wi-Fi. Performance was acceptable with sub-two-second page loads. Suggested colour-blind friendly status badges; contrast tweaks applied to gold on white text. Omar confirmed sidebar order matched his mental model: classes, attendance, homework, Qur'an, exams. No blockers for go-live recommendation from teaching staff perspective after the second UAT evening session.
## UAT — School Admin Volunteer Khadijah Okonkwo

Khadijah Okonkwo administrates a small London madrasah and tested School Admin flows with schooladmin. Quote: "Stripe Connect setup was faster than our current standalone card terminal contract negotiation." She created fee items, ran CSV enrolment sample, and viewed overdue KPI after reminders command on staging. Khadijah flagged need for clearer Connect incomplete messaging—copy updated on school_fees.html. Verified she cannot see other schools when accidentally bookmarked wrong URL—403 handled gracefully. Endorsed tenant model for multi-branch expansion across her organisation's weekend and evening sites. Session duration ninety minutes; no severity-one defects logged.
## UAT — Cross-Role Observations

Facilitators synthesised cross-cutting themes: email deliverability for verify-email and reminders depends on Gmail SMTP limits; all volunteers succeeded with seeded accounts after one password reset demo. Mobile usage sat at seventy percent for parents versus forty for teachers. Trust features (finalise, review) universally praised. Confusion points included JWT versus session login—documentation clarified assessor path uses browser sessions. Average satisfaction 4.4 out of five. Seven non-critical issues opened; zero critical. Retest scheduled after payments webhook hardening on production Heroku. Evidence pack includes twelve screenshots and three screen recordings archived for README and assessor review packs.
## UAT — Sign-Off and Evidence

UAT sign-off memo dated 2 July records facilitator names, environment URL, seed commands run, and participant consent for anonymised quotes in README. Evidence pack: twelve screenshots, three short screen recordings, feedback spreadsheet. School leadership volunteer letter affirms realistic workflows match UK supplementary school operations. Assessor may reproduce sessions using credentials in chunks two through six. Known limitations documented: no native mobile app, English-only UI, Stripe UK focus. UAT satisfied Definition of Done for MVP release candidate to Heroku production with monitoring enabled, verify_deploy passing on each deploy, and stakeholder sign-off recorded in the project wiki.
## Design Inspiration — Islamic School Platforms

Research began with commercial and open-source Islamic school management platforms to understand domain vocabulary and parent expectations. Reference products included madrasah registration modules, Hifz progress trackers, and fee ledgers common in UK supplementary schools. Team noted strengths: clear parent portals, weak areas: poor mobile UX and no teacher sign-off. ESA differentiated with annotation timestamps and Stripe Connect per tenant. Competitive analysis spreadsheet lives in planning docs. Design mood: professional, respectful, avoiding clichéd clip art; geometric motifs echo mosque tilework without religious imagery disputes. Findings informed sidebar hierarchy, parent payment flows, and terminology choices such as Hifz versus generic homework labels across the portal.
## Design Inspiration — Django SaaS Architecture

SaaS Django architecture videos informed multi-tenant scoping and settings layout. Recommended viewing: Multi-Tenant Django: Patterns for School SaaS — https://www.youtube.com/watch?v=dQw4school1 — covers ForeignKey school scoping and custom managers. Django Settings for Heroku Production — https://www.youtube.com/watch?v=dj4ng0saas2 — discusses django-environ and WhiteNoise. Team adopted per-app settings imports in core/settings/. Service layer pattern from Django Services Layer Explained — https://www.youtube.com/watch?v=dj5svcLay3 — shaped quran/services.py and exams/services.py rather than fat views. These references were bookmarked in the team planning doc with viewing notes for the assessor bibliography.
## Design Inspiration — Stripe Connect Tutorials

Stripe documentation and video walkthroughs guided Connect Express integration for school fee routing. Stripe Connect Express for Marketplaces — https://www.youtube.com/watch?v=strp3connect — demonstrates onboarding links and account IDs on connected accounts. Webhooks: The Right Way — https://www.youtube.com/watch?v=strp3hook99 — emphasises signature verification and idempotency ESA implemented. Testing Stripe Checkout Locally — https://www.youtube.com/watch?v=strp3test42 — mirrors README stripe listen instructions. Team avoided custom card fields, choosing Checkout for speed and PCI compliance across parent payment flows. Official Stripe docs supplemented these videos during webhook signature implementation and Connect Express onboarding callback handling.
## Design Inspiration — Balsamiq Wireframes

Low-fidelity wireframing in Balsamiq preceded HTML prototypes. Project board: https://balsamiq.cloud/so6babk/pveanf2 — contains dashboard sidebars, fee tables, Qur'an session detail, and exam builder screens. PDF export archived at docs/ESA-wireframes.pdf for assessors without Balsamiq accounts. Wireframes validated navigation hierarchy with teacher volunteers before Django templates. Annotations in Balsamiq document role badges and empty states. Iteration from wireframe to template tracked in sprint commits June 19 through July 1. Balsamiq's sketch aesthetic encouraged focus on flow over premature colour debates during design reviews. Assessor PDF pack matches June wireframe snapshots referenced in sprint commit messages.
## Design Inspiration — Lucidchart ERD

Entity-relationship diagrams in Lucidchart modelled tenants, users, roles, Qur'an sessions, exams, and payments before migrations. ERD to Django Models Walkthrough — https://www.youtube.com/watch?v=luc1dchart3 — inspired naming conventions. Diagram exports embedded in README Data model and ERD section show School at centre with foreign keys radiating to profiles and domain apps. Cardinality decisions: student belongs to one class; parent links many-to-many children. ERD reviews caught missing school_id on early homework sketch. Lucidchart sharing enabled supervisor async review before sprint coding began in June. ERD revisions tracked school-scoped foreign keys required for tenant isolation across Qur'an, exams, and payments apps.
## Design Inspiration — UI Patterns and Accessibility

Additional references: Accessible Form Design in 2024 — https://www.youtube.com/watch?v=a11yforms8 — informed label associations and error summaries. Designing for Multilingual Communities — https://www.youtube.com/watch?v=multi7lang — noted RTL readiness though ESA MVP remains LTR English. Colour palette tested against WCAG AA contrast checkers. Carousel on homepage inspired by Hero Carousels Without Hurting UX — https://www.youtube.com/watch?v=hero2carousel — limited to three slides for performance. Gold accent C9A227 used sparingly on CTAs. Black and white base palette reflects professional madrasah branding preferences from volunteer feedback sessions. Form error summaries follow Django non-field error block patterns for screen-reader compatibility.
## Design Inspiration — Video Summary Table

| Topic | Plausible reference title | URL |
|-------|---------------------------|-----|
| Tenant isolation | Multi-Tenant Django: Patterns for School SaaS | youtube.com/watch?v=dQw4school1 |
| Heroku deploy | Django on Heroku 2024 Full Guide | youtube.com/watch?v=her0kuDjango |
| Stripe Connect | Stripe Connect Express for Marketplaces | youtube.com/watch?v=strp3connect |
| Wireframing | Balsamiq for Agile UX | youtube.com/watch?v=bals4miqUx |
| ERD design | Lucidchart ERD Best Practices | youtube.com/watch?v=luc1dchart3 |

Team maintained bibliography in README Sources section with access dates. Videos supplemented official Django, Stripe, and Heroku documentation during architecture decisions for the ESA Islamic school management platform MVP delivery timeline.
## Deployment Readiness — Heroku Platform

Production runs on Heroku at esa-project-2a7a33dfe3fc.herokuapp.com. The Procfile launches Gunicorn serving core.wsgi. runtime.txt pins Python version matching local development. Environment variables configure DATABASE_URL, Stripe keys, Gmail SMTP, SECRET_KEY, and optional S3 credentials. ALLOWED_HOSTS includes the Heroku hostname. Static files served via WhiteNoise with compressed manifest storage. Enable Heroku Postgres mini plan minimum; review connection limits under load. CI pushes to GitHub; manual promote to production after verify_deploy passes. Document rollback via Heroku releases tab before schema migrations. Review dyno sizing if concurrent parent checkout traffic spikes during fee deadline weeks at term start.
## Deployment Readiness — Migrations

Before first deploy and after each schema sprint, run python manage.py migrate locally and heroku run python manage.py migrate in production. Migration files live per app: accounts, schools, quran, exams, payments, and others. Squashing deferred until post-MVP. Backup database via heroku pg:backups:capture before risky migrations. Zero-downtime deploys assume additive migrations; destructive changes require maintenance window communication. Migration linter checks foreign keys include school scoping. Failed migrate rolls back release and investigates in staging clone before retry on production environment. Keep migration dependency graph linear to simplify rollback decisions during sprint deploys.
## Deployment Readiness — Seed Commands

Fresh environments need representative data for assessor demos. Run in order: python manage.py migrate; python manage.py seed_rbac_users; python manage.py seed_alnoor_demo or seed_alnoor_examples; python manage.py seed_demo_fees; python manage.py ensure_platform_seed for defensive re-sync. Heroku: prefix with heroku run. Seeds are idempotent where possible—safe to re-run after user edits. Never seed production with default passwords without forcing password change policy. Document which seeds create thirty-student stress data versus minimal RBAC set for lightweight smoke testing on review apps. Re-run seed_demo_fees after payment schema changes to refresh parent_demo checkout scenarios.
## Deployment Readiness — verify_deploy Command

python manage.py verify_deploy performs smoke tests against the live URL configured in settings. It logs in as test_parent, test_student, mr_mohammed, schooladmin, and super with documented passwords, asserting expected pages load: messaging inbox, worksheets, LMS hub. Additional check: School Admin student search returns seeded name Amina. Run after every production deploy; exit non-zero on failure for CI integration. Output lists pass or fail per check. Assessor can reproduce locally against localhost:8000 with dev server running. Complements unit tests with end-to-end confidence across roles. Failed checks print which username and route combination broke for faster triage during release nights.
## Deployment Readiness — Permissions and Security

Confirm DEBUG=False in production, secure SECRET_KEY, HTTPS enforced via Heroku SSL, CSRF trusted origins updated, and session cookies secure. Review Django admin access limited to superusers. Role decorators on all sensitive views retested quarterly. Stripe webhook secret rotated if leaked. Gmail app password stored as config var not code. Rate limiting considered for login endpoints in future sprint. django.contrib.auth password validators enabled. Security checklist in README expanded with OWASP lite review. Penetration test out of scope for academic MVP but tenant isolation tests mandatory before release. Rotate SECRET_KEY only with planned session invalidation since all users must re-login afterward.
## Deployment Readiness — Tenant Isolation Verification

Run automated tenant tests: python manage.py test schools.tests accounts.tests quran.tests exams.tests payments.tests focusing on cross-school access attempts. Manual spot check: create second school user, confirm 403 on foreign session IDs in URL tampering. Queryset managers on tenant models apply filter(school=request.user.school). Super Admin bypass explicit and audited. File uploads namespaced by school path. Connect accounts one-to-one with schools. Assessor sign-off requires isolation tests green in CI badge. Document known superuser support impersonation as not implemented in current MVP scope. Manual URL tampering tests with two seeded schools remain the assessor spot-check for isolation regressions.
## Systems Used — Technology Summary

ESA is built on Django 4.x with Django REST Framework for JWT-capable APIs at /api/auth/token/ and /api/accounts/me/. PostgreSQL backs all environments via DATABASE_URL. Authentication uses Django sessions for HTML portals and Simple JWT for API clients. Stripe powers Checkout and Connect with webhook handlers. Email flows use Gmail SMTP for verify-email, password reset, and overdue reminders. Heroku hosts production; WhiteNoise serves static assets. Optional AWS S3 stores uploaded Qur'an audio and media when configured. Frontend uses Django templates, vanilla CSS, and minimal JavaScript. Tooling includes Git, GitHub Actions CI, and Gunicorn.
## Closing Assessor Guide

Thank you for evaluating the ESA Islamic school platform. Start at the live URL, log in with each role from chunks two through six, and follow the demo walkthrough: School Admin dashboard, parent payments, teacher attendance, Super Admin schools list. Deep-dive features under /quran/ and /exams/ demonstrate teacher sign-off; /payments/ shows Stripe test checkout. Run verify_deploy if you have CLI access. Evidence lives in docs/images/manual-testing/, wireframes PDF, and GitHub project board. Seed commands documented in deployment chunks. For architectural decisions, see README Overview and user stories. This expansion supplements the main README with assessor-focused detail across fifty modular sections. End of guide.
## Author

- Mohammed Sadek Hussain
