# ESA — Education and Schooling Applications

**ESA (Education and Schooling Applications)** is a full-stack multi-tenant SaaS platform for Islamic schools. It helps staff manage admissions, learning, attendance, academic progress, teacher-verified sign-offs, messaging, and payments (including Stripe Connect payouts to schools) in one place.

> **Current tree:** Static HTML/CSS wireframes live at the repository root (`*.html`, `css/base.css`). Preview with `python3 -m http.server 8080` then open http://127.0.0.1:8080/ . The Django and API sections below describe the planned implementation and are unchanged from the module specification.

## Table of Contents

- [Overview](#overview)
  - [Project goals](#project-goals)
  - [Planning notes (written at project start)](#planning-notes-written-at-project-start)
- [Quick links](#quick-links)
- [Key UI screenshots](#key-ui-screenshots)
- [Features](#features)
- [User Experience (UX)](#user-experience-ux)
  - [Responsive behaviour](#responsive-behaviour)
  - [How responsiveness was tested](#how-responsiveness-was-tested)
  - [User stories](#user-stories)
- [Wireframes](#wireframes)
  - [Wireframe inventory](#wireframe-inventory)
- [Design](#design)
  - [Data model and ERD (entity relationships)](#data-model-and-erd-entity-relationships)
  - [Visual language](#visual-language)
  - [Colour palette](#colour-palette)
  - [Typography](#typography)
  - [Accessibility](#accessibility)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [Development](#development)
  - [Local setup](#local-setup)
  - [Environment variables](#environment-variables)
  - [Run locally](#run-locally)
- [Deployment](#deployment)
- [Testing and Bugs](#testing-and-bugs)
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
- [Author](#author)

---

## Quick links

Assessor-facing links and evidence paths:

| Resource | Link or path |
|----------|--------------|
| **Source repository** | https://github.com/sadek17481748/ESA |
| **Live deployment** | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| **Bug tracker (GitHub Project board)** | https://github.com/users/sadek17481748/projects/8/views/1 |
| **Wireframes (README anchor)** | [Wireframes](#wireframes) |
| **ERD / data model** | [Data model and ERD](#data-model-and-erd-entity-relationships) |
| **Test credentials** | https://esa-project-2a7a33dfe3fc.herokuapp.com/ |
| **Manual test evidence (screenshots)** | `docs/images/manual-testing/` |
| **Validation evidence** | `docs/images/validation/` |
| **Sprint checklist** | Follow the delivery timeline under [Planning notes](#planning-notes-written-at-project-start) |

---

## Overview

ESA is designed for multiple schools (tenants) with strict data isolation, role-based access control, JWT-ready APIs (Django REST Framework), and a mobile-responsive dashboard. **Teacher sign-off** is a core trust layer: Hifz progress, homework/worksheets, and exam results only become official after an authenticated teacher verifies them (with re-authentication on sign-off and audit logging planned alongside implementation).

Planned core roles:

- **Super Admin**: manage schools, platform-wide settings, subscriptions, and analytics.
- **School Admin**: manage staff/students/parents, set fees, and connect Stripe for payouts.
- **Teacher**: manage classes/subjects, attendance, homework, exams, and progress sign-offs.
- **Student**: view timetable/work and submit recordings and assignments.
- **Parent**: monitor progress and payments, and make payments.

### Project goals

1. **Full-stack Django application** — Build a production-quality Django project following the Model-View-Template (MVT) pattern, backed by a relational PostgreSQL database. Each major feature area (accounts, schools, hifz, payments, etc.) lives in its own reusable Django app so the codebase stays modular and testable.

2. **Multi-tenant architecture** — Every school operates as an isolated tenant. All database queries are scoped to the authenticated user's school so that no data ever leaks between institutions. Tenant isolation is enforced at the model-manager level and verified with automated tests.

3. **Role-based access control (RBAC)** — Five distinct roles (Super Admin, School Admin, Teacher, Student, Parent) each have explicit permissions. Views, API endpoints, and templates all check the user's role before granting access, ensuring that a student can never reach a teacher-only page and a School Admin from one school can never see another school's data.

4. **End-to-end CRUD with immediate UI feedback** — Users can create, read, update, and delete records (students, assignments, attendance marks, fee items, etc.) and see changes reflected in the interface immediately. Form validation is handled server-side with clear inline error messages, and success feedback is shown after every action.

5. **Teacher sign-off as a trust layer** — Hifz completion, homework approval, and exam finalisation all require an authenticated teacher to explicitly sign off. Sign-off actions demand password re-entry, generate an AuditLog record, and are the only pathway for progress data to appear on student and parent reports. This prevents self-reporting and ensures data integrity.

6. **Stripe Connect payment routing** — School Admins connect their institution's Stripe account via OAuth. Parent fee payments are processed through Stripe Checkout and routed directly to the school's connected account, with an optional platform commission. Webhooks confirm payment status and trigger receipt generation.

7. **Responsive, accessible UI** — All pages are designed mobile-first using a black, white, and gold colour palette with subtle Arabic geometric motifs. The interface targets WCAG AA contrast ratios, full keyboard navigation, and semantic HTML so it is usable on phones, tablets, and desktops by all users.

8. **Incremental, well-documented development** — The project follows a detailed weekly delivery timeline. Each feature is committed in small, reviewable steps with conventional commit messages. The README, inline documentation, and test suite grow alongside the code so the full development journey is visible to assessors.

### Planning notes (written at project start)

This section captures the early plan in plain language to keep scope clear while building step-by-step.

#### Architecture notes (initial)

- Multi-tenant: each record belongs to a `School` tenant; all queries are scoped to the authenticated user's tenant.
- Auth: JWT-based authentication for API and role-based permissions for views/actions.
- RBAC: explicit roles and permission checks (Super Admin vs School Admin vs Teacher vs Student vs Parent).

#### Delivery timeline (May 10 → July 1)

The goal is to have the application in a stable, deployable state by **July 1**, leaving **July 1 → July 7** as buffer for final polish, assessor checks, and contingency.

- **May 10 – May 14 (Foundation)**
  - Create Django project + settings (env-based config, Postgres, static/media structure).
  - Add core apps scaffolding (`accounts`, `schools`, etc.) and baseline URL structure.
  - Create custom user model and authentication foundations (JWT).
  - Establish tenant model (`School`) and a consistent way to scope data to a school.

- **May 15 – May 21 (RBAC + tenant isolation)**
  - Define roles and permission strategy (Super Admin / School Admin / Teacher / Student / Parent).
  - Implement permission checks and tenant query scoping in DRF and template views.
  - Add audit logging foundations for sensitive actions.

- **May 22 – May 28 (School setup flows)**
  - School Admin can create/manage teachers, students, parents (CRUD).
  - Year groups / classes models and assignment flows.
  - Bulk student import (CSV) initial version.

- **May 29 – June 4 (Subjects + timetable)**
  - Custom subjects per school (Hifz / Alimiyah / General) + teacher assignment.
  - Timetable creation and student/teacher views.
  - Attendance tracking basics linked to timetable/class.

- **June 5 – June 11 (Homework + worksheets + sign-off)**
  - Homework/worksheet assignment and submission flows.
  - Teacher sign-off verification: approve/reject submissions with secure server-side rules.
  - Notifications for assignments and sign-off outcomes (in-app first).

- **June 12 – June 18 (Hifz tracking + sign-off)**
  - Hifz records (status: Not Started / In Progress / Completed only via sign-off).
  - Smart revision suggestions (basic rules first, improve iteratively).
  - Teacher sign-off flow with re-auth requirement (password re-entry).

- **June 19 – June 23 (Qur'an annotation system)**
  - Qur'an text display and per-student session annotation model.
  - Mistake tagging (Tajweed / Memorisation / Fluency), timestamps, comments.
  - Audio upload and playback for recitations + teacher audio feedback.

- **June 24 – June 28 (Exams + sign-off finalisation)**
  - Exam creation (MCQ auto-mark + written/manual).
  - Results with "finalised" teacher sign-off requirement before being official.
  - Parent/student reporting views show only verified/finalised outcomes where required.

- **June 29 – July 1 (Payments + deployment-ready pass)**
  - Fees: pending vs completed payments, parent payment journey.
  - Stripe Connect onboarding for schools + payment routing to school accounts (platform fee optional).
  - Webhooks + receipts (PDF basic) + overdue reminders (email + in-app).
  - Stabilisation: permissions review, tenant isolation review, and deployment checklist.

**July 1 – July 7 (Buffer)**

- Full regression testing and bug fixes.
- Evidence collection (screenshots, test runs, validation, deployment notes).
- README expansion (data schema, deployment steps, testing evidence, assessor quick links).

#### Build order (high level)

- Project setup (Django + DRF) and configuration for Postgres + environment variables.
- Custom user model and authentication foundations.
- Tenant model (`School`) + isolation rules.
- Core learning flows: subjects, timetables, attendance.
- Progress systems: Hifz tracking + verification sign-off, worksheets, exams.
- Payments: fees, pending/completed payments, Stripe Connect payout flow.
- Notifications + messaging.
- Analytics dashboards.

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

- **Multi-tenant schools** — each school is a fully isolated tenant.
- **RBAC (roles + permissions)** — five roles with explicit permission checks.
- **Custom subjects per school** — Hifz, Alimiyah, General categories.
- **Timetable system** — weekly grid with conflict detection.
- **Attendance tracking** — per-session register with absence flagging.
- **Hifz tracking** — surah/juz progress with teacher sign-off.
- **Qur'an annotation** — recitation tagging (Tajweed / Memorisation / Fluency) with audio.
- **Teacher sign-off verification** — Hifz, worksheets, and exams require authenticated sign-off.
- **Payments with Stripe Connect** — fees routed directly to school bank accounts.
- **Notifications (email + in-app)** — assignment alerts, absence alerts, overdue fees.
- **Messaging** — teacher–parent direct messaging.
- **Analytics dashboards** — attendance rates, Hifz progress, fee collection.

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

The wireframes are built as static HTML/CSS pages that live at the repository root. Each page represents a key screen of the application and uses the shared stylesheet (`css/base.css`) to maintain visual consistency. They serve as the design blueprint — showing layout, navigation, and content hierarchy — before full Django template integration.

To preview the wireframes locally:

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

---

## Design

### Data model and ERD (entity relationships)

The ERD describes the planned relational structure for the ESA database. The diagram will be produced using dbdiagram.io or Lucidchart and added to `docs/erd.png`.

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

The full ERD diagram image will be added to `docs/erd.png` and linked here once generated.

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

- **Stripe Connect** (planned)

### Tools

| Tool | Used for |
|------|----------|
| **Git** | Version control |
| **GitHub** | Repository hosting, Issues, Projects |
| **PostgreSQL / psql** | Database, ad-hoc SQL checks |
| **VS Code / Cursor** | Editing and integrated terminal |
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
| `*.html` | Static wireframe pages (18 files — see [Wireframe inventory](#wireframe-inventory)) |
| `templates/` | Django templates (to be populated as apps are built) |
| `static/` | Django static assets (to be populated) |
| `docs/` | Documentation, ERD, screenshots, validation evidence (to be populated) |

---

## Development

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
| `STRIPE_SECRET_KEY` | (payments phase) |
| `STRIPE_WEBHOOK_SECRET` | (payments phase) |

### Run locally

```bash
python manage.py runserver
```

- Admin: http://127.0.0.1:8000/admin/
- JWT obtain pair: `POST /api/auth/token/` with `username` and `password`.
- JWT refresh: `POST /api/auth/token/refresh/` with `refresh` token.

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

Parent school fees use Stripe Checkout in test mode (same API keys as my `stripe_demo` project).

1. Copy Stripe keys into `.env` (`STRIPE_PUBLISHABLE_KEY`, `STRIPE_SECRET_KEY`).
2. Run migrations and seed demo data:

   ```bash
   source .venv/bin/activate
   python manage.py migrate
   python manage.py seed_demo_fees
   ```

3. Start the server and log in as `parent_demo` / `demo1234`, then open `/payments/`.
4. Click **Pay now** on a fee — use Stripe test card `4242 4242 4242 4242`, any future expiry, any CVC.
5. Optional webhook forwarding: `stripe listen --forward-to localhost:8000/payments/webhook/`

---

## Deployment

Deployment will use Heroku (or Render) with a managed PostgreSQL database.

### Deployment steps (planned)

1. Install Heroku CLI and login:

   ```bash
   brew tap heroku/brew && brew install heroku
   heroku login
   ```

2. Create the app and add PostgreSQL:

   ```bash
   heroku create esa-app
   heroku addons:create heroku-postgresql:essential-0 -a esa-app
   ```

3. Set config vars:

   ```bash
   heroku config:set SECRET_KEY="a-long-random-string" -a esa-app
   heroku config:set DEBUG=False -a esa-app
   heroku config:set ALLOWED_HOSTS="esa-app.herokuapp.com" -a esa-app
   ```

4. Deploy and initialise:

   ```bash
   git push heroku main
   heroku run python manage.py migrate -a esa-app
   heroku run python manage.py createsuperuser -a esa-app
   heroku open -a esa-app
   ```

**Production notes:**
- `Procfile` runs the app with **Gunicorn**.
- Heroku provides `DATABASE_URL` automatically.
- WhiteNoise serves static files in production.
- Use `heroku logs --tail` to diagnose startup issues.

**Live site URL:** (to be added after deployment)

---

## Testing and Bugs

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
After login, users go to `/dashboard/` by role. Feature pages are UI placeholders while
API endpoints are wired separately.

| Route | Purpose |
|-------|---------|
| `/register/` | Parent or student sign-up |
| `/dashboard/parent/` | Parent portal |
| `/dashboard/teacher/` | Teacher workspace |
| `/dashboard/student/` | Student portal |
| `/attendance/` | Attendance screen (placeholder) |
| `/timetable/` | Timetable screen (placeholder) |
| `/worksheets/` | Homework screen (placeholder) |

Planned and executed checks for foundation, RBAC, and Stripe work. Fill **Actual**, **Pass/Fail**, and **Screenshot** as evidence is captured (`docs/images/manual-testing/`).

| # | Test | Steps | Expected | Actual | Pass/Fail | Screenshot |
|---|------|-------|----------|--------|-----------|------------|
| 1 | JWT login with valid credentials | `POST /api/auth/token/` with `teacher_demo` / `teacher1234` | `200` and access + refresh tokens returned | | | |
| 2 | JWT login with invalid password | `POST /api/auth/token/` with wrong password | `401` Unauthorized | | | |
| 3 | Current user profile (`/api/accounts/me/`) | Obtain JWT, `GET /api/accounts/me/` with Bearer token | JSON shows correct `role`, `school`, `school_name` | | | |
| 4 | School admin tenant scope (schools API) | Log in as `schooladmin`, `GET /api/schools/` | Exactly one school (own tenant) | | | |
| 5 | Super admin sees all schools | Log in as `super`, `GET /api/schools/` | All schools in database listed | | | |
| 6 | Teacher student list tenant scope | Log in as `teacher_demo`, `GET /api/students/` | Only students from Al-Noor Academy | | | |
| 7 | Parent blocked from staff student API | Log in as `parent_demo`, `GET /api/students/` | `403 Forbidden` | | | |
| 8 | Register without school rejected | `POST /api/accounts/register/` as student with no `school` | `400` with school validation error | | | |
| 9 | RBAC seed command | Run `python manage.py seed_rbac_users` | Five demo users exist with correct roles | | | |
| 10 | Tenant middleware on request | Log in via session; check `request.tenant_school` | Matches user's school | | | |
| 11 | Audit log on login | Log in as `teacher_demo` via `/accounts/login/` | New `AuditLog` row with action login and school set | | | |
| 12 | Parent fee list (own fees only) | Log in as `parent_demo`, open `/payments/` | Only this parent's outstanding and paid fees | | | |
| 13 | Unauthenticated payments redirect | Open `/payments/` logged out | Redirect to `/accounts/login/` | | | |
| 14 | Stripe Checkout redirect | On `/payments/`, click **Pay now** on a fee | Redirect to Stripe hosted checkout | | | |
| 15 | Stripe test card payment | Complete checkout with `4242 4242 4242 4242` | Success page with receipt; fee marked paid | | | |
| 16 | Stripe cancel flow | Start checkout, cancel on Stripe page | `/payments/cancel/` with no charge | | | |
| 17 | No duplicate payment on refresh | Refresh `/payments/success/?session_id=…` after pay | Single `Payment` row in admin | | | |
| 18 | Checkout amount displays correctly | Pay Term 3 tuition (£250.00) | Stripe shows £250.00 not £2.50 | | | |
| 19 | Teacher list tenant scope | Log in as `teacher_demo`, `GET /api/teachers/` | Only teachers from same school | | | |
| 20 | Class groups API tenant scope | Log in as `schooladmin`, `GET /api/classes/` | Only classes for own school | | | |
| 21 | School admin registers parent | JWT as `schooladmin`, `POST /api/parents/register/` | Parent user + profile created with school set | | | |
| 22 | School admin registers teacher | `POST /api/teachers/register/` with username/email/password | Teacher profile linked to admin's school | | | |
| 23 | Year groups CRUD | `GET/POST /api/classes/year-groups/` as school admin | List/create year groups for own school | | | |
| 24 | Enrol student in class | `POST /api/classes/enrollments/` with class + student ids | Enrollment row; rejects cross-school student | | | |
| 25 | Bulk student CSV import | `POST /api/students/import_csv/` with CSV file | `created` count and per-row errors returned | | | |
| 26 | Custom Hifz subject | `POST /api/subjects/` with track `hifz` + lead_teacher | Subject saved; missing lead_teacher returns 400 | | | |
| 27 | Timetable slot validation | `POST /api/timetable/` with end_time before start_time | 400 validation error | | | |
| 28 | Teacher timetable view | Log in as `teacher_demo`, `GET /api/timetable/?class_group=1` | Slots for requested class only | | | |
| 29 | Take class attendance | `POST /api/attendance/sessions/` with marks array | Session + marks saved; rejects non-enrolled student | | | |
| 30 | Teacher creates assignment | `POST /api/homework/assignments/` as `teacher_demo` | Assignment saved; enrolled students get notification | | | |
| 31 | Student submits homework | `POST /api/homework/submissions/{id}/submit/` as `student_demo` | Status `submitted` and timestamp set | | | |
| 32 | Teacher sign-off approve | `POST /api/homework/submissions/{id}/sign_off/` as assigning teacher | Status `approved`; student notification created | | | |
| 33 | Wrong teacher sign-off blocked | Same endpoint as another teacher | 403 or 404 (not assigned teacher) | | | |
| 34 | In-app notifications list | `GET /api/notifications/` as `student_demo` | User's own notifications, newest first | | | |
| 36 | Web registration | Open `/register/`, submit as parent with school | Account created and logged in | | | |
| 37 | Login redirect by role | Log in as `teacher_demo` | Lands on teacher dashboard | | | |
| 38 | Portal attendance page | Log in, open `/attendance/` | Placeholder page loads | | | |
| 39 | Portal timetable page | Log in, open `/timetable/` | Placeholder page loads | | | |
| 40 | Portal worksheets page | Log in, open `/worksheets/` | Placeholder page loads | | | |
| 41 | Portal messages page | Log in, open `/messages/` | Placeholder inbox loads | | | |
| 42 | Portal exams page | Log in, open `/exams/` | Placeholder page loads | | | |
| 43 | Register validation | Submit register with mismatched passwords | Inline error shown | | | |
| 44 | Home auth nav | Log in, open `/` | Dashboard and log out links shown | | | |
| 35 | Mark notification read | `POST /api/notifications/{id}/mark_read/` | `is_read` true on that row | | | |

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
| Exam create / finalise | — | — | Not started |
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

To be expanded as implementation progresses:

- Environment variables for secrets (`.env` excluded from Git)
- Hashed passwords (Django's built-in PBKDF2)
- Tenant data isolation tests (query scoping, permissions, admin boundaries)
- Permission checks for sensitive actions (especially teacher sign-offs and payments)
- CSRF protection on all forms
- JWT token expiry and rotation
- Audit logs for critical actions (sign-offs, payments, role changes)

---

## Sources and references

To be added as implementation progresses (docs, tutorials, UI references).

### ERD and schema design references

https://esa-project-2a7a33dfe3fc.herokuapp.com/

### Feature resources

https://esa-project-2a7a33dfe3fc.herokuapp.com/

### Django and DRF

https://esa-project-2a7a33dfe3fc.herokuapp.com/

### PostgreSQL

https://esa-project-2a7a33dfe3fc.herokuapp.com/

### Images used in this project

https://esa-project-2a7a33dfe3fc.herokuapp.com/

---

## Author

- Mohammed Sadek Hussain
