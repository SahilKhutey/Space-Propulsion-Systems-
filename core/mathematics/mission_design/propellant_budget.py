import numpy as np
from .tsiolkovsky import required_propellant_mass

def propellant_budget(*args, **kwargs):
    payload_kg = kwargs.get("payload_kg", None)
    dv_budgets = kwargs.get("dv_budgets", None)
    isp_s = kwargs.get("isp_s", None)
    safety_factor = kwargs.get("safety_factor", 1.0)
    
    if payload_kg is None and len(args) >= 1:
        if isinstance(args[0], (int, float)):
            payload_kg = args[0]
    if dv_budgets is None and len(args) >= 2:
        if isinstance(args[1], list):
            dv_budgets = args[1]
    if isp_s is None and len(args) >= 3:
        isp_s = args[2]
        
    if payload_kg is not None and dv_budgets is not None and isp_s is not None:
        isps = [isp_s] * len(dv_budgets) if isinstance(isp_s, (int, float)) else isp_s
        dvs = dv_budgets
        m_dry = payload_kg
        margin_pct = (safety_factor - 1.0) * 100.0
    else:
        m_dry = args[0] if len(args) > 0 else kwargs.get("m_dry", 500.0)
        dvs = args[1] if len(args) > 1 else kwargs.get("dvs", [])
        isps = args[2] if len(args) > 2 else kwargs.get("isps", [])
        margin_pct = args[3] if len(args) > 3 else kwargs.get("margin_pct", 10.0)
        
    current_dry = m_dry
    stages = []
    total_prop = 0.0
    for i, (dv, isp) in enumerate(zip(dvs, isps)):
        mp = required_propellant_mass(isp, current_dry, dv)
        total_prop += mp
        stages.append({
            "stage": i + 1,
            "delta_v": dv,
            "isp_s": isp,
            "propellant_needed_kg": mp,
            "dry_mass_before_kg": current_dry
        })
        current_dry += mp
    
    budgeted_prop = total_prop * (1.0 + margin_pct / 100.0)
    
    return {
        "stages": stages,
        "dry_mass_kg": m_dry,
        "nominal_propellant_kg": total_prop,
        "budgeted_propellant_kg": budgeted_prop,
        "total_wet_mass_kg": m_dry + budgeted_prop,
        
        # Test expected keys
        "total_dv_ms": sum(dvs),
        "total_propellant_kg": budgeted_prop,
        "wet_mass_kg": m_dry + budgeted_prop,
        "dry_mass_before_kg": m_dry,
    }
