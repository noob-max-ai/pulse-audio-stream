from tkinter import *
from tkinter import messagebox

from tkinter import ttk
from multiprocessing import Process
from pulseutils import *

import subprocess
from constants import *

## Checks

if os.system('ffmpeg -loglevel panic -version'):
    os.system("zenity --warning --text='ffmpeg not found.\nTry\nsudo apt install ffmpeg'")
    exit()

if os.system('pactl --version'):
    os.system("zenity --warning --text='pactl not found'")
    exit()

class PulseServer:
    def __init__(self, master):
        

        self.master = master
        self.master.configure(bg=DARK_BG)
        self.start_status = False
        self.mic_status = False

        self.pulse_audio_server_module = None
        self.pulse_audio_mic_module = None

        master.title("Pulse Controls")

        # style Management
        style = ttk.Style()
        style.configure('new.TFrame', background=DARK_BG)
        
        # Set Tab header colors
        ttk.Style().configure("TNotebook", background=DARK_BG, borderwidth=0)
        ttk.Style().map("TNotebook.Tab", background=[("selected", UBUNTU_PURPLE)], foreground=[("selected", UBUNTU_WHITE)]);
        ttk.Style().configure("TNotebook.Tab", background=DARK_BG, foreground=UBUNTU_WHITE);



        ## Frame Management
        self.tab_control = ttk.Notebook(self.master)

        self.pulse_audio_server = ttk.Frame(self.tab_control, style='new.TFrame')
        self.pulse_audio_mic = ttk.Frame(self.tab_control,style='new.TFrame')

        self.tab_control.add(self.pulse_audio_server, text="Pulse Audio Server" )
        self.tab_control.add(self.pulse_audio_mic, text="Pulse Mic")


        left_frame = Frame(self.pulse_audio_server , background=DARK_BG)
        right_frame = Frame(self.pulse_audio_server , background=DARK_BG)

        self.label = Label(master, text="Pulse Audio Control Panel", background=DARK_BG, foreground=UBUNTU_WHITE)
        self.label.pack()
        

        # Left Frame
        self.output_devices_listbox = Listbox(left_frame, selectbackground=UBUNTU_FG, background=DARK_BG, foreground=UBUNTU_WHITE)
        self.output_devices_listbox.pack()

        # Right Frame
        rf1 = Frame(right_frame, background=DARK_BG)
        Label(rf1 , text="Port", background=DARK_BG, foreground=UBUNTU_WHITE).pack(side=LEFT)

        # IP Address Label
        self.ip_label = Label(right_frame,text='127.0.0.1', background=DARK_BG)
        self.ip_label.pack(side=TOP)
        self.ip_label['width'] = 16
        self.ip_label.config(highlightbackground = UBUNTU_PURPLE , highlightcolor= UBUNTU_PURPLE, foreground=UBUNTU_WHITE)
        

        # Port entry
        self.port_entry = Entry(rf1, background=DARK_BG)
        self.port_entry.insert(END, '8000')
        self.port_entry.pack(side=LEFT)
        self.port_entry['width'] = 6
        self.port_entry.config(highlightbackground = UBUNTU_PURPLE , highlightcolor= UBUNTU_PURPLE, foreground=UBUNTU_WHITE)
        rf1.pack()

        # Start Button
        self.start_button = Button(right_frame, text="Start Server", command=self.start_server, 
                    background=DARK_BG, foreground=UBUNTU_WHITE,
                    activebackground=UBUNTU_PURPLE)
        self.start_button.config(highlightbackground = DARK_BG)
        self.start_button.pack(side=BOTTOM)

        # Status Light
        self.status_canvas = Canvas(self.pulse_audio_server, width=15, height=15, borderwidth=0, highlightthickness=0, bg=DARK_BG)
        self.status_circle = self.status_canvas.create_oval(0, 0, 14, 14, fill=AMRANTH_RED, width=0)
        self.status_canvas.pack(side=RIGHT, anchor=S)
        

        left_frame.pack(side=LEFT)
        right_frame.pack(side=RIGHT)
        

        self.make_pulse_mic_gui()
        self.tab_control.pack()

        
        self.poststart()
    
    # TODO: Implement more aggressive online status indicators
    
    def make_pulse_mic_gui(self):
        Label(self.pulse_audio_mic,text='Mic Server', background=DARK_BG, foreground=UBUNTU_WHITE).pack(side=TOP)

        # Port entry
        self.audio_entry = Entry(self.pulse_audio_mic, background=DARK_BG)
        self.audio_entry.insert(END, 'http://192.168.10.7:8080/audio.opus')
        self.audio_entry.pack()
        self.audio_entry['width'] = 46
        self.audio_entry.config(highlightbackground = UBUNTU_PURPLE , highlightcolor= UBUNTU_PURPLE, foreground=UBUNTU_WHITE)


        # Mic Start Button
        self.pulse_mic_start_button = Button(self.pulse_audio_mic, text="Start Server", command=self.mic_start_server, 
                    background=DARK_BG, foreground=UBUNTU_WHITE,
                    activebackground=UBUNTU_PURPLE)

        self.pulse_mic_start_button.config(highlightbackground = DARK_BG)
        self.pulse_mic_start_button.pack(anchor=CENTER)

        # Status Light Mic Server
        self.mic_status_canvas = Canvas(self.pulse_audio_mic, width=15, height=15, borderwidth=0, highlightthickness=0, bg=DARK_BG)
        self.mic_status_circle = self.mic_status_canvas.create_oval(0, 0, 14, 14, fill=AMRANTH_RED, width=0)
        self.mic_status_canvas.pack(side=BOTTOM, anchor=E)
        
    """
    Mic realted processing stuff starts here
    """

    def mic_start_server(self):
        mic_address = self.audio_entry.get()
        

        if self.mic_status:
            self.mic_status = False
            self.pulse_mic_start_button.configure(text="Start Server")

            
            self.mic_status_canvas.itemconfig(self.mic_status_circle, fill=AMRANTH_RED)

            self.mic_process.terminate()
            self.mic_process.join(timeout=1.0)
            

            unload_module( self.pulse_audio_mic_module )

        else:
            self.mic_status = True
            self.pulse_mic_start_button.configure(text="Stop Server")

            # Run mic client
            #start_mic_server('http://192.168.10.7:8080/audio.opus')

            source_name='virtualmic' 
            format='s16le'
            rate='44100'
            channels='1' 
            pipe_filename= mktemp()

            self.pulse_audio_mic_module = self.create_source(source_name, pipe_filename, format, rate, channels)
            # print("mic module:", self.pulse_audio_mic_module)
            
            #self.start_mic_server(mic_address, source_name, pipe_filename,format, rate, channels)
            #exit()

            self.mic_process = Process(target=self.start_mic_server, args=(mic_address, source_name, pipe_filename,format, rate, channels))
            self.mic_process.daemon = True
            self.mic_process.start()
            

            
            if self.is_mic_service_running():
                self.mic_status_canvas.itemconfig(self.mic_status_circle, fill=FOREST_GREEN)

    @staticmethod
    def create_source(source_name, pipe_filename, format, rate, channels):
        create_source_cmd = ["pactl", "load-module", 
                            "module-pipe-source",
                            f"source_name={source_name}", 
                            f"file={pipe_filename}",
                            f"format={format}",
                            f"rate={rate}",
                            f"channels={channels}"
                            ]

        res = subprocess.run(create_source_cmd, stdout=subprocess.PIPE)
        module_number = res.stdout.decode('utf-8').strip()
        return module_number

    @staticmethod
    def is_mic_service_running():
        cmd = ["pactl", "list"]
        tag = "virtualmic"
        res = subprocess.run(cmd, stdout=subprocess.PIPE)
        res = res.stdout.decode('utf-8').strip()
        if tag in res:
            return True
        return False
    
    def start_mic_server(self, audio_file, source_name, pipe_filename,format, rate, channels):

        ffmpeg_loglevel='panic'
        

        #self.pulse_audio_mic_module = self.create_source(source_name, pipe_filename, format, rate, channels)

        make_default_cmd = [f'pactl', "set-default-source", source_name]
        res = subprocess.run(make_default_cmd, 
                        stdout=subprocess.PIPE
                        )
        res = res.stdout.decode('utf-8')
        
        # redirect input to source via ffmpeg
        input_to_source_cmd = ["ffmpeg",
                "-y",
                "-loglevel", ffmpeg_loglevel,
                "-re", "-i", audio_file,
                "-f", format,
                "-ar", rate,
                "-ac", channels,
                ">", pipe_filename
                ]

        input_to_source_cmd = [
            "ffmpeg",
            "-y",
            "-loglevel", "panic",
            "-i", audio_file, "-f", format, "-ac", channels,
            "-ar", rate, pipe_filename
        ]

        #print( ''.join([i+' ' for i in input_to_source_cmd]))
        res = subprocess.run(input_to_source_cmd, 
                        stdout=subprocess.PIPE
                        )
        res = res.stdout.decode('utf-8')
        #print(res)

    def poststart(self):
        self.populate_sources()

    def populate_sources(self):
        sources = get_output_sources()
        for source in sources:
            self.output_devices_listbox.insert(0, source)
        self.output_devices_listbox.selection_set(len(sources)-1)
        self.output_devices_listbox['width'] = len(max(sources))-7

    def start_server(self):
        """
        Pulse Audio Sound Server
        """
        # print("Starting Server")

        # Get User Input
        output_device = self.output_devices_listbox.get(ACTIVE)
        output_port = self.port_entry.get()
        
        # For debugging only
        # print(output_port)
        # print(output_device)

        
        if not self.start_status:
            self.start_status = True
            self.start_button.configure(text="Stop Server")
            # Start Server Here
            self.pulse_audio_server_module = start_server(output_device, output_port)

            # Status Bar
            if service_is_running():
                self.status_canvas.itemconfig(self.status_circle, fill=FOREST_GREEN)
            
        else:
            self.start_status = False
            self.start_button.configure(text="Start Server")
            # Stop Server Here
            #stop_server()
            unload_module(self.pulse_audio_server_module)
            
            # Status Bar
            if not service_is_running():
                self.status_canvas.itemconfig(self.status_circle, fill=AMRANTH_RED)

        self.ip_label.configure(text=get_ip())


def pastream_gui():
    root = Tk()
    my_gui = PulseServer(root)
    root.mainloop()
