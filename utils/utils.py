import pandas as pd
from loss_model.switch_model import MOSFET

#####################################
# Function to get a list of MOSFET objects from FETs database
#####################################

def get_MOSFETs_from_database(dir : str):
    df = pd.read_excel(dir)
    MOSFET_list = []
    for row in range(df.shape[0]):
        fet_obj = df.iloc[row]
        new_MOS = MOSFET(
            part_number = fet_obj["MFG_Num"],
            price_100u = fet_obj["Price_100u_CAD"],
            Vds_rated_V = fet_obj["Vds_rated_V"],
            Id_rated_A = fet_obj["Id_rated_A"],
            R_ds_Ohm = fet_obj["Rds_on_mOhm"]*1e-3,
            Vgs_th_max_V = fet_obj["Vgs_th_max_V"],
            Vgs_max_V = fet_obj["Vgs_max_V"],
            Qg_C = fet_obj["Qg_nC"]*1e-9,
            power_W = fet_obj["Power_W"],
            V_fw_V = fet_obj["V_fw_V"], #TODO: add column for forward voltage
            t_r_s = fet_obj["t_r_ns"]*1e-9,
            t_f_s = fet_obj["t_f_ns"]*1e-9,
            R_JA_CW = fet_obj["R_JA_CW"],
            R_JC_CW = fet_obj["R_JC_CW"],
            dual = fet_obj["Dual"],
            max_temp_C = fet_obj["Max_temp_C"]
        )
        MOSFET_list.append(new_MOS)
    return MOSFET_list