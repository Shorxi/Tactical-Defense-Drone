# Open Origin Architecture: Tactical Soft-Kill Interception (Counter-UAS)

**Lead Architect:** Emanuel Schaaf  
**Project Status:** Concept & Simulation Phase (TRL 2-3)  
**Target Application:** Civilian Infrastructure & Airport Protection  

## Executive Summary
This repository contains the simulation models, chemical frameworks, and telemetric visualizations for an asymmetric, non-lethal "Soft-Kill" drone defense system. The concept relies on mid-air, piezo-injected polymerization to neutralize hostile Unmanned Aerial Vehicles (UAVs) without explosive ordnance, thereby preventing shrapnel damage to surrounding critical infrastructure.

## Biochemical Mechanism & Physics
The system utilizes a dual-fluid kinetic injection:
* **Tank A:** Sodium Alginate - A natural, water-soluble biopolymer derived from brown algae.
* **Tank B:** Calcium Chloride - An inorganic, non-toxic cross-linking salt.

Upon mid-air collision (external impingement mixing), the fluids instantly cross-link into a high-mass, viscoelastic Calcium Alginate hydrogel. Striking the target's rapidly spinning rotors, the gel induces instantaneous aerodynamic stall and critical asymmetric weight distribution, forcing a controlled descent. The payload is 100% biodegradable, ecologically neutral, and highly cost-efficient.

## Repository Contents
1. **`simulation_engine.py`**  
   A comprehensive Python script demonstrating the physical kinematics, ballistic trajectories, and aerodynamic collapse. 
   * **Note for IT/Analysis:** The script is designed to run in headless mode (`matplotlib.use("Agg")`). It generates high-resolution MP4/GIF telemetry data and will safely fall back to PillowWriter if FFmpeg is unavailable. It requires `numpy` and `matplotlib`.

2. **`Tactical-Interception-Briefing.html`**
### Live [`> Demo <`](https://zingy-granita-d61164.netlify.app)
   A standalone, zero-dependency dashboard visualizing the tactical approach, target lock, and interception timeline. It includes an interactive scientific panel for calculating the apparent dynamic viscosity of the hydrogel using the power-law fluid model.



## Execution Guide
To run the kinematic simulation locally in a secure sandbox:

```bash
# Install dependencies
pip install numpy matplotlib scipy

# Execute the headless simulation
python simulation_engine.py
