# 1. Function that generates function
# def presence_of_num_elements(number, locator):
#     def func(driver):
#         els = driver.find_elements(*self.locator)
#         if len(els) == number and els[0].is_displayed():
#             return els
#     return func


# 2. Class for callable objects
class presence_of_num_elements:
    def __init__(self, locator, number):
        self.locator = locator
        self.number = number

    def __call__(self, driver):
        els = driver.find_elements(*self.locator)
        if len(els) == self.number and els[0].is_displayed():
            return els



if __name__ == "__main__":
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    driver = webdriver.Chrome()
    base_url = "http://127.0.0.1/oxwall/"
    driver.get(base_url)
    wait = WebDriverWait(driver, 10)
    buttons = wait.until(presence_of_num_elements((By.CLASS_NAME, "ow_console_item"), 2))

    buttons[1].click()

#
# presence_of_3_elements(driver, By.CLASS_NAME, "ow_console_item")
#
#
# class presence_of_3_elements:
#     def __init__(self, by, value):
#         self.by = by
#         self.value = value
#
#     def __call__(self, wd):
#         buttons = wd.find_elements(self.by, self.value)
#         if len(buttons) == 3:
#             return buttons
#         else:
#             return False
#
#
# WebDriverWait(driver, 10).until(
#     presence_of_3_elements(By.CLASS_NAME, "ow_console_item")
# )
#
#
#
#
# class MyClass:
#     def __init__(self, const):
#         self.const = const
#
#     def __call__(self, a, b):
#         print((a + b)*self.const)
#
#
# obj = MyClass(123)
# obj2 = MyClass(1111)
#
# obj(1, 2)
# obj2(1, 0)
