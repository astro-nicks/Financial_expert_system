:- dynamic income/2, expenses/2, savings/2, debt/2, essential_expenses/2, non_essential_expenses/2, investments/2, passive_income/2.


% Your facts and rules go here


% Facts (Initial data)
% income(UserID, Amount), expenses(UserID, Amount), savings(UserID, Amount), debt(UserID, Amount)
% essential_expenses(UserID, Amount), non_essential_expenses(UserID, Amount), investments(UserID, Amount), passive_income(UserID, Amount)

% Example users (static data to start with)
income(101, 5000).
income(102, 7000).
income(103, 4000).

expenses(101, 3000).
expenses(102, 4000).
expenses(103, 3500).

savings(101, 500).
savings(102, 1000).
savings(103, 200).

debt(101, 2000).
debt(102, 1000).
debt(103, 5000).

% Dynamic advice based on user data
budget_advice(UserID, Advice) :-
    income(UserID, Income),
    expenses(UserID, Expenses),
    Balance is Income - Expenses,
    (   Balance < 500 -> Advice = 'Your budget is unbalanced. Reduce unnecessary expenses.'
    ;   Balance >= 500, Balance < 1500 -> Advice = 'Your budget is stable. Consider increasing your savings.'
    ;   Balance >= 1500 -> Advice = 'Great budgeting! Consider investing excess funds.'
    ).

savings_advice(UserID, Advice) :-
    income(UserID, Income),
    savings(UserID, Savings),
    SavingsRate is (Savings / Income) * 100,
    (   SavingsRate < 10 -> Advice = 'Increase your savings. Aim for at least 20% of income.'
    ;   SavingsRate >= 10, SavingsRate < 30 -> Advice = 'Good savings habit. Try to increase it gradually.'
    ;   SavingsRate >= 30 -> Advice = 'Excellent savings strategy! Consider investment options.'
    ).

expense_category(UserID, Category) :-
    expenses(UserID, Expenses),
    (   Expenses < 2000 -> Category = 'Low'
    ;   Expenses >= 2000, Expenses < 4000 -> Category = 'Moderate'
    ;   Expenses >= 4000 -> Category = 'High'
    ).

debt_management(UserID, Advice) :-
    income(UserID, Income),
    debt(UserID, Debt),
    DebtToIncomeRatio is (Debt / Income) * 100,
    (   DebtToIncomeRatio > 40 -> Advice = 'Your debt level is high. Consider debt repayment strategies.'
    ;   DebtToIncomeRatio >= 20, DebtToIncomeRatio =< 40 -> Advice = 'Your debt is manageable, but reducing it will improve financial health.'
    ;   DebtToIncomeRatio < 20 -> Advice = 'Your debt level is low. Keep managing it well.'
    ).

investment_advice(UserID, Advice) :-
    savings(UserID, Savings),
    calculate_risk_level(UserID, RiskLevel),
    (   Savings > 3000, RiskLevel = low -> Advice = 'Consider investing in low-risk assets like bonds or index funds.'
    ;   Savings > 3000, RiskLevel = medium -> Advice = 'You can explore a balanced investment portfolio with moderate risk.'
    ;   Savings > 3000, RiskLevel = high -> Advice = 'Consider high-risk, high-reward investments like stocks or real estate.'
    ;   Savings =< 3000 -> Advice = 'Increase your savings before considering investments.'
    ).



% ✅ Fixed Risk Level Calculation (ONLY ONE DEFINITION)
calculate_risk_level(UserID, RiskLevel) :-
    income(UserID, Income),
    debt(UserID, Debt),
    savings(UserID, Savings),
    Income > 0,
    DebtToIncomeRatio is (Debt / Income) * 100,
    SavingsRate is (Savings / Income) * 100,
    (   DebtToIncomeRatio > 40
    ->  RiskLevel = 'You have a high risk level and unfortunately can not apply for a loan'
    ;   DebtToIncomeRatio >= 20, DebtToIncomeRatio =< 40, SavingsRate < 15
    ->  RiskLevel = 'You have a medium risk level and so you are eligible to apply for the loan with some restrictions'
    ;   DebtToIncomeRatio < 20, SavingsRate >= 15
    ->  RiskLevel = 'You have a low risk value and so are eligible to appply for the loan'
    ;   RiskLevel = low   % Default case
    ).


% ✅ Fixed Credit Score Calculation
credit_score(UserID, Score) :-
    income(UserID, Income),
    savings(UserID, Savings),
    debt(UserID, Debt),
    Income > 0,
    DebtToIncomeRatio is (Debt / Income) * 100,
    SavingsRate is (Savings / Income) * 100,
    (   DebtToIncomeRatio < 20, SavingsRate > 15 -> Score = 'Excellent credit score. You can apply for a loan'
    ;   DebtToIncomeRatio >= 20, DebtToIncomeRatio =< 40, SavingsRate >= 10 -> Score = 'Good credit score, but could be improved.'
    ;   Score = 'Credit score needs improvement.'
    ).


% ✅ Loan Eligibility Check
loan_eligibility(UserID, Eligibility) :-
    income(UserID, Income),
    debt(UserID, Debt),
    Income > 0, % Ensure income is nonzero
    DebtToIncomeRatio is (Debt / Income) * 100,
    (   DebtToIncomeRatio < 30 -> Eligibility = 'Eligible for loan with good interest rates.'
    ;   DebtToIncomeRatio >= 30, DebtToIncomeRatio =< 50 -> Eligibility = 'Eligible for loan but may get higher interest rates.'
    ;   Eligibility = 'Not recommended for a loan due to high debt burden.'
    ).


% Investment Advice Based on Risk Level and Savings
investment_advice(UserID, Advice) :-
    savings(UserID, Savings),
    income(UserID, Income),
    calculate_risk_level(UserID, RiskLevel),
    (   Savings < 2000
    ->  Advice = 'Increase savings before making investments.'
    ;   RiskLevel = high
    ->  Advice = 'Stick to low-risk investments like bonds and savings accounts.'
    ;   RiskLevel = medium, Savings >= 5000
    ->  Advice = 'Diversify with stocks, ETFs, and mutual funds.'
    ;   RiskLevel = low, Savings >= 10000
    ->  Advice = 'Consider high-return investments like real estate or venture capital.'
    ;   Advice = 'Review your financial goals before investing.'
    ).

% Passive Income Options
passive_income_options(UserID, Option) :-
    savings(UserID, Savings),
    calculate_risk_level(UserID, RiskLevel),
    (   Savings < 2000
    ->  Option = 'Save more before considering passive income strategies.'
    ;   RiskLevel = high
    ->  Option = 'Consider dividend stocks, rental property, or online businesses.'
    ;   RiskLevel = medium
    ->  Option = 'Explore REITs, affiliate marketing, or automated side businesses.'
    ;   RiskLevel = low
    ->  Option = 'You can invest in high-risk options like crypto or startup funding.'
    ).

% Investment Diversification Strategy
investment_diversification(UserID, Strategy) :-
    savings(UserID, Savings),
    calculate_risk_level(UserID, RiskLevel),
    (   Savings < 5000
    ->  Strategy = 'Build an emergency fund before diversifying.'
    ;   RiskLevel = high
    ->  Strategy = 'Allocate 70% to safe assets (bonds, deposits) and 30% to moderate-risk investments.'
    ;   RiskLevel = medium
    ->  Strategy = 'Split 50% in stocks, 30% in real estate, and 20% in bonds.'
    ;   RiskLevel = low
    ->  Strategy = 'You can afford high-risk investments like IPOs, cryptocurrency, and hedge funds.'
    ).
