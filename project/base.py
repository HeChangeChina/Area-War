from auxiliary_tools.message_manager import MessageManager


class Base:
    def __init__(self):
        self.message_list = []

    def message_require(self, message, function):
        self.message_list.append([message, function])
        MessageManager.add_delegate(message, self)

    def message_remove(self, message):
        for i in range(len(self.message_list)):
            if self.message_list[i][0] == message:
                MessageManager.remove_delegate(message, self)
                del self.message_list[i]
                return True
        return False

    def receive_message(self, message, data):
        for i in range(len(self.message_list)):
            if self.message_list[i][0] == message:
                self.message_list[i][1](data)
                return True
        return False

    def clear(self):
        for i in range(len(self.message_list)):
            if_successfully_remove = self.message_remove(self.message_list[0][0])
            if if_successfully_remove is False:
                print("Warning: failed to remove message" + str(self.message_list[i][0]))

    """def start_update(self):
        self.message_require("update_60", self.before_update)

    def stop_update(self):
        self.message_remove("update_60")

    def before_update(self,data):
        self.update()

    def update(self):
        pass"""
