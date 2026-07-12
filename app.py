# ============================================================
# AI SALES DEAL GUIDANCE & PROFITABILITY COPILOT
# Streamlit MVP
# ============================================================

import streamlit as st


# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="AI Sales Deal Copilot",
    page_icon="🤖",
    layout="wide"
)


# ------------------------------------------------------------
# BUSINESS POLICIES
# ------------------------------------------------------------
# These are simulated policies created for the demo.
# They are not official Siemens policies.

GLOBAL_MAX_DISCOUNT = 25

REGIONAL_DISCOUNT_LIMITS = {
    "North America": 25,
    "Europe": 18,
    "Asia Pacific": 20
}

MINIMUM_PROFIT_MARGIN = 20


# ------------------------------------------------------------
# INPUT VALIDATION
# ------------------------------------------------------------

def validate_inputs(
    customer_name: str,
    list_price: float,
    discount: float,
    estimated_cost: float
) -> list:
    """
    Validate the basic deal inputs.

    Returns:
        A list of validation errors.
    """

    errors = []

    if not customer_name.strip():
        errors.append("Customer name cannot be empty.")

    if list_price <= 0:
        errors.append("List price must be greater than zero.")

    if discount < 0 or discount > 100:
        errors.append("Discount must be between 0% and 100%.")

    if estimated_cost < 0:
        errors.append("Estimated cost cannot be negative.")

    return errors


# ------------------------------------------------------------
# APPROVAL CALCULATION
# ------------------------------------------------------------

def get_approval_level(discount: float) -> str:
    """
    Determine the required approval based on discount.
    """

    if discount <= 10:
        return "No additional approval required"

    if discount <= 15:
        return "Sales Manager approval required"

    if discount <= 25:
        return "Sales Director approval required"

    return "VP and Pricing Committee approval required"


# ------------------------------------------------------------
# PROFITABILITY CALCULATION
# ------------------------------------------------------------

def calculate_profitability(
    list_price: float,
    discount: float,
    estimated_cost: float
) -> dict:
    """
    Calculate selling price, profit, and profit margin.
    """

    discount_amount = list_price * (discount / 100)

    final_selling_price = list_price - discount_amount

    expected_profit = final_selling_price - estimated_cost

    if final_selling_price > 0:
        profit_margin = (
            expected_profit / final_selling_price
        ) * 100
    else:
        profit_margin = 0

    return {
        "discount_amount": round(discount_amount, 2),
        "final_selling_price": round(final_selling_price, 2),
        "expected_profit": round(expected_profit, 2),
        "profit_margin": round(profit_margin, 2)
    }


# ------------------------------------------------------------
# POLICY COMPLIANCE
# ------------------------------------------------------------

def check_policy_compliance(
    region: str,
    discount: float
) -> dict:
    """
    Compare the proposed discount with regional and global limits.
    """

    regional_limit = REGIONAL_DISCOUNT_LIMITS.get(
        region,
        GLOBAL_MAX_DISCOUNT
    )

    issues = []

    if discount > regional_limit:
        issues.append(
            f"The proposed discount of {discount:.1f}% exceeds "
            f"the {region} regional limit of {regional_limit}%."
        )

    if discount > GLOBAL_MAX_DISCOUNT:
        issues.append(
            f"The proposed discount of {discount:.1f}% exceeds "
            f"the global limit of {GLOBAL_MAX_DISCOUNT}%."
        )

    if issues:
        status = "Exception or Adjustment Required"
    else:
        status = "Policy Compliant"

    return {
        "status": status,
        "regional_limit": regional_limit,
        "global_limit": GLOBAL_MAX_DISCOUNT,
        "issues": issues
    }


# ------------------------------------------------------------
# MARGIN EVALUATION
# ------------------------------------------------------------

def evaluate_margin(profit_margin: float) -> dict:
    """
    Evaluate whether the resulting profit margin is healthy.
    """

    if profit_margin >= MINIMUM_PROFIT_MARGIN:
        return {
            "status": "Healthy Margin",
            "message": (
                f"The expected profit margin is {profit_margin:.2f}%, "
                f"which meets the minimum preferred margin of "
                f"{MINIMUM_PROFIT_MARGIN}%."
            )
        }

    if profit_margin > 0:
        return {
            "status": "Low Margin",
            "message": (
                f"The expected profit margin is {profit_margin:.2f}%, "
                f"which is below the minimum preferred margin of "
                f"{MINIMUM_PROFIT_MARGIN}%."
            )
        }

    return {
        "status": "Unprofitable Deal",
        "message": (
            "The estimated cost is equal to or greater than "
            "the final selling price."
        )
    }


# ------------------------------------------------------------
# RECOMMENDATION GENERATION
# ------------------------------------------------------------

def generate_recommendation(
    policy_status: str,
    margin_status: str,
    approval: str
) -> str:
    """
    Generate the Copilot's recommended next action.
    """

    recommendations = []

    if policy_status == "Policy Compliant":
        recommendations.append(
            "The proposed discount complies with the applicable "
            "regional and global pricing policies."
        )
    else:
        recommendations.append(
            "Reduce the discount or submit a pricing exception request."
        )

    if margin_status == "Healthy Margin":
        recommendations.append(
            "The expected profit margin remains financially healthy."
        )

    elif margin_status == "Low Margin":
        recommendations.append(
            "Review the discount or estimated delivery cost before "
            "submitting the deal."
        )

    else:
        recommendations.append(
            "The deal should not proceed without pricing or cost changes."
        )

    recommendations.append(
        f"Approval guidance: {approval}."
    )

    return " ".join(recommendations)


# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

st.title("🤖 AI Sales Deal Guidance & Profitability Copilot")

st.write(
    "This initial MVP evaluates sales pricing, discount-policy "
    "compliance, expected profitability, approval requirements, "
    "and recommended next actions."
)

st.info(
    "This is an independent prototype using simulated sales data "
    "and business rules. It is not an official Siemens product."
)


# ------------------------------------------------------------
# INPUT FORM
# ------------------------------------------------------------

st.subheader("Enter Sales Deal Information")

left_column, right_column = st.columns(2)

with left_column:
    customer_name = st.text_input(
        "Customer Name",
        value="ABC Manufacturing"
    )

    product = st.selectbox(
        "Product",
        [
            "Teamcenter",
            "NX",
            "Simcenter",
            "Polarion",
            "Opcenter"
        ]
    )

    region = st.selectbox(
        "Customer Region",
        [
            "North America",
            "Europe",
            "Asia Pacific"
        ]
    )

with right_column:
    list_price = st.number_input(
        "List Price ($)",
        min_value=0.0,
        value=100000.0,
        step=1000.0
    )

    discount = st.slider(
        "Proposed Discount (%)",
        min_value=0,
        max_value=50,
        value=20
    )

    estimated_cost = st.number_input(
        "Estimated Delivery Cost ($)",
        min_value=0.0,
        value=62000.0,
        step=1000.0
    )


# ------------------------------------------------------------
# ANALYZE BUTTON
# ------------------------------------------------------------

if st.button(
    "Analyze Deal",
    type="primary",
    use_container_width=True
):

    validation_errors = validate_inputs(
        customer_name,
        list_price,
        discount,
        estimated_cost
    )

    if validation_errors:
        for error in validation_errors:
            st.error(error)

    else:
        profitability = calculate_profitability(
            list_price,
            discount,
            estimated_cost
        )

        policy_result = check_policy_compliance(
            region,
            discount
        )

        approval = get_approval_level(discount)

        margin_result = evaluate_margin(
            profitability["profit_margin"]
        )

        recommendation = generate_recommendation(
            policy_result["status"],
            margin_result["status"],
            approval
        )

        st.divider()

        st.subheader("Deal Analysis Results")

        metric1, metric2, metric3, metric4 = st.columns(4)

        metric1.metric(
            "Final Selling Price",
            f"${profitability['final_selling_price']:,.2f}"
        )

        metric2.metric(
            "Expected Profit",
            f"${profitability['expected_profit']:,.2f}"
        )

        metric3.metric(
            "Profit Margin",
            f"{profitability['profit_margin']:.2f}%"
        )

        metric4.metric(
            "Discount Amount",
            f"${profitability['discount_amount']:,.2f}"
        )

        st.subheader("Policy and Approval Analysis")

        policy_column, approval_column = st.columns(2)

        with policy_column:
            if policy_result["status"] == "Policy Compliant":
                st.success(
                    f"Policy Status: {policy_result['status']}"
                )
            else:
                st.warning(
                    f"Policy Status: {policy_result['status']}"
                )

            st.write(
                f"**Regional Discount Limit:** "
                f"{policy_result['regional_limit']}%"
            )

            st.write(
                f"**Global Discount Limit:** "
                f"{policy_result['global_limit']}%"
            )

        with approval_column:
            st.write(
                f"**Required Approval:** {approval}"
            )

            if margin_result["status"] == "Healthy Margin":
                st.success(
                    f"Margin Status: {margin_result['status']}"
                )

            elif margin_result["status"] == "Low Margin":
                st.warning(
                    f"Margin Status: {margin_result['status']}"
                )

            else:
                st.error(
                    f"Margin Status: {margin_result['status']}"
                )

            st.write(
                f"**Minimum Preferred Margin:** "
                f"{MINIMUM_PROFIT_MARGIN}%"
            )

        if policy_result["issues"]:
            st.subheader("Policy Issues")

            for issue in policy_result["issues"]:
                st.warning(issue)

        st.subheader("Profitability Assessment")

        st.write(margin_result["message"])

        st.subheader("Copilot Recommendation")

        st.info(recommendation)

        with st.expander("View Complete Deal Summary"):
            st.write(f"**Customer:** {customer_name}")
            st.write(f"**Product:** {product}")
            st.write(f"**Region:** {region}")
            st.write(f"**List Price:** ${list_price:,.2f}")
            st.write(f"**Proposed Discount:** {discount}%")
            st.write(
                f"**Discount Amount:** "
                f"${profitability['discount_amount']:,.2f}"
            )
            st.write(
                f"**Final Selling Price:** "
                f"${profitability['final_selling_price']:,.2f}"
            )
            st.write(
                f"**Estimated Delivery Cost:** "
                f"${estimated_cost:,.2f}"
            )
            st.write(
                f"**Expected Profit:** "
                f"${profitability['expected_profit']:,.2f}"
            )
            st.write(
                f"**Profit Margin:** "
                f"{profitability['profit_margin']:.2f}%"
            )
            st.write(
                f"**Policy Status:** "
                f"{policy_result['status']}"
            )
            st.write(
                f"**Required Approval:** {approval}"
            )


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.divider()

st.caption(
    "Independent MVP created to demonstrate an enterprise AI "
    "sales-operations use case using simulated information."
)