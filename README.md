# 🏦 SecureBank - Online Banking System

A complete, production-ready banking system built with Django, demonstrating Object-Oriented Programming (OOP) principles with a modern, responsive user interface.

![Django](https://img.shields.io/badge/Django-5.0-green?logo=django)
![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-yellow)

---


##Live Demo (https://banking-system-2-b8n6.onrender.com)





## 📋 Table of Contents

- [Features](#-features)
- [OOP Concepts](#-oop-concepts-demonstrated)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Project Structure](#-project-structure)
- [Usage Guide](#-usage-guide)
- [Screenshots](#-screenshots)
- [Database Schema](#-database-schema)
- [API Documentation](#-api-documentation)
- [Security](#-security)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🔐 User Management
- ✅ Secure user registration with validation
- ✅ Login/Logout functionality
- ✅ Password hashing (PBKDF2)
- ✅ User profile management
- ✅ Identity verification

### 💳 Account Management
- ✅ Create multiple accounts (Savings & Current)
- ✅ Unique account number generation
- ✅ Account type selection with different rules
- ✅ Account balance tracking
- ✅ Account status management

### 💰 Banking Operations
- ✅ **Deposit Money**: Add funds to account
- ✅ **Withdraw Money**: Withdraw with validation
  - Savings: Minimum balance check
  - Current: Overdraft facility
- ✅ **Fund Transfer**: Between accounts
- ✅ **Transaction History**: Complete audit trail
- ✅ **Balance Inquiry**: Real-time balance

### 📊 Dashboard & Reports
- ✅ User-friendly dashboard
- ✅ Account summary cards
- ✅ Recent transaction view
- ✅ Total balance calculation
- ✅ Account listing with actions

### 👨‍💼 Admin Panel
- ✅ Django admin interface
- ✅ Manage users and accounts
- ✅ View all transactions
- ✅ Search and filter capabilities
- ✅ Bulk operations

### 🎨 UI/UX
- ✅ Modern, responsive design
- ✅ Bootstrap 5 framework
- ✅ Font Awesome icons
- ✅ Gradient backgrounds
- ✅ Card-based layout
- ✅ Mobile-friendly
- ✅ Success/Error messages
- ✅ Loading indicators

---

## 🧠 OOP Concepts Demonstrated

### 1. **Encapsulation** 🔒
```python
class Account(models.Model):
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    
    def get_balance(self):
        """Controlled access to balance"""
        return self.balance
    
    def set_balance(self, amount):
        """Controlled modification with validation"""
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self.balance = amount
```

**Why?** Protects data integrity by controlling access through methods.

---

### 2. **Inheritance** 👨‍👦
```python
# Base Class
class Account(models.Model):
    account_number = models.CharField(max_length=12)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        abstract = True

# Child Classes
class SavingsAccount(Account):
    MINIMUM_BALANCE = 500
    
class CurrentAccount(Account):
    OVERDRAFT_LIMIT = 10000
```

**Why?** Code reusability - common features in base class, unique features in child classes.

---

### 3. **Polymorphism** 🎭
```python
class SavingsAccount(Account):
    def withdraw(self, amount):
        # Savings-specific logic
        if self.balance - amount < self.MINIMUM_BALANCE:
            raise ValueError("Insufficient balance")
        self.balance -= amount

class CurrentAccount(Account):
    def withdraw(self, amount):
        # Current-specific logic (allows overdraft)
        if self.balance - amount < -self.OVERDRAFT_LIMIT:
            raise ValueError("Overdraft limit exceeded")
        self.balance -= (amount + self.TRANSACTION_FEE)
```

**Why?** Same method name, different behavior based on object type.

---

### 4. **Abstraction** 🎨
```python
class Account(models.Model):
    class Meta:
        abstract = True  # Cannot be instantiated
    
    def deposit(self, amount):
        raise NotImplementedError("Subclass must implement")
    
    def withdraw(self, amount):
        raise NotImplementedError("Subclass must implement")
```

**Why?** Hides complex implementation, shows only essential features.

---

## 🛠 Tech Stack

### Backend
- **Django 5.0**: Web framework
- **Python 3.8+**: Programming language
- **SQLite**: Database (default)
- **Django ORM**: Object-Relational Mapping

### Frontend
- **Bootstrap 5.3**: CSS framework
- **HTML5**: Markup
- **CSS3**: Styling (Custom + Bootstrap)
- **JavaScript**: Interactivity
- **Font Awesome 6**: Icons

### Tools
- **pip**: Package manager
- **virtualenv**: Virtual environment
- **Git**: Version control

---

## 📥 Installation

### Prerequisites
```bash
- Python 3.8 or higher
- pip (Python package manager)
- Git
```

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/banking-system.git
cd banking-system
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser

# Enter:
# Username: admin
# Email: admin@securebank.com
# Password: [your secure password]
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

### Step 7: Access Application
- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 📁 Project Structure

```
banking_system/
│
├── banking_project/              # Django project settings
│   ├── __init__.py
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
│
├── accounts/                     # Main banking application
│   ├── migrations/              # Database migrations
│   │   └── __init__.py
│   │
│   ├── templates/               # HTML templates
│   │   └── accounts/
│   │       ├── base.html        # Base template
│   │       ├── home.html        # Landing page
│   │       ├── login.html       # Login page
│   │       ├── register.html    # Registration
│   │       ├── dashboard.html   # User dashboard
│   │       ├── create_account.html
│   │       ├── account_detail.html
│   │       ├── deposit.html
│   │       ├── withdraw.html
│   │       ├── transfer.html
│   │       └── transaction_history.html
│   │
│   ├── static/                  # Static files (CSS, JS, Images)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── __init__.py
│   ├── admin.py                 # Admin panel configuration
│   ├── apps.py                  # App configuration
│   ├── models.py                # OOP Classes (Account, Transaction)
│   ├── forms.py                 # Form classes
│   ├── views.py                 # Business logic
│   ├── urls.py                  # URL routing
│   └── tests.py                 # Unit tests
│
├── media/                        # User uploaded files
├── static/                       # Collected static files
├── db.sqlite3                   # Database file
├── manage.py                    # Django management script
├── requirements.txt             # Project dependencies
├── setup.py                     # Automated setup script
└── README.md                    # This file
```

---

## 📖 Usage Guide

### 1. Register New User
1. Navigate to http://127.0.0.1:8000/
2. Click **Register**
3. Fill in all required fields:
   - Personal info (name, email, username)
   - Contact details (phone, address)
   - Identity proof (Aadhaar/PAN/Passport)
4. Click **Create Account**

### 2. Login
1. Go to Login page
2. Enter username and password
3. Click **Login**
4. Redirected to Dashboard

### 3. Create Bank Account
1. From Dashboard, click **Create Account**
2. Choose account type:
   - **Savings**: Min balance ₹500, 4% interest
   - **Current**: Min balance ₹1000, overdraft ₹10,000
3. Enter initial deposit
4. Click **Create Account**
5. Unique account number generated

### 4. Deposit Money
1. From Dashboard, find your account
2. Click **Deposit** (green plus icon)
3. Enter amount
4. Click **Deposit**
5. Transaction recorded

### 5. Withdraw Money
1. From Dashboard, find your account
2. Click **Withdraw** (yellow minus icon)
3. Enter amount
4. System checks:
   - Savings: Minimum balance maintained
   - Current: Overdraft limit not exceeded
5. Click **Withdraw**

### 6. Transfer Funds
1. From Dashboard, find source account
2. Click **Transfer** (blue exchange icon)
3. Enter recipient account number
4. Enter amount
5. Add description (optional)
6. Click **Transfer**
7. Both accounts updated atomically

### 7. View Transaction History
1. Click on account number
2. View detailed account information
3. See all transactions with:
   - Transaction ID
   - Type (Deposit/Withdrawal/Transfer)
   - Amount
   - Balance after transaction
   - Timestamp

### 8. Admin Panel (Superuser Only)
1. Navigate to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Manage:
   - Users
   - Customer Profiles
   - Savings Accounts
   - Current Accounts
   - Transactions

---

## 📸 Screenshots

### Home Page
![Home Page](screenshots/home.png)
- Hero section with features
- Login and register buttons
- Feature highlights

### Dashboard
![Dashboard](screenshots/dashboard.png)
- Summary cards (balance, accounts, transactions)
- Account list with actions
- Recent transactions

### Account Detail
![Account Detail](screenshots/account_detail.png)
- Account information
- Transaction history
- Action buttons

### Deposit/Withdraw
![Transaction](screenshots/transaction.png)
- Simple form interface
- Validation feedback
- Success messages

---

## 🗄️ Database Schema

### Tables

#### 1. `auth_user` (Django default)
- User authentication data
- Fields: id, username, email, password, first_name, last_name

#### 2. `accounts_customerprofile`
- Extended user information
- Fields: id, user_id (FK), phone, address, date_of_birth, identity_proof, identity_number

#### 3. `accounts_savingsaccount`
- Savings account data
- Fields: id, account_number, customer_id (FK), balance, is_active, created_at

#### 4. `accounts_currentaccount`
- Current account data
- Fields: id, account_number, customer_id (FK), balance, is_active, created_at

#### 5. `accounts_transaction`
- Transaction records
- Fields: id, transaction_id, account_id (FK), transaction_type, amount, balance_after, timestamp

### Relationships
```
User (1) ──── (1) CustomerProfile
  │
  ├── (1) ──── (Many) SavingsAccount ──── (Many) Transaction
  │
  └── (1) ──── (Many) CurrentAccount ──── (Many) Transaction
```

---

## 🔐 Security

### Authentication & Authorization
- ✅ Django built-in authentication system
- ✅ Password hashing with PBKDF2-SHA256
- ✅ Session-based authentication
- ✅ CSRF protection on all forms
- ✅ Login required decorators

### Data Protection
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS prevention (template auto-escaping)
- ✅ User input validation
- ✅ Form field validation
- ✅ Minimum/maximum value checks

### Transaction Safety
- ✅ Database transactions (ACID properties)
- ✅ Rollback on error
- ✅ Atomic operations
- ✅ Concurrent access handling

### Best Practices
- ✅ Environment variables for secrets (production)
- ✅ Debug mode disabled (production)
- ✅ HTTPS enforcement (production)
- ✅ Rate limiting (production)
- ✅ Regular security updates

---

## 🧪 Testing

### Run Tests
```bash
python manage.py test accounts
```

### Test Coverage
- User registration validation
- Account creation
- Deposit operations
- Withdrawal validation
- Transfer atomicity
- Balance calculations
- Transaction recording

---

## 🚀 Deployment

### Production Checklist

1. **Environment Variables**
```python
# settings.py
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

2. **Database**
```python
# Use PostgreSQL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'banking_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Static Files**
```bash
python manage.py collectstatic
```

4. **Security Settings**
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Deployment Platforms
- **Heroku**: Easy deployment
- **AWS**: Scalable infrastructure
- **DigitalOcean**: VPS hosting
- **PythonAnywhere**: Python-focused hosting

---

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` file for details.

---

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- Font Awesome
- Stack Overflow Community
- GitHub Copilot

---

## 📞 Contact

**Project Maintainer**: Your Name
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/Anamikamishra464)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

---

## 🎯 Future Enhancements

- [ ] Email verification
- [ ] SMS notifications
- [ ] Two-factor authentication
- [ ] Loan management system
- [ ] Credit/Debit card feature
- [ ] Bill payment integration
- [ ] Investment options
- [ ] Mobile app (React Native)
- [ ] AI-powered chatbot
- [ ] Analytics dashboard
- [ ] Multi-currency support
- [ ] Biometric authentication

---

## 📚 Documentation

For detailed documentation, visit:
- [Installation Guide](docs/INSTALLATION.md)
- [OOP Concepts](docs/OOP_CONCEPTS.md)
- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

---

## ⭐ Star This Repository

If you found this project helpful, please give it a star! It helps others discover it.

---

**Built with ❤️ using Django and OOP principles**

© 2026 SecureBank. All rights reserved.
