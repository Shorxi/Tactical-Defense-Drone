# Lead Architect: Emanuel Schaaf
# Open Origin Architecture
# Modul: Tactical Soft-Kill Interception & High-Fidelity Crash Simulation

import sys
import traceback

try:
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import math
    import random
except ImportError as e:
    print(f"Import Error: {e}")
    input("Press Enter to exit...")
    sys.exit(1)

def build_animation():
    # 1. Setup Canvas & Dark Mode
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#161b22')
    
    ax.grid(color='#30363d', linestyle='-', linewidth=0.5, alpha=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')
    
    ax.set_xlim(-8, 8)
    ax.set_ylim(-1, 12)
    ax.set_title("Open Origin Architecture: Taktischer Anflug & Kinetischer Soft-Kill", color="white", fontsize=14, pad=20)
    ax.set_xlabel("X-Achse (Meter)", color="white")
    ax.set_ylabel("Y-Achse (Flughöhe in Meter)", color="white")
    ax.tick_params(colors="white")

    # 2. System Constants
    fps = 30
    duration = 8.5
    frames = int(fps * duration)
    
    target_hover_x = 4.0
    target_hover_y = 8.5
    
    # 3. Initialize Artists (Plot Elements)
    # Fluids
    fluid_A, = ax.plot([], [], 'o', color='#00ffcc', markersize=4, label="Natriumalginat (Tank A)")
    fluid_B, = ax.plot([], [], 'o', color='#ff00ff', markersize=4, label="Calciumchlorid (Tank B)")
    gel_proj, = ax.plot([], [], 'o', color='#ffd700', markersize=12, label="Hydrogel Projektil")
    gel_splash, = ax.plot([], [], 'o', color='#ffd700', markersize=16, alpha=0.8)
    
    # Target Drone Parts (UAV)
    t_color = "#a8b2c1"
    t_danger = "#ff3333"
    t_body, = ax.plot([], [], '-', color=t_color, linewidth=10, solid_capstyle='round', label="Feindliche Drohne")
    t_arm_L, = ax.plot([], [], '-', color=t_color, linewidth=4)
    t_arm_R, = ax.plot([], [], '-', color=t_color, linewidth=4)
    t_motor_L, = ax.plot([], [], '-', color='#586069', linewidth=6)
    t_motor_R, = ax.plot([], [], '-', color='#586069', linewidth=6)
    t_gear, = ax.plot([], [], '-', color='#586069', linewidth=2)
    t_rotor_L1, = ax.plot([], [], '-', color=t_danger, linewidth=2)
    t_rotor_L2, = ax.plot([], [], '-', color=t_danger, linewidth=2, alpha=0.5)
    t_rotor_R1, = ax.plot([], [], '-', color=t_danger, linewidth=2)
    t_rotor_R2, = ax.plot([], [], '-', color=t_danger, linewidth=2, alpha=0.5)
    t_debris, = ax.plot([], [], 'x', color=t_color, markersize=8)

    # Interceptor Drone Parts (Abfangdrohne)
    i_color = "#24292e"
    i_accent = "#00ffcc"
    i_body, = ax.plot([], [], '-', color=i_color, linewidth=12, solid_capstyle='round', label="Interceptor (Open Origin)")
    i_arm_L, = ax.plot([], [], '-', color=i_color, linewidth=5)
    i_arm_R, = ax.plot([], [], '-', color=i_color, linewidth=5)
    i_motor_L, = ax.plot([], [], '-', color=i_accent, linewidth=4)
    i_motor_R, = ax.plot([], [], '-', color=i_accent, linewidth=4)
    i_nozzle, = ax.plot([], [], '-', color='#ff00ff', linewidth=3)
    i_rotor_L1, = ax.plot([], [], '-', color=i_accent, linewidth=2)
    i_rotor_L2, = ax.plot([], [], '-', color=i_accent, linewidth=2, alpha=0.5)
    i_rotor_R1, = ax.plot([], [], '-', color=i_accent, linewidth=2)
    i_rotor_R2, = ax.plot([], [], '-', color=i_accent, linewidth=2, alpha=0.5)
    
    # Telemetry HUD
    status_box = ax.text(-7.5, 10.8, "INITIALIZING...", color="white", fontsize=10, 
                         fontfamily='monospace', bbox=dict(facecolor='#161b22', edgecolor='#30363d', alpha=0.9))
    
    ax.legend(facecolor='#161b22', edgecolor='#30363d', labelcolor='white', loc='upper left', fontsize=9, bbox_to_anchor=(0.0, 0.95))

    # 4. Helper Functions & Geometry
    def rotate_point(px, py, cx, cy, angle):
        s = math.sin(angle)
        c = math.cos(angle)
        px -= cx
        py -= cy
        return (px * c - py * s) + cx, (px * s + py * c) + cy

    def transform_geo(geometry, cx, cy, angle):
        tx, ty = [], []
        for px, py in geometry:
            nx, ny = rotate_point(px + cx, py + cy, cx, cy, angle)
            tx.append(nx)
            ty.append(ny)
        return tx, ty

    # Base geometries relative to (0,0)
    geo_t_body = [(-0.4, 0), (0.4, 0)]
    geo_t_arm_L = [(-0.4, 0), (-1.4, 0)]
    geo_t_arm_R = [(0.4, 0), (1.4, 0)]
    geo_t_motor_L = [(-1.4, -0.1), (-1.4, 0.2)]
    geo_t_motor_R = [(1.4, -0.1), (1.4, 0.2)]
    geo_t_gear = [(-0.3, 0), (-0.5, -0.5), (0.0, -0.5), (0.5, -0.5), (0.3, 0)]

    geo_i_body = [(-0.5, 0), (0.5, 0)]
    geo_i_arm_L = [(-0.5, 0), (-1.2, 0.2)] # Angled arms for aggressive look
    geo_i_arm_R = [(0.5, 0), (1.2, 0.2)]
    geo_i_motor_L = [(-1.2, 0.1), (-1.2, 0.4)]
    geo_i_motor_R = [(1.2, 0.1), (1.2, 0.4)]
    geo_i_nozzle = [(0.0, 0.0), (0.3, 0.4)] # Pointing forward/up

    # 5. Physics State Variables
    shot_starts = np.linspace(3.5, 3.9, 5) # Time sequence when interceptor fires
    debris_particles = []

    def update(frame):
        t = frame / fps
        
        # --- INTERCEPTOR FLIGHT PATH ---
        i_cx, i_cy, i_angle = 0, 0, 0
        if t < 2.5:
            # Approach Phase (Smooth interpolation from bottom left to firing position)
            progress = t / 2.5
            ease = progress * progress * (3 - 2 * progress) # Smoothstep
            i_cx = -6.0 + ease * 4.0 # Ends at -2.0
            i_cy = 2.0 + ease * 5.5  # Ends at 7.5
            i_angle = -0.3 * (1 - ease) # Tilts forward during flight, levels out
        else:
            # Hover & Aim Phase
            i_cx = -2.0 + math.sin(t*2)*0.02
            i_cy = 7.5 + math.cos(t*2)*0.02
            i_angle = 0.15 # Tilted up to aim at target
            
        # Get absolute nozzle position for fluid emission
        nozzle_tip_x, nozzle_tip_y = rotate_point(0.3 + i_cx, 0.4 + i_cy, i_cx, i_cy, i_angle)
        nozzle_base_A_x, nozzle_base_A_y = rotate_point(0.2 + i_cx, 0.4 + i_cy, i_cx, i_cy, i_angle)
        nozzle_base_B_x, nozzle_base_B_y = rotate_point(0.4 + i_cx, 0.4 + i_cy, i_cx, i_cy, i_angle)
        collision_point = (1.5, 8.3) # Point in air where fluids mix

        # --- TARGET FLIGHT PATH (UAV) ---
        t_cx = target_hover_x
        t_cy = target_hover_y + math.sin(t * 3) * 0.05
        t_angle = 0.0
        r_fail = False
        crashed = False
        hit_registered = False

        # --- FLUID DYNAMICS ---
        xa, ya, xb, yb, xg, yg = [], [], [], [], [], []
        
        for start_t in shot_starts:
            if t > start_t:
                dt = t - start_t
                f_speed = 18.0
                dist_to_col = math.sqrt((collision_point[0]-nozzle_tip_x)**2 + (collision_point[1]-nozzle_tip_y)**2)
                t_to_col = dist_to_col / f_speed
                
                if dt < t_to_col:
                    # Pre-collision (Fluids separate)
                    ratio = dt / t_to_col
                    xa.append(nozzle_base_A_x + ratio * (collision_point[0] - nozzle_base_A_x))
                    ya.append(nozzle_base_A_y + ratio * (collision_point[1] - nozzle_base_A_y))
                    xb.append(nozzle_base_B_x + ratio * (collision_point[0] - nozzle_base_B_x))
                    yb.append(nozzle_base_B_y + ratio * (collision_point[1] - nozzle_base_B_y))
                else:
                    # Post impingement (Gel block)
                    dt_gel = dt - t_to_col
                    g_x = collision_point[0] + dt_gel * 18.0
                    g_y = collision_point[1] + dt_gel * 4.0 - 0.5 * 9.81 * (dt_gel**2)
                    
                    if g_x < target_hover_x + 0.5:
                        xg.append(g_x)
                        yg.append(g_y)
                    else:
                        hit_registered = True

        fluid_A.set_data(xa, ya)
        fluid_B.set_data(xb, yb)
        gel_proj.set_data(xg, yg)

        # --- TELEMETRY & TARGET STATE MACHINE ---
        status = "SYS: STANDBY"
        color_hud = "white"

        if t < 2.5:
            status = "SYS: TARGET ACQUIRED\nACT: INTERCEPTOR APPROACH\nSPD: MACH 0.2"
            color_hud = "#00ffcc"
        elif t >= 2.5 and t < shot_starts[0]:
            status = "SYS: IN POSITION\nACT: TARGET LOCK SECURED\nARM: PIEZO INJECTORS READY"
            color_hud = "#ffd700"
        elif t >= shot_starts[0] and not hit_registered:
            status = "SYS: FIRING PAYLOAD\nACT: 2K-POLYMER INJECTION\nSTS: LAMINAR DOWNWASH"
            color_hud = "#ff00ff"
            
        time_since_hit = 0
        if hit_registered:
            first_hit_t = shot_starts[0] + (math.sqrt((collision_point[0]-nozzle_tip_x)**2 + (collision_point[1]-nozzle_tip_y)**2) / 18.0) + ((target_hover_x + 0.5 - collision_point[0])/18.0)
            time_since_hit = t - first_hit_t
            
            if time_since_hit > 0:
                r_fail = True
                status = "SYS: GEL IMPACT CONFIRMED\nERR: RIGHT ROTOR BLOCKED\nERR: MASS ASYMMETRY\nERR: CRITICAL STALL"
                color_hud = "#ff00ff"
                
                # Falling Physics
                t_cy = target_hover_y - 0.5 * 9.81 * (time_since_hit ** 2)
                t_angle = 0.5 * 12.0 * (time_since_hit ** 2) # Tumble clockwise
                t_cx = target_hover_x + 1.5 * time_since_hit # Drift right
                
                if t_cy <= 0.4:
                    t_cy = 0.4
                    crash_t = math.sqrt((target_hover_y - 0.4) / (0.5 * 9.81))
                    t_angle = 0.5 * 12.0 * (crash_t ** 2)
                    t_cx = target_hover_x + 1.5 * crash_t
                    crashed = True
                    status = "SYS: TARGET NEUTRALIZED\nRES: KINETIC DESTRUCTION\nACT: MISSION ACCOMPLISHED"
                    color_hud = "#ffd700"

                    if not debris_particles:
                        for _ in range(12):
                            debris_particles.append({
                                'x': t_cx, 'y': t_cy,
                                'vx': random.uniform(-5, 5),
                                'vy': random.uniform(3, 8)
                            })

        # --- RENDER TARGET DRONE ---
        b_x, b_y = transform_geo(geo_t_body, t_cx, t_cy, t_angle)
        t_body.set_data(b_x, b_y)
        al_x, al_y = transform_geo(geo_t_arm_L, t_cx, t_cy, t_angle)
        t_arm_L.set_data(al_x, al_y)
        ar_x, ar_y = transform_geo(geo_t_arm_R, t_cx, t_cy, t_angle)
        t_arm_R.set_data(ar_x, ar_y)
        ml_x, ml_y = transform_geo(geo_t_motor_L, t_cx, t_cy, t_angle)
        t_motor_L.set_data(ml_x, ml_y)
        mr_x, mr_y = transform_geo(geo_t_motor_R, t_cx, t_cy, t_angle)
        t_motor_R.set_data(mr_x, mr_y)
        g_x, g_y = transform_geo(geo_t_gear, t_cx, t_cy, t_angle)
        t_gear.set_data(g_x, g_y)

        if not crashed:
            w_L = 0.7 if (frame % 2 == 0) else 0.2
            rlx, rly = transform_geo([(-1.4 - w_L/2, 0.25), (-1.4 + w_L/2, 0.25)], t_cx, t_cy, t_angle)
            t_rotor_L1.set_data(rlx, rly); t_rotor_L2.set_data(rlx, [y + 0.05 for y in rly])
        else:
            t_rotor_L1.set_data([], []); t_rotor_L2.set_data([], [])

        if not r_fail and not crashed:
            w_R = 0.7 if (frame % 2 == 0) else 0.2
        elif r_fail and not crashed:
            w_R = 0.7 # Stopped
        else:
            w_R = 0
            
        if not crashed:
            rrx, rry = transform_geo([(1.4 - w_R/2, 0.25), (1.4 + w_R/2, 0.25)], t_cx, t_cy, t_angle)
            t_rotor_R1.set_data(rrx, rry)
            if not r_fail: t_rotor_R2.set_data(rrx, [y + 0.05 for y in rry])
            else: t_rotor_R2.set_data([], [])
        else:
            t_rotor_R1.set_data([], []); t_rotor_R2.set_data([], [])

        if r_fail:
            sx, sy = transform_geo([(1.4, 0.2), (1.2, 0.1), (1.5, 0.0)], t_cx, t_cy, t_angle)
            gel_splash.set_data(sx, sy)
        else:
            gel_splash.set_data([], [])

        if crashed:
            deb_x, deb_y = [], []
            t_deb = time_since_hit - crash_t
            for p in debris_particles:
                nx = p['x'] + p['vx'] * t_deb
                ny = p['y'] + p['vy'] * t_deb - 0.5 * 9.81 * (t_deb**2)
                if ny < 0: ny = 0
                deb_x.append(nx); deb_y.append(ny)
            t_debris.set_data(deb_x, deb_y)
        else:
            t_debris.set_data([], [])

        # --- RENDER INTERCEPTOR DRONE ---
        ib_x, ib_y = transform_geo(geo_i_body, i_cx, i_cy, i_angle)
        i_body.set_data(ib_x, ib_y)
        ial_x, ial_y = transform_geo(geo_i_arm_L, i_cx, i_cy, i_angle)
        i_arm_L.set_data(ial_x, ial_y)
        iar_x, iar_y = transform_geo(geo_i_arm_R, i_cx, i_cy, i_angle)
        i_arm_R.set_data(iar_x, iar_y)
        iml_x, iml_y = transform_geo(geo_i_motor_L, i_cx, i_cy, i_angle)
        i_motor_L.set_data(iml_x, iml_y)
        imr_x, imr_y = transform_geo(geo_i_motor_R, i_cx, i_cy, i_angle)
        i_motor_R.set_data(imr_x, imr_y)
        inoz_x, inoz_y = transform_geo(geo_i_nozzle, i_cx, i_cy, i_angle)
        i_nozzle.set_data(inoz_x, inoz_y)

        iw_L = 0.8 if (frame % 2 == 0) else 0.3
        irlx, irly = transform_geo([(-1.2 - iw_L/2, 0.45), (-1.2 + iw_L/2, 0.45)], i_cx, i_cy, i_angle)
        i_rotor_L1.set_data(irlx, irly); i_rotor_L2.set_data(irlx, [y + 0.05 for y in irly])
        
        iw_R = 0.8 if (frame % 2 == 0) else 0.3
        irrx, irry = transform_geo([(1.2 - iw_R/2, 0.45), (1.2 + iw_R/2, 0.45)], i_cx, i_cy, i_angle)
        i_rotor_R1.set_data(irrx, irry); i_rotor_R2.set_data(irrx, [y + 0.05 for y in irry])

        # Update HUD
        status_box.set_text(status)
        status_box.set_color(color_hud)

        return (fluid_A, fluid_B, gel_proj, gel_splash, 
                t_body, t_arm_L, t_arm_R, t_motor_L, t_motor_R, t_gear, t_debris,
                t_rotor_L1, t_rotor_L2, t_rotor_R1, t_rotor_R2,
                i_body, i_arm_L, i_arm_R, i_motor_L, i_motor_R, i_nozzle,
                i_rotor_L1, i_rotor_L2, i_rotor_R1, i_rotor_R2,
                status_box)

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=33, blit=True)

    # 6. Strict Export Protocol
    writer_video = animation.FFMpegWriter(fps=fps, bitrate=3000)
    writer_gif = animation.PillowWriter(fps=fps)
    
    file_prefix = "open_origin_tactical_interception"
    
    try:
        print(f"Starte physikalische Simulation und MP4-Export ({file_prefix}.mp4)...")
        ani.save(f"{file_prefix}.mp4", writer=writer_video)
        print(f"Exported MP4 successfully: {file_prefix}.mp4")
    except Exception as e:
        print(f"FFMpeg failed: {e}. Falling back to GIF...")
        try:
            ani.save(f"{file_prefix}.gif", writer=writer_gif)
            print(f"Exported GIF successfully: {file_prefix}.gif")
        except Exception as gif_err:
            print(f"GIF fallback failed: {gif_err}")
    finally:
        plt.close(fig)

def run_simulation():
    print("Initialize System: Open Origin Architecture")
    print("Modul: Full Tactical Interception Sequence")
    try:
        build_animation()
    except KeyboardInterrupt:
        print("\nProcess aborted by user.")
    except Exception as e:
        print(f"\nRuntime error during execution: {e}")
        traceback.print_exc()
    finally:
        input("\nPress Enter to close window and exit...")

if __name__ == "__main__":
    run_simulation()