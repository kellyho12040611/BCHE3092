import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import linregress


def parse_values(text: str, label: str) -> list[float]:
    try:
        values = [float(value.strip()) for value in text.split(",")]
    except ValueError as exc:
        raise ValueError(f"{label} must contain comma-separated numbers.") from exc

    if not values or not all(np.isfinite(value) for value in values):
        raise ValueError(f"{label} must contain finite numbers.")
    return values


st.set_page_config(page_title="Bradford Assay", page_icon="🧪")
st.title("Bradford Assay")
st.write("Create a standard curve and estimate the protein concentration of an unknown sample.")

with st.sidebar:
    st.header("Assay inputs")
    concentrations_text = st.text_input(
        "BSA standard concentrations (comma-separated)",
        value="0, 2, 4, 6, 8, 10",
        help="Enter concentrations in ascending or descending order.",
    )
    absorbances_text = st.text_input(
        "Standard absorbances (comma-separated)",
        value="0.05, 0.18, 0.31, 0.44, 0.58, 0.70",
    )
    concentration_unit = st.text_input("Concentration unit", value="µg/mL")
    unknown_absorbance = st.number_input(
        "Unknown sample absorbance",
        value=0.39,
        format="%.4f",
    )

try:
    concentrations = parse_values(concentrations_text, "BSA concentrations")
    absorbances = parse_values(absorbances_text, "Standard absorbances")

    if len(concentrations) != len(absorbances):
        raise ValueError("Enter the same number of concentrations and absorbances.")
    if len(concentrations) < 2:
        raise ValueError("Enter at least two standard pairs.")
    if any(value < 0 for value in concentrations):
        raise ValueError("BSA concentrations cannot be negative.")
    if len(set(concentrations)) < 2:
        raise ValueError("Standards must include at least two different concentrations.")

    standards = pd.DataFrame(
        {"Concentration": concentrations, "Absorbance": absorbances}
    )
    fit = linregress(standards["Concentration"], standards["Absorbance"])
    if np.isclose(fit.slope, 0):
        raise ValueError("The fitted line has a zero slope, so the unknown cannot be calculated.")

    unknown_concentration = (unknown_absorbance - fit.intercept) / fit.slope

    st.subheader("Standard curve")
    figure, axis = plt.subplots()
    axis.scatter(
        standards["Concentration"],
        standards["Absorbance"],
        color="royalblue",
        label="BSA standards",
    )
    x_line = np.linspace(standards["Concentration"].min(), standards["Concentration"].max(), 100)
    axis.plot(x_line, fit.slope * x_line + fit.intercept, color="darkorange", label="Linear fit")
    axis.set_xlabel(f"Protein concentration ({concentration_unit})")
    axis.set_ylabel("Absorbance")
    axis.set_title("Bradford assay standard curve")
    axis.legend()
    axis.grid(alpha=0.25)
    st.pyplot(figure)
    plt.close(figure)

    st.markdown(
        f"**Line of best fit:** Absorbance = {fit.slope:.4g} × concentration "
        f"{fit.intercept:+.4g}"
    )
    st.markdown(f"**R²:** {fit.rvalue**2:.4f}")
    st.metric("Unknown protein concentration", f"{unknown_concentration:.4g} {concentration_unit}")

    if not standards["Concentration"].min() <= unknown_concentration <= standards["Concentration"].max():
        st.warning("The unknown is outside the standards' concentration range; this estimate is an extrapolation.")

except ValueError as error:
    st.error(str(error))