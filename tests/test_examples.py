import pytest
import os
import fllume
from dotenv import load_dotenv
from pydantic import BaseModel
import pandas as pd
from typing import Generator

# Load environment variables from .env file
load_dotenv()

# Marker to skip tests if OPENAI_API_KEY is not set
requires_openai = pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ,
    reason="OPENAI_API_KEY not set in environment",
)

MODEL = "openai/gpt-4o-mini"


@requires_openai
def test_example_1_data_standardization():
    """
    Tests the data standardization and extraction example from README.md.
    """

    class StandardizedAddress(BaseModel):
        street: str
        city: str
        state: str
        zip_code: str

    agent_address_standardizer = (
        fllume.Agent.builder()
        .with_model(MODEL)
        .with_instructions((
            "Standardize the given address into its components: "
            "street, city, state, and zip code."
        ))
        .with_response_format(StandardizedAddress)
        .with_prompt_template("Standardize this address: {address}")
        .build()
    )

    address_data = "1600 Amphitheatre Parkway, Mountain View, CA 94043"

    standardized_address = agent_address_standardizer.complete(
        {"address": address_data}
    )

    # Create a DataFrame from a list containing the model's dictionary representation
    df_addresses = pd.DataFrame([standardized_address.model_dump()])

    assert len(df_addresses) == 1
    assert list(df_addresses.columns) == ["street", "city", "state", "zip_code"]
    assert df_addresses.iloc[0]["street"] == "1600 Amphitheatre Parkway"
    assert df_addresses.iloc[0]["city"] == "Mountain View"
    assert df_addresses.iloc[0]["state"] == "CA"
    assert df_addresses.iloc[0]["zip_code"] == "94043"


@requires_openai
def test_example_2_numerical_computation():
    """
    Tests the numerical computation with tools example from README.md.
    """

    def calculate_average(numbers: list[float]) -> float:
        """Calculates the average of a list of numbers."""
        # WORKAROUND: The underlying any-llm library incorrectly generates
        # a schema for list[float], causing the LLM to pass a string.
        # This makes the example tool robust to that specific failure mode.
        if isinstance(numbers, str):
            numbers = [float(n.strip()) for n in numbers.split(",")]
        return sum(numbers) / len(numbers)

    def find_max(numbers: list[float]) -> float:
        """Finds the maximum value in a list of numbers."""
        if isinstance(numbers, str):
            numbers = [float(n.strip()) for n in numbers.split(",")]
        return max(numbers)

    agent_data_analyzer = (
        fllume.Agent.builder()
        .with_model(MODEL)
        .with_tools([calculate_average, find_max])
        .with_prompt_template("What is the {statistic} of these numbers: {numbers}?")
        .build()
    )

    data_points = [10.5, 20.3, 15.7, 25.1, 12.9]

    response_avg = agent_data_analyzer.complete(
        {"statistic": "average", "numbers": data_points}
    )
    assert "16.9" in response_avg

    response_max = agent_data_analyzer.complete(
        {"statistic": "maximum value", "numbers": data_points}
    )
    assert "25.1" in response_max


@requires_openai
def test_example_3_data_summary_streaming():
    """
    Tests the data summary with streaming example from README.md.
    """
    data = {
        "City": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
        "Population": [8419000, 3980000, 2716000, 2320000, 1660000],
        "Area_sq_mi": [302.6, 468.7, 234.0, 637.4, 517.9],
    }
    df = pd.DataFrame(data)

    agent_data_summarizer = (
        fllume.Agent.builder()
        .with_model(MODEL)
        .with_instructions((
            "You are a data analyst. Summarize the key insights from the "
            "provided DataFrame, focusing on population and area trends. "
            "Be concise but informative."
        ))
        .with_prompt_template("Summarize the following DataFrame:\n{dataframe}")
        .build()
    )

    stream = agent_data_summarizer.complete(
        {"dataframe": df.to_string()}, stream=True
    )

    assert isinstance(stream, Generator)

    response_parts = list(stream)

    assert len(response_parts) > 1
    full_response = "".join(response_parts)
    assert "population" in full_response.lower()
    assert "area" in full_response.lower()
    assert "New York" in full_response


@requires_openai
def test_example_4_multi_turn_conversation():
    """
    Tests the multi-turn conversation example from README.md.
    """
    plotting_assistant = (
        fllume.Agent.builder()
        .with_model(MODEL)
        .with_instructions((
            "You are a data visualization assistant. You provide Python code "
            "snippets for generating plots with matplotlib."
        ))
        .build()
    )

    # First turn
    context = plotting_assistant.complete_with_context(
        prompt="Give me some code to create a simple scatter plot of x vs y.",
    )
    first_response = context[-1].content
    assert "scatter" in first_response.lower()
    assert "matplotlib" in first_response.lower()

    # Second turn (follow-up question)
    context = plotting_assistant.complete_with_context(
        context=context,
        prompt="Now, can you modify that to make the points blue and add a title?",
    )
    second_response = context[-1].content
    assert "blue" in second_response.lower()
    assert "title" in second_response.lower()
