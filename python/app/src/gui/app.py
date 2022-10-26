from gui.main_frame import MainFrame
from gui.new_chat_frame import NewChatFrame
from gui.new_contact_frame import NewContactFrame
import toga

class MessageApp(toga.App):
    
    def startup(self):
        self.main_window = MainFrame("main_window", "App")

        # Pruebas ventanas ##############################
        new_chat_window = NewChatFrame()
        new_chat_window.app = self

        new_contact_window = NewContactFrame()
        # new_contact_window.app = self
        # new_contact_window.show()

        self.windows = [ new_chat_window, new_contact_window]
        for w in self.windows:
            try:
                w.show()
            except Exception:
                print("Ventana aún no implementada")

        #################################################

        self.main_window.show()