# Calculadora-de-pseudonumeros
Calculadora con 3 tipos de algoritmos generadores de numeros pseudoaleatorios y pruebas estadisticas

# Calculadora de Pseudonúmeros  

Este proyecto es una **calculadora de números pseudoaleatorios** implementada en **Python (Tkinter + NumPy + Matplotlib + SciPy)**.  
Permite generar secuencias de pseudonúmeros mediante distintos **algoritmos clásicos** y aplicar sobre ellos **tres pruebas estadísticas fundamentales**.  

---
- **Menu principal** se puede escoger entre 3 opciones mediante tres algoritmos:
  1. Cuadrados medios (1 semilla).  
  2. Producto medio (2 semillas).  
  3. Multiplicador constante.  

- **Pruebas estadísticas integradas**:
  1. Prueba de medias → verifica si la media se acerca a la esperada (0.5 en uniforme(0,1)).  
  2. Prueba de varianza → compara la varianza obtenida con la teórica (1/12 en uniforme(0,1)).  
  3. Prueba de uniformidad (Chi-cuadrado) → evalúa si los números se distribuyen de forma uniforme en intervalos.  

- **Visualización gráfica**:
  - Histogramas de números, medias y varianzas.  

- **Exportación de resultados**:
  - Guardado en txt con su procedimiento 

---

## Tecnologías utilizadas
El proyecto utiliza las siguientes librerías de Python:  

```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pypandoc
from scipy.stats import chi2, norm
import os
import subprocess

## Herramientas
OpenAI. (2025). ChatGPT (GPT-5 mini) [Large language model]. https://openai.com/chatgpt
import sys

