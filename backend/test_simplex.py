# test_tu_modulo.py

import torch
import pytest
from Simplex import Simplex

@pytest.fixture
def first_sample_json_data():
    return {
        "functionVariables": [40, 30],
        "equationVariables": [[1, 1], [2,1]],
        "selectedSymbols": [2, 2],
        "equationEqual": [12, 16],
        "variables": 2,
        "constraints": 2,
        "type": "Max",
        "expectedResult": [0.0, 0.0, 20.0, 10.0, 400.0]
    }

@pytest.fixture
def second_sample_json_data():
    return {
        "functionVariables": [19, 20, 21],
        "equationVariables": [[13, 10, 2], [8, 11, 1]],
        "selectedSymbols": [2, 2],
        "equationEqual": [21, 22],
        "variables": 3,
        "constraints": 2,
        "type": "Max",
        "expectedResult": [117.5000,  85.0000,   0.0000,  10.5000,   0.0000, 220.5000]
    }

@pytest.fixture
def third_sample_json_data():
    return {
        "functionVariables": [0.8, 0.6],
        "equationVariables": [[0.2, 0.59], [2, 1]],
        "selectedSymbols": [2, 2],
        "equationEqual": [25, 100],
        "variables": 2,
        "constraints": 2,
        "type": "Min",
        "expectedResult": [0.8000, 0.6000, 0.0000, 0.0000, 0.0000]
    }

#==================== Unitaries ===============================#

def test_first_json_list(first_sample_json_data):
    """
    The function `test_first_json_list` tests if the attributes of an instance of the `Simplex` class
    match the expected values from a given JSON data.
    
    @param first_sample_json_data The parameter `first_sample_json_data` is a JSON object that contains
    the following keys:
    """
    instance = Simplex(first_sample_json_data)
    instance.json_list()

    expected_cost_function_variables = torch.tensor(first_sample_json_data["functionVariables"], dtype=torch.float64)
    assert torch.all(torch.eq(instance.cost_function_variables, expected_cost_function_variables))

    expected_equation_matrix_variables = torch.tensor(first_sample_json_data["equationVariables"], dtype=torch.float64)
    assert torch.all(torch.eq(instance.equation_matrix_variables, expected_equation_matrix_variables))

    assert instance.selected_symbols == first_sample_json_data["selectedSymbols"]

    expected_equation_results = torch.tensor(first_sample_json_data["equationEqual"], dtype=torch.float64)
    assert torch.all(torch.eq(instance.equation_results, expected_equation_results))

    assert instance.number_of_variables == first_sample_json_data["variables"]
    assert instance.number_of_constraints == first_sample_json_data["constraints"]
    assert instance.type_min_max == first_sample_json_data["type"]

def test_json_list_second_case(second_sample_json_data):
    """
    The function `test_json_list_second_case` tests if the attributes of an instance of the `Simplex`
    class match the expected values from a given JSON data.
    
    @param second_sample_json_data The `second_sample_json_data` parameter is a JSON object that
    contains the following keys:
    """
    instance = Simplex(second_sample_json_data)
    instance.json_list()

    expected_cost_function_variables = torch.tensor(second_sample_json_data["functionVariables"], dtype=torch.float64)
    assert torch.all(torch.eq(instance.cost_function_variables, expected_cost_function_variables))

    expected_equation_matrix_variables = torch.tensor(second_sample_json_data["equationVariables"], dtype=torch.float64)
    assert torch.all(torch.eq(instance.equation_matrix_variables, expected_equation_matrix_variables))

    assert instance.selected_symbols == second_sample_json_data["selectedSymbols"]

    expected_equation_results = torch.tensor(second_sample_json_data["equationEqual"], dtype=torch.float64)
    assert torch.all(torch.eq(instance.equation_results, expected_equation_results))

    assert instance.number_of_variables == second_sample_json_data["variables"]
    assert instance.number_of_constraints == second_sample_json_data["constraints"]
    assert instance.type_min_max == second_sample_json_data["type"]

def test_json_list_third_case(third_sample_json_data):
    """
    The function `test_json_list_third_case` tests if the attributes of an instance of the `Simplex`
    class match the expected values from a given JSON data.
    
    @param third_sample_json_data The `third_sample_json_data` parameter is a JSON object that contains
    the following keys:
    """
    instance = Simplex(third_sample_json_data)
    instance.json_list()

    expected_cost_function_variables = torch.tensor(third_sample_json_data["functionVariables"], dtype=torch.float64)
    assert torch.all(torch.eq(instance.cost_function_variables, expected_cost_function_variables))

    expected_equation_matrix_variables = torch.tensor(third_sample_json_data["equationVariables"], dtype=torch.float64)
    assert torch.all(torch.eq(instance.equation_matrix_variables, expected_equation_matrix_variables))

    assert instance.selected_symbols == third_sample_json_data["selectedSymbols"]

    expected_equation_results = torch.tensor(third_sample_json_data["equationEqual"], dtype=torch.float64)
    assert torch.all(torch.eq(instance.equation_results, expected_equation_results))

    assert instance.number_of_variables == third_sample_json_data["variables"]
    assert instance.number_of_constraints == third_sample_json_data["constraints"]
    assert instance.type_min_max == third_sample_json_data["type"]

#==================== Functional ===============================#

def test_simplex_solver_functionality(first_sample_json_data):
    """
    The function tests the functionality of a simplex solver by comparing its output with an expected
    result.
    
    @param first_sample_json_data The parameter `first_sample_json_data` is expected to be a JSON object
    containing the necessary data for running the simplex solver. It should have the following
    structure:
    """
    instance = Simplex(first_sample_json_data)
    instance.start_simplex()

    expected_result = torch.tensor(first_sample_json_data["expectedResult"], dtype=torch.float64)

    assert torch.all(torch.eq(instance.matrixResult, expected_result))

def test_simplex_solver_functionality_second(second_sample_json_data):
    """
    The function tests the functionality of a simplex solver using a given sample JSON data.
    
    @param second_sample_json_data The parameter `second_sample_json_data` is a JSON object that
    contains the data needed for the simplex solver. It should have the following structure:
    """
    instance = Simplex(second_sample_json_data)
    instance.start_simplex()

    expected_result = torch.tensor(second_sample_json_data["expectedResult"], dtype=torch.float64)

    assert torch.all(torch.eq(instance.matrixResult, expected_result))

def test_simplex_solver_functionality_third(third_sample_json_data):
    """
    The function tests the functionality of a simplex solver using a given sample JSON data.
    
    @param third_sample_json_data The parameter `third_sample_json_data` is a JSON object that contains
    the necessary data for running the simplex solver. It likely includes information such as the
    objective function, constraints, and initial tableau. The specific structure of the JSON object will
    depend on the implementation of the simplex solver.
    """
    instance = Simplex(third_sample_json_data)
    instance.start_simplex()

    expected_result = torch.tensor(third_sample_json_data["expectedResult"], dtype=torch.float64)

    assert torch.all(torch.eq(instance.matrixResult, expected_result))


