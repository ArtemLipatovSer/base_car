import tkinter as tk

def frame_state_set(frames, state):
    for frame in frames:
        for child in frame.winfo_children():
            try:
                child.delete(0, tk.END)
            except:
                pass
            child.configure(state=state)
