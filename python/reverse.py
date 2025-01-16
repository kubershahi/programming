class Manipulate: 
    def __init__(self, text):
        self.text = text
    

    def reverse(self):
        text_list = list(self.text)
        l , r = 0, len(text_list) - 1
        while l < r: 
            text_list[l], text_list[r] = text_list[r], text_list[l]
            l += 1
            r -= 1
        self.text = "".join(text_list)
        return self.text


if __name__ == "__main__":
    string_manipulator = Manipulate("hello")
    reversed_text = string_manipulator.reverse()
    print(reversed_text)
