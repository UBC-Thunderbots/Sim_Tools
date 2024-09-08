import numpy as np
from dataclasses import dataclass
from system.specs import *

@dataclass
class MOSFET:
    part_number: str
    price_100u: float
    Vds_rated_V: float
    Id_rated_A: float
    R_ds_Ohm: float
    Vgs_th_max_V: float
    Vgs_max_V: float
    Qg_C: float
    power_W: float
    V_fw_V : float
    t_r_s: float
    t_f_s: float
    R_JA_CW: float
    R_JC_CW: float
    dual: bool
    max_temp_C: float

################################################
# Reference for loss calculations: https://application-notes.digchip.com/070/70-41484.pdf
################################################

def conduction_loss(SW : MOSFET, op_conds : md_op_specs):
    HS_loss = SW.R_ds_Ohm * op_conds.I_rms_A**2 * (1/8 + (op_conds.mod_indx * op_conds.power_fact)/(3*np.pi))
    LS_loss = HS_loss
    return np.array((HS_loss, LS_loss))
    
def deadtime_loss(SW : MOSFET, op_conds : md_op_specs):
    # conservative estimate: assuming I_rms go through diode, 
    # free-wheeling current flows through HS and LS each half of the time,
    # neglect diode resistance
    # TODO: implement more accurate model from app note
    total_loss = SW.V_fw_V * op_conds.I_rms_A * (2*op_conds.DT_s) * op_conds.f_SW_Hz
    return np.array((total_loss/2, total_loss/2))

def switching_loss(SW : MOSFET, op_conds : md_op_specs):
    # TODO: refer to app note for more accurate model
    # rough first-order estimate
    HS_loss = 0.5 * (op_conds.V_bus_V * op_conds.I_rms_A) * (SW.t_r_s + SW.t_f_s) * op_conds.f_SW_Hz
    LS_loss = 0 # assuming zero-voltage switching condition
    return np.array((HS_loss, LS_loss))

def gate_charge_loss(SW : MOSFET, op_conds : md_op_specs):
    # when MOSFET turns on, driver supply (1/2)QV to the gate capacitor, and also lost (1/2)QV to resistive elements
    # when MOSFET turns off, (1/2)QV stored in the gate capacitor is dissipated in the resistive gate drive elements
    # so, the total energy dissipated for each FET over a switching cycle is QV
    loss = SW.Qg_C * op_conds.V_drv_V * op_conds.f_SW_Hz 
    return np.array((loss, loss))
    
#TODO: add other losses, but they are negligible

def run_SW_sim(SW : MOSFET, op_conds : md_op_specs, heat_sink : bool = False):
    sim_res = {
        "conduction_loss_W" : conduction_loss(SW, op_conds),
        "switching_loss_W" : switching_loss(SW, op_conds),
        "deadtime_loss_W" : deadtime_loss(SW, op_conds),
        "gate_charge_loss_W" : gate_charge_loss(SW, op_conds),
        "total_loss_W" : np.array([0.0,0.0]),
        "temp_rise_Ta_C" : None,
        "temp_rise_Tc_C" : None
    }
    for loss in ["conduction_loss_W", "switching_loss_W", "deadtime_loss_W", "gate_charge_loss_W"]:
        sim_res["total_loss_W"] += sim_res[loss]
    sim_res["temp_rise_Ta_C"] = SW.R_JA_CW * np.sum(sim_res["total_loss_W"])
    sim_res["temp_rise_Tc_C"] = SW.R_JC_CW * np.sum(sim_res["total_loss_W"])
    return sim_res
    