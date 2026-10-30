# Pakistan Patriotic Youth (PPY) Membership Management System – Backend

A centralized membership and organizational management system designed to manage Pakistan Patriotic Youth (PPY), including member registration, identity verification, organizational hierarchy, leadership promotions, membership cards, and administrative workflows.

## Project Overview

The PPY Membership Management System aims to digitize and streamline the organization's membership and administrative processes.

The backend provides RESTful APIs to manage members, organizations, positions, verification requests, membership applications, promotions, digital cards, and audit records.

## Key Features

- **User Accounts:** User registration, authentication, and account management.
- **Organization Management:** Manage the organizational hierarchy from national to local levels.
- **Membership Management:** Submit, review, approve, reject, and manage membership applications.
- **Document Verification:** Upload and review identity documents and police verification certificates.
- **Position Management:** Manage organizational positions and their corresponding levels.
- **Promotion Management:** Submit and review leadership promotion applications.
- **Digital Cards:** Manage membership and leadership identification cards.
- **Audit Logs:** Maintain records of important administrative activities.
- **Reusable Common Utilities:** Shared models, serializers, validators, permissions, pagination, and exception handling.

## Organizational Hierarchy

The system follows a structured organizational hierarchy:

1. National Level
2. Provincial Level
3. District Level
4. Tehsil / Taluka Level

Members must follow the defined organizational progression and eligibility requirements when applying for leadership positions.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django 5.2 | Backend framework |
| Django REST Framework | REST API development |
| PostgreSQL | Database |
| JWT | Token-based authentication |
| django-filter | API filtering |
| Git & GitHub | Version control and collaboration |

## Project Structure

```text
patrioticYouth_Backend/
│
├── apps/
│   ├── accounts/
│   ├── audit/
│   ├── cards/
│   ├── common/
│   ├── memberships/
│   ├── organizations/
│   ├── positions/
│   ├── promotions/
│   └── verification/
│
├── config/
│   ├── settings/
│   │   ├── __init__.py
│   │   └── base.py
│   └── urls.py
│
├── media/
├── static/
├── tests/
├── requirements/
├── .env.example
├── .gitignore
└── manage.py
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/waqaralisoomro915-cloud/Pakistan-Patriotic-Youth-PPY-Membership-Management-System_Backend.git

cd Pakistan-Patriotic-Youth-PPY-Membership-Management-System_Backend
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

Install the packages listed in the project's requirements file:

```bash
pip install -r requirements.txt
```

If your requirements file is inside the `requirements/` directory, use its actual filename, for example:

```bash
pip install -r requirements/base.txt
```

### 4. Configure Environment Variables

Create a `.env` file using `.env.example` as a reference.

Configure your environment variables, including:

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
```

Add your database credentials and other required settings according to your Django configuration.

**Important:** Never commit your real `.env` file or production secrets to GitHub.

### 5. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Backend development server:

```text
http://127.0.0.1:8000/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

## API Modules

| Module | Responsibility |
|---|---|
| Accounts | User accounts and authentication |
| Organizations | Organizational structure |
| Positions | Organizational positions |
| Memberships | Membership applications and approvals |
| Verification | Identity and police document verification |
| Promotions | Leadership promotion workflows |
| Cards | Membership and leadership cards |
| Audit | Administrative activity records |
| Common | Shared backend utilities |

## API Route Prefixes

| Module | Route |
|---|---|
| Accounts | `/api/accounts/` |
| Organizations | `/api/organizations/` |
| Audit | `/api/audit/` |
| Cards | `/cards/` |
| Memberships | `/memberships/` |
| Promotions | `/promotions/` |
| Verification | `/verification/` |

The route prefixes reflect the current Django URL configuration.

## Business Workflow

The intended membership workflow is:

1. A user registers an account.
2. The user submits a membership application.
3. The user uploads identity and police verification documents.
4. An authorized administrator reviews the verification documents.
5. The administrator separately reviews and approves or rejects the membership application.
6. Approved members can receive membership cards.
7. Eligible members can apply for leadership positions according to organizational hierarchy and service-duration requirements.
8. Approved leadership appointments can qualify members for leadership cards.

## Security and Validation

The backend incorporates:

- Authentication and permission checks.
- Server-side input validation.
- Document extension and file-size validation.
- Read-only audit records.
- Controlled membership and promotion review actions.
- Database relationships and integrity constraints.

Production deployment should additionally use secure file storage, HTTPS, production secrets, and appropriate database and access controls.

## Development Status

<badge color="success">Backend development in progress</badge>

The project is being developed module by module, with a focus on clean architecture, reusable components, data integrity, permissions, and business-rule enforcement.

Some workflows and production-level security controls are still under development.

## Author

**Waqar Ali**

Junior Full-Stack Developer | Django | Django REST Framework | React | Python

- GitHub: [@waqaralisoomro915-cloud](https://github.com/waqaralisoomro915-cloud)

---

*Building a structured digital platform for transparent and efficient organizational management.*
