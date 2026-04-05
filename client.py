import threading
from socket import *
from customtkinter import *


class MainWindow(CTk):
   def __init__(self):
       super().__init__()
       self.geometry('500x400')
       self.title("Chat")


       # ===== MENU =====
       self.menu_frame = CTkFrame(self, width=40)
       self.menu_frame.pack(side="left", fill="y")


       self.is_show_menu = False


       self.btn = CTkButton(self.menu_frame, text='▶️', width=30, command=self.toggle_menu)
       self.btn.pack(pady=5)


       # ===== MAIN FRAME =====
       self.main_frame = CTkFrame(self)
       self.main_frame.pack(side="left", fill="both", expand=True)


       # ===== CHAT =====
       self.chat_field = CTkTextbox(self.main_frame, state="disabled")
       self.chat_field.pack(fill="both", expand=True, padx=5, pady=5)


       # ===== INPUT =====
       self.bottom_frame = CTkFrame(self.main_frame, height=40)
       self.bottom_frame.pack(fill="x")


       self.message_entry = CTkEntry(self.bottom_frame, placeholder_text="Введіть повідомлення")
       self.message_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)


       self.send_button = CTkButton(self.bottom_frame, text=">", width=50, command=self.send_message)
       self.send_button.pack(side="right", padx=5, pady=5)


       # ===== USER =====
       self.username = "Yaroslav"


       # ===== SOCKET =====
       try:
           self.sock = socket(AF_INET, SOCK_STREAM)
           self.sock.connect(("localhost", 8080))


           hello = f"TEXT@{self.username}@[SYSTEM] {self.username} приєднався до чату!\n"
           self.sock.send(hello.encode())


           threading.Thread(target=self.recv_message, daemon=True).start()


       except Exception as e:
           self.add_message(f"❌ Помилка підключення: {e}")


   # ===== MENU =====
   def toggle_menu(self):
       if not self.is_show_menu:
           self.menu_frame.configure(width=200)
           self.btn.configure(text="◀️")


           self.name_label = CTkLabel(self.menu_frame, text="Ім'я")
           self.name_label.pack(pady=10)


           self.name_entry = CTkEntry(self.menu_frame)
           self.name_entry.pack(pady=5)


           self.save_btn = CTkButton(self.menu_frame, text="Зберегти", command=self.save_name)
           self.save_btn.pack(pady=5)


       else:
           self.menu_frame.configure(width=40)
           self.btn.configure(text="▶️")


           for widget in self.menu_frame.winfo_children()[1:]:
               widget.destroy()


       self.is_show_menu = not self.is_show_menu


   def save_name(self):
       new_name = self.name_entry.get()
       if new_name:
           self.username = new_name
           self.add_message(f"[SYSTEM] Твоє ім'я змінено на {new_name}")


   # ===== CHAT =====
   def add_message(self, text):
       self.chat_field.configure(state="normal")
       self.chat_field.insert("end", text + "\n")
       self.chat_field.configure(state="disabled")
       self.chat_field.see("end")


   def send_message(self):
       message = self.message_entry.get()
       if message:
           data = f"TEXT@{self.username}@{message}\n"
           try:
               self.sock.sendall(data.encode())
               self.add_message(f"{self.username}: {message}")
           except:
               self.add_message("❌ Помилка відправки")


       self.message_entry.delete(0, "end")


   def recv_message(self):
       buffer = ""
       while True:
           try:
               chunk = self.sock.recv(4096)
               if not chunk:
                   break


               buffer += chunk.decode()


               while "\n" in buffer:
                   line, buffer = buffer.split("\n", 1)
                   self.handle_line(line.strip())


           except:
               break


       self.sock.close()


   def handle_line(self, line):
       if not line:
           return


       parts = line.split("@", 2)
       if parts[0] == "TEXT" and len(parts) >= 3:
           author = parts[1]
           message = parts[2]
           self.add_message(f"{author}: {message}")
       else:
           self.add_message(line)


# ===== RUN =====
if __name__ == "__main__":
   app = MainWindow()
   app.mainloop()



