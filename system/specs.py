######################################
# System specifications
######################################
from dataclasses import dataclass

@dataclass
class md_op_specs:
    V_bus_V : float # DC-link voltage
    V_drv_V : float # gate drive voltage
    I_rms_A : float # rms output current
    power_fact : float # motor power factor
    f_SW_Hz : float # switching frequency
    elec_freq_Hz : float # motor electrical frequency
    mod_indx : float # modulation index
    DT_s : float # fixed deadtime
    
MD_v6_specs = md_op_specs(
    V_bus_V = 24,
    V_drv_V = 12,
    I_rms_A = 5, # just an estimate #TODO: make this number more easily adjustable
    power_fact = 0.95,
    f_SW_Hz = 20000,
    elec_freq_Hz = 1000,
    mod_indx = 1.15, # assuming max for space vector modulation
    DT_s = 20e-9
)
