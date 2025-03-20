import ftplib
import csv
import re
import threading
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Global variables for thread-safe operations
print_lock = threading.Lock()
sensitive_keywords = ['password', 'config', 'backup', 'secret', '.sql', '.env', '.png', '.jpg', '.mp3', '.mp4', 'credentials']
sensitive_pattern = re.compile(r'|'.join(map(re.escape, sensitive_keywords)), re.IGNORECASE)

# Colors for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def print_banner():
    banner = f"""
{Colors.CYAN}
███████╗████████╗██████╗       ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
██╔════╝╚══██╔══╝██╔══██╗      ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
█████╗     ██║   ██████╔╝█████╗███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
██╔══╝     ██║   ██╔═══╝ ╚════╝██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
██║        ██║   ██║           ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
╚═╝        ╚═╝   ╚═╝           ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
{Colors.RESET}
{Colors.YELLOW}Version: {Colors.MAGENTA}v1.0{Colors.RESET}
{Colors.YELLOW}Description: {Colors.WHITE}FTP Hunter is a tool for scanning FTP servers and detecting sensitive files.{Colors.RESET}
{Colors.RED}Contact: {Colors.BLUE}https://linktr.ee/xtawb{Colors.RESET}
{Colors.RED}Github : {Colors.BLUE}https://github.com/xtawb{Colors.RESET}
"""
    print(banner)

def get_ftp_tree(ftp, current_dir='', prefix='', is_last=False, depth=0, max_depth=10):
    if depth > max_depth:
        return []  # Prevent infinite recursion
    tree = []
    original_dir = ftp.pwd()
    
    try:
        ftp.cwd(current_dir)
    except ftplib.error_perm as e:
        return [f"{prefix}└── {Colors.RED}[Permission Denied: {current_dir}]{Colors.RESET}"]
    except Exception as e:
        return [f"{prefix}└── {Colors.RED}[Error: {str(e)}]{Colors.RESET}"]
    
    try:
        files = []
        try:
            ftp.retrlines('MLSD', files.append)
        except:
            ftp.retrlines('LIST', files.append)
    except ftplib.error_perm:
        ftp.cwd(original_dir)
        return [f"{prefix}└── {Colors.RED}[Listing Denied]{Colors.RESET}"]
    except Exception as e:
        ftp.cwd(original_dir)
        return [f"{prefix}└── {Colors.RED}[Error: {str(e)}]{Colors.RESET}"]
    
    entries = []
    for line in files:
        try:
            name = line.split()[-1]  # Extract name for different formats
            is_dir = 'type=dir' in line.lower() or line.startswith('d')
            entries.append((name, is_dir))
        except:
            continue
    
    entries.sort(key=lambda x: (not x[1], x[0]))
    
    for i, (name, is_dir) in enumerate(entries):
        try:
            if i == len(entries) - 1:
                new_prefix = prefix + '└── '
                next_prefix = prefix + '    '
            else:
                new_prefix = prefix + '├── '
                next_prefix = prefix + '│   '
            
            # Highlight sensitive files
            if sensitive_pattern.search(name):
                tree.append(f"{new_prefix}{Colors.RED}{name}{Colors.RESET}")
            else:
                tree.append(f"{new_prefix}{name}")
            
            if is_dir:
                subtree = get_ftp_tree(ftp, name, next_prefix, i == len(entries)-1, depth+1, max_depth)
                tree.extend(subtree)
        except Exception as e:
            tree.append(f"{new_prefix}{Colors.RED}[Error: {str(e)}]{Colors.RESET}")
            continue
    
    try:
        ftp.cwd(original_dir)
    except:
        pass
    return tree

def check_ftp_login(ip, username, password):
    ftp = ftplib.FTP()
    try:
        # Set a timeout for connection and operations
        socket.setdefaulttimeout(10)  # Global socket timeout
        ftp.connect(ip, port=21, timeout=10)
        ftp.login(user=username, passwd=password)
        ftp.set_pasv(True)  # Enable passive mode
        return True, ftp
    except ftplib.error_perm as e:
        print(f"{Colors.RED}[-] Login failed for {ip}: {str(e)}{Colors.RESET}")
        ftp.close()
        return False, None
    except Exception as e:
        print(f"{Colors.RED}[-] Connection error for {ip}: {str(e)}{Colors.RESET}")
        ftp.close()
        return False, None

def process_ip(ip):
    try:
        # Attempt root login
        success, ftp = check_ftp_login(ip, 'root', 'toor')
        if success:
            tree = get_ftp_tree(ftp)
            with print_lock:
                print(f"\n{Colors.GREEN}[+] Server: {ip}{Colors.RESET}")
                print(f"{Colors.GREEN}[+] Root Login Successful!{Colors.RESET}")
                print("\nDirectory Tree:")
                for line in tree:
                    print(line)
            ftp.quit()
            return {
                'IP': ip,
                'Login Type': 'root',
                'Directory Tree': '\n'.join(tree),
                'Timestamp': datetime.now().isoformat()
            }
        
        # Attempt anonymous login
        success, ftp = check_ftp_login(ip, 'anonymous', 'guest')
        if success:
            tree = get_ftp_tree(ftp)
            with print_lock:
                print(f"\n{Colors.GREEN}[+] Server: {ip}{Colors.RESET}")
                print(f"{Colors.GREEN}[+] Anonymous Login Successful!{Colors.RESET}")
                print("\nDirectory Tree:")
                for line in tree:
                    print(line)
            ftp.quit()
            return {
                'IP': ip,
                'Login Type': 'anonymous',
                'Directory Tree': '\n'.join(tree),
                'Timestamp': datetime.now().isoformat()
            }
        
        with print_lock:
            print(f"\n{Colors.RED}[-] Server: {ip}{Colors.RESET}")
            print(f"{Colors.RED}[-] Failed to login (root/anonymous){Colors.RESET}")
        return None
    except Exception as e:
        with print_lock:
            print(f"\n{Colors.RED}[!] Error processing {ip}: {str(e)}{Colors.RESET}")
        return None

def main():
    print_banner()
    
    # Prompt user for the path to the IPs file
    ip_file = input(f"\n{Colors.CYAN}[*] Enter the path to the IPs file (e.g., ips.txt): {Colors.RESET}").strip()
    
    try:
        with open(ip_file, 'r') as file:
            ips = list(set(file.read().splitlines()))
    except FileNotFoundError:
        print(f"\n{Colors.RED}[!] Error: File '{ip_file}' not found!{Colors.RESET}")
        return
    
    # Print the number of IPs to be scanned
    print(f"\n{Colors.CYAN}[*] Number of IPs to scan: {len(ips)}{Colors.RESET}")
    
    report = []
    successful_ips = []
    failed_ips = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_ip, ip): ip for ip in ips}
        for future in as_completed(futures):
            entry = future.result()
            if entry:
                report.append(entry)
                successful_ips.append(entry['IP'])
            else:
                failed_ips.append(futures[future])
    
    # Print summary
    print(f"\n{Colors.CYAN}[*] Scan completed!{Colors.RESET}")
    print(f"{Colors.GREEN}[+] Successful logins: {len(successful_ips)}{Colors.RESET}")
    print(f"{Colors.RED}[-] Failed logins: {len(failed_ips)}{Colors.RESET}")
    
    # Save successful IPs to a file
    if successful_ips:
        with open('successful_ips.txt', 'w') as f:
            for ip in successful_ips:
                f.write(f"{ip}\n")
        print(f"{Colors.GREEN}[+] Successful IPs saved to successful_ips.txt{Colors.RESET}")
    
    # Save report to CSV
    if report:
        with open('ftp_report.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=report[0].keys())
            writer.writeheader()
            writer.writerows(report)
        print(f"{Colors.GREEN}[+] Report saved to ftp_report.csv{Colors.RESET}")
    else:
        print(f"{Colors.RED}[-] No data to save in report{Colors.RESET}")

if __name__ == '__main__':
    main()
