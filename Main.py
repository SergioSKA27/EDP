import streamlit as st
import sympy as sp
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
import re
from sympy.abc import x,y
#Autor: Sergio Demis Lopez Martinez


st.header('Método de Isoclinas')

#---------------------------Data input---------------------------
fx = st.text_input(r'Ingrese la ecuacion en la forma $\frac{dy}{dx} = f(x,y)$','x*y')
func = sp.parse_expr(fx,transformations='all')
st.latex(r'\frac{dy}{dx} = '+sp.latex(func))
#x,y = sp.symbols('x,y')
ft = sp.lambdify((x, y), func)


cvalues = st.text_input(r'Ingrese los valores de $c$','-3...3')

if re.search('...', cvalues):
    mn,mx = cvalues.split('...')
    vals = range(int(mn),int(mx)+1)
else:
    vals = list(map(float, cvalues.split(',')))

st.write(vals)


col1,col2 = st.columns(2)

with col1:
    x_rango1 = st.number_input(r'Ingrese el valor minimo de $x$',min_value=-10,max_value=10,value=-3)
    x_rango2 = st.number_input(r'Ingrese el valor maximo de $x$',min_value=-10,max_value=10,value=3)

with col2:
    y_rango1 = st.number_input(r'Ingrese el valor minimo de $y$',min_value=-10,max_value=10,value=-3)
    y_rango2 = st.number_input(r'Ingrese el valor maximo de $y$',min_value=-10,max_value=10,value=3)


x_vals = np.linspace(x_rango1, x_rango2, 100)
y_vals = np.linspace(y_rango1, y_rango2, 100)
xx, yy = np.meshgrid(x_vals, y_vals)
zz = ft(xx,yy)

c = 1


fig = go.Figure()
colors = []

for i in vals:
    random_color = f'rgb({random.randint(1, 255)}, {random.randint(1, 255)}, {random.randint(1, 255)})'
    if random_color in colors:
        random_color = f'rgb({random.randint(1, 255)}, {random.randint(1, 255)}, {random.randint(1, 255)})'
    colors.append(random_color)
    fig.add_trace(go.Contour(
        x=x_vals,
        y=y_vals,
        z=zz,
        colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],  # Transparent color scale
        showscale=False,
        contours=dict(
            start=i,
            end=i,
            size=0.1
        ),
        line=dict(
            color=random_color,  # Color of the contour line
            width=3          # Width of the contour line
        ),
    ))


for i in vals:
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', line=dict(color=colors[i]),name='c = '+str(i)))

fig.add_vline(x=0, line_width=1)
fig.add_hline(y=0, line_width=1)

fig.update_layout(
    xaxis_title='X',
    yaxis_title='Y',
    title=f'Directional Field with Names for the implicit function f(x, y) = {c} in 2D',
)


st.plotly_chart(fig)
f = sp.symbols('f', cls=sp.Function)
eq = st.text_input(r'Ingrese la ecuación diferencial','Derivative(f(x), x) + 2*f(x)')
diff_eq_str = sp.parse_expr(eq)

st.latex(sp.latex(diff_eq_str))
st.latex(sp.latex(sp.dsolve(diff_eq_str).free_symbols))
st.write(diff_eq_str.free_symbols)
