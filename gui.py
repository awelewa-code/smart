"""
Graphical user interface for the ATM system using Tkinter.

This module provides a GUI interface that uses the same ATMService layer
as the CLI, ensuring consistent behavior across interfaces.

Design Pattern: View (MVC)
- All UI code isolated here
- All operations delegated to ATMService
- No business logic in this module
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from typing import Optional, Callable
import threading

from .services import ATMService
from .database import ATMDatabase
from .config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, APP_NAME


class ATMGUI:
    """
    Graphical user interface for ATM operations using Tkinter.
    
    Provides login, account creation, and banking operation screens
    all using the shared ATMService business logic layer.
    """

    def __init__(self, root: tk.Tk, service: ATMService):
        """
        Initialize the GUI with a Tkinter root and service.
        
        Args:
            root: Tkinter root window
            service: ATMService instance for business logic
        """
        self.root = root
        self.service = service

        # Configure window
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        # Current frame reference
        self.current_frame: Optional[tk.Frame] = None

        # Start with login screen
        self.show_login_screen()

    # ========================================================================
    # HELPER METHODS FOR UI
    # ========================================================================

    def clear_window(self) -> None:
        """Clear all widgets from the window."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = None

    def create_frame(self) -> tk.Frame:
        """Create and return a new main frame."""
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame
        return frame

    def create_header(self, parent: tk.Frame, title: str) -> None:
        """Create a header section."""
        header = tk.Frame(parent, bg="#2c3e50", height=60)
        header.pack(fill=tk.X, pady=(0, 20))

        label = tk.Label(
            header,
            text=title,
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        label.pack(pady=15)

    def create_label_entry(
        self,
        parent: tk.Frame,
        label_text: str,
        is_password: bool = False
    ) -> tk.Entry:
        """Create a label with an entry field."""
        label = tk.Label(parent, text=label_text, font=("Arial", 10), bg="#f0f0f0")
        label.pack(anchor=tk.W, padx=30, pady=(10, 5))

        entry = tk.Entry(parent, font=("Arial", 11), width=30)
        if is_password:
            entry.config(show="•")
        entry.pack(padx=30, pady=5)

        return entry

    def create_button(
        self,
        parent: tk.Frame,
        text: str,
        command: Callable,
        bg_color: str = "#3498db",
        fg_color: str = "white"
    ) -> tk.Button:
        """Create a styled button."""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 11, "bold"),
            bg=bg_color,
            fg=fg_color,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        return button

    def show_info(self, title: str, message: str) -> None:
        """Show an information message box."""
        messagebox.showinfo(title, message)

    def show_error(self, title: str, message: str) -> None:
        """Show an error message box."""
        messagebox.showerror(title, message)

    def show_success(self, title: str, message: str) -> None:
        """Show a success message box."""
        messagebox.showinfo(title, message)

    # ========================================================================
    # LOGIN AND REGISTRATION SCREENS
    # ========================================================================

    def show_login_screen(self) -> None:
        """Display the login screen."""
        self.clear_window()
        frame = self.create_frame()

        self.create_header(frame, f"{APP_NAME} - Login")

        # Username
        username_entry = self.create_label_entry(frame, "Username:")

        # PIN
        pin_entry = self.create_label_entry(frame, "PIN:", is_password=True)

        # Buttons
        button_frame = tk.Frame(frame, bg="#f0f0f0")
        button_frame.pack(pady=20)

        login_btn = self.create_button(
            button_frame,
            "Login",
            lambda: self.handle_login(username_entry.get(), pin_entry.get())
        )
        login_btn.pack(side=tk.LEFT, padx=10)

        register_btn = self.create_button(
            button_frame,
            "Register",
            self.show_register_screen,
            bg_color="#27ae60"
        )
        register_btn.pack(side=tk.LEFT, padx=10)

        exit_btn = self.create_button(
            button_frame,
            "Exit",
            self.root.quit,
            bg_color="#e74c3c"
        )
        exit_btn.pack(side=tk.LEFT, padx=10)

        # Focus on username field
        username_entry.focus()

    def show_register_screen(self) -> None:
        """Display the account registration screen."""
        self.clear_window()
        frame = self.create_frame()

        self.create_header(frame, f"{APP_NAME} - Create Account")

        # Username
        username_entry = self.create_label_entry(frame, "Username (min 3 characters):")

        # PIN
        pin_entry = self.create_label_entry(frame, "PIN (4 digits):", is_password=True)

        # PIN Confirm
        pin_confirm_entry = self.create_label_entry(frame, "Confirm PIN:", is_password=True)

        # Buttons
        button_frame = tk.Frame(frame, bg="#f0f0f0")
        button_frame.pack(pady=20)

        register_btn = self.create_button(
            button_frame,
            "Create Account",
            lambda: self.handle_create_account(
                username_entry.get(),
                pin_entry.get(),
                pin_confirm_entry.get()
            ),
            bg_color="#27ae60"
        )
        register_btn.pack(side=tk.LEFT, padx=10)

        back_btn = self.create_button(
            button_frame,
            "Back",
            self.show_login_screen,
            bg_color="#95a5a6"
        )
        back_btn.pack(side=tk.LEFT, padx=10)

        username_entry.focus()

    def handle_login(self, username: str, pin: str) -> None:
        """Handle login button click."""
        success, message = self.service.authenticate(username, pin)

        if success:
            self.show_success("Login", message)
            self.show_dashboard()
        else:
            self.show_error("Login Failed", message)

    def handle_create_account(self, username: str, pin: str, pin_confirm: str) -> None:
        """Handle account creation."""
        if pin != pin_confirm:
            self.show_error("Error", "PINs do not match")
            return

        success, message = self.service.create_account(username, pin)

        if success:
            self.show_success("Account Created", message)
            self.show_login_screen()
        else:
            self.show_error("Creation Failed", message)

    # ========================================================================
    # DASHBOARD AND OPERATIONS
    # ========================================================================

    def show_dashboard(self) -> None:
        """Display the main dashboard after login."""
        self.clear_window()
        frame = self.create_frame()

        username = self.service.get_current_username()
        self.create_header(frame, f"Welcome, {username}")

        # Balance display
        success, balance, _ = self.service.get_balance()
        balance_frame = tk.Frame(frame, bg="white", relief=tk.RAISED, bd=2)
        balance_frame.pack(fill=tk.X, padx=20, pady=10)

        balance_label = tk.Label(
            balance_frame,
            text="Current Balance",
            font=("Arial", 12),
            bg="white"
        )
        balance_label.pack(pady=5)

        balance_amount = tk.Label(
            balance_frame,
            text=f"${balance:.2f}",
            font=("Arial", 24, "bold"),
            fg="#27ae60",
            bg="white"
        )
        balance_amount.pack(pady=10)

        # Action buttons
        button_frame = tk.Frame(frame, bg="#f0f0f0")
        button_frame.pack(pady=20)

        deposit_btn = self.create_button(
            button_frame,
            "Deposit",
            self.show_deposit_screen,
            bg_color="#3498db"
        )
        deposit_btn.pack(pady=5, fill=tk.X, padx=30)

        withdraw_btn = self.create_button(
            button_frame,
            "Withdraw",
            self.show_withdraw_screen,
            bg_color="#e67e22"
        )
        withdraw_btn.pack(pady=5, fill=tk.X, padx=30)

        history_btn = self.create_button(
            button_frame,
            "Transaction History",
            self.show_transaction_history,
            bg_color="#9b59b6"
        )
        history_btn.pack(pady=5, fill=tk.X, padx=30)

        logout_btn = self.create_button(
            button_frame,
            "Logout",
            self.handle_logout,
            bg_color="#e74c3c"
        )
        logout_btn.pack(pady=5, fill=tk.X, padx=30)

    def show_deposit_screen(self) -> None:
        """Display the deposit screen."""
        self.clear_window()
        frame = self.create_frame()

        self.create_header(frame, "Deposit Funds")

        amount_entry = self.create_label_entry(frame, "Amount to Deposit: $")

        button_frame = tk.Frame(frame, bg="#f0f0f0")
        button_frame.pack(pady=20)

        deposit_btn = self.create_button(
            button_frame,
            "Confirm Deposit",
            lambda: self.handle_deposit(amount_entry.get()),
            bg_color="#27ae60"
        )
        deposit_btn.pack(side=tk.LEFT, padx=10)

        back_btn = self.create_button(
            button_frame,
            "Cancel",
            self.show_dashboard,
            bg_color="#95a5a6"
        )
        back_btn.pack(side=tk.LEFT, padx=10)

        amount_entry.focus()

    def handle_deposit(self, amount: str) -> None:
        """Handle deposit operation."""
        try:
            amount_float = float(amount)
            success, message = self.service.deposit(amount_float)

            if success:
                self.show_success("Deposit", message)
                self.show_dashboard()
            else:
                self.show_error("Deposit Failed", message)

        except ValueError:
            self.show_error("Invalid Input", "Please enter a valid amount")

    def show_withdraw_screen(self) -> None:
        """Display the withdrawal screen."""
        self.clear_window()
        frame = self.create_frame()

        self.create_header(frame, "Withdraw Funds")

        amount_entry = self.create_label_entry(frame, "Amount to Withdraw: $")

        button_frame = tk.Frame(frame, bg="#f0f0f0")
        button_frame.pack(pady=20)

        withdraw_btn = self.create_button(
            button_frame,
            "Confirm Withdrawal",
            lambda: self.handle_withdraw(amount_entry.get()),
            bg_color="#e67e22"
        )
        withdraw_btn.pack(side=tk.LEFT, padx=10)

        back_btn = self.create_button(
            button_frame,
            "Cancel",
            self.show_dashboard,
            bg_color="#95a5a6"
        )
        back_btn.pack(side=tk.LEFT, padx=10)

        amount_entry.focus()

    def handle_withdraw(self, amount: str) -> None:
        """Handle withdrawal operation."""
        try:
            amount_float = float(amount)
            success, message = self.service.withdraw(amount_float)

            if success:
                self.show_success("Withdrawal", message)
                self.show_dashboard()
            else:
                self.show_error("Withdrawal Failed", message)

        except ValueError:
            self.show_error("Invalid Input", "Please enter a valid amount")

    def show_transaction_history(self) -> None:
        """Display transaction history."""
        self.clear_window()
        frame = self.create_frame()

        self.create_header(frame, "Transaction History")

        # Get history
        success, transactions, message = self.service.get_transaction_history()

        # Text widget for displaying history
        text_widget = scrolledtext.ScrolledText(
            frame,
            font=("Courier", 9),
            bg="white",
            fg="#333",
            height=15,
            width=60
        )
        text_widget.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        if not transactions:
            text_widget.insert(tk.END, message)
        else:
            # Format and display transactions
            header = f"{'Date/Time':<25} {'Type':<12} {'Amount':<15} {'Balance':<12}\n"
            header += "-" * 70 + "\n"
            text_widget.insert(tk.END, header)

            for txn in transactions:
                dt = txn.timestamp.split('T')[0] + ' ' + txn.timestamp.split('T')[1][:8]
                line = f"{dt:<25} {txn.transaction_type:<12} ${txn.amount:>10.2f}   ${txn.balance_after:>10.2f}\n"
                text_widget.insert(tk.END, line)

        text_widget.config(state=tk.DISABLED)

        # Back button
        button_frame = tk.Frame(frame, bg="#f0f0f0")
        button_frame.pack(pady=10)

        back_btn = self.create_button(
            button_frame,
            "Back to Dashboard",
            self.show_dashboard,
            bg_color="#95a5a6"
        )
        back_btn.pack()

    def handle_logout(self) -> None:
        """Handle logout button click."""
        success, message = self.service.logout()
        if success:
            self.show_success("Logout", message)
            self.show_login_screen()


def run_gui() -> None:
    """
    Initialize and run the GUI application.
    
    This is the entry point for graphical mode.
    """
    db = ATMDatabase()
    service = ATMService(db)

    root = tk.Tk()
    gui = ATMGUI(root, service)

    root.mainloop()
