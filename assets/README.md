# Memory Guardian: Project Assets Descriptions

This directory contains the visual assets used in the Memory Guardian project documentation and presentations. Below are detailed descriptions, design specifications, and accessibility alternative text for each asset.

---

## 1. Architecture Diagram
* **File Path**: `assets/architecture-diagram.png`
* **Purpose**: Visualizes the multi-agent graph layout, context propagation, MCP tool isolation, and human-in-the-loop security gates.

### Visual Layout & Structure
The diagram uses a horizontal left-to-right layout to represent the sequential workflow:
1. **Input Agents (Left)**: Grouped vertically are the three telemetry collectors: `Web Activity`, `Screen Time`, and `Health Recovery`. Below them, the `Model Context Protocol (MCP) Server` is clearly labeled and shown connected.
2. **Concierge Orchestrator Agent (Center)**: The main central agent that orchestrates the workflow.
3. **Risk Scoring & Security Checkpoint (Middle)**: The `Risk Scoring Agent` and the `Security Gate Checkpoint` process the aggregated telemetry at the core of the workflow.
4. **Human-in-the-Loop Approval Gates (Right)**: Aligned vertically on the right, these gates represent the safety checks for `Low Risk`, `Medium Risk`, and `High Risk` classifications.

### Design Aesthetics & Colors
* **Theme**: Modern developer dark mode with neon accents.
* **Background**: Deep obsidian background with optimized contrast.
* **Readability**: Reduced glow intensity and clean directional arrows pointing left-to-right to improve layout clarity and text hierarchy.
* **MCP Label**: Clearly labeled as "Model Context Protocol (MCP) Server."

### Alt Text / Accessibility Description
> "A dark-mode software architecture diagram for Memory Guardian flowing from left to right. On the left, a group of three input agents (Web Activity, Screen Time, and Health Recovery) are connected to the Model Context Protocol (MCP) Server. These flow into the central Concierge Orchestrator Agent. In the middle, the Risk Scoring Agent and Security Gate Checkpoint process the metrics. On the right, the Human-in-the-Loop Approval Gates are vertically aligned and clearly labeled for Low, Medium, and High Risk."

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
