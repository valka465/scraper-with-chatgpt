import sqlite3
import subprocess
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from tkinter import messagebox
import requests
import json, os, re
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
from tkinter import scrolledtext
import openai
from ttkbootstrap.scrolled import ScrolledFrame
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
import time


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        subprocess.Popen(['python', 'check_bd.py'])
        self.iconbitmap(r'logo.ico')
        self.title("Scrape-It.Cloud")
        self.geometry("600x500")
        os.makedirs("output", exist_ok=True)
        
        self.create_widgets()
        self.create_theme_slider()
        self.set_light_theme()

    def create_widgets(self):

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Settings")

        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="SERP")

        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="Maps")

        tab5 = ttk.Frame(self.notebook)
        self.notebook.add(tab5, text="ChatGPT with Scraper")

        tab6 = ttk.Frame(self.notebook)
        self.notebook.add(tab6, text="Shopify")

        tab7 = ttk.Frame(self.notebook)
        self.notebook.add(tab7, text="Zillow")

        tab8 = ttk.Frame(self.notebook)
        self.notebook.add(tab8, text="Any")

        # Tab 1

        label_serp_api = ttk.Label(tab1, text="Scrape-It.Cloud API:", font=('Helvetica', 12))
        label_serp_api.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.entry_serp_api = ttk.Entry(tab1, width=50)
        self.entry_serp_api.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        label_chatgpt_api = ttk.Label(tab1, text="ChatGPT API:", font=('Helvetica', 12))
        label_chatgpt_api.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.entry_chatgpt_api = ttk.Entry(tab1, width=50)
        self.entry_chatgpt_api.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        button_save = ttk.Button(tab1, text="Upload", command=self.on_upload_clicked, style='Large.TButton')
        button_save.place(relx=0.35, rely=0.6, anchor=tk.CENTER)
        
        button_save = ttk.Button(tab1, text="Save", command=self.on_save_clicked, style='Large.TButton')
        button_save.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        
        button_save = ttk.Button(tab1, text="Delete", command=self.on_delete_clicked, style='Large.TButton')
        button_save.place(relx=0.65, rely=0.6, anchor=tk.CENTER)

        #Tab2

        label_serp_keyword = ttk.Label(tab2, text="Keyword:", font=('Helvetica', 12))
        label_serp_keyword.place(relx=0.15, rely=0.1, anchor=tk.CENTER)

        self.entry_serp_keyword = ttk.Entry(tab2, width=50)
        self.entry_serp_keyword.place(relx=0.6, rely=0.1, anchor=tk.CENTER)

        label_serp_start = ttk.Label(tab2, text="Start:", font=('Helvetica', 12))
        label_serp_start.place(relx=0.15, rely=0.2, anchor=tk.CENTER)

        self.entry_serp_start = ttk.Entry(tab2, width=50)
        self.entry_serp_start.place(relx=0.6, rely=0.2, anchor=tk.CENTER)
        self.entry_serp_start.insert(0, "0")

        label_serp_number = ttk.Label(tab2, text="Results (10-100):", font=('Helvetica', 12))
        label_serp_number.place(relx=0.15, rely=0.3, anchor=tk.CENTER)

        self.entry_serp_number = ttk.Entry(tab2, width=50)
        self.entry_serp_number.place(relx=0.6, rely=0.3, anchor=tk.CENTER)
        self.entry_serp_number.insert(0, "100")

        label_serp_tbm = ttk.Label(tab2, text="Scraped Data Type:")
        label_serp_tbm.place(relx=0.15, rely=0.4, anchor=tk.CENTER)

        self.tbm_serp_var = tk.StringVar()
        self.tbm_serp_var.set("Google SERP")

        self.tbm_serp_menu = tk.Menubutton(tab2, width=50, textvariable=self.tbm_serp_var, borderwidth=1, relief="raised")
        self.tbm_serp_menu.place(relx=0.6, rely=0.4, anchor=tk.CENTER)

        self.tbm_serp_options = ["Google SERP", "Google Images", "Google Videos", "Google News", "Google Locals", "Google Shopping"]
        self.tbm_serp_menu.menu = tk.Menu(self.tbm_serp_menu, tearoff=0)
        self.tbm_serp_menu["menu"] = self.tbm_serp_menu.menu

        for tbm in self.tbm_serp_options:
            self.tbm_serp_menu.menu.add_radiobutton(label=tbm, variable=self.tbm_serp_var, value=tbm)

        # Device Type Menubutton and Menu
        label_serp_device_type = ttk.Label(tab2, text="Device Type:")
        label_serp_device_type.place(relx=0.15, rely=0.5, anchor=tk.CENTER)

        self.device_serp_type_var = tk.StringVar()
        self.device_serp_type_var.set("Desktop")

        self.device_serp_type_menu = tk.Menubutton(tab2, width=50, textvariable=self.device_serp_type_var, borderwidth=1, relief="raised")
        self.device_serp_type_menu.place(relx=0.6, rely=0.5, anchor=tk.CENTER)

        self.device_serp_type_options = ["Desktop", "Tablet", "Mobile"]
        self.device_serp_type_menu.menu = tk.Menu(self.device_serp_type_menu, tearoff=0)
        self.device_serp_type_menu["menu"] = self.device_serp_type_menu.menu

        for device_type in self.device_serp_type_options:
            self.device_serp_type_menu.menu.add_radiobutton(label=device_type, variable=self.device_serp_type_var, value=device_type)

        # Language Menubutton and Menu
        label_serp_language = ttk.Label(tab2, text="Choose the language:")
        label_serp_language.place(relx=0.15, rely=0.6, anchor=tk.CENTER)

        self.language_serp_var = tk.StringVar()
        self.language_serp_var.set("English — en")

        self.language_serp_menu = tk.Menubutton(tab2, width=50, textvariable=self.language_serp_var, borderwidth=1, relief="raised")
        self.language_serp_menu.place(relx=0.6, rely=0.6, anchor=tk.CENTER)


        language_serp_options = [
            "No Selection", "Afrikaans — af", "Akan — ak", "Albanian — sq", "Amharic — am", "Arabic — ar", "Armenian — hy", "Azerbaijani — az", "Basque — eu", "Belarusian — be",
            "Bengali — bn", "Bihari — bh", "Bork, bork, bork! — xx-bork", "Bosnian — bs", "Breton — br", "Bulgarian — bg", "Bhutanese — bt", "Cambodian — km", "Catalan — ca",
            "Cherokee — chr", "Chichewa — ny", "Chinese (Simplified) — zh-cn", "Chinese (Traditional) — zh-tw", "Corsican — co", "Croatian — hr", "Czech — cs", "Danish — da",
            "Dutch — nl", "Elmer Fudd — xx-elmer", "English — en", "Esperanto — eo", "Estonian — et", "Ewe — ee", "Faroese — fo", "Filipino — tl", "Finnish — fi", "French — fr",
            "Frisian — fy", "Ga — gaa", "Galician — gl", "Georgian — ka", "German — de", "Greek — el", "Greenlandic — kl", "Guarani — gn", "Gujarati — gu", "Hacker — xx-hacker",
            "Haitian Creole — ht", "Hausa — ha", "Hawaiian — haw", "Hebrew — iw", "Hindi — hi", "Hungarian — hu", "Icelandic — is", "Igbo — ig", "Indonesian — id", "Interlingua — ia",
            "Irish — ga", "Italian — it", "Japanese — ja", "Javanese — jw", "Kannada — kn", "Kazakh — kk", "Kinyarwanda — rw", "Kirundi — rn", "Klingon — xx-klingon", "Kongo — kg",
            "Korean — ko", "Krio (Sierra Leone) — kri", "Kurdish — ku", "Kurdish (Soranî) — ckb", "Kyrgyz — ky", "Laothian — lo", "Latin — la", "Latvian — lv", "Lingala — ln", "Lithuanian — lt",
            "Lozi — loz", "Luganda — lg", "Luo — ach", "Macedonian — mk", "Malagasy — mg", "Malay — my", "Malayalam — ml", "Maltese — mt", "Maldives — mv", "Maori — mi",
            "Marathi — mr", "Mauritian Creole — mfe", "Moldavian — mo", "Mongolian — mn", "Montenegrin — sr-me", "Nepali — ne", "Nigerian Pidgin — pcm", "Northern Sotho — nso",
            "Norwegian — no", "Norwegian (Nynorsk) — nn", "Occitan — oc", "Oriya — or", "Oromo — om", "Pashto — ps", "Persian — fa", "Pirate — xx-pirate", "Polish — pl",
            "Portuguese — pt", "Portuguese (Brazil) — pt-br", "Portuguese (Portugal) — pt-pt", "Punjabi — pa", "Quechua — qu", "Romanian — ro", "Romansh — rm", "Runyakitara — nyn",
            "Russian — ru", "Scots Gaelic — gd", "Serbian — sr", "Serbo-Croatian — sh", "Sesotho — st", "Setswana — tn", "Seychellois Creole — crs", "Shona — sn", "Sindhi — sd",
            "Sinhalese — si", "Slovak — sk", "Slovenian — sl", "Somali — so", "Spanish — es", "Spanish (Latin American) — es-419", "Sundanese — su", "Swahili — sw", "Swedish — sv",
            "Tajik — tg", "Tamil — ta", "Tatar — tt", "Telugu — te", "Thai — th", "Tigrinya — ti", "Tonga — to", "Tshiluba — lua", "Tumbuka — tum", "Turkish — tr", "Turkmen — tk",
            "Twi — tw", "Uighur — ug", "Ukrainian — uk", "Urdu — ur", "Uzbek — uz", "Vanuatu — vu", "Vietnamese — vi", "Welsh — cy", "Wolof — wo", "Xhosa — xh", "Yiddish — yi",
            "Yoruba — yo", "Zulu — zu"
        ]

        self.language_serp_menu.menu = tk.Menu(self.language_serp_menu, tearoff=0)
        self.language_serp_menu["menu"] = self.language_serp_menu.menu

        for language in language_serp_options:
            self.language_serp_menu.menu.add_radiobutton(label=language, variable=self.language_serp_var, value=language)

        # Domain Menubutton and Menu
        label_serp_domain = ttk.Label(tab2, text="Select the domain:")
        label_serp_domain.place(relx=0.15, rely=0.7, anchor=tk.CENTER)

        self.domain_serp_var = tk.StringVar(value="google.com")
        self.domain_serp_menu = tk.Menubutton(tab2, textvariable=self.domain_serp_var, width=50, borderwidth=1, relief="raised")
        self.domain_serp_menu.place(relx=0.6, rely=0.7, anchor=tk.CENTER)

        self.domain_serp_options = [
            "No Selection","google.ad","google.ae","google.al","google.am","google.as","google.at","google.az","google.ba","google.be","google.bf","google.bg","google.bi",
            "google.bj","google.bs","google.bt","google.by","google.ca","google.cd","google.cf","google.cg","google.ch","google.ci","google.cl","google.cm","google.co.ao",
            "google.co.bw","google.co.ck","google.co.cr","google.co.id","google.co.il","google.co.in","google.co.jp","google.co.ke","google.co.kr","google.co.ls","google.co.ma",
            "google.co.mz","google.co.nz","google.co.th","google.co.tz","google.co.ug","google.co.uk","google.co.uz","google.co.ve","google.co.vi","google.co.za","google.co.zm",
            "google.co.zw","google.com","google.com.af","google.com.ag","google.com.ai","google.com.ar","google.com.au","google.com.bd","google.com.bh","google.com.bn","google.com.bo",
            "google.com.br","google.com.bz","google.com.co","google.com.cu","google.com.cy","google.com.do","google.com.ec","google.com.eg","google.com.et","google.com.fj","google.com.gh",
            "google.com.gi","google.com.gt","google.com.hk","google.com.jm","google.com.kh","google.com.kw","google.com.lb","google.com.ly","google.com.mm","google.com.mt",
            "google.com.mx","google.com.my","google.com.na","google.com.ng","google.com.ni","google.com.np","google.com.om","google.com.pa","google.com.pe","google.com.pg",
            "google.com.ph","google.com.pk","google.com.pr","google.com.py","google.com.qa","google.com.sa","google.com.sb","google.com.sg","google.com.sl","google.com.sv",
            "google.com.tj","google.com.tr","google.com.tw","google.com.ua","google.com.uy","google.com.vc","google.com.vn","google.cv","google.cz","google.de","google.dj",
            "google.dk","google.dm","google.dz","google.ee","google.es","google.fi","google.fm","google.fr","google.ga","google.ge","google.gl","google.gm","google.gp","google.gr",
            "google.gy","google.hn","google.hr","google.ht","google.hu","google.ie","google.iq","google.is","google.it","google.jo","google.kg","google.ki","google.kz","google.la",
            "google.li","google.lk","google.lt","google.lu","google.lv","google.md","google.mg","google.mk","google.ml","google.mn","google.ms","google.mu","google.mv","google.mw",
            "google.ne","google.nl","google.no","google.nr","google.nu","google.pl","google.ps","google.pt","google.ro","google.rs","google.ru","google.rw","google.sc","google.se",
            "google.sh","google.si","google.sk","google.sm","google.sn","google.so","google.sr","google.td","google.tg","google.tk","google.tl","google.tm","google.tn","google.to",
            "google.tt","google.vg","google.vu","google.ws"
        ]

        self.domain_serp_menu.menu = tk.Menu(self.domain_serp_menu, tearoff=0)
        self.domain_serp_menu["menu"] = self.domain_serp_menu.menu

        for domain in self.domain_serp_options:
            self.domain_serp_menu.menu.add_radiobutton(label=domain, variable=self.domain_serp_var, value=domain)

        # Country Menubutton and Menu
        label_serp_country = ttk.Label(tab2, text="Choose the Country:")
        label_serp_country.place(relx=0.15, rely=0.8, anchor=tk.CENTER)

        self.country_serp_var = tk.StringVar(value="United States — us")
        self.country_serp_menu = tk.Menubutton(tab2, textvariable=self.country_serp_var, width=50, borderwidth=1, relief="raised")
        self.country_serp_menu.place(relx=0.6, rely=0.8, anchor=tk.CENTER)

        self.country_serp_options = [
            "No Selection","Afghanistan — af","Albania — al","Algeria — dz","American Samoa — as","Andorra — ad","Angola — ao","Anguilla — ai",
            "Antarctica — aq","Antigua and Barbuda — ag","Argentina — ar","Armenia — am","Aruba — aw","Australia — au","Austria — at","Azerbaijan — az",
            "Bahamas — bs","Bahrain — bh","Bangladesh — bd","Barbados — bb","Belarus — by","Belgium — be","Belize — bz","Benin — bj","Bermuda — bm","Bhutan — bt",
            "Bolivia — bo","Bosnia and Herzegovina — ba","Botswana — bw","Bouvet Island — bv","Brazil — br","British Indian Ocean Territory — io",
            "Brunei Darussalam — bn","Bulgaria — bg","Burkina Faso — bf","Burundi — bi","Cambodia — kh","Cameroon — cm","Canada — ca","Cape Verde — cv",
            "Cayman Islands — ky","Central African Republic — cf","Chad — td","Chile — cl","China — cn","Christmas Island — cx","Cocos (Keeling) Islands — cc",
            "Colombia — co","Comoros — km","Congo — cg","Congo, the Democratic Republic of the — cd","Cook Islands — ck","Costa Rica — cr","Cote D'ivoire — ci",
            "Croatia — hr","Cuba — cu","Cyprus — cy","Czech Republic — cz","Denmark — dk","Djibouti — dj","Dominica — dm","Dominican Republic — do","Ecuador — ec",
            "Egypt — eg","El Salvador — sv","Equatorial Guinea — gq","Eritrea — er","Estonia — ee","Ethiopia — et","Falkland Islands (Malvinas) — fk",
            "Faroe Islands — fo","Fiji — fj","Finland — fi","France — fr","French Guiana — gf","French Polynesia — pf","French Southern Territories — tf",
            "Gabon — ga","Gambia — gm","Georgia — ge","Germany — de","Ghana — gh","Gibraltar — gi","Greece — gr","Greenland — gl","Grenada — gd","Guadeloupe — gp",
            "Guam — gu","Guatemala — gt","Guinea — gn","Guinea-Bissau — gw","Guyana — gy","Haiti — ht","Heard Island and Mcdonald Islands — hm",
            "Holy See (Vatican City State) — va","Honduras — hn","Hong Kong — hk","Hungary — hu","Iceland — is","India — in","Indonesia — id",
            "Iran, Islamic Republic of — ir","Iraq — iq","Ireland — ie","Israel — il","Italy — it","Jamaica — jm","Japan — jp","Jordan — jo",
            "Kazakhstan — kz","Kenya — ke","Kiribati — ki","Korea, Democratic People's Republic of — kp","Korea, Republic of — kr","Kuwait — kw",
            "Kyrgyzstan — kg","Lao People's Democratic Republic — la","Latvia — lv","Lebanon — lb","Lesotho — ls","Liberia — lr","Libyan Arab Jamahiriya — ly",
            "Liechtenstein — li","Lithuania — lt","Luxembourg — lu","Macao — mo","Macedonia, the Former Yugosalv Republic of — mk","Madagascar — mg","Malawi — mw",
            "Malaysia — my","Maldives — mv","Mali — ml","Malta — mt","Marshall Islands — mh","Martinique — mq","Mauritania — mr","Mauritius — mu","Mayotte — yt",
            "Mexico — mx","Micronesia, Federated States of — fm","Moldova, Republic of — md","Monaco — mc","Mongolia — mn","Montserrat — ms","Morocco — ma",
            "Mozambique — mz","Myanmar — mm","Namibia — na","Nauru — nr","Nepal — np","Netherlands — nl","Netherlands Antilles — an","New Caledonia — nc",
            "New Zealand — nz","Nicaragua — ni","Niger — ne","Nigeria — ng","Niue — nu","Norfolk Island — nf","Northern Mariana Islands — mp","Norway — no",
            "Oman — om","Pakistan — pk","Palau — pw","Palestinian Territory, Occupied — ps","Panama — pa","Papua New Guinea — pg","Paraguay — py","Peru — pe",
            "Philippines — ph","Pitcairn — pn","Poland — pl","Portugal — pt","Puerto Rico — pr","Qatar — qa","Reunion — re","Romania — ro","Russian Federation — ru",
            "Rwanda — rw","Saint Helena — sh","Saint Kitts and Nevis — kn","Saint Lucia — lc","Saint Pierre and Miquelon — pm","Saint Vincent and the Grenadines — vc",
            "Samoa — ws","San Marino — sm","Sao Tome and Principe — st","Saudi Arabia — sa","Senegal — sn","Serbia and Montenegro — rs","Seychelles — sc",
            "Sierra Leone — sl","Singapore — sg","Slovakia — sk","Slovenia — si","Solomon Islands — sb","Somalia — so","South Africa — za",
            "South Georgia and the South Sandwich Islands — gs","Spain — es","Sri Lanka — lk","Sudan — sd","Suriname — sr","Svalbard and Jan Mayen — sj",
            "Swaziland — sz","Sweden — se","Switzerland — ch","Syrian Arab Republic — sy","Taiwan, Province of China — tw","Tajikistan — tj",
            "Tanzania, United Republic of — tz","Thailand — th","Timor-Leste — tl","Togo — tg","Tokelau — tk","Tonga — to","Trinidad and Tobago — tt",
            "Tunisia — tn","Turkey — tr","Turkmenistan — tm","Turks and Caicos Islands — tc","Tuvalu — tv","Uganda — ug","Ukraine — ua","United Arab Emirates — ae",
            "United Kingdom — uk","United Kingdom — gb","United States — us","United States Minor Outlying Islands — um","Uruguay — uy","Uzbekistan — uz","Vanuatu — vu",
            "Venezuela — ve","Viet Nam — vn","Virgin Islands, British — vg","Virgin Islands, U.S. — vi","Wallis and Futuna — wf","Western Sahara — eh",
            "Yemen — ye","Zambia — zm","Zimbabwe — zw"
        ]

        self.country_serp_menu.menu = tk.Menu(self.country_serp_menu, tearoff=0)
        self.country_serp_menu["menu"] = self.country_serp_menu.menu

        for country in self.country_serp_options:
            self.country_serp_menu.menu.add_radiobutton(label=country, variable=self.country_serp_var, value=country)
        

        # Add the "Save as Excel" and "Save as JSON" checkboxes
        self.var_save_as_serp_excel = tk.BooleanVar()
        self.var_save_as_serp_json = tk.BooleanVar()

        self.checkbutton_serp_excel = ttk.Checkbutton(tab2, text="Save as Excel", variable=self.var_save_as_serp_excel)
        self.checkbutton_serp_excel.place(relx=0.3, rely=0.9, anchor=tk.CENTER)

        self.checkbutton_serp_json = ttk.Checkbutton(tab2, text="Save as JSON", variable=self.var_save_as_serp_json)
        self.checkbutton_serp_json.place(relx=0.7, rely=0.9, anchor=tk.CENTER)


        # Add the "Run" button
        button_serp_run = ttk.Button(tab2, text="Run", command=self.on_run_serp_clicked, style='Large.TButton')
        button_serp_run.place(relx=0.5, rely=0.95, anchor=tk.CENTER)



        #Tab3

        label_keyword = ttk.Label(tab3, text="Keyword:", font=('Helvetica', 12))
        label_keyword.place(relx=0.15, rely=0.1, anchor=tk.CENTER)

        self.entry_keyword = ttk.Entry(tab3, width=50)
        self.entry_keyword.place(relx=0.6, rely=0.1, anchor=tk.CENTER)

        label_domain = ttk.Label(tab3, text="Domain:", font=('Helvetica', 12))
        label_domain.place(relx=0.15, rely=0.2, anchor=tk.CENTER)
        

        self.entry_domain = ttk.Entry(tab3, width=50)
        self.entry_domain.place(relx=0.6, rely=0.2, anchor=tk.CENTER)

        self.entry_domain.insert(0, "com")

        label_start = ttk.Label(tab3, text="Start:", font=('Helvetica', 12))
        label_start.place(relx=0.15, rely=0.3, anchor=tk.CENTER)

        self.entry_start = ttk.Entry(tab3, width=50)
        self.entry_start.place(relx=0.6, rely=0.3, anchor=tk.CENTER)
        self.entry_start.insert(0, "0")

        label_ll = ttk.Label(tab3, text="LL:", font=('Helvetica', 12))
        label_ll.place(relx=0.15, rely=0.4, anchor=tk.CENTER)

        self.entry_ll = ttk.Entry(tab3, width=50)
        self.entry_ll.place(relx=0.6, rely=0.4, anchor=tk.CENTER)

        self.entry_ll.insert(0, "@40.7455096,-74.0083012,14z")

        label_country = ttk.Label(tab3, text="Country:", font=('Helvetica', 12))
        label_country.place(relx=0.15, rely=0.5, anchor=tk.CENTER)

        self.country_var = tk.StringVar()
        self.country_var.set("Select Country")  # Значение по умолчанию

        self.country_menu = tk.Menubutton(tab3, width=50, textvariable=self.country_var, borderwidth=1, relief="raised")
        self.country_menu.place(relx=0.6, rely=0.5, anchor=tk.CENTER)

        self.country_menu.menu = tk.Menu(self.country_menu, tearoff=0)
        self.country_menu["menu"] = self.country_menu.menu

        countries = ["USA", "United Kingdom", "Germany", "Ireland", "France", "Italy",
                     "Sweden", "Brazil", "Canada", "Japan", "Singapore", "India", "Indonesia"]

        for country in countries:
            self.country_menu.menu.add_radiobutton(label=country, variable=self.country_var, value=country)

        self.var_save_as_excel = tk.BooleanVar()
        self.var_save_as_json = tk.BooleanVar()

        checkbutton_excel = ttk.Checkbutton(tab3, text="Save as Excel", variable=self.var_save_as_excel)
        checkbutton_excel.place(relx=0.3, rely=0.65, anchor=tk.CENTER)

        checkbutton_json = ttk.Checkbutton(tab3, text="Save as JSON", variable=self.var_save_as_json)
        checkbutton_json.place(relx=0.7, rely=0.65, anchor=tk.CENTER)

        button_run = ttk.Button(tab3, text="Run", command=self.on_run_maps_clicked, style='Large.TButton')
        button_run.place(relx=0.5, rely=0.8, anchor=tk.CENTER)


        ###### Tab5

        label_gen_domain = ttk.Label(tab5, text="Put a Link to Scrape:", font=('Helvetica', 12))
        label_gen_domain.place(relx=0.2, rely=0.1, anchor=tk.CENTER)

        self.entry_gen_domain = ttk.Entry(tab5, width=50)
        self.entry_gen_domain.place(relx=0.65, rely=0.1, anchor=tk.CENTER)
        self.entry_gen_domain.insert(0, "https://esprima.org/demo/parse.html")

        label_chatgpt_prompt = ttk.Label(tab5, text="Put a Prompt to ChatGPT:", font=('Helvetica', 12))
        label_chatgpt_prompt.place(relx=0.2, rely=0.2, anchor=tk.CENTER)

        self.entry_chatgpt_prompt = ttk.Entry(tab5, width=50)
        self.entry_chatgpt_prompt.place(relx=0.65, rely=0.2, anchor=tk.CENTER)

        self.text_area = scrolledtext.ScrolledText(tab5, wrap=tk.WORD, width=80, height=15)
        self.text_area.place(relx=0.5, rely=0.67, anchor=tk.CENTER)

        self.example_text = "Here will be result."
        self.text_area.insert(tk.INSERT, self.example_text)

        # Add the "Run" button

        button_generation_run = ttk.Button(tab5, text="Return all Text from site", command=self.on_run_text_gen_clicked, style='Large.TButton')
        button_generation_run.place(relx=0.25, rely=0.32, anchor=tk.CENTER)

        button_generation_run = ttk.Button(tab5, text="Run Generation", command=self.on_run_gen_clicked, style='Success')
        button_generation_run.place(relx=0.75, rely=0.32, anchor=tk.CENTER)

        ###### Tab6

        label_link_shopify = ttk.Label(tab6, text="Link:", font=('Helvetica', 12))
        label_link_shopify.place(relx=0.15, rely=0.1, anchor=tk.CENTER)

        self.entry_link_shopify = ttk.Entry(tab6, width=55)
        self.entry_link_shopify.place(relx=0.65, rely=0.1, anchor=tk.CENTER)
        self.entry_link_shopify.insert(0, "https://libertasbella.com")

        label_limit_shopify = ttk.Label(tab6, text="Limit (from 1 to 250):", font=('Helvetica', 12))
        label_limit_shopify.place(relx=0.15, rely=0.2, anchor=tk.CENTER)

        self.entry_limit_shopify = ttk.Entry(tab6, width=55)
        self.entry_limit_shopify.place(relx=0.65, rely=0.2, anchor=tk.CENTER)

        label_page_shopify = ttk.Label(tab6, text="Page:", font=('Helvetica', 12))
        label_page_shopify.place(relx=0.15, rely=0.3, anchor=tk.CENTER)

        self.entry_page_shopify = ttk.Entry(tab6, width=55)
        self.entry_page_shopify.place(relx=0.65, rely=0.3, anchor=tk.CENTER)

        label_col_shopify = ttk.Label(tab6, text="Collection:", font=('Helvetica', 12))
        label_col_shopify.place(relx=0.15, rely=0.4, anchor=tk.CENTER)

        self.entry_col_shopify = ttk.Entry(tab6, width=55)
        self.entry_col_shopify.place(relx=0.65, rely=0.4, anchor=tk.CENTER)


        self.var_save_shopify_as_excel = tk.BooleanVar()
        self.var_save_shopify_as_json = tk.BooleanVar()

        checkbutton_shopify_excel = ttk.Checkbutton(tab6, text="Save as Excel", variable=self.var_save_shopify_as_excel)
        checkbutton_shopify_excel.place(relx=0.3, rely=0.8, anchor=tk.CENTER)

        checkbutton_shopify_json = ttk.Checkbutton(tab6, text="Save as JSON", variable=self.var_save_shopify_as_json)
        checkbutton_shopify_json.place(relx=0.7, rely=0.8, anchor=tk.CENTER)


        #Buttons

        button_generation_run = ttk.Button(tab6, width=30, text="Get Collection", command=self.on_run_get_coll, style='Large.TButton')
        button_generation_run.place(relx=0.25, rely=0.9, anchor=tk.CENTER)

        button_generation_run = ttk.Button(tab6, width=30, text="Get Products", command=self.on_run_get_prod, style='Success')
        button_generation_run.place(relx=0.75, rely=0.9, anchor=tk.CENTER)


        ###### Tab7

        label_property = ttk.Label(tab7, text="Zillow Property", font=('Helvetica', 12))
        label_property.place(relx=0.55, rely=0.1, anchor=tk.CENTER)

        label_link_zillow = ttk.Label(tab7, text="Link to Property:", font=('Helvetica', 12))
        label_link_zillow.place(relx=0.12, rely=0.2, anchor=tk.CENTER)

        self.entry_link_zillow = ttk.Entry(tab7, width=55)
        self.entry_link_zillow.place(relx=0.55, rely=0.2, anchor=tk.CENTER)
        self.entry_link_zillow.insert(0, "https://www.zillow.com/homedetails/301-E-79th-St-APT-23S-New-York-NY-10075/31543731_zpid/")

        button_generation_run = ttk.Button(tab7, text="Get", command=self.on_run_zillow_property, style='Large.TButton')
        button_generation_run.place(relx=0.91, rely=0.2, anchor=tk.CENTER)

        label_listing = ttk.Label(tab7, text="Zillow Listing", font=('Helvetica', 12))
        label_listing.place(relx=0.55, rely=0.35, anchor=tk.CENTER)

        self.property_params = []

# # Sort

        label_keyword_zillow = ttk.Label(tab7, text="Keyword:", font=('Helvetica', 12))
        label_keyword_zillow.place(relx=0.15, rely=0.45, anchor=tk.CENTER)

        self.entry_keyword_zillow = ttk.Entry(tab7, width=55)
        self.entry_keyword_zillow.place(relx=0.55, rely=0.45, anchor=tk.CENTER)


        # Type

        self.property_type_var = tk.StringVar()
        self.property_type_var.set("Type")

        self.property_type_menu = tk.Menubutton(tab7, width=55, textvariable=self.property_type_var, borderwidth=1, relief="raised")
        self.property_type_menu.place(relx=0.55, rely=0.55, anchor=tk.CENTER)

        self.property_type_options = ["forSale", "forRent", "sold"]

        self.property_type_menu.menu = tk.Menu(self.property_type_menu, tearoff=0)
        self.property_type_menu["menu"] = self.property_type_menu.menu

        for type_option in self.property_type_options:
            self.property_type_menu.menu.add_radiobutton(label=type_option, variable=self.property_type_var, value=type_option)

        self.property_params.append(("type", self.property_type_var))

        # Home Types    

        self.property_home_types_var = tk.StringVar()
        self.property_home_types_var.set("Home Types")

        self.property_home_types_menu = tk.Menubutton(tab7, width=55, textvariable=self.property_home_types_var, borderwidth=1, relief="raised")
        self.property_home_types_menu.place(relx=0.55, rely=0.65, anchor=tk.CENTER)

        self.property_home_types_options = ["house", "townhome", "multiFamily", "condo", "lot", "apartment", "manufactured"]

        self.property_home_types_menu.menu = tk.Menu(self.property_home_types_menu, tearoff=0)
        self.property_home_types_menu["menu"] = self.property_home_types_menu.menu

        home_type_var = tk.StringVar()  # Variable to hold the selected home type

        for home_type_option in self.property_home_types_options:
            self.property_home_types_menu.menu.add_radiobutton(label=home_type_option, variable=self.property_home_types_var, value=home_type_option)

        self.property_params.append(("homeTypes", home_type_var))

        self.var_save_zillow_as_excel = tk.BooleanVar()
        self.var_save_zillow_as_json = tk.BooleanVar()

        checkbutton_zillow_excel = ttk.Checkbutton(tab7, text="Save as Excel", variable=self.var_save_zillow_as_excel)
        checkbutton_zillow_excel.place(relx=0.4, rely=0.8, anchor=tk.CENTER)

        checkbutton_zillow_json = ttk.Checkbutton(tab7, text="Save as JSON", variable=self.var_save_zillow_as_json)
        checkbutton_zillow_json.place(relx=0.7, rely=0.8, anchor=tk.CENTER)

        # Add the "Run" button

        button_generation_run = ttk.Button(tab7, text="Get Listing Data", command=self.on_run_zillow_clicked, style='Success')
        button_generation_run.place(relx=0.55, rely=0.9, anchor=tk.CENTER)



        ###### Tab8
        
        label_link_any_domain = ttk.Label(tab8, text="Put a Link to Scrape:", font=('Helvetica', 12))
        label_link_any_domain.place(relx=0.15, rely=0.1, anchor=tk.CENTER)

        self.entry_link_any_domain = ttk.Entry(tab8, width=60)
        self.entry_link_any_domain.place(relx=0.65, rely=0.1, anchor=tk.CENTER)
        self.entry_link_any_domain.insert(0, "https://esprima.org/demo/parse.html")

        label_any_proxy = ttk.Label(tab8, text="Proxy:", font=('Helvetica', 12))
        label_any_proxy.place(relx=0.1, rely=0.2, anchor=tk.CENTER)

        self.any_proxy_type_var = tk.StringVar()
        self.any_proxy_type_var.set("datacenter")

        self.any_proxy_type_menu = tk.Menubutton(tab8, width=20, textvariable=self.any_proxy_type_var, borderwidth=1, relief="raised")
        self.any_proxy_type_menu.place(relx=0.45, rely=0.2, anchor=tk.CENTER)

        self.any_proxy_type_options = ["datacenter", "residential"]
        self.any_proxy_type_menu.menu = tk.Menu(self.any_proxy_type_menu, tearoff=0)
        self.any_proxy_type_menu["menu"] = self.any_proxy_type_menu.menu

        for any_proxy_type in self.any_proxy_type_options:
            self.any_proxy_type_menu.menu.add_radiobutton(label=any_proxy_type, variable=self.any_proxy_type_var, value=any_proxy_type)

        self.any_proxy_country_type_var = tk.StringVar()
        self.any_proxy_country_type_var.set("USA")

        self.any_proxy_country_type_menu = tk.Menubutton(tab8, width=20, textvariable=self.any_proxy_country_type_var, borderwidth=1, relief="raised")
        self.any_proxy_country_type_menu.place(relx=0.7, rely=0.2, anchor=tk.CENTER)

        self.any_proxy_country_type_options = ["USA", "United Kingdom", "Germany", "Ireland", "France", "Italy", "Sweden", "Brazil", "Canada", "Japan", "Singapore", "India", "Indonesia"]
        self.any_proxy_country_type_menu.menu = tk.Menu(self.any_proxy_country_type_menu, tearoff=0)
        self.any_proxy_country_type_menu["menu"] = self.any_proxy_country_type_menu.menu

        for any_proxy_country_type in self.any_proxy_country_type_options:
            self.any_proxy_country_type_menu.menu.add_radiobutton(label=any_proxy_country_type, variable=self.any_proxy_country_type_var, value=any_proxy_country_type)

        self.var_use_proxy = tk.BooleanVar()

        checkbutton_use_proxy = ttk.Checkbutton(tab8, text="Use proxy", variable=self.var_use_proxy)
        checkbutton_use_proxy.place(relx=0.9, rely=0.2, anchor=tk.CENTER)

        label_rules = ttk.Label(tab8, text="Title", font=('Helvetica', 7))
        label_rules.place(relx=0.45, rely=0.26, anchor=tk.CENTER)

        label_rules = ttk.Label(tab8, text="CSS Selector", font=('Helvetica', 7))
        label_rules.place(relx=0.7, rely=0.26, anchor=tk.CENTER)

        label_rules = ttk.Label(tab8, text="Extraction Rules:", font=('Helvetica', 12))
        label_rules.place(relx=0.15, rely=0.3, anchor=tk.CENTER)

        self.scrolled_frame = ScrolledFrame(tab8)
        self.scrolled_frame.place(relx=0.6, rely=0.5, anchor=tk.CENTER)

        self.rule_entry_list = []  

        add_rule_button = ttk.Button(tab8, text="+", command=self.add_rule, style='Success')
        add_rule_button.place(relx=0.9, rely=0.3, anchor=tk.CENTER)

        self.var_save_any_as_excel = tk.BooleanVar()
        self.var_save_any_as_json = tk.BooleanVar()

        checkbutton_any_excel = ttk.Checkbutton(tab8, text="Save as Excel", variable=self.var_save_any_as_excel)
        checkbutton_any_excel.place(relx=0.3, rely=0.8, anchor=tk.CENTER)

        checkbutton_any_json = ttk.Checkbutton(tab8, text="Save as JSON", variable=self.var_save_any_as_json)
        checkbutton_any_json.place(relx=0.7, rely=0.8, anchor=tk.CENTER)


        # Add the "Run" button

        button_generation_run = ttk.Button(tab8, text="Run", command=self.on_run_any_tab_clicked, style='Success')
        button_generation_run.place(relx=0.5, rely=0.9, anchor=tk.CENTER)



        ###### Settings

        self.proxy_countries = {
            "USA": "US",
            "United Kingdom": "UK",
            "Germany": "DE",
            "Ireland": "IE",
            "France": "FR",
            "Italy": "IT",
            "Sweden": "SE",
            "Brazil": "BR",
            "Canada": "CA",
            "Japan": "JP",
            "Singapore": "SG",
            "India": "IN",
            "Indonesia": "ID"
        }


        self.serp_domain_codes = {
            "No Selection": "",
            "google.ad": "google.ad", "google.ae": "google.ae", "google.al": "google.al", "google.am": "google.am", "google.as": "google.as", "google.at": "google.at",
            "google.az": "google.az", "google.ba": "google.ba", "google.be": "google.be", "google.bf": "google.bf", "google.bg": "google.bg", "google.bi": "google.bi",
            "google.bj": "google.bj", "google.bs": "google.bs", "google.bt": "google.bt", "google.by": "google.by", "google.ca": "google.ca", "google.cd": "google.cd",
            "google.cf": "google.cf", "google.cg": "google.cg", "google.ch": "google.ch", "google.ci": "google.ci", "google.cl": "google.cl", "google.cm": "google.cm",
            "google.co.ao": "google.co.ao", "google.co.bw": "google.co.bw", "google.co.ck": "google.co.ck", "google.co.cr": "google.co.cr", "google.co.id": "google.co.id",
            "google.co.il": "google.co.il", "google.co.in": "google.co.in", "google.co.jp": "google.co.jp", "google.co.ke": "google.co.ke", "google.co.kr": "google.co.kr",
            "google.co.ls": "google.co.ls", "google.co.ma": "google.co.ma", "google.co.mz": "google.co.mz", "google.co.nz": "google.co.nz", "google.co.th": "google.co.th",
            "google.co.tz": "google.co.tz", "google.co.ug": "google.co.ug", "google.co.uk": "google.co.uk", "google.co.uz": "google.co.uz", "google.co.ve": "google.co.ve",
            "google.co.vi": "google.co.vi", "google.co.za": "google.co.za", "google.co.zm": "google.co.zm", "google.co.zw": "google.co.zw", "google.com": "google.com", "google.com.af": "google.com.af",
            "google.com.ag": "google.com.ag", "google.com.ai": "google.com.ai", "google.com.ar": "google.com.ar", "google.com.au": "google.com.au", "google.com.bd": "google.com.bd",
            "google.com.bh": "google.com.bh", "google.com.bn": "google.com.bn", "google.com.bo": "google.com.bo", "google.com.br": "google.com.br", "google.com.bz": "google.com.bz",
            "google.com.co": "google.com.co", "google.com.cu": "google.com.cu", "google.com.cy": "google.com.cy", "google.com.do": "google.com.do", "google.com.ec": "google.com.ec",
            "google.com.eg": "google.com.eg", "google.com.et": "google.com.et", "google.com.fj": "google.com.fj", "google.com.gh": "google.com.gh", "google.com.gi": "google.com.gi",
            "google.com.gt": "google.com.gt", "google.com.hk": "google.com.hk", "google.com.jm": "google.com.jm", "google.com.kh": "google.com.kh", "google.com.kw": "google.com.kw",
            "google.com.lb": "google.com.lb", "google.com.ly": "google.com.ly", "google.com.mm": "google.com.mm", "google.com.mt": "google.com.mt", "google.com.mx": "google.com.mx",
            "google.com.my": "google.com.my", "google.com.na": "google.com.na", "google.com.ng": "google.com.ng", "google.com.ni": "google.com.ni", "google.com.np": "google.com.np",
            "google.com.om": "google.com.om", "google.com.pa": "google.com.pa", "google.com.pe": "google.com.pe", "google.com.pg": "google.com.pg", "google.com.ph": "google.com.ph", "google.com.pk": "google.com.pk",
            "google.com.pr": "google.com.pr", "google.com.py": "google.com.py", "google.com.qa": "google.com.qa", "google.com.sa": "google.com.sa", "google.com.sb": "google.com.sb",
            "google.com.sg": "google.com.sg", "google.com.sl": "google.com.sl", "google.com.sv": "google.com.sv", "google.com.tj": "google.com.tj", "google.com.tr": "google.com.tr",
            "google.com.tw": "google.com.tw", "google.com.ua": "google.com.ua", "google.com.uy": "google.com.uy", "google.com.vc": "google.com.vc", "google.com.vn": "google.com.vn",
            "google.cv": "google.cv", "google.cz": "google.cz", "google.de": "google.de", "google.dj": "google.dj", "google.dk": "google.dk", "google.dm": "google.dm",
            "google.dz": "google.dz", "google.ee": "google.ee", "google.es": "google.es", "google.fi": "google.fi", "google.fm": "google.fm", "google.fr": "google.fr", "google.ga": "google.ga",
            "google.ge": "google.ge", "google.gl": "google.gl", "google.gm": "google.gm", "google.gp": "google.gp", "google.gr": "google.gr", "google.gy": "google.gy", "google.hn": "google.hn",
            "google.hr": "google.hr", "google.ht": "google.ht", "google.hu": "google.hu", "google.ie": "google.ie", "google.iq": "google.iq", "google.is": "google.is",
            "google.it": "google.it", "google.jo": "google.jo", "google.kg": "google.kg", "google.ki": "google.ki", "google.kz": "google.kz", "google.la": "google.la", "google.li": "google.li",
            "google.lk": "google.lk", "google.lt": "google.lt", "google.lu": "google.lu", "google.lv": "google.lv", "google.md": "google.md", "google.mg": "google.mg", "google.mk": "google.mk",
            "google.ml": "google.ml", "google.mn": "google.mn", "google.ms": "google.ms", "google.mu": "google.mu", "google.mv": "google.mv", "google.mw": "google.mw", "google.ne": "google.ne",
            "google.nl": "google.nl", "google.no": "google.no", "google.nr": "google.nr", "google.nu": "google.nu", "google.pl": "google.pl", "google.ps": "google.ps", "google.pt": "google.pt",
            "google.ro": "google.ro", "google.rs": "google.rs", "google.ru": "google.ru", "google.rw": "google.rw", "google.sc": "google.sc", "google.se": "google.se",
            "google.sh": "google.sh", "google.si": "google.si", "google.sk": "google.sk", "google.sm": "google.sm", "google.sn": "google.sn", "google.so": "google.so",
            "google.sr": "google.sr", "google.td": "google.td", "google.tg": "google.tg", "google.tk": "google.tk", "google.tl": "google.tl", "google.tm": "google.tm",
            "google.tn": "google.tn", "google.to": "google.to", "google.tt": "google.tt", "google.vg": "google.vg", "google.vu": "google.vu", "google.ws": "google.ws"
        }
        self.serp_language_codes = {
            "No Selection": "", "Afrikaans — af": "af", "Akan — ak": "ak", "Albanian — sq": "sq", "Samoa — ws": "ws", "Amharic — am": "am", "Arabic — ar": "ar", "Armenian — hy": "hy",
            "Azerbaijani — az": "az", "Basque — eu": "eu", "Belarusian — be": "be", "Bemba — bem": "bem", "Bengali — bn": "bn", "Bihari — bh": "bh", "Bork, bork, bork! — xx-bork": "xx-bork",
            "Bosnian — bs": "bs", "Breton — br": "br", "Bulgarian — bg": "bg", "Bhutanese — bt": "bt", "Cambodian — km": "km", "Catalan — ca": "ca", "Cherokee — chr": "chr",
            "Chichewa — ny": "ny", "Chinese (Simplified) — zh-cn": "zh-cn", "Chinese (Traditional) — zh-tw": "zh-tw", "Corsican — co": "co", "Croatian — hr": "hr",
            "Czech — cs": "cs", "Danish — da": "da", "Dutch — nl": "nl", "Elmer Fudd — xx-elmer": "xx-elmer", "English — en": "en", "Esperanto — eo": "eo", "Estonian — et": "et",
            "Ewe — ee": "ee", "Faroese — fo": "fo", "Filipino — tl": "tl", "Finnish — fi": "fi", "French — fr": "fr", "Frisian — fy": "fy", "Ga — gaa": "gaa", "Galician — gl": "gl",
            "Georgian — ka": "ka", "German — de": "de", "Greek — el": "el", "Greenlandic — kl": "kl", "Guarani — gn": "gn", "Gujarati — gu": "gu", "Hacker — xx-hacker": "xx-hacker",
            "Haitian Creole — ht": "ht", "Hausa — ha": "ha", "Hawaiian — haw": "haw", "Hebrew — iw": "iw", "Hindi — hi": "hi", "Hungarian — hu": "hu", "Icelandic — is": "is",
            "Igbo — ig": "ig", "Indonesian — id": "id", "Interlingua — ia": "ia", "Irish — ga": "ga", "Italian — it": "it", "Japanese — ja": "ja", "Javanese — jw": "jw",
            "Kannada — kn": "kn", "Kazakh — kk": "kk", "Kinyarwanda — rw": "rw", "Kirundi — rn": "rn", "Klingon — xx-klingon": "xx-klingon", "Kongo — kg": "kg", "Korean — ko": "ko",
            "Krio (Sierra Leone) — kri": "kri", "Kurdish — ku": "ku", "Kurdish (Soranî) — ckb": "ckb", "Kyrgyz — ky": "ky", "Laothian — lo": "lo", "Latin — la": "la", "Latvian — lv": "lv",
            "Lingala — ln": "ln", "Lithuanian — lt": "lt", "Lozi — loz": "loz", "Luganda — lg": "lg", "Luo — ach": "ach", "Macedonian — mk": "mk", "Malagasy — mg": "mg",
            "Malay — my": "my", "Malayalam — ml": "ml", "Maltese — mt": "mt", "Maldives — mv": "mv", "Maori — mi": "mi", "Marathi — mr": "mr", "Mauritian Creole — mfe": "mfe",
            "Moldavian — mo": "mo", "Mongolian — mn": "mn", "Montenegrin — sr-me": "sr-me", "Nepali — ne": "ne", "Nigerian Pidgin — pcm": "pcm", "Northern Sotho — nso": "nso", "Norwegian — no": "no",
            "Norwegian (Nynorsk) — nn": "nn", "Occitan — oc": "oc", "Oriya — or": "or", "Oromo — om": "om", "Pashto — ps": "ps", "Persian — fa": "fa", "Pirate — xx-pirate": "xx-pirate",
            "Polish — pl": "pl", "Portuguese — pt": "pt", "Portuguese (Brazil) — pt-br": "pt-br", "Portuguese (Portugal) — pt-pt": "pt-pt", "Punjabi — pa": "pa", "Quechua — qu": "qu",
            "Romanian — ro": "ro", "Romansh — rm": "rm", "Runyakitara — nyn": "nyn", "Russian — ru": "ru", "Scots Gaelic — gd": "gd", "Serbian — sr": "sr", "Serbo-Croatian — sh": "sh",
            "Sesotho — st": "st", "Setswana — tn": "tn", "Seychellois Creole — crs": "crs", "Shona — sn": "sn", "Sindhi — sd": "sd", "Sinhalese — si": "si", "Slovak — sk": "sk",
            "Slovenian — sl": "sl", "Somali — so": "so", "Spanish — es": "es", "Spanish (Latin American) — es-419": "es-419", "Sundanese — su": "su", "Swahili — sw": "sw",
            "Swedish — sv": "sv", "Tajik — tg": "tg", "Tamil — ta": "ta", "Tatar — tt": "tt", "Telugu — te": "te", "Thai — th": "th", "Tigrinya — ti": "ti", "Tonga — to": "to",
            "Tshiluba — lua": "lua", "Tumbuka — tum": "tum", "Turkish — tr": "tr", "Turkmen — tk": "tk", "Twi — tw": "tw", "Uighur — ug": "ug", "Ukrainian — uk": "uk",
            "Urdu — ur": "ur", "Uzbek — uz": "uz", "Vanuatu — vu": "vu", "Vietnamese — vi": "vi", "Welsh — cy": "cy", "Wolof — wo": "wo", "Xhosa — xh": "xh",
            "Yiddish — yi": "yi", "Yoruba — yo": "yo", "Zulu — zu": "zu",
        }
        
        self.serp_country_codes = {
            "No Selection": "", "Afghanistan — af": "af", "Albania — al": "al", "Algeria — dz": "dz", "American Samoa — as": "as", "Andorra — ad": "ad", "Angola — ao": "ao",
            "Anguilla — ai": "ai", "Antarctica — aq": "aq", "Antigua and Barbuda — ag": "ag", "Argentina — ar": "ar", "Armenia — am": "am", "Aruba — aw": "aw", "Australia — au": "au",
            "Austria — at": "at", "Azerbaijan — az": "az", "Bahamas — bs": "bs", "Bahrain — bh": "bh", "Bangladesh — bd": "bd", "Barbados — bb": "bb", "Belarus — by": "by",
            "Belgium — be": "be", "Belize — bz": "bz", "Benin — bj": "bj", "Bermuda — bm": "bm", "Bhutan — bt": "bt", "Bolivia — bo": "bo", "Bosnia and Herzegovina — ba": "ba", "Botswana — bw": "bw",
            "Bouvet Island — bv": "bv", "Brazil — br": "br", "British Indian Ocean Territory — io": "io", "Brunei Darussalam — bn": "bn", "Bulgaria — bg": "bg", "Burkina Faso — bf": "bf",
            "Burundi — bi": "bi", "Cambodia — kh": "kh", "Cameroon — cm": "cm", "Canada — ca": "ca", "Cape Verde — cv": "cv", "Cayman Islands — ky": "ky", "Central African Republic — cf": "cf",
            "Chad — td": "td", "Chile — cl": "cl", "China — cn": "cn", "Christmas Island — cx": "cx", "Cocos (Keeling) Islands — cc": "cc", "Colombia — co": "co", "Comoros — km": "km",
            "Congo — cg": "cg", "Congo, the Democratic Republic of the — cd": "cd", "Cook Islands — ck": "ck", "Costa Rica — cr": "cr", "Cote D'ivoire — ci": "ci", "Croatia — hr": "hr",
            "Cuba — cu": "cu", "Cyprus — cy": "cy", "Czech Republic — cz": "cz", "Denmark — dk": "dk", "Djibouti — dj": "dj", "Dominica — dm": "dm", "Dominican Republic — do": "do",
            "Ecuador — ec": "ec", "Egypt — eg": "eg", "El Salvador — sv": "sv", "Equatorial Guinea — gq": "gq", "Eritrea — er": "er", "Estonia — ee": "ee", "Ethiopia — et": "et",
            "Falkland Islands (Malvinas) — fk": "fk", "Faroe Islands — fo": "fo", "Fiji — fj": "fj", "Finland — fi": "fi", "France — fr": "fr", "French Guiana — gf": "gf", "French Polynesia — pf": "pf",
            "French Southern Territories — tf": "tf", "Gabon — ga": "ga", "Gambia — gm": "gm", "Georgia — ge": "ge", "Germany — de": "de", "Ghana — gh": "gh", "Gibraltar — gi": "gi",
            "Greece — gr": "gr", "Greenland — gl": "gl", "Grenada — gd": "gd", "Guadeloupe — gp": "gp", "Guam — gu": "gu", "Guatemala — gt": "gt", "Guinea — gn": "gn", "Guinea-Bissau — gw": "gw",
            "Guyana — gy": "gy", "Haiti — ht": "ht", "Heard Island and Mcdonald Islands — hm": "hm", "Holy See (Vatican City State) — va": "va", "Honduras — hn": "hn", "Hong Kong — hk": "hk",
            "Hungary — hu": "hu", "Iceland — is": "is", "India — in": "in", "Indonesia — id": "id", "Iran, Islamic Republic of — ir": "ir", "Iraq — iq": "iq", "Ireland — ie": "ie",
            "Israel — il": "il", "Italy — it": "it", "Jamaica — jm": "jm", "Japan — jp": "jp", "Jordan — jo": "jo", "Kazakhstan — kz": "kz", "Kenya — ke": "ke", "Kiribati — ki": "ki",
            "Korea, Democratic People's Republic of — kp": "kp", "Korea, Republic of — kr": "kr", "Kuwait — kw": "kw", "Kyrgyzstan — kg": "kg", "Lao People's Democratic Republic — la": "la", "Latvia — lv": "lv",
            "Lebanon — lb": "lb", "Lesotho — ls": "ls", "Liberia — lr": "lr", "Libyan Arab Jamahiriya — ly": "ly", "Liechtenstein — li": "li", "Lithuania — lt": "lt", "Luxembourg — lu": "lu",
            "Macao — mo": "mo", "Macedonia, the Former Yugosalv Republic of — mk": "mk", "Madagascar — mg": "mg", "Malawi — mw": "mw", "Malaysia — my": "my", "Maldives — mv": "mv",
            "Mali — ml": "ml", "Malta — mt": "mt", "Marshall Islands — mh": "mh", "Martinique — mq": "mq", "Mauritania — mr": "mr", "Mauritius — mu": "mu", "Mayotte — yt": "yt",
            "Mexico — mx": "mx", "Micronesia, Federated States of — fm": "fm", "Moldova, Republic of — md": "md", "Monaco — mc": "mc", "Mongolia — mn": "mn", "Montserrat — ms": "ms",
            "Morocco — ma": "ma", "Mozambique — mz": "mz", "Myanmar — mm": "mm", "Namibia — na": "na", "Nauru — nr": "nr", "Nepal — np": "np", "Netherlands — nl": "nl", "Netherlands Antilles — an": "an",
            "New Caledonia — nc": "nc", "New Zealand — nz": "nz", "Nicaragua — ni": "ni", "Niger — ne": "ne", "Nigeria — ng": "ng", "Niue — nu": "nu", "Norfolk Island — nf": "nf", "Northern Mariana Islands — mp": "mp",
            "Norway — no": "no", "Oman — om": "om", "Pakistan — pk": "pk", "Palau — pw": "pw", "Palestinian Territory, Occupied — ps": "ps", "Panama — pa": "pa", "Papua New Guinea — pg": "pg",
            "Paraguay — py": "py", "Peru — pe": "pe", "Philippines — ph": "ph", "Pitcairn — pn": "pn", "Poland — pl": "pl", "Portugal — pt": "pt", "Puerto Rico — pr": "pr",
            "Qatar — qa": "qa", "Reunion — re": "re", "Romania — ro": "ro", "Russian Federation — ru": "ru", "Rwanda — rw": "rw", "Saint Helena — sh": "sh", "Saint Kitts and Nevis — kn": "kn",
            "Saint Lucia — lc": "lc", "Saint Pierre and Miquelon — pm": "pm", "Saint Vincent and the Grenadines — vc": "vc", "Samoa — ws": "ws", "San Marino — sm": "sm", "Sao Tome and Principe — st": "st",
            "Saudi Arabia — sa": "sa", "Senegal — sn": "sn", "Serbia and Montenegro — rs": "rs", "Seychelles — sc": "sc", "Sierra Leone — sl": "sl", "Singapore — sg": "sg",
            "Slovakia — sk": "sk", "Slovenia — si": "si", "Solomon Islands — sb": "sb", "Somalia — so": "so", "South Africa — za": "za", "South Georgia and the South Sandwich Islands — gs": "gs", "Spain — es": "es",
            "Sri Lanka — lk": "lk", "Sudan — sd": "sd", "Suriname — sr": "sr", "Svalbard and Jan Mayen — sj": "sj", "Swaziland — sz": "sz", "Sweden — se": "se", "Switzerland — ch": "ch",
            "Syrian Arab Republic — sy": "sy", "Taiwan, Province of China — tw": "tw", "Tajikistan — tj": "tj", "Tanzania, United Republic of — tz": "tz", "Thailand — th": "th", "Timor-Leste — tl": "tl",
            "Togo — tg": "tg", "Tokelau — tk": "tk", "Tonga — to": "to", "Trinidad and Tobago — tt": "tt", "Tunisia — tn": "tn", "Turkey — tr": "tr", "Turkmenistan — tm": "tm", "Turks and Caicos Islands — tc": "tc",
            "Tuvalu — tv": "tv", "Uganda — ug": "ug", "Ukraine — ua": "ua", "United Arab Emirates — ae": "ae", "United Kingdom — uk": "uk", "United Kingdom — gb": "gb", "United States — us": "us",
            "United States Minor Outlying Islands — um": "um", "Uruguay — uy": "uy", "Uzbekistan — uz": "uz", "Vanuatu — vu": "vu", "Venezuela — ve": "ve", "Viet Nam — vn": "vn", "Virgin Islands, British — vg": "vg",
            "Virgin Islands, U.S. — vi": "vi", "Wallis and Futuna — wf": "wf", "Western Sahara — eh": "eh", "Yemen — ye": "ye", "Zambia — zm": "zm", "Zimbabwe — zw": "zw"
        }

######

    def add_rule(self):
        new_rule_entry = ttk.Entry(self.scrolled_frame, width=19)
        new_rule_entry.grid(row=len(self.rule_entry_list) // 2, column=0, padx=5, pady=5)

        new_css_entry = ttk.Entry(self.scrolled_frame, width=19)
        new_css_entry.grid(row=len(self.rule_entry_list) // 2, column=1, padx=5, pady=5)

        self.rule_entry_list.append(new_rule_entry)
        self.rule_entry_list.append(new_css_entry)

#### Tab8
     
    def on_run_any_tab_clicked(self):
        link = self.entry_link_any_domain.get()
        save_as_excel = self.var_save_any_as_excel.get()
        save_as_json = self.var_save_any_as_json.get()
        proxy_type = self.any_proxy_type_var.get()
        proxy_country_type = self.any_proxy_country_type_var.get()
        use_proxy = self.var_use_proxy.get()
        rules_data = []  # List to store the extracted data
        try:
            extr_r = ""
            extract_rules = {}
            for i in range(0, len(self.rule_entry_list), 2):
                rule_text = self.rule_entry_list[i].get()
                css_selector = self.rule_entry_list[i + 1].get()
                if (rule_text !="" and css_selector !=""):
                    if (i != len(self.rule_entry_list)-2):
                        extr_r = str(extr_r)+'"'+str(rule_text)+'":"'+str(css_selector)+'",'
                    else:
                        extr_r = str(extr_r)+'"'+str(rule_text)+'":"'+str(css_selector)+'"'
                    extract_rules[rule_text] = css_selector
        except Exception as e:
            pass
        api = self.entry_serp_api.get()
        if not link:
            messagebox.showerror("Error", "Please enter a link.")
            return
        if not api.strip():
            messagebox.showerror("Error", "Scrape-It.Cloud API field cannot be empty.")
            return
        
        try:
            api_url = 'https://api.scrape-it.cloud/scrape'
            headers = {'x-api-key': api,
                        'Content-Type': 'application/json'}

            if extr_r and use_proxy:
                payload = json.dumps({
                "extract_rules": extract_rules,
                "wait": 0,
                "block_resources": False,
                "proxy_type": proxy_type,
                "proxy_country": proxy_country_type,
                "url": link
                })

            elif extr_r:
                payload = json.dumps({
                "extract_rules": extract_rules,
                "wait": 0,
                "block_resources": False,
                "url": link
                })
            elif use_proxy:
                payload = json.dumps({
                "wait": 0,
                "block_resources": False,
                "proxy_type": proxy_type,
                "proxy_country": proxy_country_type,
                "url": link
                })
            else:
                payload = json.dumps({
                "wait": 0,
                "block_resources": False,
                "url": link
                })


            response = requests.request("POST", api_url, headers=headers, data=payload)
            data = response.json()

            if save_as_json:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_name = f"output/scraped_data_{timestamp}.json"
                with open(file_name, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4)
                messagebox.showinfo("Success", f"Data has been saved to {file_name}")

            if save_as_excel:

                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_name = f"output/scraped_data_{timestamp}.xlsx"
                try:
                    if extr_r:
                        data = data['scrapingResult']['extractedData']
                    else:
                        data = data['scrapingResult']
                    df = pd.DataFrame(data)
                    df.to_excel(file_name, index=False)

                    messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                except Exception as e:
                    print(f"Failed to make API request: {e}")

        except Exception as e:
            print("Error", e)
        


#### Tab7

    def on_run_zillow_property(self):

        link_zillow = self.entry_link_zillow.get()
        api_scrape = self.entry_serp_api.get()
        if not link_zillow:
            messagebox.showerror("Error", "Please enter a link to Zillow store.")
            return
        if not api_scrape.strip():
            messagebox.showerror("Error", "Scrape-It.Cloud API field cannot be empty.")
            return
        try:
            api_url = 'https://api.scrape-it.cloud/zillow/property'
            headers = {'x-api-key': api_scrape}

            params = {
                'url': link_zillow
            }

            try:
                url = api_url + '?' + urllib.parse.urlencode(params)
                request = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(request) as response:
                    if response.status == 200:
                        # Parse the JSON response
                        data = json.loads(response.read().decode())
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        file_name = f"output/zillow_property_{timestamp}.json"
                        with open(file_name, "w", encoding="utf-8") as file:
                            json.dump(data, file, indent=4)
                        messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                        file_name = f"output/zillow_property_{timestamp}.xlsx"
                        try:
                            property_data = data.get('property', {})
                            df = pd.DataFrame([property_data])  # Create a DataFrame from the property data

                            # Define the Excel file name
                            excel_file_name = f"output/zillow_property_{timestamp}.xlsx"

                            # Save the DataFrame to Excel
                            df.to_excel(excel_file_name, index=False)

                            messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                        except Exception as e:
                            print(f"Failed to make API request: {e}")
                    if response.status == 403:
                        messagebox.showerror("Error", "You don't have enough API credits to perform this request.")
                        return
                    
                    if response.status == 401:
                        messagebox.showerror("Error", "Invalid API Key.")
                        return
                    
                    if response.status == 429:
                        messagebox.showerror("Error", "You reached concurrency limit.")
                        return
            except Exception as e:
                pass
        except Exception as e:
            pass


    def on_run_zillow_clicked(self):
        save_as_json = self.var_save_zillow_as_json.get()
        save_as_excel = self.var_save_zillow_as_excel.get()
        keyword_zillow = self.entry_keyword_zillow.get()
        type_zillow = self.property_type_var.get()
        api_scrape = self.entry_serp_api.get()
        property_home_types = self.property_home_types_var.get()

        if not keyword_zillow:
            messagebox.showerror("Error", "Please enter a keyword to search in Zillow store.")
            return
        if not api_scrape.strip():
            messagebox.showerror("Error", "Scrape-It.Cloud API field cannot be empty.")
            return
        if type_zillow == "Type":
            messagebox.showerror("Error", "Please, select Type.")
            return
        try:
            api_url = 'https://api.scrape-it.cloud/zillow/listing'
            headers = {'x-api-key': api_scrape}

            params = {
                "keyword": keyword_zillow,
                "type": type_zillow
            }

            if property_home_types != "Home Types":
                params['homeTypes'] = property_home_types

            try:

                url = api_url + '?' + urllib.parse.urlencode(params)
                print(url)
                request = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(request) as response:
                    response_content = response.read().decode('utf-8')
                    print(response_content)
                    if response.status == 200:
                        # Parse the JSON response
                        data = json.loads(response_content)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        if save_as_json:
                            file_name = f"output/zillow_property_{timestamp}.json"
                            with open(file_name, "w", encoding="utf-8") as file:
                                json.dump(data, file, indent=4)
                            messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                        if save_as_excel:
                            file_name = f"output/zillow_properties_{timestamp}.xlsx"
                            try:
                                properties_data = data['properties']
                                df = pd.DataFrame(properties_data)  # Create a DataFrame from the property data

                                # Define the Excel file name
                                excel_file_name = f"output/zillow_property_{timestamp}.xlsx"

                                # Save the DataFrame to Excel
                                df.to_excel(excel_file_name, index=False)

                                messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                            except Exception as e:
                                print(f"Failed to make API request: {e}")
                    if response.status == 403:
                        messagebox.showerror("Error", "You don't have enough API credits to perform this request.")
                        return
                    
                    if response.status == 401:
                        messagebox.showerror("Error", "Invalid API Key.")
                        return
                    
                    if response.status == 429:
                        messagebox.showerror("Error", "You reached concurrency limit.")
                        return
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
#### Tab6

    def on_run_get_prod(self):
        save_as_json = self.var_save_shopify_as_json.get()
        save_as_excel = self.var_save_shopify_as_excel.get()
        col_shopify = self.entry_col_shopify.get()
        page_shopify = self.entry_page_shopify.get()
        limit_shopify = self.entry_limit_shopify.get()
        link_shopify = self.entry_link_shopify.get()
        api_scrape = self.entry_serp_api.get()
        if not link_shopify:
            messagebox.showerror("Error", "Please enter a link to Shopify store.")
            return
        if not api_scrape.strip():
            messagebox.showerror("Error", "Scrape-It.Cloud API field cannot be empty.")
            return
        try:
            api_url = 'https://api.scrape-it.cloud/shopify/products'
            headers = {'x-api-key': api_scrape}

            params = {
                'url': link_shopify
            }
            if col_shopify:
                params['collection'] = col_shopify
            if page_shopify:
                params['page'] = page_shopify
            elif limit_shopify:
                params['limit'] = limit_shopify

            try:
                url = api_url + '?' + urllib.parse.urlencode(params)
                print(url)
                request = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(request) as response:
                    if response.status == 200:
                        # Parse the JSON response
                        data = json.loads(response.read().decode())
                        if save_as_json:
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            file_name = f"output/shopify_products_{timestamp}.json"
                            with open(file_name, "w", encoding="utf-8") as file:
                                json.dump(data, file, indent=4)
                            messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                        if save_as_excel:

                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            file_name = f"shopify_products_{timestamp}.xlsx"
                            folder_name = f"output/shopify_products_{timestamp}"
                            os.makedirs(folder_name, exist_ok=True)
                            image_path = os.path.join(folder_name, file_name)

                            try:
                                temp = data['products']
                                df = pd.DataFrame(temp)
                                df.to_excel(image_path, index=False)
                                for product in data['products']:
                                    test = product['product_type']
                                    
                                    try:
                                        file_name = f"variant_{test}_{timestamp}.xlsx"   
                                        image_path = os.path.join(folder_name, file_name)
                                        temp = product['variants']
                                        df = pd.DataFrame(temp)
                                        df.to_excel(image_path, index=False)
                                    except Exception as e:
                                        print(f"Error: {e}")

                                    try:
                                        file_name = f"images_{test}_{timestamp}.xlsx"   
                                        image_path = os.path.join(folder_name, file_name)
                                        temp = product['images']
                                        df = pd.DataFrame(temp)
                                        df.to_excel(image_path, index=False)
                                    except Exception as e:
                                        print(f"Error: {e}")


                                messagebox.showinfo("Success", f"Data has been saved in {folder_name} folder.")

                            except Exception as e:
                                print(f"Failed to make API request: {e}")
                    if response.status == 403:
                        messagebox.showerror("Error", "You don't have enough API credits to perform this request.")
                        return
                    
                    if response.status == 401:
                        messagebox.showerror("Error", "Invalid API Key.")
                        return
                    
                    if response.status == 429:
                        messagebox.showerror("Error", "You reached concurrency limit.")
                        return
            except Exception as e:
                pass
        except Exception as e:
            pass



    def on_run_get_coll(self):
        save_as_json = self.var_save_shopify_as_json.get()
        save_as_excel = self.var_save_shopify_as_excel.get()
        link_shopify = self.entry_link_shopify.get()
        api_scrape = self.entry_serp_api.get()
        if not link_shopify:
            messagebox.showerror("Error", "Please enter a link to Shopify store.")
            return
        if not api_scrape.strip():
            messagebox.showerror("Error", "Scrape-It.Cloud API field cannot be empty.")
            return
        try:
            api_url = 'https://api.scrape-it.cloud/shopify/collections'
            headers = {'x-api-key': api_scrape}

            params = {
                'url': link_shopify
            }

            try:
                url = api_url + '?' + urllib.parse.urlencode(params)
                print(url)
                request = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(request) as response:
                    if response.status == 200:
                        # Parse the JSON response
                        data = json.loads(response.read().decode())
                        if save_as_json:
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            file_name = f"output/shopify_collection_{timestamp}.json"
                            with open(file_name, "w", encoding="utf-8") as file:
                                json.dump(data, file, indent=4)
                            messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                        if save_as_excel:

                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            file_name = f"output/shopify_collection_{timestamp}.xlsx"
                            try:
                                data = data['collections']
                                df = pd.DataFrame(data)
                                df.to_excel(file_name, index=False)

                                messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                            except Exception as e:
                                print(f"Failed to make API request: {e}")
                    if response.status == 403:
                        messagebox.showerror("Error", "You don't have enough API credits to perform this request.")
                        return
                    
                    if response.status == 401:
                        messagebox.showerror("Error", "Invalid API Key.")
                        return
                    
                    if response.status == 429:
                        messagebox.showerror("Error", "You reached concurrency limit.")
                        return
            except Exception as e:
                pass
        except Exception as e:
            pass

#### Tab5

    def on_run_gen_clicked(self):
        link = self.entry_gen_domain.get()
        api_scrape = self.entry_serp_api.get()
        api_gpt = self.entry_chatgpt_api.get()
        chatgpt_prompt = self.entry_chatgpt_prompt.get()

        if not link:
            messagebox.showerror("Error", "Please enter a link to target resource.")
            return
        if not api_scrape.strip():
            messagebox.showerror("Error", "Scrape-It.Cloud API field cannot be empty.")
            return
        if not api_gpt.strip():
            messagebox.showerror("Error", "ChatGPT API field cannot be empty.")
            return
        if not chatgpt_prompt:
            messagebox.showerror("Error", "ChatGPT prompt field cannot be empty.")
            return

        try:
            api_url = 'https://api.scrape-it.cloud/scrape'
            headers = {
                'x-api-key': api_scrape,
                'Content-Type': 'application/json'
            }
            data = {
                'url': link
            }
            response = requests.post(api_url, headers=headers, json=data)

            if response.status_code == 200:
                data = json.loads(response.text)
                try:
                    results = data['scrapingResult']['content']
                    soup = BeautifulSoup(results, 'html.parser')
                    all_text = soup.get_text()
                    cleaned_text = "\n".join(line for line in all_text.splitlines() if line.strip())
                    openai.api_key = api_gpt
                    completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": str(str(chatgpt_prompt)+":\n"+str(cleaned_text))}
                    ]
                    )

                    chat_response = completion.choices[0].message.content
                    self.text_area.delete("1.0", "end")  # Очищаем текстовое поле
                    self.text_area.insert("1.0", chat_response)
                except Exception as e:
                    messagebox.showerror("Error", e)
            if response.status == 403:
                messagebox.showerror("Error", "You don't have enough API credits to perform this request.")
                return
                        
            if response.status == 401:
                messagebox.showerror("Error", "Invalid API Key.")
                return
                        
            if response.status == 429:
                messagebox.showerror("Error", "You reached concurrency limit.")
                return
    
        except requests.exceptions.RequestException as e:
            print("Error:", e)


    def on_run_text_gen_clicked(self):
        link = self.entry_gen_domain.get()
        api_scrape = self.entry_serp_api.get()
        api_gpt = self.entry_chatgpt_api.get()
        chatgpt_prompt = self.entry_chatgpt_prompt.get()

        if not link:
            messagebox.showerror("Error", "Please enter a link to target resource.")
            return
        if not api_scrape.strip():
            messagebox.showerror("Error", "Scrape-It.Cloud API field cannot be empty.")
            return
        if not api_gpt.strip():
            messagebox.showerror("Error", "ChatGPT API field cannot be empty.")
            return
        if not chatgpt_prompt:
            messagebox.showerror("Error", "ChatGPT prompt field cannot be empty.")
            return

        try:
            api_url = 'https://api.scrape-it.cloud/scrape'
            headers = {
                'x-api-key': api_scrape,
                'Content-Type': 'application/json'
            }
            data = {
                'url': link,
            }
            response = requests.post(api_url, headers=headers, json=data)

            if response.status_code == 200:
                data = json.loads(response.text)
                try:
                    results = data['scrapingResult']['content']
                    soup = BeautifulSoup(results, 'html.parser')
                    all_text = soup.get_text()
                    cleaned_text = "\n".join(line for line in all_text.splitlines() if line.strip())
                    self.text_area.delete("1.0", "end") 
                    self.text_area.insert("1.0", cleaned_text)
                except Exception as e:
                    messagebox.showerror("Error", e)
            if response.status == 403:
                messagebox.showerror("Error", "You don't have enough API credits to perform this request.")
                return
                        
            if response.status == 401:
                messagebox.showerror("Error", "Invalid API Key.")
                return
                        
            if response.status == 429:
                messagebox.showerror("Error", "You reached concurrency limit.")
                
    
        except requests.exceptions.RequestException as e:
            print("Error:", e)


#### Tab2

    def on_run_serp_clicked(self):
        country_codes = self.serp_country_codes
        language_codes = self.serp_language_codes
        domain_codes = self.serp_domain_codes

        keyword = self.entry_serp_keyword.get()
        number = self.entry_serp_number.get()
        start = self.entry_serp_start.get()
        tbm = self.tbm_serp_var.get()
        device_type = self.device_serp_type_var.get()
        language = self.language_serp_var.get()
        domain = self.domain_serp_var.get()
        country = self.country_serp_var.get()
        save_as_excel = self.var_save_as_serp_excel.get()
        save_as_json = self.var_save_as_serp_json.get()
        api = self.entry_serp_api.get()
        if not keyword:
            messagebox.showerror("Error", "Please enter a keyword.")
            return
        if not api.strip():
            messagebox.showerror("Error", "Scrape-It.Cloud API field cannot be empty.")
            return
        if not start:
            start = "1"
        if not number:
            number = "100"
        if not country or country == "No Selection":
            country_codes = "us"  
        else:
            country_codes = country_codes.get(country)
        if not domain or domain == "No Selection":
            domain_codes = "google.com" 
        else:
            domain_codes = domain_codes.get(domain)
        if not language or language == "No Selection":
            language_codes = "en"  
        else:
            language_codes = language_codes.get(language)
        #####
        try:
            api_url = 'https://api.scrape-it.cloud/scrape/google'
            headers = {'x-api-key': api}

            params = {
                'q': keyword.lower(),
                'domain': domain_codes,
                "deviceType": device_type.lower(),
                "start": start,
                "num": number,
                "gl": country_codes,
                "hl": language_codes
            }
            if tbm == 'Google Images':
                params['tbm'] = 'isch'
            elif tbm == 'Google Videos':
                params['tbm'] = 'vid'
            elif tbm == 'Google News':
                params['tbm'] = 'nws'
            elif tbm == 'Google Locals':
                params['tbm'] = 'lcl'
            elif tbm == 'Google Shopping':
                params['tbm'] = 'shop'

            if tbm == 'Google Images':
                try:
                    url = api_url + '?' + urllib.parse.urlencode(params)
                    print(url)
                    request = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(request) as response:
                        if response.status == 200:
                            # Parse the JSON response
                            data = json.loads(response.read().decode())

                            # Create a folder with the keyword name
                            folder_name = "output/"+str(re.sub(r'[^\w\-]+', '_', keyword))
                            os.makedirs(folder_name, exist_ok=True)

                            # Save the images to the folder
                            images_results = data['imagesResults']
                            messagebox.showinfo("Proccessing", f"Press 'ok' to start downloading images. Please, wait a few minutes, while images are dowmloding.")
                            for image in images_results:
                                print(image['title'], ": ", image['original'])
                                try:
                                    image_title = re.sub(r'[^\w\-]+', '_', image['title'])
                                    image_url = image['original']
                                    image_extension = image_url.split('.')[-1]
                                    image_file_name = f"{image_title}.{image_extension}"
                                    image_path = os.path.join(folder_name, image_file_name)

                                    with urllib.request.urlopen(image_url) as image_response:
                                        if image_response.status == 200:
                                            with open(image_path, "wb") as file:
                                                file.write(image_response.read())
                                        else:
                                            print(f"Failed to download the image '{image_title}'. Status code:", image_response.status_code)
                                except Exception as e:
                                    print("Failed to download the image:", e)
                            messagebox.showinfo("Success", f"Images was downloaded successfully.")
                            if self.var_save_as_serp_json.get():
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                file_name = f"images_{keyword}_{timestamp}.json"
                                with open(file_name, "w", encoding="utf-8") as file:
                                    json.dump(data, file, indent=4)
                                messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                            if self.var_save_as_serp_excel.get():
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                file_name = f"images_{keyword}_{timestamp}.xlsx"
                                try:
                                    images_data = data['imagesResults']
                                    df = pd.DataFrame(images_data)
                                    df.to_excel(file_name, index=False)

                                    messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                                except Exception as e:
                                    print(f"Failed to make API request: {e}")
                        if response.status == 403:
                            messagebox.showerror("Error", "You don't have enough API credits to perform this request.")
                            return
                                    
                        if response.status == 401:
                            messagebox.showerror("Error", "Invalid API Key.")
                            return
                                    
                        if response.status == 429:
                            messagebox.showerror("Error", "You reached concurrency limit.")
                            
                                
                        else:
                            print("Failed to get the API response. Status code:", response.status)
                except Exception as e:
                    messagebox.showerror("Error", str("Failed to make the API request:", e))

            elif tbm == 'Google SERP':
                try:
                    url = api_url + '?' + urllib.parse.urlencode(params)
                    print(url)
                    request = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(request) as response:
                        if response.status == 200:
                            # Parse the JSON response
                            data = json.loads(response.read().decode())

                            if self.var_save_as_serp_json.get():
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                file_name = f"output/serp_{keyword}_{timestamp}.json"
                                with open(file_name, "w", encoding="utf-8") as file:
                                    json.dump(data, file, indent=4)
                                messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                            if self.var_save_as_serp_excel.get():
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                file_name = f"output/serp_{keyword}_{timestamp}.xlsx"
                                try:
                                    serp_data = data['organicResults']
                                    df = pd.DataFrame(serp_data)
                                    df.to_excel(file_name, index=False)

                                    messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                                except Exception as e:
                                    print(f"Failed to make API request: {e}")
                        if response.status == 403:
                            messagebox.showerror("Error", "You don't have enough API credits to perform this request.")
                            return
                                    
                        if response.status == 401:
                            messagebox.showerror("Error", "Invalid API Key.")
                            return
                                    
                        if response.status == 429:
                            messagebox.showerror("Error", "You reached concurrency limit.")
                            
                                
                        else:
                            print("Failed to get the API response. Status code:", response.status)
                except Exception as e:
                    messagebox.showerror("Error", str("Failed to make the API request:", e))
            elif tbm == 'Google Videos':
                try:
                    url = api_url + '?' + urllib.parse.urlencode(params)
                    print(url)
                    request = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(request) as response:
                        if response.status == 200:
                            # Parse the JSON response
                            data = json.loads(response.read().decode())

                            if self.var_save_as_serp_json.get():
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                file_name = f"output/videos_{keyword}_{timestamp}.json"
                                with open(file_name, "w", encoding="utf-8") as file:
                                    json.dump(data, file, indent=4)
                                messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                            if self.var_save_as_serp_excel.get():
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                file_name = f"output/videos_{keyword}_{timestamp}.xlsx"
                                try:
                                    videos_data = data['organicResults']
                                    df = pd.DataFrame(videos_data)
                                    df.to_excel(file_name, index=False)

                                    messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                                except Exception as e:
                                    print(f"Failed to make API request: {e}")
                        if response.status == 403:
                            messagebox.showerror("Error", "You don't have enough API credits to perform this request.")
                            return
                                    
                        if response.status == 401:
                            messagebox.showerror("Error", "Invalid API Key.")
                            return
                                    
                        if response.status == 429:
                            messagebox.showerror("Error", "You reached concurrency limit.")
                            
                                
                        else:
                            print("Failed to get the API response. Status code:", response.status)
                except Exception as e:
                    messagebox.showerror("Error", str("Failed to make the API request:", e))
            elif tbm == 'Google News':
                try:
                    url = api_url + '?' + urllib.parse.urlencode(params)
                    print(url)
                    request = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(request) as response:
                        if response.status == 200:
                            # Parse the JSON response
                            data = json.loads(response.read().decode())

                            if self.var_save_as_serp_json.get():
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                file_name = f"output/news_{keyword}_{timestamp}.json"
                                with open(file_name, "w", encoding="utf-8") as file:
                                    json.dump(data, file, indent=4)
                                messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                            if self.var_save_as_serp_excel.get():
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                file_name = f"output/news_{keyword}_{timestamp}.xlsx"
                                try:
                                    news_data = data['newsResults']
                                    df = pd.DataFrame(news_data)
                                    df.to_excel(file_name, index=False)

                                    messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                                except Exception as e:
                                    print(f"Failed to make API request: {e}")
                        if response.status == 403:
                            messagebox.showerror("Error", "You don't have enough API credits to perform this request.")
                            return
                                    
                        if response.status == 401:
                            messagebox.showerror("Error", "Invalid API Key.")
                            return
                                    
                        if response.status == 429:
                            messagebox.showerror("Error", "You reached concurrency limit.")
                            
                                
                        else:
                            print("Failed to get the API response. Status code:", response.status)
                except Exception as e:
                    messagebox.showerror("Error", str("Failed to make the API request:", e))
            elif tbm == 'Google Locals':
                try:
                    url = api_url + '?' + urllib.parse.urlencode(params)
                    print(url)
                    request = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(request) as response:
                        if response.status == 200:
                            # Parse the JSON response
                            data = json.loads(response.read().decode())

                            if self.var_save_as_serp_json.get():
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                file_name = f"output/locals_{keyword}_{timestamp}.json"
                                with open(file_name, "w", encoding="utf-8") as file:
                                    json.dump(data, file, indent=4)
                                messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                            if self.var_save_as_serp_excel.get():
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                file_name = f"output/locals_{keyword}_{timestamp}.xlsx"
                                try:
                                    locals_data = data['localResults']
                                    df = pd.DataFrame(locals_data)
                                    df.to_excel(file_name, index=False)

                                    messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                                except Exception as e:
                                    print(f"Failed to make API request: {e}")
                        if response.status == 403:
                            messagebox.showerror("Error", "You don't have enough API credits to perform this request.")
                            return
                                    
                        if response.status == 401:
                            messagebox.showerror("Error", "Invalid API Key.")
                            return
                                    
                        if response.status == 429:
                            messagebox.showerror("Error", "You reached concurrency limit.")
                            
                                
                        else:
                            print("Failed to get the API response. Status code:", response.status)
                except Exception as e:
                    messagebox.showerror("Error", str("Failed to make the API request:", e))

            elif tbm == 'Google Shopping':
                try:
                    url = api_url + '?' + urllib.parse.urlencode(params)
                    print(url)
                    request = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(request) as response:
                        if response.status == 200:
                            # Parse the JSON response
                            data = json.loads(response.read().decode())

                            if self.var_save_as_serp_json.get():
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                file_name = f"output/shopping_{keyword}_{timestamp}.json"
                                with open(file_name, "w", encoding="utf-8") as file:
                                    json.dump(data, file, indent=4)
                                messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                            if self.var_save_as_serp_excel.get():
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                file_name = f"output/shopping_{keyword}_{timestamp}.xlsx"
                                try:
                                    shopping_data = data['shoppingResults']
                                    df = pd.DataFrame(shopping_data)
                                    df.to_excel(file_name, index=False)

                                    messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                                except Exception as e:
                                    print(f"Failed to make API request: {e}")
                        if response.status == 403:
                            messagebox.showerror("Error", "You don't have enough API credits to perform this request.")
                            return
                                    
                        if response.status == 401:
                            messagebox.showerror("Error", "Invalid API Key.")
                            return
                                    
                        if response.status == 429:
                            messagebox.showerror("Error", "You reached concurrency limit.")
                            
                                
                        else:
                            print("Failed to get the API response. Status code:", response.status)
                except Exception as e:
                    messagebox.showerror("Error", str("Failed to make the API request:", e))


        except Exception as e:
            print("Error", e)


    def on_run_maps_clicked(self):
        # Получаем значения полей
        country_codes = {
            "": "US",
            "USA": "US",
            "United Kingdom": "UK",
            "Germany": "DE",
            "Ireland": "IE",
            "France": "FR",
            "Italy": "IT",
            "Sweden": "SE",
            "Brazil": "BR",
            "Canada": "CA",
            "Japan": "JP",
            "Singapore": "SG",
            "India": "IN",
            "Indonesia": "ID"
        }
        keyword = self.entry_keyword.get()
        domain = self.entry_domain.get()
        start = self.entry_start.get()
        ll = self.entry_ll.get()
        country = self.country_var.get()
        api = self.entry_serp_api.get()
        if not keyword:
            messagebox.showerror("Error", "Please enter a keyword.")
            return
        if not api.strip():
            messagebox.showerror("Error", "Scrape-It.Cloud API field cannot be empty.")
            return
        if not domain:
            domain = "com"
        if not start:
            start = "0"
        if not ll:
            ll = "@40.7455096,-74.0083012,14z"
        if not country or country == "Select Country":
            country_code = "US" 
        else:
            country_code = country_codes.get(country)
        
        ###
        try:
            url = "https://api.scrape-it.cloud/scrape/google/locals"
            headers = {
                'x-api-key': api,
                'Content-Type': 'application/json'
            }
            payload = {
                "country": country_code,
                "domain": domain,
                "keyword": keyword,
                "start": start,
                "ll": ll
            }
            response = requests.post(url, headers=headers, data=json.dumps(payload))

            if response.status_code == 200:
                data = response.json()
               
                if self.var_save_as_json.get():
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    file_name = f"{keyword}_{timestamp}.json"
                    with open(file_name, "w", encoding="utf-8") as file:
                        json.dump(data, file, indent=4)
                    messagebox.showinfo("Success", f"Data has been saved to {file_name}")

                if self.var_save_as_excel.get():
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    file_name = f"output/{keyword}_{timestamp}.xlsx"
                    try:
                        if 'locals' in data.get('scrapingResult', {}):
                            locals_data = data['scrapingResult']['locals']

                            # Create a DataFrame from the 'locals' data
                            df = pd.DataFrame(locals_data)

                            # Save the DataFrame to the Excel file
                            df.to_excel(file_name, index=False)



                    except Exception as e:
                        print(f"Failed to make API request: {e}")
                    messagebox.showinfo("Success", f"Data has been saved to {file_name}")
            if response.status == 403:
                messagebox.showerror("Error", "You don't have enough API credits to perform this request.")
                return
                        
            if response.status == 401:
                messagebox.showerror("Error", "Invalid API Key.")
                return
                        
            if response.status == 429:
                messagebox.showerror("Error", "You reached concurrency limit.")
                          

            else:
                messagebox.showerror("Error", f"Failed to make API request: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to make API request: {e}")

    def on_save_clicked(self):
        serp_api = self.entry_serp_api.get()
        chatgpt_api = self.entry_chatgpt_api.get()

        if not serp_api.strip():
            messagebox.showerror("Error", "Scrape-It.Cloud API field cannot be empty.")
            return

        try:
            connection = sqlite3.connect("user_data.db")  
            cursor = connection.cursor()
            cursor.execute("INSERT INTO user (scrapeitapi, gptapi) VALUES (?, ?)", (serp_api, chatgpt_api))
            connection.commit()
            connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")  

    def on_upload_clicked(self):
        try:
            connection = sqlite3.connect("user_data.db")  
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            connection.close()

            if row:
                serp_api, chatgpt_api = row[1], row[2]
                self.entry_serp_api.delete(0, tk.END)
                self.entry_serp_api.insert(0, serp_api)
                self.entry_chatgpt_api.delete(0, tk.END)
                self.entry_chatgpt_api.insert(0, chatgpt_api)
            else:
                messagebox.showinfo("Upload Failed", "No data found in the database.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def on_delete_clicked(self):
        serp_api = self.entry_serp_api.get()
        chatgpt_api = self.entry_chatgpt_api.get()

        try:
            connection = sqlite3.connect("user_data.db")  
            cursor = connection.cursor()
            cursor.execute("DELETE FROM user WHERE scrapeitapi=? AND gptapi=?", (serp_api, chatgpt_api))
            connection.commit()

            if cursor.rowcount > 0:
                self.entry_serp_api.delete(0, tk.END)
                self.entry_chatgpt_api.delete(0, tk.END)
                messagebox.showinfo("Delete Success", "Data has been deleted from the database.")
            else:
                messagebox.showinfo("Delete Failed", "No matching data found in the database.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete data: {e}")

    def create_theme_slider(self):
        self.theme_slider = ttk.Checkbutton(self, onvalue=1, offvalue=0, command=self.on_theme_slider_change, style='Roundtoggle.Toolbutton')
        self.theme_slider.pack(side=tk.TOP, padx=10, pady=10)

    def on_theme_slider_change(self):
        if self.theme_slider.instate(['selected']):
            self.set_dark_theme()
        else:
            self.set_light_theme()

    def set_light_theme(self):
        style = Style(theme='flatly')
        style.configure('.', font=('Helvetica', 10))

    def set_dark_theme(self):
        style = Style(theme='darkly')
        style.configure('.', font=('Helvetica', 10))

if __name__ == "__main__":
    app = App()
    app.mainloop()
