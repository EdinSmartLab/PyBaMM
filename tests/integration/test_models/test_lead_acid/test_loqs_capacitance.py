#
# Tests for the lead-acid LOQS model
#
import pybamm
from pybamm.solvers.scikits_ode_solver import scikits_odes_spec
import tests

import unittest
import numpy as np


class TestLeadAcidLOQSCapacitance(unittest.TestCase):
    def test_basic_processing_differential(self):
        options = {"capacitance": "differential"}
        model = pybamm.lead_acid.LOQS(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()

    @unittest.skipIf(scikits_odes_spec is None, "scikits.odes not installed")
    def test_basic_processing_algebraic(self):
        options = {"capacitance": "algebraic"}
        model = pybamm.lead_acid.LOQS(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()

    def test_basic_processing_1p1D_differential(self):
        options = {"capacitance": "differential", "bc_options": {"dimensionality": 1}}
        model = pybamm.lead_acid.LOQS(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all(skip_output_tests=True)

    @unittest.skipIf(scikits_odes_spec is None, "scikits.odes not installed")
    def test_basic_processing_1p1D_algebraic(self):
        options = {"capacitance": "algebraic", "bc_options": {"dimensionality": 1}}
        model = pybamm.lead_acid.LOQS(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all(skip_output_tests=True)

    def test_optimisations(self):
        options = {"capacitance": "differential"}
        model = pybamm.lead_acid.LOQS(options)
        optimtest = tests.OptimisationsTest(model)

        original = optimtest.evaluate_model()
        simplified = optimtest.evaluate_model(simplify=True)
        using_known_evals = optimtest.evaluate_model(use_known_evals=True)
        simp_and_known = optimtest.evaluate_model(simplify=True, use_known_evals=True)
        simp_and_python = optimtest.evaluate_model(simplify=True, to_python=True)
        np.testing.assert_array_almost_equal(original, simplified, decimal=5)
        np.testing.assert_array_almost_equal(original, using_known_evals)
        np.testing.assert_array_almost_equal(original, simp_and_known, decimal=5)
        np.testing.assert_array_almost_equal(original, simp_and_python, decimal=5)


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    unittest.main()