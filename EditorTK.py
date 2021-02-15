import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter import filedialog
import sys
import os
import threading
import platform
import subprocess
import BWSISOEditor
from BWSTableEditors import SetLanguageUsed, LanguageUsed


def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def main():

    def lock_window():
        pass

    def unlock_window():
        pass

    window = tk.Tk()
    window.title("Berwick Saga Editor")
    window.resizable(height=False, width=False)

    title_font = tkFont.Font(family="Helvetica", size=24)
    ui_font = tkFont.Font(family="Helvetica", size=11)
    script_font = tkFont.Font(family="Monaco", size=11)

    source_rom = tk.StringVar(value="")
    target_rom = tk.StringVar(value="")

    def select_src():
        file = filedialog.askopenfilename(initialdir=sys.argv[0], title="Select Source Rom", filetypes=(("iso files", "*.iso"),))
        source_rom.set(file)

    def select_tar():
        file = filedialog.asksaveasfilename(initialdir=sys.argv[0], title="Save Target Rom", filetypes=(("iso files", "*.iso"),))
        if not file.endswith(".iso"):
            file += ".iso"
        target_rom.set(file)

    main_frame = tk.Frame(window)
    main_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(main_frame, text="Berwick Saga Editor", font=title_font).pack()

    f_frame1 = tk.Frame(main_frame)
    f_frame1.pack()
    tk.Label(f_frame1, text="Source ROM (.iso):", font=ui_font).pack(side=tk.LEFT)
    src_ent = tk.Entry(f_frame1, textvariable=source_rom, font=ui_font)
    src_btn = tk.Button(f_frame1, text="Select", font=ui_font, command=select_src)
    src_ent.pack(side=tk.LEFT)
    src_btn.pack(side=tk.LEFT)

    f_frame2 = tk.Frame(main_frame)
    f_frame2.pack()
    tk.Label(f_frame2, text="Target ROM (.iso):", font=ui_font).pack(side=tk.LEFT)
    tar_ent = tk.Entry(f_frame2, textvariable=target_rom, font=ui_font)
    tar_btn = tk.Button(f_frame2, text="Save As", font=ui_font, command=select_tar)
    tar_ent.pack(side=tk.LEFT)
    tar_btn.pack(side=tk.LEFT)

    use_translation = tk.BooleanVar(value=LanguageUsed == 1)

    def SetTranslationPatch():
        SetLanguageUsed(1) if use_translation.get() else SetLanguageUsed(0)

    use_translation_box = tk.Checkbutton(main_frame, font=ui_font, text="Use Translation Patch", command=SetTranslationPatch, variable=use_translation)
    use_translation_box.pack()

    script_box = tk.Text(main_frame, font=script_font, highlightbackground="black", highlightthickness=2)
    script_box.pack(padx=10, pady=10)

    def thread_start():
        messagebox.showinfo("Message", "Patching Started!")
        try:
            lock_window()
            BWSISOEditor.ModifyData3(source_rom.get(), target_rom.get(), script_box.get("1.0", "end"))
            messagebox.showinfo("Success!", "Successfully patched!")
            open_file(os.path.dirname(target_rom.get()))
        except Exception:
            messagebox.showinfo("Error!", "An error occurred during patching.")
        finally:
            unlock_window()

    def patch():
        th = threading.Thread(target=thread_start, args=())
        th.start()

    def load_script():
        file = filedialog.askopenfilename(initialdir=sys.argv[0], title="Select Source Rom", filetypes=(("text files", "*.txt"),("all files","*.*")))
        script_box.delete("1.0", "end")
        with open(file, "r") as f:
            script_box.insert("1.0", f.read())

    def save_script():
        file = filedialog.asksaveasfilename(initialdir=sys.argv[0], title="Save Target Rom", filetypes=(("iso files", "*.iso"),("all files","*.*")))
        with open(file, "w") as f:
            f.write(script_box.get("1.0", "end"))

    f_frame3 = tk.Frame(main_frame)
    f_frame3.pack()
    load_btn = tk.Button(f_frame3, text="Load Script", font=ui_font, command=load_script)
    save_btn = tk.Button(f_frame3, text="Save Script", font=ui_font, command=save_script)
    patch_btn = tk.Button(f_frame3, text="Patch!", font=ui_font, command=patch)
    load_btn.pack(side=tk.LEFT)
    save_btn.pack(side=tk.LEFT)
    patch_btn.pack(side=tk.LEFT)

    def lock_window():
        load_btn.configure(state='disabled')
        save_btn.configure(state='disabled')
        patch_btn.configure(state='disabled')
        script_box.configure(state='disabled')
        src_ent.configure(state='disabled')
        src_btn.configure(state='disabled')
        tar_ent.configure(state='disabled')
        tar_btn.configure(state='disabled')
        use_translation_box.configure(state='disabled')

    def unlock_window():
        load_btn.configure(state='normal')
        save_btn.configure(state='normal')
        patch_btn.configure(state='normal')
        script_box.configure(state='normal')
        src_ent.configure(state='normal')
        src_btn.configure(state='normal')
        tar_ent.configure(state='normal')
        tar_btn.configure(state='normal')
        use_translation_box.configure(state='normal')

    window.lift()
    window.attributes('-topmost', True)
    window.after_idle(window.attributes, '-topmost', False)
    window.mainloop()


if __name__ == '__main__':
    main()
