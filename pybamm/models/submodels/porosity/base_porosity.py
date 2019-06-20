#
# Base class for porosity
#
import pybamm


class BaseModel(pybamm.BaseSubModel):
    """Base class for porosity

    Parameters
    ----------
    param : parameter class
        The parameters to use for this submodel

    *Extends:* :class:`pybamm.BaseSubModel`
    """

    def __init__(self, param):
        super().__init__(param)

    def _get_standard_porosity_variables(self, eps):

        eps_n, eps_s, eps_p = eps.orphans

        variables = {
            "Porosity": eps,
            "Negative electrode porosity": eps_n,
            "Separator porosity": eps_s,
            "Positive electrode porosity": eps_p,
            "Average negative electrode porosity": pybamm.average(eps_n),
            "Average separator porosity": pybamm.average(eps_s),
            "Average positive electrode porosity": pybamm.average(eps_p),
        }

        return variables

    def _get_standard_porosity_change_variables(self, deps_dt):

        deps_n_dt, deps_s_dt, deps_p_dt = deps_dt.orphans

        variables = {
            "Porosity change": deps_dt,
            "Negative electrode porosity change": deps_n_dt,
            "Separator porosity change": deps_s_dt,
            "Positive electrode porosity change": deps_p_dt,
            "Average porosity change": pybamm.average(deps_dt),
            "Average negative electrode porosity change": pybamm.average(deps_n_dt),
            "Average separator porosity change": pybamm.average(deps_s_dt),
            "Average positive electrode porosity change": pybamm.average(deps_p_dt),
        }

        return variables
