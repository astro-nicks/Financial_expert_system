% Allow Prolog to modify these facts dynamically
:- dynamic income/2, expenses/2, savings/2, essential_expenses/2, non_essential_expenses/2.

% Rule: Check if the user is overspending
overspending(User) :-
    income(User, Income),
    expenses(User, Expenses),
    Expenses > Income.

% Rule: Suggest savings strategy (should save at least 20% of income)
should_save_more(User) :-
    income(User, Income),
    savings(User, Savings),
    Savings < 0.2 * Income.

% Rule: Check if essential expenses exceed 50% of income
high_essential_spending(User) :-
    income(User, Income),
    essential_expenses(User, Essentials),
    Essentials > 0.5 * Income.

% Rule: Emergency fund check (should be at least 3 months of essential expenses)
needs_emergency_fund(User) :-
    essential_expenses(User, Essentials),
    savings(User, Savings),
    Savings < 3 * Essentials.

% Rule: Identify if non-essential expenses are too high (more than 30% of income)
high_non_essential_spending(User) :-
    income(User, Income),
    non_essential_expenses(User, NonEssentials),
    NonEssentials > 0.3 * Income.
