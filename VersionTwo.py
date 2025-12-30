import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle
from matplotlib.widgets import Slider

# ---------------- Figure ----------------
fig, (ax_mech, ax_plot_pv , ax_plot_ts) = plt.subplots(1,3, figsize=(14, 6))
plt.subplots_adjust(bottom=0.20)

ax_mech.set_xlim(0, 1)
ax_mech.set_ylim(0, 1)
ax_mech.set_aspect('equal')
ax_mech.axis('off')

y_offset = 0.4

# ---------------- Regenerator --------------
regenerator = Rectangle(
    (0.35,0.071 + y_offset),
    0.15,
    0.2,
    facecolor = 'white',
    edgecolor = 'black',
    linewidth = 2
)
ax_mech.add_patch(regenerator)

regenerator_text = ax_mech.text(
    0.40,0.171 + y_offset,
    "R",
    fontsize = 20,
    verticalalignment = 'center'
)

# ---------------- Static cylinder1 ----------------
cylinder1 = Rectangle(
    (0.05, 0.1 + y_offset),   # bottom-left corner
    0.30,          # width
    0.15,          # height
    fill=False,
    linewidth=2
)
ax_mech.add_patch(cylinder1)

cylinder1_text = ax_mech.text(
    0.05, 0.05 + y_offset,
    "Compressor",
    fontsize = 10,
    verticalalignment = 'center'
)


# ---------------- Static cylinder2 ----------------
cylinder2 = Rectangle(
    (0.5, 0.1 + y_offset),   # bottom-left corner
    0.30,          # width
    0.15,          # height
    fill=False,
    linewidth=2
)
ax_mech.add_patch(cylinder2)

cylinder2_text = ax_mech.text(
    0.55,0.05 + y_offset,
    "Expander",
    fontsize = 10,
    verticalalignment = 'center'
)

# ---------------- Piston1 ----------------
piston_width = 0.04
piston1 = Rectangle(
    (0.054, 0.101 + y_offset),   # initial position
    piston_width,
    0.15,
    color='gray'
)
ax_mech.add_patch(piston1)

# --------------- Piston2 ----------------

piston2 = Rectangle(
    (0.753, 0.101 + y_offset),
    piston_width,
    0.15,
    color = 'gray'
)
ax_mech.add_patch(piston2)


# ----------------- Slider ------------------

slider_ax = fig.add_axes([0.09,y_offset - 0.08,0.24,0.04])
slider = Slider(
    ax=slider_ax,
    label='Cycle Position',
    #valmin=0.054,
    #valmax=0.054 + 0.3 - piston_width - 0.01 ,
    #valinit=0.054
    valmin = 0,
    valmax = 1,
    valinit = 0
)

# ---------------- P-V -----------------
ax_plot_pv.set_title("P-V Diagram")
ax_plot_pv.set_xlabel("V")
ax_plot_pv.set_ylabel("P")
ax_plot_pv.tick_params(
    axis = 'both',
    which = 'both',
    labelbottom = False,
    labelleft = False
)
pv_point, = ax_plot_pv.plot([],[],'b-')

R = 8.314
vmax_c = 1
vmax_e = 1
v_dead = 0.01
T_c = 10 + 273.15
T_h = 100 + 273.15
# 1-2 
v_12 = np.linspace(vmax_c,vmax_c*0.5,20)
p_12 = R*T_c/v_12
#ax_plot_pv.plot(v_12,p_12,'b')

# 2-3
T_23 = np.linspace(T_c,T_h,20)
v_23 = vmax_c * 0.5 + (T_23)*0
p_23 = R*T_23/v_23
#ax_plot_pv.plot(v_23,p_23,'b')

# 3-4
v_34 = np.linspace(vmax_c*0.5,vmax_e,20)
p_34 = R*T_h/v_34
#ax_plot_pv.plot(v_34,p_34,'b')

# 4-1
T_41 = np.linspace(T_h,T_c,20)
v_41 = vmax_e + 0*(T_41)
p_41 = R*T_41/v_41
#ax_plot_pv.plot(v_41,p_41,'b')

v_t = []
v_t.extend(v_12)
v_t.extend(v_23)
v_t.extend(v_34)
v_t.extend(v_41) 
p_t = []
p_t.extend(p_12)
p_t.extend(p_23)
p_t.extend(p_34)
p_t.extend(p_41)

ax_plot_pv.set_xlim(min(v_t)*0.75, max(v_t) *1.25)
ax_plot_pv.set_ylim(min(p_t)*0.75 , max(p_t)*1.25)
pv_point.set_data(v_t[:],p_t[:])
#fig.canvas.draw_idle()

# -------------- T-S Diagram --------------
ax_plot_ts.set_title("T-S Diagram")
ax_plot_ts.set_xlabel("S")
ax_plot_ts.set_ylabel("T")
ax_plot_ts.tick_params(
    axis = 'both',
    which = 'both',
    labelbottom = False,
    labelleft = False
)
ts_point, = ax_plot_ts.plot([],[],'b-')

R = 0.287
cp = 1.005
s1 = 0.5 

s_12 = s1-R * np.log(p_12/p_12[0])
s_23 = s_12[-1] + cp*np.log(T_23/T_c) - R*np.log(p_23/p_12[-1])
s_34 = s_23[-1] - R*np.log(p_34/p_23[-1])
s_41 = s_34[-1] + cp*np.log(T_41/T_h) - R*np.log(p_41/p_34[-1])
#print(s_41)

s_t = []
T_t = []
s_t.extend(s_12)
s_t.extend(s_23)
s_t.extend(s_34)
s_t.extend(s_41)
T_12 = np.zeros(len(p_12)) + T_c
T_t.extend(T_12)
T_t.extend(T_23)
T_34 = np.zeros(len(p_34)) + T_h
T_t.extend(T_34)
T_t.extend(T_41)

ax_plot_ts.set_xlim(min(s_t)*0.75, max(s_t) *1.25)
ax_plot_ts.set_ylim(min(T_t)*0.75 , max(T_t)*1.25)
ts_point.set_data(s_t[:],T_t[:])

# ---------------- Labeling ----------------

# PV
pv_text1 = ax_plot_pv.text(
    0.70, 0.075,
    "1",
    transform=ax_plot_pv.transAxes,
    fontsize=10,
    verticalalignment='top',
)

pv_text2 = ax_plot_pv.text(
    0.1, 0.47,
    "2",
    transform=ax_plot_pv.transAxes,
    fontsize=10,
    verticalalignment='top',
)

pv_text3 = ax_plot_pv.text(
    0.1, 0.75,
    "3",
    transform=ax_plot_pv.transAxes,
    fontsize=10,
    verticalalignment='top',
)

pv_text4 = ax_plot_pv.text(
    0.7, 0.27,
    "4",
    transform=ax_plot_pv.transAxes,
    fontsize=10,
    verticalalignment='top',
)

# TS

ts_text1 = ax_plot_ts.text(
    0.43, 0.27,
    "1",
    transform=ax_plot_ts.transAxes,
    fontsize=10,
    verticalalignment='top',
)

ts_text2 = ax_plot_ts.text(
    0.1, 0.27,
    "2",
    transform=ax_plot_ts.transAxes,
    fontsize=10,
    verticalalignment='top',
)

ts_text3 = ax_plot_ts.text(
    0.38, 0.67,
    "3",
    transform=ax_plot_ts.transAxes,
    fontsize=10,
    verticalalignment='top',
)

ts_text4 = ax_plot_ts.text(
    0.73, 0.67,
    "4",
    transform=ax_plot_ts.transAxes,
    fontsize=10,
    verticalalignment='top',
)


# ---------------- Position ----------------
def position(val):
    compressor_position = 0
    expander_position = 0
    if val < (2/5):
        compressor_position = 2.5*val
    elif (val >= (2/5)) and (val < (3/5)):
        compressor_position = 1
    elif (val <= 1 ) and (val >= (3/5)):
        compressor_position = 1 - 2.5*(val - (3/5))
    
    if val < (1/5):
        expander_position = 0
    elif (val >= (1/5)) and (val < (3/5)):
        expander_position = 2.5*(val-(1/5))
    elif (val >= (3/5)) and (val <= 1):
        expander_position = 1 - 2.5*(val - (3/5))

    return [compressor_position,expander_position]

# ---------------- Red Dot -----------------

pv_dot, = ax_plot_pv.plot([],[],'ro', markersize = 6)
ts_dot, = ax_plot_ts.plot([],[],'ro', markersize = 6)
N_pv = len(p_t)
N_ts = len(T_t)

def x_to_index(x):
    N_process = len(p_12)
    n = 0
    if x<(1/5):
        n = int((x - 0)/((1/5) - 0)*(N_process-1))
    elif (x>=(1/5)) and (x<(2/5)):
        n = int((x - (1/5))/((2/5) - (1/5))*(N_process)) + N_process
    elif (x>=(2/5)) and (x < (3/5)):
        n = int((x - (2/5))/((3/5)-(2/5))*(N_process-1)) + 2*N_process
    elif (x>=(3/5)) and (x<=1):
        n = int((x-(3/5))/((1 - (3/5)))*(N_process-1)) + 3*N_process
    return n
# ---------------- Callback ----------------

last_val = {"x":None}

def update(val):
    if last_val["x"] is not None:
        if abs(val - last_val["x"]) < 1e-2:
            return
    [cp,ex] = position(slider.val) 
    cp = 0.25*cp + 0.054
    ex = 0.25*ex + 0.504 
    piston1.set_x(cp)
    piston2.set_x(ex)
    i = x_to_index(slider.val)
    pv_dot.set_data([v_t[i]],[p_t[i]])
    ts_dot.set_data([s_t[i]],[T_t[i]])
    fig.canvas.draw_idle()

# animation = FuncAnimation(
#     fig,
#     update,
#     frames=len(t),
#     interval=30,
#     blit=True
# )

slider.on_changed(update)

# ----------------- Animation ----------------

frames = np.linspace(0,1,120)

def animated(frame_val):
    slider.set_val(frame_val)
    return piston1,piston2,pv_point,ts_point

animation = FuncAnimation(
    fig,
    animated,
    frames=frames,
    interval = 40,
    blit = False
)

writer = PillowWriter(fps = 25)
animation.save("AlphaStirlingEngineFunction.gif", writer=writer)


plt.show()
