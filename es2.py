"""
Si vuole risolvere numericamente il moto di un proiettile in aria usando un metodo del second’ordine.

L’equazione del moto è:

    m * d^2r/dt^2 = - k * v - g * versor{y}
    con: v0 = (v0 * costheta, v0 * sintheta)
         r0 = (0, 0)
    
a) Si crei una funzione che, per un k scelto dall’utente, ritorni la gittata
b) Si determini per un k fissato l’angolo θmax per cui si ottiene gittata massima
c) Si grafichi θmax in funzione di k nell’intervallo [0, 0.4]
"""

# L'idea è usare RK2 separando l'equazione del moto in due di ordine 1

import math as ma
import numpy as np
import matplotlib.pyplot as plt

#==================#
# === FUNZIONI === #
#==================#

# Divido in due funzioni:
# => m * d^2r/dt^2 = - k * v - g * versor{y}
# => *) dy/dt = v
# => *) m * dv/dt = - k * v - g * versor{y}

# => definisco:
#    X(t) = (x(t), y(t), vx(t), vy(t))
#    X'(t) = (vx(t), vy(t), - k/m * vx, - k/m * vy - g)
#    e metto tutto nello stesso array a 4 componenti in una funzione f

# FUNZIONE DA INTEGRARE
def f(t, X):
    x, y, vx, vy = X
    dxdt = vx
    dydt = vy
    dvxdt = - (k/m) * vx
    dvydt = - (k/m) * vy - g
    return np.array([dxdt, dydt, dvxdt, dvydt])
    # RICORDA => np.array([, , ,]) => crea un vettore numerico (np.array()) che contiene la lista delle derivate del mio sistema []. => lo mettiamo in un array perché sugli array possiamo fare direttamete operazioni come somme prodotti etc mentre con le liste no (le liste possono infatti contenere anche caratteri diversi dai numeri)

# RK2
dt = 0.001
def rk2_step(t, X, dt):
    k1 = f(t, X)
    k2 = f(t + 0.5 * dt, X + 0.5 * dt * k1)
    return X + dt * k2
    
""" (a), (b) """

# GITTATA
def gittata(k, theta):
    
    # Velocità iniziali
    v0x = v0 * ma.cos(theta)
    v0y = v0 * ma.sin(theta)

    # Inizializzo variabili
    t = 0
    dt = 0.01                  # Passo temporale più piccolo per maggiore precisione

    # Stato iniziale: X = [x, y, vx, vy]
    X = np.array([r0x, r0y, v0x, v0y])

    # Simulo il moto finché il corpo non tocca terra (ovvero fino a quando y è postivo o al massimo nullo)
    while X[1] >= 0:
        X = rk2_step(t, X, dt)
        t += dt

    # Quando y < 0, restituisco la coordinata x (gittata)
        
    return X[0]

#=============#
# === COST === #
#=============#

g = 9.81
m = 1 # => fisso 1kg di massa
k = float(input(f"Scegli k: "))

r0x = 0
r0y = 0

v0 = 10 # => scelgo v0 = 10 m/s

# ----------------------------

""" (b) """

# np.linspace(start, stop, num) => escludo gli estremi => crea una lista
theta_values = np.linspace(0.01, ma.pi/2 - 0.01, 1000)

gittate = []

for theta in theta_values:
    gittata_values = gittata(k, theta)
    gittate.append(gittata_values)
    
index_gittata_max = np.argmax(gittate)

theta_max = theta_values[index_gittata_max]

theta_max_gradi = theta_max * 180/(ma.pi)

print(f"Il valore di theta per massimizzare la gittata con k appena scelto dall'utente è {theta_max_gradi:.1f}°")

""" (a) """
    
print(f"La gittata per: k = {k:.1f}, è: {gittata(k, theta_max):.3f}m")

""" (c) """

print(f"Aspetta il grafico di θ_max vs k variabile ...")

# (c) θmax(k) su [0,0.4]

k_var = np.linspace(0.0, 0.4, 50)

# Riuso theta_values definito prima

theta_opt_deg = []
for ks in k_var:
    # 1) aggiorno la variabile globale k usata in f()
    k = ks

    # 2) calcolo la gittata per tutti gli angoli
    gittate = [gittata(ks, th) for th in theta_values]

    # 3) trovo l'indice della gittata massima
    idx_max = np.argmax(gittate)

    # 4) converto in gradi e salvo
    theta_opt_deg.append(theta_values[idx_max] * 180/ma.pi)

# Plotto
plt.plot(k_var, theta_opt_deg, 'o-')
plt.xlabel('k [kg/s]')
plt.ylabel('θₘₐₓ [°]')
plt.title('Angolo di gittata massima in funzione di k')
plt.grid(True)
plt.show()
