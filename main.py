# main.py
import json
import random
import string
import streamlit as st
from pathlib import Path
import pandas as pd

# Configure page
st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Card styling */
    .stCard {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2d2d2d 0%, #1a1a1a 100%);
    }
    
    /* Success/Error messages */
    .success-message {
        padding: 1rem;
        background: #d4edda;
        color: #155724;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    
    .error-message {
        padding: 1rem;
        background: #f8d7da;
        color: #721c24;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
    }
    
    /* Info boxes */
    .info-box {
        background: #e7f3ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
        margin: 1rem 0;
    }
    
    /* Account details card */
    .detail-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        border: 1px solid #e0e0e0;
    }
    
    .detail-card:hover {
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    
    /* Header styling */
    .header-text {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 0.5rem 0;
    }
    
    /* Balance display */
    .balance-display {
        font-size: 2rem;
        font-weight: bold;
        color: #28a745;
        text-align: center;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
        border: 2px solid #28a745;
        margin: 1rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #6c757d;
        border-top: 1px solid #dee2e6;
        margin-top: 2rem;
    }
    
    /* Custom input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

class Bank:
    database = 'data.json'
    data = []
    
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            # Create empty database if doesn't exist
            with open(database, 'w') as fs:
                json.dump([], fs)
            data = []
    except Exception as err:
        st.error(f"Database error: {err}")
        data = []
        
    @classmethod
    def __Update(cls):
        try:
            with open(cls.database, 'w') as fs:
                json.dump(Bank.data, fs, indent=2)
            return True
        except Exception as e:
            st.error(f"Error updating database: {e}")
            return False
            
    @classmethod
    def __AccountGenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)
    
    @staticmethod
    def find_user(account_number, pin):
        try:
            pin = int(pin)
            for user in Bank.data:
                if user['account'] == account_number and user['pin'] == pin:
                    return user
            return None
        except (ValueError, TypeError):
            return None
    
    def CreateAccount(self, name, age, email, pin):
        if age < 18:
            return False, "Age must be 18 or above"
        if len(str(pin)) != 4:
            return False, "PIN must be exactly 4 digits"
        if any(user['email'] == email for user in Bank.data):
            return False, "Email already registered"
        
        account_number = Bank.__AccountGenerate()
        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account": account_number,
            "balance": 0
        }
        
        Bank.data.append(info)
        if Bank.__Update():
            return True, f"Account created successfully! Account Number: {account_number}"
        return False, "Error creating account"
    
    def DepositMoney(self, account_number, pin, amount):
        user = Bank.find_user(account_number, pin)
        if user is None:
            return False, "Invalid account number or PIN"
        if amount <= 0:
            return False, "Amount must be greater than 0"
        if amount > 10000:
            return False, "Maximum deposit limit is 10000"
        
        user['balance'] += amount
        if Bank.__Update():
            return True, f"Successfully deposited ${amount:.2f}. New balance: ${user['balance']:.2f}"
        return False, "Error processing deposit"
    
    def WithdrawMoney(self, account_number, pin, amount):
        user = Bank.find_user(account_number, pin)
        if user is None:
            return False, "Invalid account number or PIN"
        if amount <= 0:
            return False, "Amount must be greater than 0"
        if user['balance'] < amount:
            return False, f"Insufficient balance. Available: ${user['balance']:.2f}"
        
        user['balance'] -= amount
        if Bank.__Update():
            return True, f"Successfully withdrew ${amount:.2f}. New balance: ${user['balance']:.2f}"
        return False, "Error processing withdrawal"
    
    def ShowDetails(self, account_number, pin):
        user = Bank.find_user(account_number, pin)
        if user is None:
            return False, "Invalid account number or PIN"
        return True, user
    
    def UpdateDetails(self, account_number, pin, new_name=None, new_email=None, new_pin=None):
        user = Bank.find_user(account_number, pin)
        if user is None:
            return False, "Invalid account number or PIN"
        
        if new_name:
            user['name'] = new_name
        if new_email:
            user['email'] = new_email
        if new_pin:
            if len(str(new_pin)) == 4:
                user['pin'] = new_pin
            else:
                return False, "PIN must be 4 digits"
        
        if Bank.__Update():
            return True, "Details updated successfully"
        return False, "Error updating details"
    
    def Delete(self, account_number, pin):
        user = Bank.find_user(account_number, pin)
        if user is None:
            return False, "Invalid account number or PIN"
        
        Bank.data.remove(user)
        if Bank.__Update():
            return True, "Account deleted successfully"
        return False, "Error deleting account"

# Initialize Bank object
bank = Bank()

# Sidebar navigation
st.sidebar.image("https://img.icons8.com/color/96/000000/bank-building.png", width=80)
st.sidebar.title("🏦 Bank Management")
st.sidebar.markdown("---")

# Main navigation
menu = st.sidebar.radio(
    "Choose an option",
    ["🏠 Home", "📝 Create Account", "💰 Deposit", "💳 Withdraw", "👤 Account Details", "✏️ Update Account", "🗑️ Delete Account", "📊 Dashboard"]
)

st.sidebar.markdown("---")
st.sidebar.info("🔒 Your banking is secure with us")

# Main content area
if menu == "🏠 Home":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="header-text">Welcome to Bank Management System</h1>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### 🌟 Your Trusted Banking Partner")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        total_accounts = len(Bank.data)
        total_balance = sum(user['balance'] for user in Bank.data)
        avg_balance = total_balance / total_accounts if total_accounts > 0 else 0
        
        with col1:
            st.metric("Total Accounts", total_accounts)
        with col2:
            st.metric("Total Balance", f"${total_balance:,.2f}")
        with col3:
            st.metric("Average Balance", f"${avg_balance:,.2f}")
        with col4:
            st.metric("Active Users", total_accounts)
        
        st.markdown("---")
        st.markdown("### 🚀 Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Create New Account", use_container_width=True):
                st.success("Navigate to Create Account tab")
        with col2:
            if st.button("💰 Deposit Money", use_container_width=True):
                st.success("Navigate to Deposit tab")

elif menu == "📝 Create Account":
    st.markdown('<h1 class="header-text">📝 Create New Account</h1>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([1, 1])
        with col1:
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=1, max_value=120, step=1)
        with col2:
            email = st.text_input("Email Address")
            pin = st.text_input("Create 4-digit PIN", type="password", max_chars=4)
        
        if st.button("Create Account", use_container_width=True):
            if not name or not email or not pin:
                st.error("Please fill all fields")
            elif len(pin) != 4 or not pin.isdigit():
                st.error("PIN must be exactly 4 digits")
            else:
                success, message = bank.CreateAccount(name, age, email, int(pin))
                if success:
                    st.success(message)
                    st.balloons()
                else:
                    st.error(message)

elif menu == "💰 Deposit":
    st.markdown('<h1 class="header-text">💰 Deposit Money</h1>', unsafe_allow_html=True)
    
    with st.container():
        account = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        amount = st.number_input("Deposit Amount", min_value=0.01, step=1.0)
        
        if st.button("Deposit", use_container_width=True):
            if not account or not pin:
                st.error("Please fill all fields")
            else:
                success, message = bank.DepositMoney(account, int(pin), amount)
                if success:
                    st.success(message)
                    st.balloons()
                else:
                    st.error(message)

elif menu == "💳 Withdraw":
    st.markdown('<h1 class="header-text">💳 Withdraw Money</h1>', unsafe_allow_html=True)
    
    with st.container():
        account = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        amount = st.number_input("Withdraw Amount", min_value=0.01, step=1.0)
        
        if st.button("Withdraw", use_container_width=True):
            if not account or not pin:
                st.error("Please fill all fields")
            else:
                success, message = bank.WithdrawMoney(account, int(pin), amount)
                if success:
                    st.success(message)
                else:
                    st.error(message)

elif menu == "👤 Account Details":
    st.markdown('<h1 class="header-text">👤 Account Details</h1>', unsafe_allow_html=True)
    
    with st.container():
        account = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        
        if st.button("Show Details", use_container_width=True):
            if not account or not pin:
                st.error("Please fill all fields")
            else:
                success, result = bank.ShowDetails(account, int(pin))
                if success:
                    st.success("Account found!")
                    st.markdown("---")
                    
                    # Display user details in a nice format
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### 👤 Personal Information")
                        st.write(f"**Name:** {result['name']}")
                        st.write(f"**Age:** {result['age']}")
                        st.write(f"**Email:** {result['email']}")
                    with col2:
                        st.markdown("### 💰 Account Information")
                        st.write(f"**Account Number:** {result['account']}")
                        st.write(f"**Balance:** ${result['balance']:.2f}")
                    
                    # Balance card
                    if result['balance'] > 0:
                        st.markdown(f'<div class="balance-display">💰 Balance: ${result["balance"]:.2f}</div>', unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Your balance is zero")
                else:
                    st.error(result)

elif menu == "✏️ Update Account":
    st.markdown('<h1 class="header-text">✏️ Update Account Details</h1>', unsafe_allow_html=True)
    st.info("Leave fields empty if you don't want to change them")
    
    with st.container():
        account = st.text_input("Account Number")
        pin = st.text_input("Current PIN", type="password")
        st.markdown("---")
        st.markdown("### Update Fields (Optional)")
        new_name = st.text_input("New Name (optional)")
        new_email = st.text_input("New Email (optional)")
        new_pin = st.text_input("New PIN (optional)", type="password", max_chars=4)
        
        if st.button("Update Details", use_container_width=True):
            if not account or not pin:
                st.error("Account number and PIN are required")
            else:
                success, message = bank.UpdateDetails(
                    account, int(pin),
                    new_name if new_name else None,
                    new_email if new_email else None,
                    int(new_pin) if new_pin and new_pin.isdigit() else None
                )
                if success:
                    st.success(message)
                    st.balloons()
                else:
                    st.error(message)

elif menu == "🗑️ Delete Account":
    st.markdown('<h1 class="header-text">🗑️ Delete Account</h1>', unsafe_allow_html=True)
    st.warning("⚠️ This action cannot be undone! All your data will be permanently deleted.")
    
    with st.container():
        account = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        confirm = st.checkbox("I understand this action is irreversible")
        
        if st.button("Delete Account", use_container_width=True):
            if not account or not pin:
                st.error("Please fill all fields")
            elif not confirm:
                st.error("Please confirm that you understand the consequences")
            else:
                success, message = bank.Delete(account, int(pin))
                if success:
                    st.success(message)
                    st.balloons()
                else:
                    st.error(message)

elif menu == "📊 Dashboard":
    st.markdown('<h1 class="header-text">📊 Dashboard</h1>', unsafe_allow_html=True)
    
    if Bank.data:
        # Create DataFrame for display
        df = pd.DataFrame(Bank.data)
        
        # Show statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Accounts", len(df))
        with col2:
            st.metric("Total Balance", f"${df['balance'].sum():,.2f}")
        with col3:
            st.metric("Average Balance", f"${df['balance'].mean():,.2f}")
        
        st.markdown("---")
        st.markdown("### 📋 All Account Holders")
        
        # Display table with all users
        display_df = df[['name', 'age', 'email', 'account', 'balance']].copy()
        display_df['balance'] = display_df['balance'].apply(lambda x: f"${x:.2f}")
        
        # Add color to balance
        st.dataframe(display_df, use_container_width=True)
        
        # Show distribution
        st.markdown("---")
        st.markdown("### 📊 Account Balance Distribution")
        
        if len(df) > 0:
            # Create a bar chart of balances
            chart_data = df[['name', 'balance']].copy()
            chart_data = chart_data.sort_values('balance', ascending=False)
            st.bar_chart(chart_data.set_index('name'))
        
        # Show low balance accounts
        st.markdown("---")
        st.markdown("### ⚠️ Accounts with Low Balance (< $100)")
        low_balance = df[df['balance'] < 100]
        if len(low_balance) > 0:
            st.dataframe(low_balance[['name', 'account', 'balance']], use_container_width=True)
        else:
            st.success("All accounts have healthy balances! 🎉")
            
    else:
        st.info("No accounts in the system yet. Create your first account!")

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer">
        <p>🏦 Bank Management System | Secure Banking at Your Fingertips</p>
        <p style="font-size: 0.8rem;">© 2024 All rights reserved</p>
    </div>
""", unsafe_allow_html=True)