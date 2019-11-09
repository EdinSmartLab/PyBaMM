#
# Tests for external submodels
#
import pybamm
import unittest
import numpy as np


# only works for statevector inputs
class TestExternalSubmodel(unittest.TestCase):
    def test_external_temperature(self):

        model_options = {
            "thermal": "x-full",
            "external submodels": ["thermal"],
        }

        model = pybamm.lithium_ion.SPMe(model_options)

        neg_pts = 5
        sep_pts = 3
        pos_pts = 5
        tot_pts = neg_pts + sep_pts + pos_pts

        var_pts = {
            pybamm.standard_spatial_vars.x_n: neg_pts,
            pybamm.standard_spatial_vars.x_s: sep_pts,
            pybamm.standard_spatial_vars.x_p: pos_pts,
            pybamm.standard_spatial_vars.r_n: 5,
            pybamm.standard_spatial_vars.r_p: 5,
        }

        sim = pybamm.Simulation(model, var_pts=var_pts)
        sim.build()

        t_eval = np.linspace(0, 0.17, 100)

        for t in t_eval:
            T = np.zeros((tot_pts, 1))
            external_variables = {"Cell temperature": T}
            sim.step(external_variables=external_variables)


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    unittest.main()