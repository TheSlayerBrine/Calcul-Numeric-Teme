from Interfata.tema_x import IterationBase
from tkinter import Toplevel,Label
from Tema1.implementation_1 import *

def show_machine_precision():
    u = placeholder_function()
    if u != 0:
        return f"cea mai mica precizie masina calculata in functie de puterile lui 10 este {u}"
    else:
        return f"exista precizie masina mai mica decat {u} scrisa ca o putere a lui 10"
    
def show_associativity_verification():
    u = placeholder_function()
    result, left, right = verify_associativity(u)
    if result == True: 
        return f"Adunarea este asociativa, {left} = {right}"
    else:
        return f"Adunarea nu este asociativa, {left} != {right}"
    
def show_polynomials():
    sorted_polynomials,sorted_timing=compute_sin()
    hierarchy = f"Ierarhia este: \n"
    for idx, (P, freq) in enumerate(sorted_polynomials, 1):
        hierarchy+=f"Polinomul {P} - Apărut de {freq} ori în top 3\n"
    
    hierarchy+="\nTimpul de execuție pentru fiecare polinom (ordine crescătoare):\n"
    for P, t in sorted_timing:
        hierarchy+=f"{P}: {t:.15f} secunde\n"
    return hierarchy

class Iteration1(IterationBase):
    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("1024x576")
        w.configure(bg="#6F7172")
        w.title("Iteration 1")
        
        Iteration1.newButton(w, 0.5, 0.3, "Iteration 1 - Action 1", "White", "#426E93", show_machine_precision)
        Iteration1.newButton(w, 0.5, 0.4, "Iteration 1 - Action 2", "White", "#426E93", show_associativity_verification)
        Iteration1.newButton(w, 0.5, 0.5, "Iteration 1 - Action 3", "White", "#426E93", show_polynomials)

        
        
            
