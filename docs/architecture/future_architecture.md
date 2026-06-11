# Future Architecture

## Strategic Technical Evolution

PropSim's next-generation architecture (v2.0 - v3.0) focuses on three pillars:

1. **Real-time Physics Simulation using WebGPU**
   - Offload heavy plasma particle-in-cell (PIC) and CFD thermal simulations to client-side GPUs.
   - Reduce server-side execution costs by leveraging browser-level compute via WebAssembly + WebGPU.

2. **Federated Simulation Nodes**
   - Secure distributed simulation network for government and enterprise customers.
   - Run classified or proprietary thruster calculations on on-premise hardware nodes while aggregating results via encrypted federated links.

3. **Blockchain-based Telemetry Audits**
   - Append-only cryptographic ledger for recording simulation logs.
   - Ensure end-to-end data integrity for military and regulatory validation reporting.
