from pydantic import BaseModel, Field
from typing import List, Optional

class Anomaly(BaseModel):
    anomaly_type: str = Field(..., description="Type of anomaly (e.g., Thermal, Power, Propulsion)")
    severity: str = Field(..., description="Severity level: low, medium, high, critical")
    timestamp: float = Field(..., description="Simulation timestamp")
    message: str = Field(..., description="Human-readable description of the anomaly")
    node_id: Optional[int] = Field(None, description="Optional node index for multi-node systems")

class RootCause(BaseModel):
    root_cause: str = Field(..., description="Identified root cause")
    subsystem: str = Field(..., description="Failed subsystem (Propulsion, Thermal, Power, Orbit, Control)")
    failure_path: List[str] = Field(default_factory=list, description="Chain of events leading to failure")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level of the diagnosis")

class Recommendation(BaseModel):
    title: str = Field(..., description="Title of the recommendation")
    description: str = Field(..., description="Detailed explanation of the proposed fix")
    expected_impact: str = Field(..., description="Estimated performance or success rate delta")
    confidence: float = Field(..., ge=0.0, le=1.0)

class MissionFailure(BaseModel):
    failed: bool = Field(..., description="Whether the mission failed")
    reason: str = Field(..., description="Reason for failure")
    limiting_subsystem: str = Field(..., description="The subsystem that limited mission success")
    fails_first: str = Field(..., description="The component or node that failed first")

class EngineeringReport(BaseModel):
    physically_valid: bool = Field(..., description="Is the simulation physically valid (e.g. conservation laws, efficiency limits)")
    mission_success: bool = Field(..., description="Will the mission succeed")
    limiting_subsystem: str = Field(..., description="Subsystem that limits performance")
    fails_first: str = Field(..., description="Component or subsystem that fails first")
    design_improvements: List[Recommendation] = Field(default_factory=list, description="Top design improvements")
    risks_and_uncertainties: List[str] = Field(default_factory=list, description="Identified risks")
    prediction_confidence: float = Field(..., ge=0.0, le=1.0, description="Overall prediction confidence")
