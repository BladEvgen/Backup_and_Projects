class MainClass:
    def __init__(self, text: str):
        self.text = text


class ChildMain(MainClass):
    def __init__(self, text: str, number: int | float):
        super().__init__(text)
        self.number = number


class MainClassPrivate:
    def __init__(self, text: None | str):
        self._text = text

    def set_text(self, new_text=None):
        if new_text is not None:
            self._text = new_text
        else:
            self._text = ""

    def get_text(self):
        return self._text


class ChildMainPrivate(MainClassPrivate):
    def __init__(self, text, number):
        super().__init__(text)
        self._number = number

    def set_number(self, new_number):
        self._number = new_number

    def get_number(self):
        return self._number


class Roman:
    def __init__(self, value1: int, value2: int, action: str = "+"):
        self.value1 = value1
        self.value2 = value2
        self.action = action

    @staticmethod
    def _to_decimal(roman):
        roman_dict = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
        decimal = 0
        prev_value = 0
        for char in reversed(roman):
            value = roman_dict[char]
            decimal += value if value >= prev_value else -value
            prev_value = value
        return decimal

    @staticmethod
    def _to_roman(decimal):
        roman_dict = {
            1000: "M",
            900: "CM",
            500: "D",
            400: "CD",
            100: "C",
            90: "XC",
            50: "L",
            40: "XL",
            10: "X",
            9: "IX",
            5: "V",
            4: "IV",
            1: "I",
        }
        roman = ""
        for value, symbol in roman_dict.items():
            while decimal >= value:
                roman += symbol
                decimal -= value
        return roman

    def get_result(self, action: str | None):
        if action is not None:
            self.action = action
        decimal1 = self._to_decimal(self.value1)
        decimal2 = self._to_decimal(self.value2)
        match self.action:
            case "+":
                return self._to_roman(decimal1 + decimal2)
            case "-":
                return self._to_roman(decimal1 - decimal2)
            case "*":
                return self._to_roman(decimal1 * decimal2)
            case "/":
                return self._to_roman(decimal1 / decimal2)
            case _:
                raise Exception("Unknown action")

def main():
    main_obj = MainClass("Hello")

    print(main_obj.text)

    child_obj = ChildMain("Child", 123)

    print(type(child_obj.text), child_obj.text)
    print(type(child_obj.number), child_obj.number)

    print("\n\n\nIncapsulating")

    main_obj_priv = MainClassPrivate("Hello")
    main_obj_priv.set_text("World")
    print(main_obj_priv.get_text())

    child_obj_priv = ChildMainPrivate("Child", 123)
    child_obj_priv.set_text("New Child")

    child_obj_priv.set_number(456)

    print(child_obj_priv.get_text())
    print(child_obj_priv.get_number())
    
    
    print("\n\n\nRoman")
    r = Roman("VI", "II")
    print(r.get_result("+"))  
    print(r.get_result("-"))  
    print(r.get_result("*"))  
    print(r.get_result("/"))  
    print("\nRaise Error\n")
    print(r.get_result("%"))



if __name__ == "__main__":
    main()
