class MessageManager:
    delegate = []
    @classmethod
    def add_delegate(cls, message, delegater):
        cls.delegate.append([message, delegater])

    @classmethod
    def send_message(cls, message, user_data):
        for items in cls.delegate:
            if message == items[0]:
                items[1].receive_message(message, user_data)

    @classmethod
    def remove_delegate(cls, message, delegate):
        # print("delegate remove:" + message + ", delegate:" + str(delegate) + ", now " + str(len(cls.delegate)) + " left.")
        # print("delegate list:" + str(cls.delegate))
        i = 0
        while i < len(cls.delegate):
            if cls.delegate[i][0] == message and cls.delegate[i][1] == delegate:
                del cls.delegate[i]
                break
            i += 1
        # print("delegate Number:" + str(len(cls.delegate)))
