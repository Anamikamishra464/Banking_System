"""
Banking System Views - Business Logic Layer
Handles all user interactions and processes
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db import transaction as db_transaction
from decimal import Decimal

from .models import SavingsAccount, CurrentAccount, Transaction, CustomerProfile
from .forms import (
    RegistrationForm, AccountCreationForm, DepositForm, 
    WithdrawalForm, TransferForm, SearchAccountForm
)


# ============================================================================
# AUTHENTICATION VIEWS
# ============================================================================

def home(request):
    """Landing page"""
    return render(request, 'accounts/home.html')


def register(request):
    """
    User registration view.
    Creates new user and customer profile.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created successfully for {user.username}! Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """
    User login view.
    Authenticates and logs in user.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


# ============================================================================
# DASHBOARD AND ACCOUNT MANAGEMENT
# ============================================================================

@login_required
def dashboard(request):
    """
    Main dashboard showing all accounts and summary.
    Demonstrates OOP: Uses polymorphism to handle different account types.
    """
    # Get all accounts for the user (use correct related_names)
    savings_accounts = SavingsAccount.objects.filter(customer=request.user, is_active=True)
    current_accounts = CurrentAccount.objects.filter(customer=request.user, is_active=True)
    
    # Calculate total balance (uses get_balance method - encapsulation)
    total_balance = sum(acc.get_balance() for acc in savings_accounts)
    total_balance += sum(acc.get_balance() for acc in current_accounts)
    
    # Get recent transactions
    recent_transactions = []
    for acc in savings_accounts:
        recent_transactions.extend(acc.transactions.all()[:5])
    for acc in current_accounts:
        recent_transactions.extend(acc.transactions.all()[:5])
    
    # Sort by timestamp
    recent_transactions.sort(key=lambda x: x.timestamp, reverse=True)
    recent_transactions = recent_transactions[:10]
    
    context = {
        'savings_accounts': savings_accounts,
        'current_accounts': current_accounts,
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
        'total_accounts': savings_accounts.count() + current_accounts.count(),
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def create_account(request):
    """
    Create new bank account.
    Demonstrates OOP: Uses inheritance - creates SavingsAccount or CurrentAccount.
    """
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account_type = form.cleaned_data['account_type']
            initial_deposit = form.cleaned_data['initial_deposit']
            
            try:
                # Polymorphism: Create appropriate account type
                if account_type == 'savings':
                    # Create account with zero balance first
                    account = SavingsAccount.objects.create(
                        customer=request.user,
                        balance=0
                    )
                    # Use polymorphic deposit method to record initial deposit
                    account.deposit(initial_deposit)
                    messages.success(request, f'Savings Account created successfully! Account Number: {account.account_number}')
                
                elif account_type == 'current':
                    # Create account with zero balance first
                    account = CurrentAccount.objects.create(
                        customer=request.user,
                        balance=0
                    )
                    # Use polymorphic deposit method to record initial deposit
                    account.deposit(initial_deposit)
                    messages.success(request, f'Current Account created successfully! Account Number: {account.account_number}')
                
                return redirect('dashboard')
            
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AccountCreationForm()
    
    return render(request, 'accounts/create_account.html', {'form': form})


@login_required
def account_detail(request, account_number):
    """
    View detailed account information.
    Demonstrates OOP: Handles both account types polymorphically.
    """
    # Try to find account in both types
    account = None
    
    try:
        account = SavingsAccount.objects.get(
            account_number=account_number,
            customer=request.user,
            is_active=True
        )
    except SavingsAccount.DoesNotExist:
        try:
            account = CurrentAccount.objects.get(
                account_number=account_number,
                customer=request.user,
                is_active=True
            )
        except CurrentAccount.DoesNotExist:
            messages.error(request, 'Account not found.')
            return redirect('dashboard')
    
    # Get transactions
    transactions = account.transactions.all()[:20]
    
    # Get minimum balance (polymorphic method)
    min_balance = account.get_minimum_balance()
    
    context = {
        'account': account,
        'transactions': transactions,
        'min_balance': min_balance,
    }
    
    return render(request, 'accounts/account_detail.html', context)


# ============================================================================
# TRANSACTION VIEWS
# ============================================================================

@login_required
def deposit_money(request, account_number):
    """
    Deposit money into account.
    Demonstrates OOP: Uses polymorphic deposit method.
    """
    # Find account
    account = None
    try:
        account = SavingsAccount.objects.get(
            account_number=account_number,
            customer=request.user,
            is_active=True
        )
    except SavingsAccount.DoesNotExist:
        try:
            account = CurrentAccount.objects.get(
                account_number=account_number,
                customer=request.user,
                is_active=True
            )
        except CurrentAccount.DoesNotExist:
            messages.error(request, 'Account not found.')
            return redirect('dashboard')
    
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            try:
                # Polymorphic method call - works for both account types
                account.deposit(amount)
                messages.success(request, f'Successfully deposited ₹{amount}. New balance: ₹{account.get_balance()}')
                return redirect('account_detail', account_number=account_number)
            except Exception as e:
                messages.error(request, f'Deposit failed: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DepositForm()
    
    context = {
        'form': form,
        'account': account,
    }
    
    return render(request, 'accounts/deposit.html', context)


@login_required
def withdraw_money(request, account_number):
    """
    Withdraw money from account.
    Demonstrates OOP: Uses polymorphic withdraw method with different rules.
    """
    # Find account
    account = None
    try:
        account = SavingsAccount.objects.get(
            account_number=account_number,
            customer=request.user,
            is_active=True
        )
    except SavingsAccount.DoesNotExist:
        try:
            account = CurrentAccount.objects.get(
                account_number=account_number,
                customer=request.user,
                is_active=True
            )
        except CurrentAccount.DoesNotExist:
            messages.error(request, 'Account not found.')
            return redirect('dashboard')
    
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            try:
                # Polymorphic method call - different behavior for each account type
                account.withdraw(amount)
                messages.success(request, f'Successfully withdrawn ₹{amount}. New balance: ₹{account.get_balance()}')
                return redirect('account_detail', account_number=account_number)
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f'Withdrawal failed: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = WithdrawalForm()
    
    context = {
        'form': form,
        'account': account,
        'min_balance': account.get_minimum_balance(),
    }
    
    return render(request, 'accounts/withdraw.html', context)


@login_required
def transfer_money(request, account_number):
    """
    Transfer money between accounts.
    Demonstrates: Database transactions and error handling.
    """
    # Find sender account
    from_account = None
    try:
        from_account = SavingsAccount.objects.get(
            account_number=account_number,
            customer=request.user,
            is_active=True
        )
    except SavingsAccount.DoesNotExist:
        try:
            from_account = CurrentAccount.objects.get(
                account_number=account_number,
                customer=request.user,
                is_active=True
            )
        except CurrentAccount.DoesNotExist:
            messages.error(request, 'Account not found.')
            return redirect('dashboard')
    
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            to_account_number = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data.get('description', 'Fund Transfer')
            
            # Find recipient account
            to_account = None
            try:
                to_account = SavingsAccount.objects.get(account_number=to_account_number, is_active=True)
            except SavingsAccount.DoesNotExist:
                try:
                    to_account = CurrentAccount.objects.get(account_number=to_account_number, is_active=True)
                except CurrentAccount.DoesNotExist:
                    messages.error(request, 'Recipient account not found.')
                    return redirect('transfer_money', account_number=account_number)
            
            # Perform transfer using database transaction
            try:
                with db_transaction.atomic():
                    # Withdraw from sender (uses polymorphic method)
                    from_account.withdraw(amount)
                    
                    # Deposit to recipient (uses polymorphic method)
                    to_account.deposit(amount)
                    
                    # Update transaction descriptions
                    last_withdrawal = from_account.transactions.latest('timestamp')
                    last_withdrawal.description = f"Transfer to {to_account_number}: {description}"
                    last_withdrawal.transaction_type = Transaction.TRANSFER_OUT
                    last_withdrawal.save()
                    
                    last_deposit = to_account.transactions.latest('timestamp')
                    last_deposit.description = f"Transfer from {account_number}: {description}"
                    last_deposit.transaction_type = Transaction.TRANSFER_IN
                    last_deposit.save()
                
                messages.success(request, f'Successfully transferred ₹{amount} to {to_account_number}')
                return redirect('account_detail', account_number=account_number)
            
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f'Transfer failed: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TransferForm(initial={'from_account': account_number})
    
    context = {
        'form': form,
        'account': from_account,
    }
    
    return render(request, 'accounts/transfer.html', context)


@login_required
def transaction_history(request, account_number):
    """View complete transaction history"""
    # Find account
    account = None
    try:
        account = SavingsAccount.objects.get(
            account_number=account_number,
            customer=request.user,
            is_active=True
        )
    except SavingsAccount.DoesNotExist:
        try:
            account = CurrentAccount.objects.get(
                account_number=account_number,
                customer=request.user,
                is_active=True
            )
        except CurrentAccount.DoesNotExist:
            messages.error(request, 'Account not found.')
            return redirect('dashboard')
    
    transactions = account.transactions.all()
    
    context = {
        'account': account,
        'transactions': transactions,
    }
    
    return render(request, 'accounts/transaction_history.html', context)
