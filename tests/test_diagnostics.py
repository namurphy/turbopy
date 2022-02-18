"""
Tests for the diagonstics.py file
"""
import pytest
import numpy as np
from turbopy.core import Simulation
from turbopy.diagnostics import FieldDiagnostic


@pytest.fixture(name='simple_field_csv')
def field_fixt_csv(tmp_path):
    """Pytest fixture for FieldDiagnostic class writing to csv file"""
    sim_dic = {"Grid": {"N": 2, "r_min": 0, "r_max": 1},
               "Clock": {"start_time": 0,
                         "end_time": 10,
                         "num_steps": 100},
               "Tools": {"ExampleTool": {}},
               "PhysicsModules": {"ExampleModule": {}},
               "Diagnostics": {
                   "directory": f"{tmp_path}/default_output",
                   # "clock": {},
                   "field": [
                       {"component": "Component",
                        "field": "Field",
                        "output_type": "csv",
                        "filename": "output.csv",
                        "dump_interval": 1}
                       ]
               }
               }
    sim = Simulation(sim_dic)
    sim.read_diagnostics_from_input()
    sim.read_clock_from_input()
    sim.read_grid_from_input()
    return sim.diagnostics[0]


@pytest.fixture(name='simple_field_npy')
def field_fixt_npy(tmp_path):
    """Pytest fixture for FieldDiagnostic class writing to npy file"""
    sim_dic = {"Grid": {"N": 2, "r_min": 0, "r_max": 1},
               "Clock": {"start_time": 0,
                         "end_time": 10,
                         "num_steps": 100},
               "Tools": {"ExampleTool": {}},
               "PhysicsModules": {"ExampleModule": {}},
               "Diagnostics": {
                   "directory": f"{tmp_path}/default_output",
                   # "clock": {},
                   "field": [
                       {"component": "Component",
                        "field": "Field",
                        "output_type": "npy",
                        "filename": "output.npy",
                        "dump_interval": 1}
                       ]
               }
               }
    sim = Simulation(sim_dic)
    sim.read_diagnostics_from_input()
    sim.read_clock_from_input()
    sim.read_grid_from_input()
    return sim.diagnostics[0]

# Test methods for FieldDiagnostic class with csv file
def test_init_should_create_class_instance_when_called(simple_field_csv):
    """Tests init method in FieldDiagnostic class"""
    assert simple_field_csv.component == "Component"
    assert simple_field_csv.field_name == "Field"
    assert simple_field_csv.output == "csv"
    assert simple_field_csv.field is None
    assert simple_field_csv.dump_interval is None
    assert simple_field_csv.last_dump is None
    assert simple_field_csv.diagnostic_size is None
    assert simple_field_csv.field_was_found is False


def test_check_step_should_update_last_dump_after_dump_interval_has_passed(simple_field_csv):
    """Tests check_step method in FieldDiagnostic class"""
    simple_field_csv.inspect_resource({"Field": np.linspace(0, 1, 2)})
    simple_field_csv.initialize()
    simple_field_csv._owner.clock.time = 1
    simple_field_csv.check_step()
    assert simple_field_csv.last_dump == 1


def test_initialize_should_set_remaining_parameters_when_called(simple_field_csv):
    """Tests initialize method in FieldDiagnostic class for declared attributes"""
    with pytest.raises(RuntimeError):
        assert simple_field_csv.initialize()
    simple_field_csv.inspect_resource({"Field": np.linspace(0, 1, 2)})
    simple_field_csv.initialize()
    assert simple_field_csv.dump_interval == 1
    assert simple_field_csv.last_dump == 0
    assert simple_field_csv.diagnostic_size == (11, 2)
    

def test_initialize_should_set_outputter_parameters_when_called(simple_field_csv, tmp_path):
    simple_field_csv.inspect_resource({"Field": np.linspace(0, 1, 2)})
    simple_field_csv.initialize()
    assert simple_field_csv.outputter._filename == f"{tmp_path}/default_output/output.csv"
    assert np.allclose(simple_field_csv.outputter._buffer, np.zeros((11, 2)))
    assert simple_field_csv.outputter._buffer_index == 0


def test_inspect_resource_should_assign_field_attribute_if_field_name_in_resource(simple_field_csv):
    """Tests inspect_resource method in FieldDiagnostic class"""
    array_to_share = np.linspace(0, 1, 2)
    simple_field_csv.inspect_resource({"Field": array_to_share})
    assert simple_field_csv.field_was_found is True
    assert simple_field_csv.field is array_to_share


def test_csv_diagnose_should_append_data_to_csv_when_called(simple_field_csv):
    """Tests csv_diagnose method in FieldDiagnostic class"""
    simple_field_csv.inspect_resource({"Field": np.linspace(0, 1, 2)})
    simple_field_csv.initialize()
    simple_field_csv.do_diagnostic()
    assert np.allclose(simple_field_csv.outputter._buffer[
                            simple_field_csv.outputter._buffer_index - 1, :],
                       simple_field_csv.field)
    assert simple_field_csv.outputter._buffer_index == 1


# Test methods for FieldDiagnostic class with npy files
def test_init_should_create_class_instance_when_called_npy(simple_field_npy):
    """Tests init method in FieldDiagnostic class"""
    assert simple_field_npy.component == "Component"
    assert simple_field_npy.field_name == "Field"
    assert simple_field_npy.output == "npy"
    assert simple_field_npy.field is None
    assert simple_field_npy.dump_interval is None
    assert simple_field_npy.last_dump is None
    assert simple_field_npy.diagnostic_size is None
    assert simple_field_npy.field_was_found is False


def test_check_step_should_update_last_dump_after_dump_interval_has_passed_npy(simple_field_npy):
    """Tests check_step method in FieldDiagnostic class"""
    simple_field_npy.inspect_resource({"Field": np.linspace(0, 1, 2)})
    simple_field_npy.initialize()
    simple_field_npy._owner.clock.time = 1
    simple_field_npy.check_step()
    assert simple_field_npy.last_dump == 1


def test_initialize_should_set_remaining_parameters_when_called_npy(simple_field_npy):
    """Tests initialize method in FieldDiagnostic class for declared attributes"""
    with pytest.raises(RuntimeError):
        assert simple_field_npy.initialize()
    simple_field_npy.inspect_resource({"Field": np.linspace(0, 1, 2)})
    simple_field_npy.initialize()
    assert simple_field_npy.dump_interval == 1
    assert simple_field_npy.last_dump == 0
    assert simple_field_npy.diagnostic_size == (11, 2)


def test_initialize_should_set_outputter_parameters_when_called_npy(simple_field_npy, tmp_path):
    simple_field_npy.inspect_resource({"Field": np.linspace(0, 1, 2)})
    simple_field_npy.initialize()
    assert simple_field_npy.outputter._filename == f"{tmp_path}/default_output/output.npy"
    assert np.allclose(simple_field_npy.outputter._buffer, np.zeros((11, 2)))
    assert simple_field_npy.outputter._buffer_index == 0


def test_inspect_resource_should_assign_field_attribute_if_field_name_in_resource_npy(simple_field_npy):
    """Tests inspect_resource method in FieldDiagnostic class"""
    array_to_share = np.linspace(0, 1, 2)
    simple_field_npy.inspect_resource({"Field": array_to_share})
    assert simple_field_npy.field_was_found is True
    assert simple_field_npy.field is array_to_share


def test_csv_diagnose_should_append_data_to_csv_when_called_npy(simple_field_npy):
    """Tests npy_diagnose method in FieldDiagnostic class"""
    simple_field_npy.inspect_resource({"Field": np.linspace(0, 1, 2)})
    simple_field_npy.initialize()
    simple_field_npy.do_diagnostic()
    assert np.allclose(simple_field_npy.outputter._buffer[
                       simple_field_npy.outputter._buffer_index - 1, :],
                       simple_field_npy.field)
    assert simple_field_npy.outputter._buffer_index == 1
