from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle

CENT = Decimal("0.01")


def money(value):
    return f"${value.quantize(CENT, rounding=ROUND_HALF_UP):,.2f}"


def calculate_paycheck(gross_pay):
    """Calculate an estimate using the user's supplied assumptions."""
    gross_pay = Decimal(str(gross_pay))
    social_security = gross_pay * Decimal("0.062")
    medicare = gross_pay * Decimal("0.0145")
    pa_state = gross_pay * Decimal("0.0307")
    warrington_local = gross_pay * Decimal("0.0125")
    pa_sui = gross_pay * Decimal("0.0007")
    silver_spring_lst = Decimal("2.00")

    biweekly_standard_deduction = Decimal("619.20")
    taxable_federal_income = max(
        Decimal("0"), gross_pay - biweekly_standard_deduction
    )
    bracket_1_limit = Decimal("476.70")

    if taxable_federal_income <= 0:
        federal_tax = Decimal("0")
    elif taxable_federal_income <= bracket_1_limit:
        federal_tax = taxable_federal_income * Decimal("0.10")
    else:
        federal_tax = (
            bracket_1_limit * Decimal("0.10")
            + (taxable_federal_income - bracket_1_limit) * Decimal("0.12")
        )

    taxes = [
        ("Federal income tax", federal_tax),
        ("Social Security", social_security),
        ("Medicare", medicare),
        ("Pennsylvania state tax", pa_state),
        ("Warrington local tax", warrington_local),
        ("PA unemployment (SUI)", pa_sui),
        ("Silver Spring LST", silver_spring_lst),
    ]
    total_taxes = sum((amount for _, amount in taxes), Decimal("0"))
    net_pay = gross_pay - total_taxes
    return taxes, total_taxes, net_pay


class PaycheckCalculator(App):
    def build(self):
        self.title = "Paycheck Calculator"
        self.bg = get_color_from_hex("#101820")
        self.card = get_color_from_hex("#1B2835")
        self.accent = get_color_from_hex("#55D6BE")
        self.text_color = get_color_from_hex("#F4F7FA")
        self.muted = get_color_from_hex("#AAB8C5")

        root = BoxLayout(
            orientation="vertical", padding=dp(20), spacing=dp(12)
        )
        with root.canvas.before:
            Color(*self.bg)
            self.background = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._update_bg, size=self._update_bg)

        scroll = ScrollView(do_scroll_x=False)
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None,
            padding=(0, dp(4), 0, dp(18)),
        )
        content.bind(minimum_height=content.setter("height"))

        content.add_widget(
            self.label("PAYCHECK ESTIMATOR", 22, True, self.accent)
        )
        content.add_widget(
            self.label(
                "Enter your gross biweekly pay to estimate take-home pay.",
                14, False, self.muted
            )
        )
        content.add_widget(
            self.label("Gross pay ($)", 15, True, self.text_color)
        )

        self.gross_input = TextInput(
            hint_text="e.g. 900.00",
            multiline=False,
            input_filter="float",
            font_size=dp(22),
            size_hint_y=None,
            height=dp(58),
            padding=(dp(14), dp(15)),
            background_normal="",
            background_active="",
            background_color=self.card,
            foreground_color=self.text_color,
            cursor_color=self.accent,
            hint_text_color=self.muted,
        )
        content.add_widget(self.gross_input)

        calculate_button = Button(
            text="CALCULATE TAKE-HOME PAY",
            size_hint_y=None,
            height=dp(54),
            font_size=dp(15),
            bold=True,
            background_normal="",
            background_color=self.accent,
            color=get_color_from_hex("#101820"),
        )
        calculate_button.bind(on_release=self.calculate)
        content.add_widget(calculate_button)

        self.result_label = self.label(
            "Your net pay will appear here.", 18, True, self.text_color
        )
        content.add_widget(self.result_label)

        self.breakdown = BoxLayout(
            orientation="vertical",
            spacing=dp(7),
            size_hint_y=None,
            padding=(dp(14), dp(14)),
        )
        self.breakdown.bind(minimum_height=self.breakdown.setter("height"))
        content.add_widget(self.breakdown)

        content.add_widget(
            self.label(
                "Estimate only. This uses configured tax rates, local "
                "deductions, and a simplified federal withholding formula. "
                "Actual payroll withholding may differ. Check the assumptions "
                "against your current pay stub before relying on the result.",
                12, False, self.muted
            )
        )
        scroll.add_widget(content)
        root.add_widget(scroll)
        return root

    def _update_bg(self, widget, _value):
        self.background.pos = widget.pos
        self.background.size = widget.size

    def label(self, text, size=14, bold=False, color=None):
        widget = Label(
            text=text,
            font_size=dp(size),
            bold=bold,
            color=color or self.text_color,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(max(30, size * 2.0)),
        )
        widget.bind(
            width=lambda obj, width: setattr(obj, "text_size", (width, None))
        )
        return widget

    def calculate(self, _button):
        raw = self.gross_input.text.strip().replace(",", "").replace("$", "")
        try:
            gross = Decimal(raw)
            if not gross.is_finite() or gross < 0:
                raise InvalidOperation
        except (InvalidOperation, ValueError):
            self.result_label.text = "Enter a valid gross pay amount."
            self.breakdown.clear_widgets()
            return

        taxes, total_taxes, net_pay = calculate_paycheck(gross)
        self.result_label.text = f"ESTIMATED TAKE-HOME\n{money(net_pay)}"
        self.result_label.color = self.accent
        self.breakdown.clear_widgets()
        self.breakdown.add_widget(
            self.label("DEDUCTION BREAKDOWN", 15, True, self.accent)
        )
        self.add_row("Gross pay", gross, strong=True)
        for name, amount in taxes:
            self.add_row(name, amount)
        self.add_row("Total deductions", total_taxes, strong=True)
        self.add_row("NET PAY", net_pay, strong=True, highlight=True)

    def add_row(self, name, amount, strong=False, highlight=False):
        row = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(8))
        color = self.accent if highlight else self.text_color
        name_label = Label(
            text=name, font_size=dp(13), bold=strong, color=color,
            halign="left", valign="middle", size_hint_x=0.68
        )
        name_label.bind(size=lambda obj, size: setattr(obj, "text_size", size))
        amount_label = Label(
            text=money(amount), font_size=dp(13), bold=strong, color=color,
            halign="right", valign="middle", size_hint_x=0.32
        )
        amount_label.bind(
            size=lambda obj, size: setattr(obj, "text_size", size)
        )
        row.add_widget(name_label)
        row.add_widget(amount_label)
        self.breakdown.add_widget(row)


if __name__ == "__main__":
    PaycheckCalculator().run()
