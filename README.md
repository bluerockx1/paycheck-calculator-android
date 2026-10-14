# Paycheck Calculator for Android

A small Android paycheck estimator built with Python and Kivy. GitHub Actions builds a debug APK automatically when code is pushed to `main`, or when the workflow is run manually.

## Features

- Enter gross biweekly pay.
- See estimated take-home pay and an itemized deduction breakdown.
- Builds an Android debug APK using GitHub Actions.

## Build and download

1. Open the repository's **Actions** tab.
2. Select **Build Android APK**.
3. If there is no completed run, open **Run workflow** and start one.
4. Open a successful run and download **paycheck-calculator-debug-apk** under Artifacts.
5. Extract the ZIP and install the APK on your Android phone. You may need to allow installation from your browser or file manager.

The artifact is a debug APK, not a Play Store release. GitHub retains it for 14 days.

## Calculation assumptions

The app preserves the supplied calculation model:

- Social Security: 6.2%
- Medicare: 1.45%
- Pennsylvania state tax: 3.07%
- Local tax: 1.25%, labeled Warrington local tax
- Pennsylvania SUI: 0.07%
- Silver Spring LST: $2.00 per paycheck
- Federal taxable income: gross pay less a $619.20 biweekly deduction, floored at zero
- Federal calculation: 10% on the first $476.70 of the calculated taxable amount, then 12% on the remainder

**Important:** This is a user-configured estimate, not authoritative payroll or tax advice. In particular, local tax labels/rates, the local services tax, the federal deduction, and the federal brackets may not match an individual's actual withholding. Verify them against a current pay stub and official guidance before relying on the estimate.
