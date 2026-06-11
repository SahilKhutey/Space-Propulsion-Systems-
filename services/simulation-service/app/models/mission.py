from datetime import datetime
from sqlalchemy import String, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    initial_orbit: Mapped[str] = mapped_column(String(50))
    target_orbit: Mapped[str] = mapped_column(String(50))
    payload_mass_kg: Mapped[float] = mapped_column(Float)
    thruster_type: Mapped[str] = mapped_column(String(50))
    duration_years: Mapped[float] = mapped_column(Float, default=5.0)
    parameters: Mapped[dict] = mapped_column(JSON, default=dict)

    delta_v_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    propellant_mass_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_mass_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    transfer_time_days: Mapped[float | None] = mapped_column(Float, nullable=True)
    success_probability: Mapped[float | None] = mapped_column(Float, nullable=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner = relationship("User", back_populates="missions")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    mission_id: Mapped[int | None] = mapped_column(ForeignKey("missions.id"), nullable=True)
    thruster_id: Mapped[int | None] = mapped_column(ForeignKey("thrusters.id"), nullable=True)

    run_type: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(30), default="pending")
    results: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    execution_time_s: Mapped[float | None] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
