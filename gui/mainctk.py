import customtkinter
customtkinter.set_default_color_theme("blue")

class IPframe(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = customtkinter.CTkLabel(self,)
        self.label.pack()
        self.label_startip = customtkinter.CTkLabel(self,text="Start")
        self.label_startip.pack()
        self.ip_input_1 = customtkinter.CTkEntry(self, 46, state='disabled')
        self.ip_input_1.pack(fill='x')
        self.label_endip = customtkinter.CTkLabel(self,text="End")
        self.label_endip.pack()
        self.ip_input_2 = customtkinter.CTkEntry(self, 46, state='disabled')
        self.ip_input_2.pack(fill='x')

    def update_iprangeEntry(self, startip: str, endip:str):
        self.ip_input_1.configure(state='normal')
        self.ip_input_1.delete(0, 'end')
        self.ip_input_1.insert(0, startip)
        self.ip_input_1.configure(state='disabled')
        self.ip_input_2.configure(state='normal')
        self.ip_input_2.delete(0, 'end')
        self.ip_input_2.insert(0, endip)
        self.ip_input_2.configure(state='disabled')

    def change_entrystate(self, entry: customtkinter.CTkEntry, cbox: customtkinter.CTkCheckBox):
        state = cbox.get()
        if state == 1: entry.configure(state='normal')
        else: entry.configure(state='disabled')

class GuiApp(customtkinter.CTk):
    def __init__(self, *args, title: str="App", **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1080x680")
        self.minsize(1080,680)
        self.title(title)
        self.iconbitmap("icon.ico")

        # popup windows notification
        self.withdraw()

        ## row and column config
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure((0,1,2), weight=1) 
        self.grid_columnconfigure(3, weight=0)

        ## main console frame
        self.frame_console = customtkinter.CTkFrame(self, )
        self.frame_console.grid(row=0, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")
        self.console_label = customtkinter.CTkLabel(self.frame_console,  anchor="w")
        self.console_label.pack(side="top")
        self.console_textbox = customtkinter.CTkTextbox(self.frame_console, state="disabled")
        self.console_textbox.pack(side="top", expand=True, fill="both")
        self.console_textbox_2 = customtkinter.CTkTextbox(self.frame_console, height=200 , state="disabled")
        self.console_textbox_2.pack(side="top", fill="x", pady=10)

        ## Side bar textbox
        self.frame_sideframe = customtkinter.CTkFrame(self,)
        self.frame_sideframe.grid(row=0, column=3, rowspan=3, padx=5, pady=10, sticky="ns")
        self.setting_label_int = customtkinter.CTkLabel(self.frame_sideframe, 200, 28,)
        self.setting_label_int.pack(padx=10,)
        self.console_infobox = customtkinter.CTkTextbox(self.frame_sideframe, 230, state="disabled",  )
        self.console_infobox.pack(padx=5, fill="x")
        self.setting_label_intchange = customtkinter.CTkLabel(self.frame_sideframe, 200, 28,)
        self.setting_label_intchange.pack(padx=10, pady=5,)
        self.setting_om_int = customtkinter.CTkOptionMenu(self.frame_sideframe, 200, 28 , dynamic_resizing=False)
        self.setting_om_int.pack(padx=10, pady=(0,5),)
        self.cbox_customscan = customtkinter.CTkCheckBox(self.frame_sideframe)
        self.cbox_customscan.pack(padx=10, pady=5, side='bottom')
        self.setting_customscan = IPframe(self.frame_sideframe, fg_color="transparent")
        self.setting_customscan.pack(padx=10, pady=5, side='bottom')

        ## scan options
        self.frame_scanoption = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_scanoption.grid(row=1, column=0, columnspan=3, padx=5, pady=(0,10), sticky="ew")
        self.cbox_detail = customtkinter.CTkCheckBox(self.frame_scanoption)
        self.cbox_detail.pack(side="left", padx=5, pady=5)
        self.cbox_http = customtkinter.CTkCheckBox(self.frame_scanoption)
        self.cbox_http.pack(side="left", padx=5, pady=5)
        self.cbox_https = customtkinter.CTkCheckBox(self.frame_scanoption)
        self.cbox_https.pack(side="left", padx=5, pady=5)
        self.cbox_skipping = customtkinter.CTkCheckBox(self.frame_scanoption)
        self.cbox_skipping.pack(side="left", padx=5, pady=5)

        ## control panel 
        self.frame_control = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_control.grid(row=2, column=0, columnspan=3, padx=5, pady=(0,10), sticky="ew")
        self.button_startPing = customtkinter.CTkButton(self.frame_control,)
        self.button_startPing.pack(side="left", padx=15, pady=5)
        self.button_getNetwork = customtkinter.CTkButton(self.frame_control,)
        self.button_getNetwork.pack(side="left", padx=15, pady=5)
        self.button_cleanConsole = customtkinter.CTkButton(self.frame_control,)
        self.button_cleanConsole.pack(side="left", padx=15, pady=5)
        self.button_savetxt = customtkinter.CTkButton(self.frame_control,)
        self.button_savetxt.pack(side="left", padx=15, pady=5)

        ## indication
        self.progressbar =customtkinter.CTkProgressBar(self, 740, 10, mode = "indeterminnate")

    ## degub
    def printtoself(self,):
        pass

    # console helper 2.0:
    @staticmethod
    def console_txtbox_helper(text:str, txtbox: customtkinter.CTkTextbox, newline: bool=True, ):
        txtbox.configure(state="normal")
        if text == 'clear':
            txtbox.delete(1.0, "end")
            return
        if newline:
            txtbox.insert("end", f"{text}\n")
        else:
            txtbox.insert("end", f"{text}")
        txtbox.see("end")
        txtbox.configure(state="disabled")

    ## console helper:
    def console_textbox_addnewline(self, text: str):
        self.console_txtbox_helper(text, self.console_textbox)

    def console_textbox_addtoend(self, text: str):
        self.console_txtbox_helper(text, self.console_textbox, newline=False)

    def console_textbox_clear(self):
        self.console_txtbox_helper('clear', self.console_textbox)

    def cconsole_infobox_addnewline(self, text: str):
        self.console_txtbox_helper(text, self.console_infobox)

    def console_textbox_2_addnewline(self, text: str):
        self.console_txtbox_helper(text, self.console_textbox_2)

    def console_textbox_2_clear(self):
        self.console_txtbox_helper('clear', self.console_textbox_2)

    ##  progressbar helper
    def progressbar_show(self):
        self.button_startPing.configure(state="disabled")
        self.button_getNetwork.configure(state="disabled")
        self.button_cleanConsole.configure(state="disabled")
        self.button_savetxt.configure(state="disabled")
        self.cbox_detail.configure(state="disabled")
        self.cbox_http.configure(state="disabled")
        self.cbox_https.configure(state="disabled")
        self.cbox_skipping.configure(state="disabled")
        self.setting_om_int.configure(state='disabled')
        self.cbox_customscan.configure(state='disabled')

        self.progressbar.start()
        self.progressbar.grid(row=3, column=0, columnspan=4, sticky="ew")

    def progressbar_hide(self):
        self.progressbar.grid_forget()
        self.progressbar.stop()
        self.button_startPing.configure(state="normal")
        self.button_getNetwork.configure(state="normal")
        self.button_cleanConsole.configure(state="normal")
        self.button_savetxt.configure(state="normal")
        self.cbox_detail.configure(state="normal")
        self.cbox_http.configure(state="normal")
        self.cbox_https.configure(state="normal")
        self.cbox_skipping.configure(state="normal")
        self.setting_om_int.configure(state='normal')
        self.cbox_customscan.configure(state='normal')

    ## Confirm box
    def confirm_popup(self, _note: str=None):
        note = _note
        self.popupwindow = customtkinter.CTkToplevel(self)
        self.popupwindow.geometry("500x260")
        self.popupwindow.title("Wellcome")
        self.popupwindow.resizable(False, False)
        self.textbox = customtkinter.CTkTextbox(self.popupwindow, 460, 180,)
        self.textbox.insert("end", note)
        self.textbox.configure(state="disabled")
        self.textbox.pack(side="top", padx=20, pady=20)
        self.button_popup = customtkinter.CTkButton(self.popupwindow, 140, 30, text="OK!", )
        self.button_popup.pack(side="top", padx=20, pady=0)
    
    ## Function to change Scanner setting
    @staticmethod
    def changesetting(cbox: customtkinter.CTkCheckBox, app, setting: str):
        state = cbox.get()
        if state == 1: app.setting[f'{setting}'] = True
        else: app.setting[f'{setting}'] = False
        print(setting, app.setting[f'{setting}'])

    def button_savefile(self):
        try:
            with open(customtkinter.filedialog.asksaveasfilename(initialdir="./", title="Save .txt", defaultextension=".txt", filetypes=(("Text Files", "*.txt"),)),"w") as f:
                f.write(self.console_textbox.get(1.0, "end"))
        except:
            print("No file selected")
            pass
        else:
            print("save")
        