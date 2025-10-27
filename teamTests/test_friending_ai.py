from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.setup_driver()
    
    def setup_driver(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--remote-debugging-port=9222')
        
        service = Service('/home/Dayne/bin/chromedriver')
        self.driver = webdriver.Chrome(options=options, service=service)
        self.wait = WebDriverWait(self.driver, 10)
    
    def pass_test(self, test_name):
        self.passed += 1
        print(f"[PASSED] - {test_name}")
    
    def fail_test(self, test_name, reason=""):
        self.failed += 1
        print(f"[FAILED] - {test_name}" + (f": {reason}" if reason else ""))
    
    def test_login_page_loads(self):
        """Test that login page loads successfully"""
        try:
            self.driver.get("http://localhost:5005/loginscreen")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
            self.pass_test("Login page loads")
        except Exception as e:
            self.fail_test("Login page loads", str(e))
    
    def test_login_form_elements_exist(self):
        """Test that all login form elements are present"""
        try:
            username = self.driver.find_element(By.CSS_SELECTOR, "input[name='username']")
            password = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            create_btn = self.driver.find_element(By.CSS_SELECTOR, "input[value='Create']")
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "input[value='Login']")
            
            if username and password and create_btn and login_btn:
                self.pass_test("All login form elements exist")
            else:
                self.fail_test("All login form elements exist")
        except Exception as e:
            self.fail_test("All login form elements exist", str(e))
    
    def test_create_existing_account(self):
        """Test creating an account that already exists"""
        try:
            username = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
            password = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            
            username.clear()
            password.clear()
            username.send_keys("John")
            password.send_keys("Doe")
            
            create_btn = self.driver.find_element(By.CSS_SELECTOR, "input[value='Create']")
            create_btn.click()
            
            # Check for error banner
            error_banner = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert-danger")))
            
            if error_banner and error_banner.is_displayed():
                self.pass_test("Duplicate account creation shows error")
            else:
                self.fail_test("Duplicate account creation shows error")
        except Exception as e:
            self.fail_test("Duplicate account creation shows error", str(e))
    
    def test_successful_login(self):
        """Test logging in with valid credentials"""
        try:
            username = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
            password = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            
            username.clear()
            password.clear()
            username.send_keys("John")
            password.send_keys("Doe")
            
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "input[value='Login']")
            login_btn.click()
            
            # Wait for redirect to main page (check for element that only appears after login)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.jumbotron")))
            self.pass_test("Successful login with valid credentials")
        except Exception as e:
            self.fail_test("Successful login with valid credentials", str(e))
    
    def test_add_friend_form_exists(self):
        """Test that Add Friend form is present after login"""
        try:
            add_friend_form = self.driver.find_element(By.CSS_SELECTOR, "form[action='/addfriend']")
            add_friend_title = self.driver.find_element(By.CSS_SELECTOR, "div.col-lg-3 h3.card-title").text
            
            if add_friend_form:
                self.pass_test("Add Friend form exists")
            else:
                self.fail_test("Add Friend form exists")
            
            if add_friend_title == "Add Friend":
                self.pass_test("Add Friend form title is correct")
            else:
                self.fail_test("Add Friend form title is correct", f"Expected 'Add Friend', got '{add_friend_title}'")
        except Exception as e:
            self.fail_test("Add Friend form elements", str(e))
    
    def test_add_friend_input_exists(self):
        """Test that Add Friend input field exists"""
        try:
            add_friend_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='username']")
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[name='addfriend']")
            
            if add_friend_input and submit_btn:
                self.pass_test("Add Friend input and submit button exist")
            else:
                self.fail_test("Add Friend input and submit button exist")
        except Exception as e:
            self.fail_test("Add Friend input and submit button exist", str(e))
    
    def test_add_friend_successfully(self):
        """Test successfully adding a friend"""
        try:
            add_friend_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='username']")
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[name='addfriend']")
            
            add_friend_input.clear()
            add_friend_input.send_keys("jane")
            submit_btn.click()
            
            # Wait for success banner
            success_banner = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert-success")))
            
            if success_banner and success_banner.is_displayed():
                self.pass_test("Successfully added friend")
            else:
                self.fail_test("Successfully added friend")
        except Exception as e:
            self.fail_test("Successfully added friend", str(e))
    
    def test_add_duplicate_friend(self):
        """Test adding the same friend twice"""
        try:
            add_friend_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='username']")
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[name='addfriend']")
            
            add_friend_input.clear()
            add_friend_input.send_keys("jane")
            submit_btn.click()
            
            # Check for error or info message
            try:
                alert = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.alert-danger, div.alert-warning, div.alert-info")
                ))
                if alert:
                    self.pass_test("Duplicate friend addition shows appropriate message")
                else:
                    self.fail_test("Duplicate friend addition shows appropriate message")
            except TimeoutException:
                self.fail_test("Duplicate friend addition shows appropriate message", "No alert shown")
        except Exception as e:
            self.fail_test("Duplicate friend addition shows appropriate message", str(e))
    
    def test_add_nonexistent_friend(self):
        """Test adding a friend that doesn't exist"""
        try:
            add_friend_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='username']")
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[name='addfriend']")
            
            add_friend_input.clear()
            add_friend_input.send_keys("nonexistentuser12345")
            submit_btn.click()
            
            # Check for error message
            try:
                error_banner = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert-danger")))
                if error_banner:
                    self.pass_test("Adding nonexistent friend shows error")
                else:
                    self.fail_test("Adding nonexistent friend shows error")
            except TimeoutException:
                self.fail_test("Adding nonexistent friend shows error", "No error shown")
        except Exception as e:
            self.fail_test("Adding nonexistent friend shows error", str(e))
    
    def test_empty_friend_input(self):
        """Test submitting empty friend request"""
        try:
            add_friend_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='username']")
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[name='addfriend']")
            
            add_friend_input.clear()
            submit_btn.click()
            
            # Check if HTML5 validation works or if custom error appears
            is_required = add_friend_input.get_attribute("required")
            
            if is_required is not None:
                self.pass_test("Empty friend input has required attribute")
            else:
                # Check for custom error message
                try:
                    error = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert-danger")))
                    if error:
                        self.pass_test("Empty friend input shows error")
                except:
                    self.fail_test("Empty friend input validation", "No validation found")
        except Exception as e:
            self.fail_test("Empty friend input validation", str(e))
    
    def test_friend_list_visible(self):
        """Test if friend list is displayed"""
        try:
            # Look for friend list container (adjust selector based on your HTML)
            friend_list = self.driver.find_element(By.CSS_SELECTOR, "div.jumbotron, ul.friend-list, div.friend-container")
            
            if friend_list and friend_list.is_displayed():
                self.pass_test("Friend list is visible")
            else:
                self.fail_test("Friend list is visible")
        except NoSuchElementException:
            self.fail_test("Friend list is visible", "Friend list element not found")
        except Exception as e:
            self.fail_test("Friend list is visible", str(e))
    
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        try:
            self.driver.get("http://localhost:5005/loginscreen")
            
            username = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
            password = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            
            username.clear()
            password.clear()
            username.send_keys("InvalidUser")
            password.send_keys("WrongPassword")
            
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "input[value='Login']")
            login_btn.click()
            
            # Check for error message
            try:
                error = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert-danger")))
                if error:
                    self.pass_test("Invalid login shows error message")
                else:
                    self.fail_test("Invalid login shows error message")
            except TimeoutException:
                self.fail_test("Invalid login shows error message", "No error displayed")
        except Exception as e:
            self.fail_test("Invalid login shows error message", str(e))
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("=" * 50)
        print("--= Beginning Test Suite =--")
        print("=" * 50)
        
        try:
            # Page load and form tests
            self.test_login_page_loads()
            self.test_login_form_elements_exist()
            
            # Account creation tests
            self.test_create_existing_account()
            
            # Login tests
            self.test_successful_login()
            
            # Add friend form tests
            self.test_add_friend_form_exists()
            self.test_add_friend_input_exists()
            
            # Friend functionality tests
            self.test_add_friend_successfully()
            self.test_add_duplicate_friend()
            self.test_add_nonexistent_friend()
            self.test_empty_friend_input()
            self.test_friend_list_visible()
            
            # Invalid login test
            self.test_invalid_login()
            
        except Exception as e:
            print(f"\n[CRITICAL ERROR] Test suite failed: {e}")
        finally:
            self.print_summary()
            self.driver.quit()
    
    def print_summary(self):
        """Print test results summary"""
        total = self.passed + self.failed
        print("\n" + "=" * 50)
        print("--= Test Summary =--")
        print("=" * 50)
        print(f"Total Tests: {total}")
        print(f"Passed: {self.passed} ({self.passed/total*100:.1f}%)" if total > 0 else "Passed: 0")
        print(f"Failed: {self.failed} ({self.failed/total*100:.1f}%)" if total > 0 else "Failed: 0")
        print("=" * 50)

if __name__ == "__main__":
    tester = TestRunner()
    tester.run_all_tests()
