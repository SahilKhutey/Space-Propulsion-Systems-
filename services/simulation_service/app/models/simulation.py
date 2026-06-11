from datetime import datetime
from sqlalchemy import String, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base


class ThermalResult(Base):
    __tablename__ = "thermal_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    simulation_run_id: Mapped[int] = mapped_column(ForeignKey("simulation_runs.id"))
    component: Mapped[str] = mapped_column(String(100))
    min_temp_k: Mapped[float] = mapped_column(Float)
    max_temp_k: Mapped[float] = mapped_column(Float)
    steady_state_k: Mapped[float] = mapped_column(Float)
    time_series: Mapped[dict] = mapped_column(JSON, default=dict)
    hotspots: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PowerResult(Base):
    __tablename__ = "power_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    simulation_run_id: Mapped[int] = mapped_column(ForeignKey("simulation_runs.id"))
    solar_power_w: Mapped[float] = mapped_column(Float)
    eclipse_loss_wh: Mapped[float] = mapped_column(Float)
    battery_capacity_wh: Mapped[float] = mapped_column(Float)
    thruster_duty_cycle: Mapped[float] = mapped_column(Float)
    consumption_profile: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
