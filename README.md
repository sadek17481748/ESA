# Islamic School Applications (ISA)

Islamic School Applications (ISA) is a full-stack SaaS platform for Islamic schools to manage admissions, learning, attendance, progress, messaging, and payments in one place.

## Table of Contents

- [Overview](#overview)
  - [Project goals](#project-goals)
  - [Planning notes (written at project start)](#planning-notes-written-at-project-start)
- [Quick links (assessor)](#quick-links-assessor)
- [Features](#features)
- [User Experience (UX)](#user-experience-ux)
  - [User stories](#user-stories)
- [Wireframes](#wireframes)
- [Design](#design)
  - [Visual language](#visual-language)
  - [Colour palette](#colour-palette)
  - [Typography](#typography)
  - [Accessibility](#accessibility)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [Data model](#data-model)
  - [Tenant model](#tenant-model)
  - [Core entities (planned)](#core-entities-planned)
- [Development](#development)
  - [Local setup](#local-setup)
  - [Environment variables](#environment-variables)
  - [Run locally](#run-locally)
- [API overview](#api-overview)
- [Payments (Stripe Connect)](#payments-stripe-connect)
- [Testing and Bugs](#testing-and-bugs)
  - [Manual testing](#manual-testing)
  - [Automated testing](#automated-testing)
- [Deployment](#deployment)
- [Security](#security)
- [Sources and references](#sources-and-references)
- [Author](#author)

---

## Overview

ISA is designed for multiple schools (tenants) with strict data isolation, role-based access control, and a modern dashboard interface.

Planned core roles:

- **Super Admin**: manage schools, platform-wide settings, subscriptions, and analytics.
- **School Admin**: manage staff/students/parents, set fees, and connect Stripe for payouts.
- **Teacher**: manage classes/subjects, attendance, homework, exams, and progress sign-offs.
- **Student**: view timetable/work and submit recordings and assignments.
- **Parent**: monitor progress and payments, and make payments.

### Project goals

- Build a real-world Django MVC application with a relational PostgreSQL database and reusable Django apps.
- Implement tenant data isolation per school and consistent role permissions.
- Implement end-to-end CRUD flows where database changes are reflected immediately in the UI.
- Implement Stripe Connect so payments are paid out directly to schools with an optional platform commission.
- Maintain a detailed commit history showing development progress in small, reviewable steps.

### Planning notes (written at project start)

This section captures the early plan in plain language to keep scope clear while building step-by-step.

#### Architecture notes (initial)

- Multi-tenant: each record belongs to a `School` tenant; all queries are scoped to the authenticated user’s tenant.
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

- **June 19 – June 23 (Qur’an annotation system)**
  - Qur’an text display and per-student session annotation model.
  - Mistake tagging (Tajweed / Memorisation / Fluency), timestamps, comments.
  - Audio upload and playback for recitations + teacher audio feedback.

- **June 24 – June 28 (Exams + sign-off finalisation)**
  - Exam creation (MCQ auto-mark + written/manual).
  - Results with “finalised” teacher sign-off requirement before being official.
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

## Quick links (assessor)

- **Repository**: (to be added)
- **Live app**: (to be added)
- **Test credentials**: (to be added)
- **Wireframes**: (to be added)

## Features

This section will be expanded as features are implemented and tested.

- **Multi-tenant schools**
- **RBAC (roles + permissions)**
- **Custom subjects per school**
- **Timetable system**
- **Attendance tracking**
- **Hifz tracking**
- **Qur’an annotation**
- **Teacher sign-off verification** (Hifz, worksheets, exams)
- **Payments with Stripe Connect**
- **Notifications (email + in-app)**
- **Messaging (real-time)**
- **Analytics dashboards**

## User Experience (UX)

### User stories

This section will be written and updated alongside development.

- As a School Admin, I want to manage teachers, students, and parents so I can run the school from one system.
- As a Teacher, I want to record attendance and assign homework so student progress is tracked.
- As a Teacher, I want to verify progress with sign-off so reports reflect authentic completion.
- As a Parent, I want to view verified progress and pay outstanding fees so I can support my child’s learning.
- As a Student, I want to view my timetable and submit recordings so my teacher can review my work.

## Wireframes

- Wireframes will be added under `docs/` and linked here.

## Design

### Visual language

- Modern, minimal dashboard UI with clear spacing and consistent components.
- Subtle Islamic geometric inspiration (mosaic/rug motifs) used sparingly in headers, dividers, and accent elements.

### Colour palette

The base palette is intentionally simple and high contrast:

- **Black / off-black** for the primary background and navigation.
- **White / off-white** for content panels and primary text contrast.
- **Gold accents** used sparingly for highlights, active states, and key actions.

Palette values and components will be documented once the frontend theme is implemented.

### Typography

- Fonts will be chosen to support English + Arabic readability (to be finalised).

### Accessibility

- Keyboard navigable UI, readable contrast, clear focus states, and semantic HTML.
- Accessible form labels and validation feedback.

## Technologies Used

### Backend

- Django (Python)
- Django REST Framework

### Database

- PostgreSQL

### Payments

- Stripe Connect

### Frontend

- Django templates with HTML/CSS/JavaScript (initial approach)

## File Structure

The Django project will be organised into apps for each reusable component:

- `accounts`
- `schools`
- `students`
- `teachers`
- `subjects`
- `timetable`
- `payments`
- `hifz`
- `alimiyah`
- `exams`
- `analytics`
- `messaging`
- `notifications`

This section will be filled out with actual paths as the project is generated.

## Data model

### Tenant model

- `School` is the tenant root.
- Tenant isolation rules will be documented and tested (query scoping, permissions, and admin boundaries).

### Core entities (planned)

- User (custom)
- School
- Teacher
- Student
- Parent
- Subject
- Class / YearGroup
- Timetable
- Attendance
- BehaviourLog
- Worksheet / WorksheetSubmission
- Exam / ExamResult
- Qur’anAnnotation
- PendingPayment / CompletedPayment
- AuditLog

## Development

### Local setup

This section will be filled out step-by-step once the Django project is created.

### Environment variables

To be added:

- `DJANGO_SECRET_KEY`
- `DEBUG`
- `DATABASE_URL` (PostgreSQL)
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`

### Run locally

To be added.

## API overview

To be added (DRF endpoints + authentication approach).

## Payments (Stripe Connect)

To be added (onboarding schools, payout flow, platform commission, webhooks).

## Testing and Bugs

### Manual testing

To be added as features ship (screens, flows, and evidence).

### Automated testing

To be added (pytest + Django test suite; TDD commits where appropriate).

## Deployment

To be added (platform choice, environment variables, Postgres provisioning, Stripe webhook configuration).

## Security

To be expanded as implementation progresses:

- Environment variables for secrets
- Tenant data isolation tests
- Permission checks for sensitive actions (especially teacher sign-offs and payments)
- Audit logs for critical actions

## Sources and references

To be added as implementation progresses (docs, tutorials, UI references).

## Author

- Mohammed Sadek Hussain
