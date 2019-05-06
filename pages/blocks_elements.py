class InputTextElement:
    def __init__(self, webelement):
        self.element = webelement

    def input(self, text):
        """Sets the text to the value supplied"""
        self.element.clear()
        self.element.send_keys(text)

    @property
    def placeholder(self):
        """Gets the text of the specified object"""
        return self.element.get_attribute("placeholder")

    @property
    def text_value(self):
        """Gets the text of the specified object"""
        return self.element.get_attribute("value")
