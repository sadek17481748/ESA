# ESA — Education and Schooling Applications

**ESA (Education and Schooling Applications)** is a full-stack multi-tenant SaaS platform for Islamic schools. It helps staff manage admissions, learning, attendance, academic progress, teacher-verified sign-offs, messaging, and payments (including Stripe Connect payouts to schools) in one place.

> **Current tree:** Static HTML/CSS wireframes live at the repository root (`*.html`, `css/base.css`). Preview with `python3 -m http.server 8080` then open http://127.0.0.1:8080/ . The Django and API sections below describe the planned implementation and are unchanged from the module specification.

## Table of Contents

- [Overview](#overview)
  - [Project goals](#project-goals)
  - [Planning notes (written at project start)](#planning-notes-written-at-project-start)
- [Quick links (assessor)](#quick-links-assessor)
- [Features](#features)
- [User Experience (UX)](#user-experience-ux)
  - [User stories](#user-stories)
- [Wireframes](#wireframes)
  - [Wireframe inventory](#wireframe-inventory)
- [Design](#design)
  - [Visual language](#visual-language)
  - [Colour palette](#colour-palette)
  - [Typography](#typography)
  - [Accessibility](#accessibility)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [Data model](#data-model)
  - [Entity-Relationship Diagram (ERD)](#entity-relationship-diagram-erd)
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
  - [Bugs](#bugs)
  - [Automated testing](#automated-testing)
- [Deployment](#deployment)
- [Security](#security)
- [Sources and references](#sources-and-references)
- [Author](#author)

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

## Quick links (assessor)

- **Repository**: https://github.com/sadek17481748/ESA
- **Live app**: (to be added)
- **Test credentials**: (to be added)
- **Wireframes**: (to be added)
- **Sprint checklist**: Follow the delivery timeline under [Planning notes](#planning-notes-written-at-project-start) (begin with **May 10–14 Foundation**). Optional: track weekly bullets as GitHub Issues on the repository above.

## Features

This section will be expanded as features are implemented and tested.

- **Multi-tenant schools**
- **RBAC (roles + permissions)**
- **Custom subjects per school**
- **Timetable system**
- **Attendance tracking**
- **Hifz tracking**
- **Qur'an annotation**
- **Teacher sign-off verification** (Hifz, worksheets, exams)
- **Payments with Stripe Connect**
- **Notifications (email + in-app)**
- **Messaging (real-time)**
- **Analytics dashboards**

## User Experience (UX)

### User stories

User stories are grouped by role. Each story follows the standard format: *"As a [role], I want to [action] so that [benefit]."* Acceptance criteria are listed beneath each story to clarify when the story is considered done.

---

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

Acceptance criteria:
- Teacher dashboard shows a weekly grid with their assigned lessons.
- Each cell shows the subject, class name, and room (if set).
- Tapping a cell links to the class detail page for that session.

**US-20 — Take a class register**
As a Teacher, I want to take a class register at the start of each lesson by marking each student as present, late, or absent so that attendance is recorded in real time.

Acceptance criteria:
- On the class page for the current session, all enrolled students are listed.
- Teacher can mark each student as Present, Late, or Absent with one tap.
- A "Save register" action persists the attendance records with the current date and session.
- The register can be edited until the end of the school day; after that it is locked.

**US-21 — Create and assign homework or worksheets**
As a Teacher, I want to create homework or worksheet assignments with a title, description, optional file attachment, and due date, and assign them to a class so that students know what to complete and by when.

Acceptance criteria:
- Teacher fills in a form with title, description, optional file upload, and due date.
- Teacher selects the target class (or multiple classes).
- On save, all students in the selected class(es) see the assignment on their dashboard.
- Students and parents receive an in-app notification about the new assignment.

**US-22 — Review and approve or reject student submissions**
As a Teacher, I want to review each student's homework or worksheet submission, leave feedback, and mark it as approved or rejected so that the student receives clear, recorded feedback.

Acceptance criteria:
- A submissions list shows all students in the class with their submission status (Not submitted, Submitted, Approved, Rejected).
- Teacher can open a submission to view the uploaded file or text response.
- Teacher can leave a text comment and set the status to Approved or Rejected.
- The status change is recorded with the teacher's user ID and a timestamp.
- The student and parent receive a notification when feedback is given.

**US-23 — Sign off Hifz progress**
As a Teacher, I want to sign off a student's Hifz progress for a specific surah or juz, moving its status from In Progress to Completed, so that completion is verified and trustworthy.

Acceptance criteria:
- On the student's Hifz record page, the teacher sees each surah/juz with its current status (Not Started, In Progress, Completed).
- Teacher can select a surah/juz that is In Progress and initiate a sign-off.
- The system prompts the teacher to re-enter their password before the sign-off is confirmed.
- On confirmation the status moves to Completed, and the record stores the teacher's ID, timestamp, and optional notes.
- An AuditLog entry of type SIGN_OFF is created.
- The student and parent see the updated status on their dashboards.

**US-24 — Re-authenticate before signing off**
As a Teacher, I want to be required to re-enter my password when performing any sign-off action so that the action is securely authenticated and cannot be performed by someone who found an unlocked device.

Acceptance criteria:
- Any sign-off action (Hifz, homework, exam) presents a password re-entry prompt before processing.
- If the password is incorrect the sign-off is rejected and an error message is shown.
- The re-authentication window is valid for that single action only; the next sign-off requires re-entry again.

**US-25 — Annotate a Qur'an recitation session**
As a Teacher, I want to annotate a student's Qur'an recitation session by tagging specific mistakes with categories (Tajweed, Memorisation, Fluency), adding timestamps and written comments, so that the student can see exactly where they need to improve.

Acceptance criteria:
- Teacher opens a student's recitation session page.
- Teacher can add one or more annotation entries, each with: mistake category (Tajweed / Memorisation / Fluency), a timestamp or ayah reference, and a text comment.
- Saved annotations appear in a list on the session page, visible to the student and parent.
- Annotations can be edited or deleted by the authoring teacher until the session is marked as reviewed.

**US-26 — Upload audio feedback on a recitation**
As a Teacher, I want to record or upload an audio clip as feedback on a student's recitation so that the student can listen to the correct pronunciation or pacing and self-correct.

Acceptance criteria:
- On the recitation session page, a file upload or record button allows the teacher to attach an audio file (MP3, WAV, or M4A, max 10 MB).
- The uploaded audio appears as a playable player on the session page.
- The student and parent can play the audio from their view of the session.

**US-27 — Create exams and enter results**
As a Teacher, I want to create exams with a title, date, subject, and question format (MCQ or written), and enter or auto-mark results for each student, so that assessment is handled in one place.

Acceptance criteria:
- Teacher creates an exam with title, date, subject, and type (MCQ / Written / Mixed).
- For MCQ exams, teacher enters questions with options and correct answers; the system auto-marks student responses.
- For written exams, teacher manually enters a score and optional comments per student.
- Results are saved as draft until the teacher finalises them.

**US-28 — Finalise exam results with sign-off**
As a Teacher, I want to finalise exam results with a sign-off so that only verified scores appear on student and parent reports, and draft scores remain internal.

Acceptance criteria:
- A "Finalise results" button is available on the exam results page when results are in draft status.
- Clicking it triggers a password re-entry prompt (same as US-24).
- On confirmation, all results for that exam move from draft to finalised.
- Finalised results become visible to students and parents.
- An AuditLog entry of type SIGN_OFF is created for the exam.
- Finalised results cannot be edited without creating a new correction record.

**US-29 — Log a behaviour incident**
As a Teacher, I want to log a behaviour incident against a student with a date, category (positive or negative), severity, and description so that there is a dated record that School Admin and parents can review.

Acceptance criteria:
- Teacher fills in a form with student name (searchable dropdown), date, category (Positive / Negative), severity (Low / Medium / High), and description.
- The incident is saved and immediately visible on the school-wide behaviour log.
- The parent of the student receives a notification about the logged incident.

**US-30 — Message parents**
As a Teacher, I want to send a message to an individual parent or to all parents of a class so that I can communicate about progress, concerns, or upcoming events.

Acceptance criteria:
- Teacher can compose a message and select a recipient: a specific parent, or "All parents of [class name]".
- The message appears in the recipient's messaging inbox.
- Recipients receive an in-app notification (and optionally an email notification).
- Sent messages are stored in the teacher's sent-items view.

**US-31 — View a teacher dashboard with class metrics**
As a Teacher, I want to see a dashboard summarising my classes' attendance rates, homework submission rates, and Hifz progress so that I can prioritise support where it is most needed.

Acceptance criteria:
- Teacher dashboard shows a card per assigned class with: attendance % this week, homework on-time %, and Hifz completion % (where applicable).
- Clicking a card navigates to the full class detail page.
- Metrics update each time the dashboard is loaded.

---

#### Student stories

**US-32 — View my personalised dashboard**
As a Student, I want to log in and see a personalised dashboard showing my timetable for today, upcoming homework deadlines, and recent progress updates so that I can quickly understand what needs my attention.

Acceptance criteria:
- Dashboard shows today's timetable slots at the top.
- An "Upcoming homework" section lists assignments due in the next 7 days, sorted by due date.
- A "Recent updates" section shows the last 5 notifications (e.g. new assignment, feedback received, Hifz status change).

**US-33 — View my weekly timetable**
As a Student, I want to view my full weekly timetable showing subjects, teachers, and times so that I can plan my week.

Acceptance criteria:
- A weekly grid shows Monday–Friday with time slots.
- Each filled slot shows the subject name and teacher name.
- The current day is highlighted.

**US-34 — View assigned homework and worksheets**
As a Student, I want to see a list of all homework and worksheet assignments with their titles, descriptions, due dates, and submission status so that I can plan my work.

Acceptance criteria:
- An assignments page lists all current and past assignments.
- Each row shows title, subject, due date, and status (Not submitted / Submitted / Approved / Rejected).
- Overdue assignments that have not been submitted are flagged.
- Clicking an assignment shows the full description and any teacher feedback.

**US-35 — Submit homework or upload a file**
As a Student, I want to submit my completed homework by entering text or uploading a file so that my teacher can review and provide feedback.

Acceptance criteria:
- On the assignment detail page, a "Submit" section allows text entry or file upload (PDF, DOCX, image, max 20 MB).
- The student can resubmit until the teacher has approved or rejected the submission.
- After submission the status changes to Submitted and the teacher is notified.

**US-36 — Upload a Qur'an recitation recording**
As a Student, I want to upload an audio recording of my Qur'an recitation so that my teacher can listen, annotate mistakes, and give feedback.

Acceptance criteria:
- On the Hifz or Qur'an recitation page, an upload button accepts audio files (MP3, WAV, M4A, max 10 MB).
- The uploaded file is stored against the student's current recitation session.
- The teacher is notified that a new recording is available for review.
- The student can re-upload until the session is marked as reviewed.

**US-37 — View my Hifz progress**
As a Student, I want to view my Hifz progress showing each surah or juz with its status (Not Started, In Progress, Completed) so that I know which parts have been verified by my teacher.

Acceptance criteria:
- A Hifz progress page lists all surahs or juz entries.
- Each entry shows its current status with a colour indicator (grey = Not Started, amber = In Progress, green = Completed).
- Completed entries show the sign-off date and teacher name.
- The student cannot change a status themselves; only teacher sign-off moves it to Completed.

**US-38 — View finalised exam results**
As a Student, I want to see my exam results once they have been finalised by my teacher so that I can track my academic performance over time.

Acceptance criteria:
- An exam results page lists all exams the student has taken.
- Only finalised (signed-off) results are shown; draft results are hidden from the student.
- Each result shows the exam title, date, subject, score, and any teacher comments.

**US-39 — Receive in-app notifications**
As a Student, I want to receive in-app notifications when new homework is assigned, when my teacher gives feedback, or when my exam results are published so that I do not miss important updates.

Acceptance criteria:
- A notification bell icon shows a count of unread notifications.
- Clicking the bell opens a dropdown listing recent notifications with a title, short description, and timestamp.
- Clicking a notification navigates to the relevant page (e.g. the assignment, the exam result).
- Notifications are marked as read once opened.

---

#### Parent stories

**US-40 — View a summary dashboard for each child**
As a Parent, I want to log in and see a summary dashboard for each of my children showing their attendance percentage, latest Hifz status, recent homework feedback, and outstanding fees so that I have a single overview without needing to navigate multiple pages.

Acceptance criteria:
- If a parent has multiple children, a child selector or tabbed view lets them switch between children.
- For each child the dashboard shows: attendance % this term, Hifz completion %, most recent homework feedback (title + status), and total outstanding fees.
- All progress data shown is based on teacher-verified (signed-off) records only.

**US-41 — View verified Hifz progress**
As a Parent, I want to view my child's Hifz progress showing which surahs have been signed off by a teacher so that I can see authentic, verified completion rather than self-reported data.

Acceptance criteria:
- The Hifz progress page mirrors the student's view (US-37) but is accessed from the parent's account.
- Each Completed entry shows the teacher's name and sign-off date.
- The parent cannot modify any status.

**US-42 — View homework submissions and teacher feedback**
As a Parent, I want to view my child's homework submissions along with the teacher's feedback and approval status so that I can support their learning at home and follow up on rejected work.

Acceptance criteria:
- A homework page lists all of the child's assignments with status (Not submitted, Submitted, Approved, Rejected).
- Clicking an assignment shows the teacher's comments and the submission file or text.
- The parent cannot submit on behalf of the child.

**US-43 — View finalised exam results**
As a Parent, I want to see my child's finalised exam results and any teacher comments so that I understand their academic performance and can discuss it with them.

Acceptance criteria:
- An exam results page shows finalised results only (same visibility rules as US-38).
- Each result shows exam title, date, subject, score, and teacher comments.

**US-44 — View outstanding fees and pay online**
As a Parent, I want to view a list of outstanding fee items with amounts and due dates and pay them online via card so that payments are convenient and instantly recorded.

Acceptance criteria:
- A fees page lists all fee items for the parent's children with amount, due date, and status (Outstanding / Paid / Overdue).
- A "Pay now" button on an outstanding item initiates a Stripe Checkout session.
- On successful payment the status changes to Paid and the payment date is recorded.
- The parent is redirected back to the fees page with a confirmation message.

**US-45 — Receive a payment receipt**
As a Parent, I want to receive a receipt after each payment so that I have proof of what I have paid for my records.

Acceptance criteria:
- After a successful payment, the parent receives an in-app notification with a link to the receipt.
- The receipt shows school name, child name, fee item description, amount paid, payment date, and a reference number.
- The parent can view past receipts from a payment history page.

**US-46 — Receive absence and overdue fee notifications**
As a Parent, I want to receive a notification when my child is marked absent and when a fee becomes overdue so that I can take action promptly.

Acceptance criteria:
- An in-app notification is sent on the day a student is marked absent, including the date and session.
- An in-app notification is sent on the day a fee becomes overdue, including the fee name and amount.
- Optionally, an email is also sent for both notification types (configurable in parent settings).

**US-47 — Message my child's teacher**
As a Parent, I want to send a message to my child's teacher so that I can raise concerns, ask questions, or discuss progress directly without needing a separate communication tool.

Acceptance criteria:
- From the child's class page or teacher list, the parent can open a message composer.
- Messages are sent to the teacher's messaging inbox.
- The teacher receives an in-app notification for new messages.
- Conversation history is preserved and visible to both parties.

**US-48 — View behaviour incidents**
As a Parent, I want to view any behaviour incident reports involving my child so that I am aware of conduct issues (positive or negative) and can discuss them at home.

Acceptance criteria:
- A behaviour page lists all incidents for the child with date, category (Positive / Negative), severity, and description.
- The parent receives a notification when a new incident is logged.
- The parent cannot edit or delete incidents.

---

#### Cross-cutting stories

**US-49 — Tenant data isolation**
As any user, I want my data to be completely isolated to my school so that I never see another school's students, teachers, classes, or financial information.

Acceptance criteria:
- Every database query is scoped to the authenticated user's school tenant.
- API responses never include records belonging to a different school.
- Attempting to access a resource from another school via direct URL returns a 403 Forbidden or 404 Not Found.
- Automated tests verify tenant isolation for all major models.

**US-50 — Responsive design**
As any user, I want the interface to be fully responsive so that I can use it comfortably on a mobile phone, tablet, or desktop computer.

Acceptance criteria:
- All pages render correctly at viewport widths of 320px, 768px, and 1280px.
- Navigation collapses to a hamburger menu on small screens.
- Tables scroll horizontally on small screens rather than breaking the layout.
- Touch targets (buttons, links) are at least 44x44px on mobile.

**US-51 — Clear form validation**
As any user, I want to see clear, specific validation messages next to the relevant form field when I make an input error so that I can correct it without confusion.

Acceptance criteria:
- Required fields show an error message if left empty on submission.
- Invalid formats (e.g. email, date) show a message describing the expected format.
- Error messages appear inline next to the field, not only as a page-level banner.
- The first errored field is scrolled into view and focused.

**US-52 — Accessibility (WCAG AA)**
As any user, I want the site to meet WCAG AA standards for colour contrast, keyboard navigation, and screen-reader support so that it is accessible to users with disabilities.

Acceptance criteria:
- All text meets a minimum contrast ratio of 4.5:1 against its background.
- All interactive elements are reachable and operable via keyboard (Tab, Enter, Escape).
- All form inputs have associated `<label>` elements or `aria-label` attributes.
- Headings follow a logical hierarchy (h1 → h2 → h3) with no skipped levels.
- Focus states are visible on all interactive elements.

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
| Landing / module index | `index.html` | Public-facing landing page with a module overview table listing all platform features. Acts as the entry point and marketing page for the platform. |
| Login | `login.html` | Login form with email and password fields, "forgot password" link, and role-aware redirect logic. Demonstrates the authentication entry point for all roles. |
| Registration | `register.html` | Registration form for new users with fields for name, email, password, and role selection. Includes inline validation placeholders. |
| Super Admin dashboard | `dashboard-super-admin.html` | Platform-level overview showing total schools, active users, revenue metrics, and a list of recent tenant sign-ups. Provides quick-action links for tenant management. |
| School Admin dashboard | `dashboard-school-admin.html` | School-level overview with cards for student count, teacher count, attendance rate, and fee collection status. Sidebar navigation links to all school management areas. |
| Teacher dashboard | `dashboard-teacher.html` | Teacher workspace showing today's timetable, class-level metrics (attendance %, submission rate, Hifz progress), and quick links to take a register or assign homework. |
| Student dashboard | `dashboard-student.html` | Student portal showing today's lessons, upcoming homework deadlines, recent notifications, and a Hifz progress summary bar. |
| Parent dashboard | `dashboard-parent.html` | Parent portal with a child selector, per-child attendance summary, latest homework feedback, Hifz progress, and outstanding fees with a "Pay now" action. |
| Analytics | `analytics.html` | School-wide analytics page with placeholder charts for attendance trends, Hifz completion rates, homework submission rates, and fee collection over time. |
| Timetable | `timetable.html` | Weekly timetable grid (Monday–Friday) with configurable time slots. Shows subject, teacher, and room per cell. Designed for both viewing and editing modes. |
| Attendance register | `attendance.html` | Class register layout listing all students with present/late/absent toggle buttons per row. Includes a date selector and a "Save register" action. |
| Hifz progress tracker | `hifz-progress.html` | Per-student Hifz tracker showing each surah/juz with status indicators (Not Started / In Progress / Completed). Completed entries display the sign-off teacher and date. |
| Qur'an annotation | `quran-annotation.html` | Recitation session page with an audio player, a list of teacher annotations (mistake category, ayah reference, comment), and an upload area for student recordings. |
| Worksheets / homework | `worksheets.html` | Assignment list with title, subject, due date, and status columns. Detail view shows the assignment description, submission upload area, and teacher feedback. |
| Exams and results | `exams.html` | Exam list with title, date, subject, and status (Draft / Finalised). Detail view shows per-student scores and a "Finalise results" sign-off button. |
| Payments / fees | `payments.html` | Fee list with amount, due date, and status (Outstanding / Paid / Overdue). Includes a Stripe Checkout "Pay now" button and a payment history section with receipts. |
| Behaviour log | `behaviour.html` | Incident log table with date, student, teacher, category (Positive / Negative), severity, and description. Includes filters and a "Log incident" form. |
| Staff messaging | `messages.html` | Messaging interface with a conversation list sidebar and a message thread view. Compose area supports selecting individual parents or all parents of a class. |

## Design

### Visual language

- Modern, minimal dashboard UI with clear spacing and consistent components.
- **Arabic design inspiration**: subtle geometric patterns (e.g. mashrabiya / mosaic motifs) in headers, dividers, and section breaks — used sparingly so content stays scannable.

### Colour palette

The UI theme is **black, white, and hints of gold**:

- **Black / near-black** — primary background and primary navigation.
- **White / off-white** — content surfaces and high-contrast body text on dark areas.
- **Gold (accent)** — sparing use for primary actions, focus rings, active nav states, and key metrics (not large fills).

Concrete CSS variables and component tokens will be added with the first template theme; contrast targets WCAG AA where feasible.

### Teacher sign-off & verification (product requirement)

- **Hifz**: surah/lesson status moves to *Completed* only after teacher sign-off; students and parents never self-approve completion.
- **Homework / worksheets**: submissions move through pending → approved/rejected with teacher id and timestamp.
- **Exams**: auto-marking may produce a draft score; results are **official** only when a teacher finalises (signs off) the record.
- **Security**: sign-off actions require **password re-entry** (2FA optional later); each sign-off creates an **AuditLog** entry (`SIGN_OFF`, target type, target id, timestamp).
- **Analytics**: parent dashboards and school reports prioritise **signed-off / finalised** data for progress percentages.

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

- `manage.py` — Django entrypoint
- `core/` — project settings, root URLconf, WSGI/ASGI
- Reusable apps (each in its own Django app):

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

**Static wireframes (present in repo):** `index.html`, role and feature `*.html` pages, and `css/base.css` — these mirror the planned app areas above until Django apps are recreated.

## Data model

### Entity-Relationship Diagram (ERD)

The ERD below describes the planned relational structure for the ESA database. It captures every core entity, its key attributes, and the relationships between entities. The diagram will be produced using a tool such as dbdiagram.io or Lucidchart and added to the `docs/` folder; the textual description here serves as the specification it is built from.

#### Design principles

- **School as tenant root** — `School` is the top-level entity. Almost every other table carries a `school_id` foreign key so that all queries can be scoped to a single tenant with a simple filter. This is the foundation of multi-tenant data isolation.
- **Single User model with role field** — Rather than separate login tables per role, a single custom `User` model stores authentication credentials and a `role` enum (super_admin, school_admin, teacher, student, parent). Role-specific profile tables (TeacherProfile, StudentProfile, ParentProfile) extend the user with additional fields relevant to that role.
- **Sign-off fields on progress records** — Entities that require teacher verification (HifzRecord, WorksheetSubmission, ExamResult) all share a common pattern: `signed_off` (boolean), `signed_off_by` (FK to User), and `signed_off_at` (datetime). This makes the trust layer consistent and auditable.
- **AuditLog for traceability** — A dedicated AuditLog table records sensitive actions (sign-offs, payment confirmations, role changes) with the acting user, action type, target model, target ID, and timestamp.

#### Entities and relationships

**User**
- `id` (PK), `email` (unique), `password_hash`, `first_name`, `last_name`, `role` (enum: super_admin / school_admin / teacher / student / parent), `school_id` (FK to School, nullable for super_admin), `is_active`, `date_joined`
- One User belongs to one School (except Super Admins who have no school).

**School**
- `id` (PK), `name`, `address`, `contact_email`, `subscription_tier`, `stripe_account_id` (nullable), `status` (active / suspended / deactivated), `created_at`
- One School has many Users, Classes, Subjects, FeeItems, and all other tenant-scoped records.

**TeacherProfile**
- `id` (PK), `user_id` (FK to User, one-to-one), `school_id` (FK to School), `qualifications`, `hire_date`
- Extends a User whose role is teacher.

**StudentProfile**
- `id` (PK), `user_id` (FK to User, one-to-one), `school_id` (FK to School), `date_of_birth`, `class_id` (FK to Class), `enrolment_date`
- Extends a User whose role is student. Belongs to one Class.

**ParentProfile**
- `id` (PK), `user_id` (FK to User, one-to-one), `school_id` (FK to School), `phone_number`
- Extends a User whose role is parent.

**ParentChild** (junction table)
- `parent_id` (FK to ParentProfile), `child_id` (FK to StudentProfile)
- Many-to-many: a parent can have multiple children; a child can have up to two parent accounts.

**YearGroup**
- `id` (PK), `school_id` (FK to School), `name` (e.g. "Year 1"), `academic_year`
- One School has many YearGroups.

**Class**
- `id` (PK), `school_id` (FK to School), `year_group_id` (FK to YearGroup), `name`, `capacity`
- One YearGroup has many Classes. One Class has many Students.

**Subject**
- `id` (PK), `school_id` (FK to School), `category` (enum: hifz / alimiyah / general), `display_name`, `is_archived`
- One School has many Subjects.

**TeacherSubjectClass** (junction table)
- `teacher_id` (FK to TeacherProfile), `subject_id` (FK to Subject), `class_id` (FK to Class)
- Assigns a teacher to a subject within a specific class.

**TimetableSlot**
- `id` (PK), `school_id` (FK to School), `class_id` (FK to Class), `subject_id` (FK to Subject), `teacher_id` (FK to TeacherProfile), `day_of_week` (enum: mon–fri), `start_time`, `end_time`, `room` (nullable)
- One Class has many TimetableSlots across the week.

**AttendanceRecord**
- `id` (PK), `school_id` (FK to School), `student_id` (FK to StudentProfile), `class_id` (FK to Class), `date`, `status` (enum: present / late / absent), `recorded_by` (FK to User), `created_at`
- One Student has many AttendanceRecords.

**HifzRecord**
- `id` (PK), `school_id` (FK to School), `student_id` (FK to StudentProfile), `surah_or_juz` (string), `status` (enum: not_started / in_progress / completed), `signed_off` (boolean, default false), `signed_off_by` (FK to User, nullable), `signed_off_at` (datetime, nullable), `notes`
- One Student has many HifzRecords (one per surah/juz). Status can only move to completed via teacher sign-off.

**QuranSession**
- `id` (PK), `school_id` (FK to School), `student_id` (FK to StudentProfile), `teacher_id` (FK to TeacherProfile), `date`, `audio_file` (file path, nullable), `teacher_audio_feedback` (file path, nullable), `is_reviewed` (boolean)
- One Student has many QuranSessions.

**QuranAnnotation**
- `id` (PK), `session_id` (FK to QuranSession), `category` (enum: tajweed / memorisation / fluency), `ayah_reference` (string), `comment`, `created_at`
- One QuranSession has many QuranAnnotations.

**Worksheet**
- `id` (PK), `school_id` (FK to School), `title`, `description`, `file_attachment` (nullable), `subject_id` (FK to Subject), `class_id` (FK to Class), `due_date`, `created_by` (FK to User), `created_at`
- One Class has many Worksheets.

**WorksheetSubmission**
- `id` (PK), `worksheet_id` (FK to Worksheet), `student_id` (FK to StudentProfile), `submitted_file` (nullable), `submitted_text` (nullable), `status` (enum: not_submitted / submitted / approved / rejected), `teacher_comment`, `signed_off_by` (FK to User, nullable), `signed_off_at` (datetime, nullable), `submitted_at`
- One Worksheet has many WorksheetSubmissions (one per student).

**Exam**
- `id` (PK), `school_id` (FK to School), `title`, `subject_id` (FK to Subject), `class_id` (FK to Class), `exam_type` (enum: mcq / written / mixed), `date`, `created_by` (FK to User), `created_at`
- One Class has many Exams.

**ExamResult**
- `id` (PK), `exam_id` (FK to Exam), `student_id` (FK to StudentProfile), `score`, `max_score`, `teacher_comment`, `status` (enum: draft / finalised), `signed_off_by` (FK to User, nullable), `signed_off_at` (datetime, nullable)
- One Exam has many ExamResults (one per student). Results are hidden from students and parents until status is finalised.

**BehaviourLog**
- `id` (PK), `school_id` (FK to School), `student_id` (FK to StudentProfile), `logged_by` (FK to User), `date`, `category` (enum: positive / negative), `severity` (enum: low / medium / high), `description`, `follow_up_notes` (nullable), `created_at`
- One Student has many BehaviourLog entries.

**FeeItem**
- `id` (PK), `school_id` (FK to School), `name`, `amount` (decimal), `due_date`, `target_type` (enum: school / year_group / student), `target_id` (polymorphic reference), `created_at`
- Defines a fee that can target the whole school, a year group, or an individual student.

**Payment**
- `id` (PK), `school_id` (FK to School), `fee_item_id` (FK to FeeItem), `parent_id` (FK to ParentProfile), `student_id` (FK to StudentProfile), `amount_paid` (decimal), `status` (enum: pending / completed / failed), `stripe_payment_intent_id` (nullable), `paid_at` (datetime, nullable), `receipt_url` (nullable)
- One FeeItem has many Payments. Status moves to completed on Stripe webhook confirmation.

**Notification**
- `id` (PK), `school_id` (FK to School), `recipient_id` (FK to User), `title`, `body`, `link` (nullable), `is_read` (boolean, default false), `created_at`
- One User has many Notifications.

**Message**
- `id` (PK), `school_id` (FK to School), `sender_id` (FK to User), `recipient_id` (FK to User), `subject`, `body`, `is_read` (boolean, default false), `sent_at`
- Supports direct messaging between teachers and parents.

**AuditLog**
- `id` (PK), `school_id` (FK to School, nullable), `user_id` (FK to User), `action` (enum: sign_off / payment_confirmed / role_changed / tenant_suspended / …), `target_model` (string), `target_id` (integer), `metadata` (JSON, nullable), `created_at`
- Records every sensitive action for traceability and compliance.

#### Key relationships summary

| Relationship | Type | Description |
|-------------|------|-------------|
| School → User | One-to-many | A school has many users across all roles. |
| User → TeacherProfile / StudentProfile / ParentProfile | One-to-one | Each user has at most one role-specific profile. |
| ParentProfile ↔ StudentProfile | Many-to-many | Via ParentChild junction table. |
| School → YearGroup → Class | One-to-many chain | A school contains year groups, each containing classes. |
| Class → StudentProfile | One-to-many | A student belongs to one class. |
| TeacherProfile ↔ Subject ↔ Class | Many-to-many | Via TeacherSubjectClass junction table. |
| Class → TimetableSlot | One-to-many | A class has many scheduled time slots per week. |
| StudentProfile → AttendanceRecord | One-to-many | A student has an attendance record per session. |
| StudentProfile → HifzRecord | One-to-many | A student has one record per surah/juz. |
| StudentProfile → QuranSession → QuranAnnotation | One-to-many chain | Sessions contain annotations. |
| Class → Worksheet → WorksheetSubmission | One-to-many chain | Worksheets are per-class; submissions are per-student. |
| Class → Exam → ExamResult | One-to-many chain | Exams are per-class; results are per-student. |
| FeeItem → Payment | One-to-many | A fee can have multiple payment attempts. |
| User → Notification | One-to-many | A user receives many notifications. |
| User → Message (sender/recipient) | One-to-many | Messages link a sender and recipient. |
| User → AuditLog | One-to-many | Every audited action records the acting user. |

The full ERD diagram image will be added to `docs/erd.png` and linked here once generated from the specification above.

### Tenant model

- `School` is the tenant root.
- Tenant isolation rules will be documented and tested (query scoping, permissions, and admin boundaries).

### Core entities (planned)

- User (custom, with role: Super Admin, School Admin, Teacher, Student, Parent)
- School (tenant root)
- Teacher, Student, Parent (profiles linked to `User` and `School`)
- Subject (custom per school: Hifz / Alimiyah / General)
- Class / YearGroup
- Timetable, Attendance
- BehaviourLog
- Worksheet, **WorksheetSubmission** (pending / approved / rejected; `signed_off_by`, `signed_off_at`)
- Exam, **ExamResult** (draft vs **finalised**; teacher sign-off fields)
- **HifzRecord** (status; `signed_off`, `signed_off_by`, `signed_off_at`, notes)
- QuranAnnotation (per student / session; Tajweed / Memorisation / Fluency tags, audio)
- PendingPayment / CompletedPayment (Stripe Connect; `reference_id` on completed)
- **AuditLog** (including `SIGN_OFF` actions)

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
- JWT obtain pair: `POST /api/auth/token/` with `username` and `password` (JSON defaults depend on client; browsable API uses session for other routes).

## API overview

- **JWT**: Simple JWT — obtain at `/api/auth/token/`, refresh at `/api/auth/token/refresh/`.
- **Default DRF permission**: authenticated (tighten per-view as apps land).
- Domain APIs (schools, students, payments, etc.) will be added app-by-app with tenant-scoped querysets.

## Payments (Stripe Connect)

To be added (onboarding schools, payout flow, platform commission, webhooks).

## Testing and Bugs

### Manual testing

To be added as features ship (screens, flows, and evidence).

### Bugs

| # | Bug description | Page / feature | Steps to reproduce | Expected behaviour | Actual behaviour | Severity | Status | Fix |
|---|----------------|----------------|--------------------|--------------------|------------------|----------|--------|-----|
| 1 | | | | | | | | |
| 2 | | | | | | | | |
| 3 | | | | | | | | |
| 4 | | | | | | | | |
| 5 | | | | | | | | |
| 6 | | | | | | | | |
| 7 | | | | | | | | |
| 8 | | | | | | | | |
| 9 | | | | | | | | |
| 10 | | | | | | | | |
| 11 | | | | | | | | |
| 12 | | | | | | | | |
| 13 | | | | | | | | |
| 14 | | | | | | | | |
| 15 | | | | | | | | |
| 16 | | | | | | | | |
| 17 | | | | | | | | |
| 18 | | | | | | | | |
| 19 | | | | | | | | |
| 20 | | | | | | | | |

### Automated testing

Run the Django test suite:

```bash
python manage.py test
```

Tests are added incrementally alongside features (see `accounts` tests for the custom user model).

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