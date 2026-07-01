# Memory Guardian: Project Assets Descriptions

This directory contains the visual assets used in the Memory Guardian project documentation and presentations. Below are detailed descriptions, design specifications, and accessibility alternative text for each asset.

---

## 1. Color-Coded Architecture Diagram
* **File Path**: `assets/architecture-diagram-color.png`
* **Purpose**: Visualizes the multi-agent graph layout, context propagation, MCP tool isolation, and human-in-the-loop security gates with risk-based color-coding.

### Visual Layout & Structure
The diagram uses a horizontal left-to-right layout to represent the sequential workflow:
1. **Input Agents (Left)**: Grouped vertically are the three telemetry collectors: `Web Activity`, `Screen Time`, and `Health Recovery` along with the `Model Context Protocol (MCP) Server`. They are represented as blue (#4DA3FF) rectangles.
2. **Concierge Orchestrator Agent (Center)**: The central hub agent that coordinates telemetry collection. Represented as a cyan (#00FFFF) circle.
3. **Risk Scoring & Security Checkpoint (Middle-Right)**: The `Risk Scoring Agent` and `Security Gate Checkpoint` process metrics. Represented as purple (#A66BFF) rectangles.
4. **Human-in-the-Loop Approval Gates (Right)**: Aligned vertically on the right, representing the safety gates:
   * **Low Risk** gate (green, #00CC66, rounded rectangle)
   * **Medium Risk** gate (orange, #FF9933, rounded rectangle)
   * **High Risk** gate (red, #FF3333, rounded rectangle)

### Design Aesthetics & Colors
* **Theme**: Modern developer dark mode with minimal glow.
* **Title**: "Memory Guardian Architecture — Color-Coded Risk Flow"
* **Arrow Labels**: Annotated with "data flow", "risk evaluation", and "approval decision" to guide the viewer through the telemetry-to-decision pipeline.
* **Legend**: Mapped shape to role: Agents (rectangles), Orchestrator (circle), Gates (rounded rectangles).

### Alt Text / Accessibility Description
> "A color-coded software architecture diagram for Memory Guardian flowing from left to right on a deep black background. On the left, Input Agents and the MCP Server are colored blue (#4DA3FF). They connect to the central Concierge Orchestrator, represented as a cyan (#00FFFF) circle. The data flows into the Risk Scoring and Security Checkpoint (purple rectangles, #A66BFF). From there, the evaluation branches into Low Risk (green, #00CC66), Medium Risk (orange, #FF9933), or High Risk (red, #FF3333) human-in-the-loop gates."


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
