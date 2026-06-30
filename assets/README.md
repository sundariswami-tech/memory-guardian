# Memory Guardian: Project Assets Descriptions

This directory contains the visual assets used in the Memory Guardian project documentation and presentations. Below are detailed descriptions, design specifications, and accessibility alternative text for each asset.

---

## 1. Architecture Diagram
* **File Path**: `assets/architecture_diagram.png`
* **Purpose**: Visualizes the multi-agent graph layout, context propagation, MCP tool isolation, and human-in-the-loop security gates.

### Visual Layout & Structure
The diagram uses a top-down and branching layout flow to represent the sequential delegation and check-point stages:
1. **Entry Point (START)**: A glowing capsule at the top that initiates the workflow.
2. **Concierge Agent (Orchestrator)**: A central dominant node that coordinates task routing.
3. **Telemetry Layer (Parallel Sub-Agents)**: Three parallel nodes branching out of the orchestrator via solid delegation paths:
   * **WebActivityAnalyzer**
   * **ScreenTimeAgent**
   * **HealthRecoveryAgent**
4. **Model Context Protocol (MCP) Server**: A distinct, isolated container representing the stdio toolset. Dashed bidirectional lines connect the sub-agents to the synthetic metrics tools inside the MCP container.
5. **Synthesis Node (RiskScoringAgent)**: Receives the metrics from the three sub-agents, computes the final Cognitive Risk Score (0-100), and records it to the validated state.
6. **Security Gate Checkpoint**: A diamond decision gate evaluating the risk score:
   * **High Risk (>70)**: Leads to a strict HITL interrupt node (Requires Explicit Approval).
   * **Medium Risk (>50)**: Leads to a warning HITL interrupt node (Soft Warning).
   * **Low Risk (<=50)**: Leads to the auto-approved memory storage terminal node.

### Design Aesthetics & Colors
* **Theme**: Modern developer dark mode.
* **Background**: Deep obsidian/charcoal `#0d0e12` with subtle grid lines.
* **Nodes**: Sleek semi-transparent glassmorphism panels with glowing borders:
  * **Orchestrator & Sub-Agents**: Electric blue (`#3b82f6`) and violet (`#8b5cf6`) accents.
  * **MCP Boundary**: Purple (`#8b5cf6`) dashed border.
  * **Security Decisions**: Cyber green (`#10b981`) for low risk, orange/amber (`#f59e0b`) for medium risk, and crimson (`#ef4444`) for high risk.
* **Typography**: Highly legible sans-serif (e.g., Outfit or Inter).

### Alt Text / Accessibility Description
> "A dark-mode flowchart showing the Memory Guardian architecture. The flow starts at a START capsule and moves to the central Concierge Agent, which delegates to three parallel sub-agents: Web Activity Analyzer, Screen Time Agent, and Health Recovery Agent. The sub-agents fetch data from an isolated Model Context Protocol (MCP) server container. The results flow into the Risk Scoring Agent, which calculates a score and passes it to a security checkpoint decision gate. The gate routes to three outcomes depending on the score: Auto-Approved Storage (risk score 50 or below), Soft User Warning (risk score 51 to 70), and Require Explicit Approval (risk score over 70)."

---

## 2. Cover Page Banner
* **File Path**: `assets/cover_page_banner.png`
* **Purpose**: Premium branding cover image for project documentation, slides, or repository header.

### Visual Components & Composition
* **Central Motif**: A glowing, semi-transparent cybernetic shield enclosing a stylized digital human brain silhouette composed of network nodes and light pathways.
* **Background**: Matte dark-slate gradient (`#0b0c10` to `#1f2833`) overlaid with abstract flow lines, glowing node networks, and subtle vertical matrix-like data streams or binary overlays.
* **Branding Typography**: The text "Memory Guardian" is rendered in a clean, futuristic, wide sans-serif typeface, glowing in ice-blue with a subtitle: "Privacy-First Cognitive Guardrails".
* **Overall Style**: Sleek, clean, high-tech corporate branding. It emphasizes security (shield) and cognitive metrics (brain network).

### Design Aesthetics & Colors
* **Theme**: Cinematic cyber-security.
* **Primary Accents**: Cyan/Ice-blue (`#00f2fe`) and deep violet/magenta (`#4facfe`).
* **Visual Density**: Balanced; the main elements are crisp and centered, while the background maintains a high-quality ambient depth of field.

### Alt Text / Accessibility Description
> "A premium high-tech branding banner with a dark background. Centered is a glowing cyan and purple cybernetic shield enclosing a digital human brain silhouette made of interconnected node points and circuits. The text 'Memory Guardian' with the subtitle 'Privacy-First Cognitive Guardrails' is printed in a clean modern sans-serif font. The background shows floating network connections and soft glowing light trails."
