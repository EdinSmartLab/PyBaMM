#
# Class for the leading-order electrolyte potential employing stefan-maxwell
#
import pybamm


class LeadingStefanMaxwellConductivity(pybamm.BaseStefanMaxwellConductivity):
    """Class for conservation of charge in the electrolyte employing the
    Stefan-Maxwell constitutive equations. (Leading refers to leading-order
    in the asymptotic reduction)

    Parameters
    ----------
    param : parameter class
        The parameters to use for this submodel

    *Extends:* :class:`pybamm.BaseStefanMaxwellConductivity`
    """

    def __init__(self, param, domain):
        super().__init__(param)
        self._domain = domain

    def get_coupled_variables(self, variables):

        ocp_n_av = variables["Average negative electrode open circuit potential"]
        eta_r_n_av = variables["Average negative reaction overpotential"]
        delta_phi_n_av = variables["Average negative electrode ohmic losses"]
        i_boundary_cc = variables["Current collector current density"]

        param = self.param
        l_n = param.l_n
        l_p = param.l_p
        x_n = pybamm.standard_spatial_vars.x_n
        x_p = pybamm.standard_spatial_vars.x_p

        phi_e_av = delta_phi_n_av - eta_r_n_av - ocp_n_av
        phi_e_n = pybamm.Broadcast(phi_e_av, ["negative electrode"])
        phi_e_s = pybamm.Broadcast(phi_e_av, ["separator"])
        phi_e_p = pybamm.Broadcast(phi_e_av, ["positive electrode"])
        phi_e = pybamm.Concatenation(phi_e_n, phi_e_s, phi_e_p)

        i_e_n = pybamm.outer(i_boundary_cc, x_n / l_n)
        i_e_s = pybamm.Broadcast(i_boundary_cc, ["separator"])
        i_e_p = pybamm.outer(i_boundary_cc, (1 - x_p) / l_p)
        i_e = pybamm.Concatenation(i_e_n, i_e_s, i_e_p)

        variables.update(self._get_standard_potential_variables(phi_e, phi_e_av))
        variables.update(self._get_standard_current_variables(i_e))

        eta_c_av = pybamm.Scalar(0)  # concentration overpotential
        delta_phi_e_av = pybamm.Scalar(0)  # ohmic losses
        variables.update(self._get_split_overpotential(eta_c_av, delta_phi_e_av))

        return variables

