# -*- coding: utf-8 -*-
# ============================================================
#   BIOMESH — DIAGNOSTIC & RESOLUTION SYSTEME WINDOWS
#   RELEASE — by Brisk
# ============================================================

import os, sys, subprocess, platform, socket, datetime, time
import ctypes, traceback, re

try:
    import winreg
    import wmi
    import psutil
except ImportError:
    pass

LOG_FILE    = "logs.txt"
HTML_REPORT = "rapport.html"
SEP         = "═" * 68
VERSION     = "RELEASE"
CREATOR     = "Brisk"
LOGO_URL    = "https://media.discordapp.net/attachments/1484121953450332202/1485332602729529506/ChatGPT_Image_22_mars_2026_18_41_21.png?ex=69c37588&is=69c22408&hm=ade2fc21f3fc1ed7910ea234d145d725a72d0f365bafbe27c7c263ce&=&format=webp&quality=lossless"

# ── ANSI ──────────────────────────────────────────────────────────────────────
C = {"reset":"\033[0m","bold":"\033[1m","dim":"\033[2m","red":"\033[91m",
     "green":"\033[92m","yellow":"\033[93m","blue":"\033[94m","cyan":"\033[96m",
     "white":"\033[97m","teal":"\033[38;5;51m","sky":"\033[38;5;75m",
     "lb":"\033[38;5;39m","lb2":"\033[38;5;45m","lb3":"\033[38;5;33m"}
def c(t,k): return f"{C.get(k,'')}{t}{C['reset']}"
def cls(): os.system("cls" if sys.platform=="win32" else "clear")

GRAD = ["\033[38;5;27m","\033[38;5;33m","\033[38;5;39m","\033[38;5;45m","\033[38;5;51m","\033[38;5;45m"]

def banner(sub="DIAGNOSTIC & RESOLUTION SYSTEME WINDOWS"):
    cls()
    lines = [
        " ██████╗ ██╗ ██████╗ ███╗   ███╗███████╗███████╗██╗  ██╗",
        " ██╔══██╗██║██╔═══██╗████╗ ████║██╔════╝██╔════╝██║  ██║",
        " ██████╔╝██║██║   ██║██╔████╔██║█████╗  ███████╗███████║",
        " ██╔══██╗██║██║   ██║██║╚██╔╝██║██╔══╝  ╚════██║██╔══██║",
        " ██████╔╝██║╚██████╔╝██║ ╚═╝ ██║███████╗███████║██║  ██║",
        " ╚═════╝ ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝",
    ]
    print()
    for i,l in enumerate(lines): print(f"  {GRAD[i]}{l}{C['reset']}")
    print()
    W=60; pad=sub.center(W)
    print(c(f"  ╔{'═'*W}╗","lb")); print(c(f"  ║{pad}║","lb"))
    print(c(f"  ║{'by '+CREATOR+'  ·  '+VERSION:>{W}}║","dim")); print(c(f"  ╚{'═'*W}╝","lb")); print()

# ── LOG ───────────────────────────────────────────────────────────────────────
log_lines   = []
resolve_log = []

def log(text, level="INFO", print_also=True):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    log_lines.append(f"[{ts}] [{level}] {text}")
    if not print_also: return
    icons={"OK":"✔","WARN":"⚠","ERR":"✘","INFO":"ℹ","HEAD":"►","SUB":"─","FIX":"⚙"}
    icon=icons.get(level," ")
    if   level=="OK":   print(c(f"  {icon}  {text}","green"))
    elif level=="WARN": print(c(f"  {icon}  {text}","yellow"))
    elif level=="ERR":  print(c(f"  {icon}  {text}","red"))
    elif level=="INFO": print(c(f"  {icon}  {text}","white"))
    elif level=="HEAD":
        print(); print(c(f"  {SEP}","lb")); print(c(f"  {icon}  {text}","lb")); print(c(f"  {SEP}","lb"))
    elif level=="SUB":  print(c(f"     {icon} {text}","sky"))
    elif level=="FIX":  print(c(f"  {icon}  {text}","teal"))
    else: print(f"     {text}")

def progress(label):
    print(c(f"\n  ⏳ {label}...","yellow"), end=" ", flush=True)
def done_progress(): print(c("OK ✔","green"))
def section(t): log(t,"HEAD"); time.sleep(0.03)

def run_cmd(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           shell=True, encoding="utf-8", errors="replace")
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except subprocess.TimeoutExpired: return "","TIMEOUT",-1
    except Exception as e: return "",str(e),-1

# ══════════════════════════════════════════════════════════════════════════════
# DIAGNOSTIC MODULES
# ══════════════════════════════════════════════════════════════════════════════

def check_system_info():
    section("INFORMATIONS SYSTEME")
    try:
        log(f"Machine   : {platform.node()}","SUB")
        log(f"OS        : {platform.system()} {platform.release()} ({platform.version()})","SUB")
        log(f"Archi     : {platform.machine()} / {platform.processor()}","SUB")
        try:
            k=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            ed=winreg.QueryValueEx(k,"ProductName")[0]; bd=winreg.QueryValueEx(k,"CurrentBuildNumber")[0]
            ubr=winreg.QueryValueEx(k,"UBR")[0]; winreg.CloseKey(k)
            log(f"Edition   : {ed} — Build {bd}.{ubr}","SUB")
        except: log("Edition Windows : registre inaccessible","WARN")
        try:
            up=time.time()-psutil.boot_time(); h=int(up//3600); m=int((up%3600)//60)
            log(f"Uptime    : {h}h {m}min","SUB")
            if h<1: log("Redémarrage récent (<1h) — crash possible","WARN")
            else: log("Uptime normal","OK")
        except: log("Uptime indisponible","WARN")
        log(f"Fuseau    : {datetime.datetime.now().astimezone().tzname()}","SUB")
        log("Informations système OK","OK")
    except Exception as e: log(f"Erreur info système : {e}","ERR")

def check_system_stability():
    section("INDICE DE STABILITE WINDOWS")
    progress("Calcul fiabilité")
    out,_,_=run_cmd('powershell "Get-CimInstance Win32_ReliabilityStabilityMetrics | Sort-Object TimeGenerated -Descending | Select-Object -First 1 SystemStabilityIndex | Format-Table -HideTableHeaders"',timeout=20)
    done_progress()
    if out:
        try:
            s=float(out.strip().replace(",","."))
            if s>=8.0: log(f"Stabilité excellente : {s}/10","OK")
            elif s>=5.0: log(f"Stabilité moyenne : {s}/10","WARN")
            else: log(f"Stabilité CRITIQUE : {s}/10","ERR")
        except: log("Score non lisible","WARN")
    else: log("Indice de stabilité non disponible","WARN")

def check_cpu():
    section("PROCESSEUR (CPU)")
    try:
        log(f"Modèle    : {platform.processor()}","SUB")
        log(f"Coeurs    : {psutil.cpu_count(logical=False)} physiques / {psutil.cpu_count(logical=True)} logiques","SUB")
        freq=psutil.cpu_freq()
        if freq: log(f"Fréquence : {freq.current:.0f} MHz (max {freq.max:.0f} MHz)","SUB")
        progress("Mesure charge CPU (3s)")
        cores=psutil.cpu_percent(interval=3,percpu=True); total=psutil.cpu_percent(interval=0)
        done_progress()
        log(f"Charge totale : {total:.1f}%","SUB")
        for i,u in enumerate(cores): log(f"  Core {i+1} : {u:.1f}%","SUB")
        if total>90: log(f"CPU saturé ({total:.1f}%) — processus suspects","ERR")
        elif total>70: log(f"CPU chargé ({total:.1f}%)","WARN")
        else: log(f"Charge CPU normale ({total:.1f}%)","OK")
        try:
            w=wmi.WMI(namespace="root\\OpenHardwareMonitor")
            for s in w.Sensor():
                if s.SensorType=="Temperature" and "CPU" in s.Name:
                    t=float(s.Value)
                    if t>90: log(f"TEMP CRITIQUE {s.Name}: {t:.1f}°C","ERR")
                    elif t>75: log(f"Temp élevée {s.Name}: {t:.1f}°C","WARN")
                    else: log(f"Temp OK {s.Name}: {t:.1f}°C","OK")
        except: log("Températures CPU : OpenHardwareMonitor non disponible","WARN")
    except Exception as e: log(f"Erreur CPU : {e}","ERR")

def check_ram():
    section("MEMOIRE RAM")
    try:
        ram=psutil.virtual_memory(); swap=psutil.swap_memory()
        log(f"RAM totale    : {ram.total/(1024**3):.2f} Go","SUB")
        log(f"RAM utilisée  : {ram.used/(1024**3):.2f} Go ({ram.percent:.1f}%)","SUB")
        log(f"RAM dispo     : {ram.available/(1024**3):.2f} Go","SUB")
        log(f"Swap          : {swap.total/(1024**3):.2f} Go | {swap.used/(1024**3):.2f} Go utilisé","SUB")
        if ram.percent>90: log(f"RAM critique ({ram.percent:.1f}%) — risque freeze","ERR")
        elif ram.percent>75: log(f"RAM élevée ({ram.percent:.1f}%)","WARN")
        else: log(f"RAM correcte ({ram.percent:.1f}%)","OK")
        if ram.total/(1024**3)<4: log("RAM insuffisante (<4 Go)","WARN")
        elif ram.total/(1024**3)>=8: log("Capacité RAM suffisante","OK")
        procs=sorted([(p.info['name'],p.info['memory_info'].rss) for p in psutil.process_iter(['name','memory_info']) if p.info.get('memory_info')],key=lambda x:x[1],reverse=True)
        log("Top 5 RAM :","SUB")
        for nm,mem in procs[:5]: log(f"  {nm:<35} {mem/(1024**2):.1f} Mo","SUB")
    except Exception as e: log(f"Erreur RAM : {e}","ERR")

def check_disks():
    section("DISQUES & STOCKAGE")
    try:
        for part in psutil.disk_partitions():
            try:
                u=psutil.disk_usage(part.mountpoint)
                log(f"Disque {part.device} ({part.fstype}) — {u.total/(1024**3):.1f} Go | {u.free/(1024**3):.1f} Go libres ({u.percent:.1f}%)","SUB")
                if u.free/(1024**3)<5: log(f"ESPACE CRITIQUE sur {part.device} (<5 Go libres)","ERR")
                elif u.percent>85: log(f"Disque presque plein ({u.percent:.1f}%)","WARN")
                else: log(f"Espace disque OK","OK")
            except PermissionError: log(f"{part.device} : accès refusé","WARN")
        progress("Mesure I/O disque")
        io1=psutil.disk_io_counters(); time.sleep(2); io2=psutil.disk_io_counters()
        done_progress()
        if io1 and io2:
            log(f"Lecture : {(io2.read_bytes-io1.read_bytes)/(1024**2)/2:.2f} Mo/s | Écriture : {(io2.write_bytes-io1.write_bytes)/(1024**2)/2:.2f} Mo/s","SUB")
        progress("Lecture SMART")
        out,_,_=run_cmd("wmic diskdrive get Model,Status,Size /format:list")
        done_progress()
        if out:
            for entry in out.strip().split("\n\n"):
                if "Model=" in entry:
                    d={l.split("=")[0].strip():l.split("=")[1].strip() for l in entry.strip().split("\n") if "=" in l}
                    model=d.get("Model","?"); status=d.get("Status","?")
                    try: sg=int(d.get("Size","0"))/(1024**3)
                    except: sg=0
                    log(f"Modèle : {model} | {sg:.0f} Go | SMART : {status}","SUB")
                    if status.lower() not in ["ok",""]: log(f"SMART anormal : {model} ({status})","ERR")
                    else: log(f"SMART OK — {model}","OK")
    except Exception as e: log(f"Erreur disques : {e}","ERR")

def check_filesystem_integrity():
    section("INTEGRITE SYSTEME DE FICHIERS (C:)")
    progress("Vérification Dirty Bit")
    out,_,_=run_cmd("fsutil dirty query C:",timeout=15)
    done_progress()
    if "n'est pas" in out.lower() or "is not dirty" in out.lower(): log("Volume C: INTACT","OK")
    elif out and ("est" in out.lower() or "is dirty" in out.lower()): log("ERREUR CRITIQUE : Volume C: corrompu (Dirty Bit activé)","ERR")
    else: log("Vérification impossible (droits insuffisants)","WARN")

def check_network():
    section("RESEAU & CONNECTIVITE")
    try:
        log(f"Hostname  : {socket.gethostname()}","SUB")
        log(f"IP locale : {socket.gethostbyname(socket.gethostname())}","SUB")
        for iface,addrs in psutil.net_if_addrs().items():
            st=psutil.net_if_stats().get(iface)
            for addr in addrs:
                if addr.family==socket.AF_INET:
                    log(f"Interface {iface:<18} {addr.address:<18} {'UP' if (st and st.isup) else 'DOWN'}","SUB")
        for label,host in {"Google DNS":"8.8.8.8","Cloudflare":"1.1.1.1","Google":"google.com","WinUpdate":"windowsupdate.microsoft.com"}.items():
            out,_,rc=run_cmd(f"ping -n 3 -w 1000 {host}",timeout=15)
            if rc==0 and "TTL=" in out:
                m=re.search(r"Moyenne = (\d+)ms|Average = (\d+)ms",out)
                log(f"Ping {label} : {(m.group(1) or m.group(2)) if m else '?'} ms","OK")
            else: log(f"Ping {label} : ECHEC","ERR")
        progress("Mesure débit (2s)")
        n1=psutil.net_io_counters(); time.sleep(2); n2=psutil.net_io_counters()
        done_progress()
        log(f"Débit : ↑{(n2.bytes_sent-n1.bytes_sent)/(1024**2)/2:.3f} Mo/s  ↓{(n2.bytes_recv-n1.bytes_recv)/(1024**2)/2:.3f} Mo/s","SUB")
        try:
            import urllib.request
            with urllib.request.urlopen("https://api.ipify.org",timeout=5) as r: log(f"IP publique : {r.read().decode()}","SUB")
        except: log("IP publique : indisponible","WARN")
    except Exception as e: log(f"Erreur réseau : {e}","ERR")

def check_power():
    section("ALIMENTATION & ENERGIE")
    try:
        out,_,_=run_cmd("powercfg /getactivescheme")
        if out:
            log(f"Plan actif : {out}","SUB")
            if any(x in out.lower() for x in ["économie","power saver","economy"]):
                log("Plan Économie d'énergie actif — peut provoquer des extinctions","WARN")
            else: log("Plan d'alimentation OK","OK")
        bat=psutil.sensors_battery()
        if bat:
            log(f"Batterie : {bat.percent:.1f}% | Branché : {bat.power_plugged}","SUB")
            if not bat.power_plugged and bat.percent<20: log("Batterie faible non branchée — risque extinction","ERR")
            elif bat.power_plugged: log("Alimentation secteur OK","OK")
        else: log("Pas de batterie (desktop)","SUB")
        progress("Historique extinctions")
        out4,_,_=run_cmd('wevtutil qe System /q:"*[System[(EventID=41 or EventID=1074 or EventID=6008 or EventID=6006)]]" /c:20 /rd:true /f:text',timeout=30)
        done_progress()
        if out4:
            events=out4.strip().split("\n\n")
            for ev in events:
                if "41" in ev and "Kernel" in ev: log("EXTINCTION CRITIQUE (Event 41 - Kernel Power) !","ERR")
                elif "6008" in ev: log("ARRÊT INATTENDU (Event 6008) !","ERR")
                elif "1074" in ev: log("Arrêt planifié (Event 1074)","SUB")
                elif "6006" in ev: log("Arrêt propre (Event 6006)","OK")
            if not any("41" in e or "6008" in e for e in events): log("Aucun crash d'alimentation récent","OK")
    except Exception as e: log(f"Erreur alimentation : {e}","ERR")

def check_gpu():
    section("CARTE GRAPHIQUE (GPU)")
    try:
        out,_,_=run_cmd("wmic path win32_VideoController get Name,DriverVersion,Status,AdapterRAM /format:list")
        if out:
            for entry in out.strip().split("\n\n"):
                if "Name=" in entry:
                    d={l.split("=")[0].strip():l.split("=")[1].strip() for l in entry.strip().split("\n") if "=" in l and len(l.split("="))>=2}
                    name=d.get("Name","?"); driver=d.get("DriverVersion","?"); status=d.get("Status","?")
                    try: vram=int(d.get("AdapterRAM","0"))/(1024**2)
                    except: vram=0
                    log(f"GPU : {name} | Driver {driver} | {vram:.0f} Mo VRAM | {status}","SUB")
                    if status.lower() not in ["ok",""]: log(f"PROBLÈME GPU : {status}","ERR")
                    else: log("GPU statut OK","OK")
        else: log("GPU : infos indisponibles","WARN")
    except Exception as e: log(f"Erreur GPU : {e}","ERR")

def check_processes():
    section("PROCESSUS & SERVICES")
    try:
        all_p=list(psutil.process_iter(['pid','name','cpu_percent','memory_info']))
        time.sleep(1)
        for p in all_p:
            try: p.cpu_percent(interval=None)
            except: pass
        time.sleep(1)
        top=sorted(all_p,key=lambda p:p.info.get('cpu_percent') or 0,reverse=True)[:10]
        log("Top 10 CPU :","SUB")
        for p in top:
            try:
                cpu=p.cpu_percent(interval=None)
                mem=(p.info['memory_info'].rss if p.info.get('memory_info') else 0)/(1024**2)
                log(f"  PID {p.pid:<6} {p.info['name']:<35} CPU:{cpu:5.1f}%  RAM:{mem:.0f} Mo","SUB")
            except: pass
        svcs={"wuauserv":"Windows Update","WinDefend":"Defender","EventLog":"Journaux",
              "Dnscache":"DNS Cache","BITS":"BITS","CryptSvc":"Cryptographic","W32Time":"Horloge"}
        log("Services critiques :","SUB")
        for svc,label in svcs.items():
            out,_,_=run_cmd(f"sc query {svc}")
            if "RUNNING" in out: log(f"  {label:<25} EN COURS ✔","OK")
            elif "STOPPED" in out: log(f"  {label:<25} ARRÊTÉ !","WARN")
            else: log(f"  {label:<25} INCONNU","WARN")
    except Exception as e: log(f"Erreur processus : {e}","ERR")

def check_browsers():
    section("NAVIGATEURS WEB")
    try:
        browsers={"Chrome":r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe",
                  "Firefox":r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe",
                  "Edge":r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe",
                  "Opera":r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\opera.exe",
                  "Brave":r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\brave.exe"}
        inst=[]
        for name,rp in browsers.items():
            try: key=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,rp); log(f"Détecté : {name}","SUB"); inst.append(name); winreg.CloseKey(key)
            except: pass
        log(f"{len(inst)} navigateur(s) installé(s)","OK" if inst else "WARN")
        for bp in ["chrome.exe","firefox.exe","msedge.exe","opera.exe","brave.exe"]:
            procs=[p for p in psutil.process_iter(['name','memory_info']) if p.info.get('name') and bp in p.info['name'].lower()]
            if procs:
                total=sum(p.info['memory_info'].rss for p in procs if p.info.get('memory_info'))
                log(f"{bp} : {len(procs)} processus | RAM : {total/(1024**2):.0f} Mo","WARN" if total/(1024**2)>1500 else "SUB")
        chrome_ext=os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions")
        if os.path.exists(chrome_ext):
            exts=[d for d in os.listdir(chrome_ext) if os.path.isdir(os.path.join(chrome_ext,d))]
            log(f"Extensions Chrome : {len(exts)}","WARN" if len(exts)>15 else "SUB")
    except Exception as e: log(f"Erreur navigateurs : {e}","ERR")

def check_updates():
    section("WINDOWS UPDATE & SECURITE")
    try:
        out,_,_=run_cmd('wmic qfe get HotFixID,InstalledOn /format:list | sort',timeout=30)
        if out:
            lines=[l for l in out.split("\n") if "InstalledOn=" in l]
            if lines: log(f"Dernière MAJ : {lines[-1].replace('InstalledOn=','').strip()}","SUB")
            log(f"Correctifs : {len([l for l in out.split(chr(10)) if 'HotFixID=KB' in l])}","SUB")
        out2,_,_=run_cmd("powershell Get-MpComputerStatus | Select-Object AntivirusEnabled,RealTimeProtectionEnabled,AntivirusSignatureLastUpdated | Format-List",timeout=20)
        if out2:
            for l in out2.strip().split("\n"):
                if l.strip(): log(f"Defender : {l.strip()}","OK" if "True" in l else "WARN")
        out3,_,_=run_cmd("netsh advfirewall show allprofiles state")
        if out3:
            if "ON" in out3.upper(): log("Pare-feu Windows : ACTIF","OK")
            else: log("Pare-feu Windows : INACTIF","WARN")
        try:
            key=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")
            uac=winreg.QueryValueEx(key,"EnableLUA")[0]
            log(f"UAC : {'ACTIVÉ' if uac else 'DÉSACTIVÉ'}","OK" if uac else "WARN")
        except: log("UAC : indisponible","WARN")
    except Exception as e: log(f"Erreur MAJ/Sécurité : {e}","ERR")

def check_system_files():
    section("INTEGRITE FICHIERS SYSTEME (SFC & DISM)")
    log("SFC /scannow — peut durer 5-15 min...","INFO")
    progress("SFC /scannow")
    out,_,_=run_cmd("sfc /scannow",timeout=900)
    done_progress()
    if out:
        if any(x in out.lower() for x in ["aucune violation","no integrity violations","did not find"]): log("SFC : Aucun fichier corrompu","OK")
        elif any(x in out.lower() for x in ["réparé","repaired"]): log("SFC : Fichiers corrompus réparés !","WARN")
        elif any(x in out.lower() for x in ["impossible","unable to fix"]): log("SFC : Fichiers corrompus NON réparables — DISM requis","ERR")
        else: log(f"SFC : {out[:200]}","SUB")
    else: log("SFC : droits admin requis","WARN")
    progress("DISM CheckHealth")
    out2,_,_=run_cmd("dism /online /cleanup-image /checkhealth",timeout=120)
    done_progress()
    if out2:
        if any(x in out2.lower() for x in ["aucune altération","no component store corruption"]): log("DISM : Image intègre","OK")
        elif any(x in out2.lower() for x in ["altéré","corruption"]): log("DISM : Image altérée — RestoreHealth requis","ERR")
        else: log(f"DISM : {out2[:200]}","SUB")

def check_event_logs():
    section("JOURNAUX D'EVENEMENTS")
    try:
        for label,cmd in [
            ("Erreurs Application",'wevtutil qe Application /q:"*[System[Level=1 or Level=2]]" /c:15 /rd:true /f:text'),
            ("Erreurs Système",'wevtutil qe System /q:"*[System[Level=1 or Level=2]]" /c:15 /rd:true /f:text'),
            ("Erreurs pilotes",'wevtutil qe System /q:"*[System[(EventID=7000 or EventID=7001 or EventID=7026 or EventID=51 or EventID=11)]]" /c:10 /rd:true /f:text'),
        ]:
            progress(f"Lecture {label}")
            out,_,_=run_cmd(cmd,timeout=30)
            done_progress()
            if out and len(out.strip())>10:
                count=out.count("Date/Heure")+out.count("Date and Time")
                log(f"{label} : {count} événement(s)","WARN" if count>0 else "OK")
                for ev in out.strip().split("\n\n")[:2]:
                    for l in [x.strip() for x in ev.split("\n") if x.strip()][:3]: log(f"  | {l}","SUB")
            else: log(f"{label} : aucun événement critique","OK")
    except Exception as e: log(f"Erreur journaux : {e}","ERR")

def check_bsod():
    section("CRASHS SYSTEME (BSOD)")
    dump_dir=r"C:\Windows\Minidump"
    try:
        if os.path.exists(dump_dir):
            dumps=[f for f in os.listdir(dump_dir) if f.endswith(".dmp")]
            if dumps:
                log(f"CRITIQUE : {len(dumps)} crash(s) BSOD détecté(s) !","ERR")
                for dp in sorted([os.path.join(dump_dir,d) for d in dumps],key=os.path.getmtime,reverse=True)[:3]:
                    dt=datetime.datetime.fromtimestamp(os.path.getmtime(dp)).strftime('%d/%m/%Y %H:%M')
                    log(f"  Crash : {dt} ({os.path.basename(dp)})","SUB")
            else: log("Aucun BSOD récent","OK")
        else: log("Dossier Minidump absent (normal si aucun crash)","OK")
    except Exception as e: log(f"Erreur BSOD : {e}","WARN")

def check_drivers():
    section("PILOTES (DRIVERS)")
    try:
        progress("Scan pilotes")
        out,_,_=run_cmd('powershell Get-WmiObject Win32_PnPEntity | Where-Object {$_.ConfigManagerErrorCode -ne 0} | Select-Object Name,DeviceID,ConfigManagerErrorCode | Format-List',timeout=30)
        done_progress()
        if out and len(out.strip())>5:
            count=out.count("Name")
            log(f"Pilotes en erreur : {count}","ERR" if count>0 else "OK")
            for l in out.strip().split("\n")[:20]:
                if l.strip(): log(f"  {l.strip()}","ERR" if "Name" in l else "SUB")
        else: log("Aucun pilote en erreur","OK")
    except Exception as e: log(f"Erreur drivers : {e}","ERR")

def check_virtual_memory():
    section("MEMOIRE VIRTUELLE & PAGEFILE")
    try:
        out,_,_=run_cmd("wmic pagefile list /format:list",timeout=15)
        if out:
            for l in out.strip().split("\n"):
                if l.strip() and "=" in l: log(f"  {l.strip()}","SUB")
    except Exception as e: log(f"Erreur PageFile : {e}","ERR")

def check_startup():
    section("DEMARRAGE & PROGRAMMES AU LANCEMENT")
    try:
        for hive_name,hive in [("HKLM",winreg.HKEY_LOCAL_MACHINE),("HKCU",winreg.HKEY_CURRENT_USER)]:
            for path in [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"]:
                try:
                    key=winreg.OpenKey(hive,path); items=[]; i=0
                    while True:
                        try: name,val,_=winreg.EnumValue(key,i); items.append((name,val)); i+=1
                        except WindowsError: break
                    if items:
                        log(f"{hive_name}\\{path.split(chr(92))[-1]} : {len(items)} entrée(s)","SUB")
                        for nm,val in items[:8]: log(f"  {nm[:35]:<35} → {val[:55]}","SUB")
                    winreg.CloseKey(key)
                except: pass
        out,_,_=run_cmd('wevtutil qe Microsoft-Windows-Diagnostics-Performance/Operational /q:"*[System[EventID=100]]" /c:5 /rd:true /f:text',timeout=20)
        if out:
            m=re.search(r"BootTime.*?(\d+)",out)
            if m:
                ms=int(m.group(1))
                log(f"Temps démarrage : {ms} ms ({ms/1000:.1f}s)","WARN" if ms>60000 else "OK")
    except Exception as e: log(f"Erreur démarrage : {e}","ERR")

# ══════════════════════════════════════════════════════════════════════════════
# MOTEUR DE RESOLUTION AUTONOME — RELEASE
# Traite TOUS les ERR et WARN détectés
# ══════════════════════════════════════════════════════════════════════════════

FIXES_DB = {
    # ── Réseau ────────────────────────────────────────────────────────────────
    "dns_flush":         {"label":"Vider le cache DNS",                        "cmd":"ipconfig /flushdns",                                                         "timeout":15},
    "ip_renew":          {"label":"Renouveler l'adresse IP",                   "cmd":"ipconfig /release & ipconfig /renew",                                        "timeout":30},
    "tcp_reset":         {"label":"Réinitialiser la pile TCP/IP & Winsock",    "cmd":"netsh int ip reset & netsh winsock reset",                                   "timeout":30},
    # ── Sécurité ──────────────────────────────────────────────────────────────
    "firewall_on":       {"label":"Activer le pare-feu Windows",               "cmd":"netsh advfirewall set allprofiles state on",                                 "timeout":15},
    "uac_enable":        {"label":"Réactiver l'UAC",                           "cmd":'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v EnableLUA /t REG_DWORD /d 1 /f',"timeout":15},
    "defender_rt":       {"label":"Activer Defender temps réel",               "cmd":"powershell Set-MpPreference -DisableRealtimeMonitoring $false",              "timeout":30},
    "defender_upd":      {"label":"Mettre à jour définitions antivirus",       "cmd":"powershell Update-MpSignature",                                             "timeout":90},
    "defender_scan":     {"label":"Scan antivirus rapide",                     "cmd":"powershell Start-MpScan -ScanType QuickScan",                               "timeout":300},
    # ── Services ──────────────────────────────────────────────────────────────
    "svc_wuauserv":      {"label":"Redémarrer Windows Update",                 "cmd":"net stop wuauserv & net start wuauserv",                                    "timeout":30},
    "svc_WinDefend":     {"label":"Redémarrer Windows Defender",               "cmd":"net stop WinDefend & net start WinDefend",                                  "timeout":30},
    "svc_Dnscache":      {"label":"Redémarrer DNS Cache",                      "cmd":"net stop Dnscache & net start Dnscache",                                    "timeout":15},
    "svc_BITS":          {"label":"Redémarrer BITS",                           "cmd":"net stop BITS & net start BITS",                                            "timeout":15},
    "svc_CryptSvc":      {"label":"Redémarrer Cryptographic Services",         "cmd":"net stop CryptSvc & net start CryptSvc",                                    "timeout":15},
    "svc_EventLog":      {"label":"Redémarrer le service Journaux",            "cmd":"net stop EventLog & net start EventLog",                                    "timeout":15},
    "svc_W32Time":       {"label":"Redémarrer l'horloge Windows",              "cmd":"net stop W32Time & net start W32Time & w32tm /resync",                      "timeout":20},
    # ── Alimentation ──────────────────────────────────────────────────────────
    "power_high":        {"label":"Plan d'alimentation : Haute Performance",   "cmd":"powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",                 "timeout":15},
    "power_balanced":    {"label":"Plan d'alimentation : Équilibré",           "cmd":"powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e",                 "timeout":15},
    # ── Disques & fichiers ────────────────────────────────────────────────────
    "temp_cleanup":      {"label":"Supprimer fichiers temporaires",            "cmd":'cmd /c "del /q /f /s %TEMP%\\* 2>nul & del /q /f /s %WINDIR%\\Temp\\* 2>nul"', "timeout":60},
    "wupd_cache_clean":  {"label":"Nettoyer cache Windows Update",             "cmd":"net stop wuauserv & rmdir /s /q C:\\Windows\\SoftwareDistribution\\Download & net start wuauserv", "timeout":60},
    "disk_cleanup_sys":  {"label":"Nettoyage disque système (cleanmgr)",       "cmd":"cleanmgr /sagerun:1",                                                       "timeout":120},
    # ── Fichiers système ──────────────────────────────────────────────────────
    "sfc_scan":          {"label":"Réparer fichiers système (SFC)",            "cmd":"sfc /scannow",                                                              "timeout":900},
    "dism_restore":      {"label":"Restaurer image Windows (DISM)",            "cmd":"dism /online /cleanup-image /restorehealth",                                "timeout":600},
    # ── Navigateurs ───────────────────────────────────────────────────────────
    "chrome_cache":      {"label":"Vider cache Chrome",                        "cmd":'powershell Remove-Item "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\\Cache\\*" -Recurse -Force -ErrorAction SilentlyContinue', "timeout":30},
    "edge_cache":        {"label":"Vider cache Edge",                          "cmd":'powershell Remove-Item "$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data\\Default\\Cache\\*" -Recurse -Force -ErrorAction SilentlyContinue', "timeout":30},
    # ── RAM ───────────────────────────────────────────────────────────────────
    "ram_gc":            {"label":"Forcer libération mémoire (GC)",            "cmd":"powershell [System.GC]::Collect()",                                         "timeout":15},
    "pagefile_auto":     {"label":"Configurer PageFile automatique",           "cmd":'powershell $cs=Get-WmiObject Win32_ComputerSystem; $cs.AutomaticManagedPagefile=$True; $cs.Put()', "timeout":15},
    # ── Réseau avancé ─────────────────────────────────────────────────────────
    "net_reset_full":    {"label":"Réinitialisation réseau complète",          "cmd":"netsh int ip reset & netsh int ipv6 reset & netsh winsock reset & ipconfig /flushdns & ipconfig /release & ipconfig /renew", "timeout":60},
}

# Règles : chaque pattern matche sur ERR et WARN
RESOLVE_RULES = [
    # Réseau
    {"match_any":["Ping","ECHEC"],             "cat":"Réseau",           "fixes":["dns_flush","ip_renew","tcp_reset"],                    "desc":"Connectivité réseau défaillante"},
    {"match_any":["IP publique : indisponible"],"cat":"Réseau",          "fixes":["dns_flush","net_reset_full"],                          "desc":"Accès Internet indisponible"},
    # Sécurité
    {"match_any":["Pare-feu Windows : INACTIF"],"cat":"Sécurité",       "fixes":["firewall_on"],                                         "desc":"Pare-feu désactivé"},
    {"match_any":["UAC : DÉSACTIVÉ"],           "cat":"Sécurité",       "fixes":["uac_enable"],                                          "desc":"UAC désactivé"},
    {"match_any":["False"],                     "cat":"Sécurité",       "fixes":["defender_rt","defender_upd"],                          "desc":"Defender temps réel inactif"},
    {"match_any":["CPU saturé","Stabilité CRITIQUE"],"cat":"Sécurité",  "fixes":["defender_scan"],                                       "desc":"Scan antivirus (stabilité critique)"},
    # Services
    {"match_any":["Windows Update","ARRÊTÉ"],   "cat":"Services",       "fixes":["svc_wuauserv"],                                        "desc":"Service Windows Update arrêté"},
    {"match_any":["Defender","ARRÊTÉ"],         "cat":"Services",       "fixes":["svc_WinDefend"],                                       "desc":"Service Windows Defender arrêté"},
    {"match_any":["DNS Cache","ARRÊTÉ"],        "cat":"Services",       "fixes":["svc_Dnscache"],                                        "desc":"Service DNS Cache arrêté"},
    {"match_any":["BITS","ARRÊTÉ"],             "cat":"Services",       "fixes":["svc_BITS"],                                            "desc":"Service BITS arrêté"},
    {"match_any":["Cryptographic","ARRÊTÉ"],    "cat":"Services",       "fixes":["svc_CryptSvc"],                                        "desc":"Service Cryptographic arrêté"},
    {"match_any":["Journaux","ARRÊTÉ"],         "cat":"Services",       "fixes":["svc_EventLog"],                                        "desc":"Service Journaux arrêté"},
    {"match_any":["Horloge","ARRÊTÉ"],          "cat":"Services",       "fixes":["svc_W32Time"],                                         "desc":"Service Horloge arrêté"},
    # Alimentation
    {"match_any":["Plan Économie d'énergie"],   "cat":"Alimentation",   "fixes":["power_high"],                                          "desc":"Plan d'énergie économie actif"},
    {"match_any":["Batterie faible"],           "cat":"Alimentation",   "fixes":["power_balanced"],                                      "desc":"Batterie faible — plan équilibré"},
    # Disques
    {"match_any":["ESPACE CRITIQUE"],           "cat":"Disques",        "fixes":["temp_cleanup","wupd_cache_clean","disk_cleanup_sys"],  "desc":"Espace disque critique"},
    {"match_any":["Disque presque plein"],      "cat":"Disques",        "fixes":["temp_cleanup","wupd_cache_clean"],                     "desc":"Disque presque plein"},
    # RAM
    {"match_any":["RAM critique","RAM élevée"], "cat":"RAM",            "fixes":["ram_gc","pagefile_auto"],                              "desc":"Utilisation RAM excessive"},
    {"match_any":["RAM insuffisante"],          "cat":"RAM",            "fixes":["ram_gc","pagefile_auto"],                              "desc":"RAM insuffisante"},
    # Navigateurs
    {"match_any":["chrome.exe","RAM : "],       "cat":"Navigateurs",    "fixes":["chrome_cache"],                                        "desc":"Chrome consomme trop de RAM"},
    {"match_any":["msedge.exe","RAM : "],       "cat":"Navigateurs",    "fixes":["edge_cache"],                                          "desc":"Edge consomme trop de RAM"},
    # Fichiers système
    {"match_any":["SFC : Fichiers corrompus","NON réparables"], "cat":"Fichiers système","fixes":["sfc_scan","dism_restore"],            "desc":"Fichiers système corrompus"},
    {"match_any":["DISM : Image altérée"],      "cat":"Fichiers système","fixes":["dism_restore"],                                       "desc":"Image Windows altérée"},
    {"match_any":["Dirty Bit","corrompu"],      "cat":"Système fichiers","fixes":["sfc_scan"],                                           "desc":"Volume C: corrompu (Dirty Bit)"},
    # Uptime
    {"match_any":["Redémarrage récent","<1h)"], "cat":"Stabilité",      "fixes":["defender_scan"],                                       "desc":"Crash récent détecté — scan préventif"},
]

def _exec_fix(fix_id):
    fix=FIXES_DB.get(fix_id)
    if not fix: return False,"Fix introuvable"
    out,err,rc=run_cmd(fix["cmd"],timeout=fix.get("timeout",30))
    return rc==0, (out or err)[:300]

def run_resolve_mode():
    global resolve_log
    resolve_log=[]
    banner("RESOLUTION AUTONOME — RELEASE")

    if not os.path.exists(LOG_FILE):
        print(); print(c(f"  {'═'*62}","red"))
        print(c("  ✘  AUCUN DIAGNOSTIC TROUVÉ — Lancez le Mode 1 d'abord","red"))
        print(c(f"  {'═'*62}","red")); print()
        input(c("  Entrée pour revenir au menu...","white"))
        return

    with open(LOG_FILE,"r",encoding="utf-8",errors="replace") as f:
        content=f.read()

    all_issues=re.findall(r"\[ERR\] (.+)",content)+re.findall(r"\[WARN\] (.+)",content)
    err_count=len(re.findall(r"\[ERR\]",content))
    warn_count=len(re.findall(r"\[WARN\]",content))

    print(c(f"  ℹ  Rapport chargé — {err_count} erreur(s), {warn_count} avertissement(s)","lb"))
    print()

    # Identifier les règles applicables (sans doublons de fixes)
    rules_to_apply=[]; applied_fixes=set()
    for rule in RESOLVE_RULES:
        for issue in all_issues:
            if any(p.lower() in issue.lower() for p in rule["match_any"]):
                if rule not in rules_to_apply:
                    rules_to_apply.append(rule)
                break

    if not rules_to_apply:
        print(c("  ✔  Aucun problème corrigeable automatiquement.","green")); print()
        input(c("  Entrée pour revenir au menu...","white")); return

    # Plan d'action
    print(c(f"  {SEP}","lb"))
    print(c(f"  ► PLAN D'ACTION — {len(rules_to_apply)} catégorie(s) à traiter","lb"))
    print(c(f"  {SEP}","lb")); print()
    for i,rule in enumerate(rules_to_apply,1):
        print(c(f"  [{i:02d}]","lb")+c(f" {rule['cat']:<20}","white")+c(f" {rule['desc']}","sky"))
    print()
    print(c("  ⚡ Résolution automatique — aucune action requise.","yellow")); print()

    # Exécution
    resolved=[]; partial=[]; failed=[]
    for rule in rules_to_apply:
        print(c(f"  {'─'*60}","dim"))
        print(c(f"  ► {rule['cat'].upper()} — {rule['desc']}","lb"))
        for fix_id in rule["fixes"]:
            if fix_id in applied_fixes: continue
            applied_fixes.add(fix_id)
            fix=FIXES_DB.get(fix_id)
            if not fix: continue
            print(c(f"  ⚙  {fix['label']}...","teal"),end=" ",flush=True)
            try:
                success,detail=_exec_fix(fix_id)
                if success:
                    print(c("✔ RÉGLÉ","green"))
                    resolved.append({"cat":rule["cat"],"action":fix["label"],"detail":detail})
                    resolve_log.append({"cat":rule["cat"],"action":fix["label"],"status":"resolved","detail":detail})
                else:
                    print(c("⚠ PARTIEL","yellow"))
                    partial.append({"cat":rule["cat"],"action":fix["label"],"detail":detail})
                    resolve_log.append({"cat":rule["cat"],"action":fix["label"],"status":"partial","detail":detail})
            except Exception as e:
                print(c(f"✘ ERREUR","red"))
                failed.append({"cat":rule["cat"],"action":fix["label"],"detail":str(e)})
                resolve_log.append({"cat":rule["cat"],"action":fix["label"],"status":"failed","detail":str(e)})

    # Bilan console
    print(); print(c(f"  {SEP}","lb")); print(c("  ► BILAN DE RÉSOLUTION","lb")); print(c(f"  {SEP}","lb")); print()
    if resolved:
        print(c(f"  ✔  {len(resolved)} action(s) résolue(s) :","green"))
        for r in resolved: print(c(f"      ✔ [{r['cat']}] {r['action']}","green"))
        print()
    if partial:
        print(c(f"  ⚠  {len(partial)} action(s) partiellement appliquée(s) :","yellow"))
        for r in partial: print(c(f"      ⚠ [{r['cat']}] {r['action']}","yellow"))
        print()
    if failed:
        print(c(f"  ✘  {len(failed)} action(s) échouée(s) :","red"))
        for r in failed: print(c(f"      ✘ [{r['cat']}] {r['action']}","red"))
        print()

    # Mise à jour du rapport HTML
    print(c("  🌐 Mise à jour du rapport HTML...","teal"))
    save_html_report(resolve_data=resolve_log)
    print(c("  ✔  Rapport mis à jour.","green")); print()
    if not partial and not failed:
        print(c("  ✔  Tous les problèmes ont été résolus automatiquement !","green"))
    else:
        print(c("  Consultez le rapport HTML pour les détails complets.","white"))
    print()
    input(c("  Entrée pour revenir au menu...","dim"))

# ══════════════════════════════════════════════════════════════════════════════
# KNOWLEDGE BASE — cliquable dans le HTML
# ══════════════════════════════════════════════════════════════════════════════

ERROR_KB=[
    {"p":["CPU saturé","CPU chargé"],"t":"Charge CPU élevée","w":"psutil cpu_percent() sur 3s","y":"Processus monopolisant le CPU, malware, driver en boucle.","g":"Déclenché si CPU > 70% (warn) ou > 90% (err)."},
    {"p":["TEMP CRITIQUE","Temp élevée"],"t":"Surchauffe CPU/GPU","w":"OpenHardwareMonitor WMI sensors","y":"Pâte thermique usée, ventilateur bouché, boîtier mal ventilé.","g":"CPU > 75°C warn, > 90°C err. GPU > 75°C warn, > 85°C err."},
    {"p":["RAM critique","RAM élevée"],"t":"RAM saturée","w":"psutil virtual_memory().percent","y":"Trop d'onglets/applications, fuite mémoire, pagefile insuffisant.","g":"Déclenché si RAM > 75% (warn) ou > 90% (err)."},
    {"p":["RAM insuffisante"],"t":"RAM insuffisante (<4 Go)","w":"psutil virtual_memory().total","y":"Windows utilise le pagefile disque (10x plus lent), lenteurs permanentes.","g":"Déclenché si RAM totale < 4 Go."},
    {"p":["ESPACE CRITIQUE"],"t":"Espace disque critique","w":"psutil disk_usage().free","y":"Windows ne peut plus créer fichiers temporaires, swap, MAJ.","g":"Déclenché si espace libre < 5 Go."},
    {"p":["Disque presque plein"],"t":"Disque presque plein (>85%)","w":"psutil disk_usage().percent","y":"Risque de basculer en zone critique rapidement.","g":"Déclenché si occupation > 85%."},
    {"p":["SMART anormal"],"t":"Santé SMART dégradée","w":"wmic diskdrive get Status","y":"Secteurs défectueux, fin de vie imminente. Risque de perte de données.","g":"Déclenché si Status WMIC ≠ 'OK'."},
    {"p":["Dirty Bit","corrompu"],"t":"Volume C: corrompu","w":"fsutil dirty query C:","y":"Extinction brutale sans arrêt propre. Structure NTFS incohérente.","g":"Déclenché si fsutil retourne volume 'dirty'."},
    {"p":["ECHEC","Ping"],"t":"Connectivité réseau défaillante","w":"ping vers 8.8.8.8, 1.1.1.1, google.com, windowsupdate","y":"Cable/WiFi, driver réseau, DNS corrompu, pare-feu, box/routeur.","g":"Déclenché si ping retourne code d'erreur ou pas de TTL."},
    {"p":["EXTINCTION CRITIQUE","Event 41","Kernel Power"],"t":"Kernel Power Event 41","w":"wevtutil — journaux Système Event ID 41","y":"Extinction non propre : coupure courant, BSOD, surchauffe.","g":"Déclenché à la détection d'un Event 41 dans les 20 derniers événements."},
    {"p":["ARRÊT INATTENDU","Event 6008"],"t":"Arrêt inattendu","w":"wevtutil — journaux Système Event ID 6008","y":"BSOD, coupure, arrêt forcé.","g":"Déclenché à la détection d'un Event 6008."},
    {"p":["BSOD","Minidump","crash"],"t":"Écrans bleus (BSOD)","w":"C:\\Windows\\Minidump — fichiers .dmp","y":"Driver incompatible, RAM défectueuse, overclocking, surchauffe.","g":"Déclenché si fichiers .dmp présents dans Minidump."},
    {"p":["SFC : Fichiers corrompus","NON réparables"],"t":"Fichiers système corrompus (SFC)","w":"sfc /scannow","y":"MAJ interrompue, virus, extinction brutale pendant écriture système.","g":"Déclenché si SFC signale violations non réparées."},
    {"p":["DISM : Image altérée"],"t":"Image Windows altérée","w":"dism /online /cleanup-image /checkhealth","y":"Component Store corrompu. DISM /RestoreHealth requis.","g":"Déclenché si DISM CheckHealth détecte corruption."},
    {"p":["Pare-feu Windows : INACTIF"],"t":"Pare-feu désactivé","w":"netsh advfirewall show allprofiles state","y":"Désactivé par logiciel tiers, malware, ou manuellement.","g":"Déclenché si profil réseau ne retourne pas ON."},
    {"p":["UAC : DÉSACTIVÉ"],"t":"UAC désactivé","w":"Registre HKLM\\...\\Policies\\System\\EnableLUA","y":"Tout programme peut s'installer sans confirmation. Risque malware.","g":"Déclenché si EnableLUA = 0 dans le registre."},
    {"p":["Pilotes en erreur","en erreur"],"t":"Pilotes matériels en erreur","w":"Win32_PnPEntity.ConfigManagerErrorCode via WMI","y":"Driver incompatible, corrompu, ou matériel défaillant.","g":"Déclenché si ConfigManagerErrorCode ≠ 0."},
    {"p":["ARRÊTÉ"],"t":"Service critique arrêté","w":"sc query {service}","y":"Service arrêté par logiciel, conflit, ou registre corrompu.","g":"Déclenché si sc query retourne STOPPED."},
    {"p":["Stabilité CRITIQUE","Stabilité moyen"],"t":"Indice de stabilité dégradé","w":"Win32_ReliabilityStabilityMetrics.SystemStabilityIndex","y":"Plantages d'apps, MAJ échouées, crashes matériels répétés.","g":"Score < 5 = erreur, entre 5 et 8 = warning."},
    {"p":["Plan Économie"],"t":"Plan énergie Économie actif","w":"powercfg /getactivescheme","y":"Réduit les perfs CPU/disque, veille prématurée.","g":"Déclenché si plan contient 'économie' ou 'power saver'."},
    {"p":["Batterie faible"],"t":"Batterie faible non branchée","w":"psutil.sensors_battery()","y":"Windows peut déclencher une extinction forcée sous 20%.","g":"Déclenché si power_plugged=False ET percent < 20%."},
    {"p":["Redémarrage récent","<1h)"],"t":"Crash récent possible","w":"psutil.boot_time()","y":"Le PC a été redémarré il y a moins d'1h. Possible crash récent.","g":"Déclenché si uptime < 3600 secondes."},
]

def _find_kb(text):
    tl=text.lower()
    for k in ERROR_KB:
        if any(p.lower() in tl for p in k["p"]): return k
    return None

def _esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"','&quot;')

# ══════════════════════════════════════════════════════════════════════════════
# SAVE LOG
# ══════════════════════════════════════════════════════════════════════════════

def save_log():
    header=[SEP,f"  BIOMESH {VERSION} — RAPPORT DE DIAGNOSTIC",
            f"  Date     : {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            f"  Machine  : {platform.node()}",f"  OS       : {platform.system()} {platform.release()}",
            f"  Créateur : {CREATOR}",SEP,""]
    with open(LOG_FILE,"w",encoding="utf-8") as f:
        f.write("\n".join(header)+"\n"+"\n".join(log_lines)+f"\n\n{SEP}\n  FIN DU RAPPORT BIOMESH {VERSION}\n{SEP}\n")
    print(); print(c(f"  📄  Rapport texte : {os.path.abspath(LOG_FILE)}","teal"))

# ══════════════════════════════════════════════════════════════════════════════
# RAPPORT HTML — GLASSMORPHISME RELEASE
# ══════════════════════════════════════════════════════════════════════════════

def save_html_report(resolve_data=None):
    errors=[l for l in log_lines if "[ERR]" in l]
    warnings=[l for l in log_lines if "[WARN]" in l]
    oks=[l for l in log_lines if "[OK]" in l]
    machine=platform.node()
    os_info=f"{platform.system()} {platform.release()}"
    now_str=datetime.datetime.now().strftime("%d/%m/%Y à %H:%M:%S")

    # Rows table
    rows=""; di=0
    for line in log_lines:
        m=re.match(r"\[(\d+:\d+:\d+)\] \[(\w+)\] (.*)",line)
        if not m: continue
        ts,lvl,txt=m.groups(); txt_s=_esc(txt)
        bc={"ERR":"#ff3b3b","WARN":"#ffb300","OK":"#00e676","INFO":"#29b6f6","SUB":"#546e7a","HEAD":"#0a4fff"}
        badge=f'<span class="badge" style="background:{bc.get(lvl,"#546e7a")}">{lvl}</span>'
        rc2={"ERR":"row-err","WARN":"row-warn","OK":"row-ok"}.get(lvl,"")
        kb=_find_kb(txt) if lvl in ("ERR","WARN") else None
        if kb:
            pid=f"dr{di}"; di+=1
            rows+=(f'<tr class="{rc2} clickable" onclick="toggleRow(\'{pid}\')">'
                   f'<td class="ts">{ts}</td><td>{badge} {txt_s} <span class="ei" id="ei-{pid}">▶</span></td></tr>'
                   f'<tr class="drow" id="{pid}"><td colspan="2"><div class="dpanel">'
                   f'<div class="dtitle">🔍 {_esc(kb["t"])}</div>'
                   f'<div class="dgrid">'
                   f'<div class="di"><div class="dlbl">📍 Où</div><div class="dval">{_esc(kb["w"])}</div></div>'
                   f'<div class="di"><div class="dlbl">❓ Pourquoi</div><div class="dval">{_esc(kb["y"])}</div></div>'
                   f'<div class="di dfull"><div class="dlbl">⚡ Déclencheur</div><div class="dval">{_esc(kb["g"])}</div></div>'
                   f'</div></div></td></tr>\n')
        else:
            rows+=f'<tr class="{rc2}"><td class="ts">{ts}</td><td>{badge} {txt_s}</td></tr>\n'

    # Issues list
    ih=""
    if not errors and not warnings:
        ih='<div class="issue-item" style="border-left-color:#00e676"><span class="ii">✔</span><span>Aucun problème majeur détecté.</span></div>'
    for idx,e in enumerate(errors):
        cl=re.sub(r"\[\d+:\d+:\d+\] \[ERR\] ","",e); cs=_esc(cl); kb=_find_kb(cl)
        ar='<span class="ia">▶</span>' if kb else ""
        oc=f'onclick="toggleIssue(this,\'e{idx}\')"' if kb else ""
        ih+=f'<div class="issue-item issue-err" {oc}><span class="ii">✘</span><span>{cs}</span>{ar}</div>\n'
        if kb:
            ih+=(f'<div class="issue-detail" id="e{idx}"><b>📍 Où :</b> {_esc(kb["w"])}<br>'
                 f'<b>❓ Pourquoi :</b> {_esc(kb["y"])}<br><b>⚡ Déclencheur :</b> {_esc(kb["g"])}</div>\n')
    for idx,w in enumerate(warnings[:25]):
        cl=re.sub(r"\[\d+:\d+:\d+\] \[WARN\] ","",w); cs=_esc(cl); kb=_find_kb(cl)
        ar='<span class="ia">▶</span>' if kb else ""
        oc=f'onclick="toggleIssue(this,\'w{idx}\')"' if kb else ""
        ih+=f'<div class="issue-item issue-warn" {oc}><span class="ii">⚠</span><span>{cs}</span>{ar}</div>\n'
        if kb:
            ih+=(f'<div class="issue-detail" id="w{idx}"><b>📍 Où :</b> {_esc(kb["w"])}<br>'
                 f'<b>❓ Pourquoi :</b> {_esc(kb["y"])}<br><b>⚡ Déclencheur :</b> {_esc(kb["g"])}</div>\n')

    # Resolve section
    rs=""
    if resolve_data:
        items=""
        for r in resolve_data:
            icon="✔" if r["status"]=="resolved" else ("⚠" if r["status"]=="partial" else "✘")
            cls3="ri-ok" if r["status"]=="resolved" else ("ri-warn" if r["status"]=="partial" else "ri-err")
            items+=f'<div class="ri {cls3}"><span class="ri-icon">{icon}</span><div><div class="ri-cat">{_esc(r["cat"])}</div><div class="ri-act">{_esc(r["action"])}</div></div></div>\n'
        rs=f'<div class="glass-section anim-up" style="animation-delay:.3s"><div class="section-title">⚙ Résolution automatique — Bilan</div><div class="resolve-grid">{items}</div></div>'

    html=f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BIOMESH {VERSION} — Rapport</title>
<link rel="icon" href="{LOGO_URL}">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=JetBrains+Mono:wght@300;400;500;600&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root{{
  --bg0:#020810;
  --bg1:#040e1f;
  --bg2:#061428;
  --glass:rgba(6,20,50,0.55);
  --glass2:rgba(8,25,60,0.7);
  --b1:#0a4fff;
  --b2:#0090ff;
  --b3:#00cfff;
  --b4:#40e0ff;
  --green:#00e676;
  --yellow:#ffb300;
  --red:#ff3b3b;
  --text:#c8e0ff;
  --dim:#5a82aa;
  --border:rgba(0,144,255,0.2);
  --border2:rgba(0,207,255,0.4);
  --glow1:rgba(10,79,255,0.15);
  --glow2:rgba(0,207,255,0.1);
  --font-head:'Orbitron',sans-serif;
  --font-mono:'JetBrains Mono',monospace;
  --font-body:'Inter',sans-serif;
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{
  background:var(--bg0);
  color:var(--text);
  font-family:var(--font-body);
  min-height:100vh;
  overflow-x:hidden;
}}

/* ── BG ANIMÉ ── */
.bg-wrap{{
  position:fixed;inset:0;z-index:0;
  overflow:hidden;
  pointer-events:none;
}}
.bg-orb{{
  position:absolute;
  border-radius:50%;
  filter:blur(80px);
  animation:orbFloat 20s ease-in-out infinite alternate;
}}
.orb1{{width:700px;height:700px;background:radial-gradient(circle,rgba(10,79,255,0.18),transparent 70%);top:-200px;left:-200px;animation-duration:18s}}
.orb2{{width:500px;height:500px;background:radial-gradient(circle,rgba(0,144,255,0.14),transparent 70%);top:30%;right:-150px;animation-duration:24s;animation-delay:-8s}}
.orb3{{width:400px;height:400px;background:radial-gradient(circle,rgba(0,207,255,0.1),transparent 70%);bottom:-100px;left:30%;animation-duration:20s;animation-delay:-4s}}
@keyframes orbFloat{{0%{{transform:translate(0,0) scale(1)}}100%{{transform:translate(40px,60px) scale(1.1)}}}}

/* Grille */
.bg-grid{{
  position:fixed;inset:0;z-index:0;
  background-image:linear-gradient(rgba(0,144,255,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,144,255,0.03) 1px,transparent 1px);
  background-size:60px 60px;
  pointer-events:none;
}}

/* Scanlines */
.bg-scan{{
  position:fixed;inset:0;z-index:0;
  background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,180,255,0.012) 3px,rgba(0,180,255,0.012) 4px);
  pointer-events:none;
}}

/* ── LAYOUT ── */
.wrap{{
  position:relative;z-index:2;
  max-width:1280px;
  margin:0 auto;
  padding:0 2rem 4rem;
}}

/* ── ANIMATIONS ── */
@keyframes fadeUp{{from{{opacity:0;transform:translateY(24px)}}to{{opacity:1;transform:none}}}}
@keyframes slideIn{{from{{opacity:0;transform:translateY(-10px)}}to{{opacity:1;transform:none}}}}
@keyframes glowPulse{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}
@keyframes borderGlow{{0%,100%{{box-shadow:0 0 20px rgba(0,144,255,0.1)}}50%{{box-shadow:0 0 40px rgba(0,207,255,0.25),0 0 80px rgba(0,144,255,0.1)}}}}
@keyframes shimmer{{0%{{background-position:-200% center}}100%{{background-position:200% center}}}}
@keyframes spin{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0.3}}}}

.anim-up{{animation:fadeUp .6s ease-out forwards;opacity:0}}

/* ── HEADER ── */
header{{
  position:relative;
  padding:3rem 2.5rem 2.5rem;
  overflow:hidden;
  border-bottom:1px solid var(--border2);
  margin-bottom:2.5rem;
  background:linear-gradient(180deg,rgba(4,14,31,0.98) 0%,rgba(4,14,31,0.0) 100%);
}}
.header-line{{
  position:absolute;bottom:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent 0%,var(--b2) 30%,var(--b3) 70%,transparent 100%);
  animation:glowPulse 3s ease-in-out infinite;
}}
.logo-group{{display:flex;align-items:center;gap:1.5rem;margin-bottom:2rem}}
.logo-img{{
  width:56px;height:56px;border-radius:12px;
  border:1px solid var(--border2);
  box-shadow:0 0 24px rgba(0,207,255,0.3);
  animation:borderGlow 4s ease-in-out infinite;
}}
.logo-text{{
  font-family:var(--font-head);
  font-size:clamp(1.4rem,3vw,2.2rem);
  font-weight:900;
  letter-spacing:.15em;
  background:linear-gradient(90deg,var(--b1) 0%,var(--b2) 40%,var(--b3) 70%,var(--b4) 100%);
  background-size:200% auto;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:shimmer 4s linear infinite;
}}
.logo-version{{
  font-family:var(--font-mono);
  font-size:.75rem;letter-spacing:.3em;
  color:var(--b3);text-transform:uppercase;
  margin-top:.3rem;
}}
.creator-tag{{
  display:inline-flex;align-items:center;gap:.5rem;
  background:rgba(0,144,255,0.1);
  border:1px solid rgba(0,144,255,0.25);
  border-radius:20px;padding:.3rem .85rem;
  font-family:var(--font-mono);font-size:.7rem;
  color:var(--b3);letter-spacing:.1em;
  margin-top:.75rem;
}}
.creator-dot{{
  width:6px;height:6px;border-radius:50%;
  background:var(--b3);
  animation:blink 2s ease-in-out infinite;
  box-shadow:0 0 6px var(--b3);
}}
.header-meta{{display:flex;gap:2rem;flex-wrap:wrap;margin-top:1.5rem}}
.meta-item{{display:flex;flex-direction:column;gap:.2rem}}
.meta-label{{font-size:.6rem;letter-spacing:.15em;color:var(--dim);text-transform:uppercase}}
.meta-value{{font-family:var(--font-mono);font-size:.8rem;color:var(--text)}}

/* ── CARDS ── */
.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem;margin-bottom:2rem}}
.card{{
  position:relative;
  background:var(--glass);
  backdrop-filter:blur(24px) saturate(1.5);
  -webkit-backdrop-filter:blur(24px) saturate(1.5);
  border:1px solid var(--border);
  border-radius:16px;
  padding:2rem 1.5rem;
  text-align:center;
  overflow:hidden;
  cursor:default;
  transition:transform .3s cubic-bezier(.34,1.56,.64,1),border-color .3s,box-shadow .3s;
  animation:fadeUp .6s ease-out forwards;opacity:0;
}}
.card:nth-child(1){{animation-delay:.1s}}.card:nth-child(2){{animation-delay:.2s}}.card:nth-child(3){{animation-delay:.3s}}
.card:hover{{transform:translateY(-6px) scale(1.02);border-color:var(--border2);box-shadow:0 20px 60px rgba(0,100,255,0.2)}}
.card::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;border-radius:16px 16px 0 0}}
.card::after{{
  content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse at 50% 0%,currentColor,transparent 60%);
  opacity:0;transition:opacity .3s;pointer-events:none;
}}
.card:hover::after{{opacity:.05}}
.card-ok{{color:var(--green)}}.card-ok::before{{background:linear-gradient(90deg,transparent,var(--green),transparent);box-shadow:0 0 20px var(--green)}}
.card-warn{{color:var(--yellow)}}.card-warn::before{{background:linear-gradient(90deg,transparent,var(--yellow),transparent);box-shadow:0 0 20px var(--yellow)}}
.card-err{{color:var(--red)}}.card-err::before{{background:linear-gradient(90deg,transparent,var(--red),transparent);box-shadow:0 0 20px var(--red)}}
.card-icon{{font-size:1.8rem;margin-bottom:.75rem;display:block;filter:drop-shadow(0 0 8px currentColor)}}
.card-num{{font-family:var(--font-head);font-size:3.5rem;font-weight:900;line-height:1;filter:drop-shadow(0 0 16px currentColor)}}
.card-lbl{{margin-top:.5rem;font-size:.65rem;letter-spacing:.15em;text-transform:uppercase;color:var(--dim)}}
.card-bar{{
  position:absolute;bottom:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,transparent,currentColor,transparent);
  opacity:.3;
}}

/* ── GLASS SECTION ── */
.glass-section{{
  background:var(--glass);
  backdrop-filter:blur(24px) saturate(1.4);
  -webkit-backdrop-filter:blur(24px) saturate(1.4);
  border:1px solid var(--border);
  border-radius:16px;
  padding:2rem 2.5rem;
  margin-bottom:1.5rem;
  box-shadow:0 8px 48px rgba(0,80,200,0.08),inset 0 1px 0 rgba(255,255,255,0.04);
  transition:border-color .3s,box-shadow .3s;
}}
.glass-section:hover{{border-color:rgba(0,144,255,0.3);box-shadow:0 12px 60px rgba(0,80,200,0.12),inset 0 1px 0 rgba(255,255,255,0.05)}}

/* ── SECTION TITLE ── */
.section-title{{
  font-family:var(--font-head);
  font-size:.65rem;letter-spacing:.25em;text-transform:uppercase;
  color:var(--b3);margin-bottom:1.25rem;
  display:flex;align-items:center;gap:.85rem;
}}
.section-title::after{{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(0,207,255,0.4),transparent)}}

/* ── ISSUES ── */
.issue-list{{display:flex;flex-direction:column;gap:.4rem}}
.issue-item{{
  display:flex;align-items:flex-start;gap:.85rem;
  background:rgba(4,12,30,0.6);
  border:1px solid var(--border);border-left:2px solid;
  border-radius:10px;padding:.75rem 1.1rem;
  font-family:var(--font-mono);font-size:.75rem;
  cursor:pointer;
  transition:background .2s,transform .2s cubic-bezier(.34,1.56,.64,1),border-color .2s;
  position:relative;overflow:hidden;
}}
.issue-item::before{{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.03),transparent);
  transform:translateX(-100%);transition:transform .4s;
}}
.issue-item:hover::before{{transform:translateX(100%)}}
.issue-item:hover{{background:rgba(6,18,50,0.8);transform:translateX(4px)}}
.issue-err{{border-left-color:var(--red)}}
.issue-warn{{border-left-color:var(--yellow)}}
.ii{{flex-shrink:0;font-size:1rem}}
.ia{{margin-left:auto;opacity:.35;transition:transform .25s cubic-bezier(.34,1.56,.64,1),opacity .2s;flex-shrink:0;font-size:.7rem}}
.issue-item.exp .ia{{transform:rotate(90deg);opacity:1;color:var(--b3)}}
.issue-detail{{
  display:none;
  background:rgba(0,20,60,0.7);
  backdrop-filter:blur(12px);
  border:1px solid var(--border2);border-top:none;
  border-radius:0 0 10px 10px;
  padding:1.1rem 1.4rem;
  font-family:var(--font-mono);font-size:.73rem;line-height:1.9;color:var(--text);
}}
.issue-detail.open{{display:block;animation:slideIn .2s ease-out}}
.issue-detail b{{color:var(--b3)}}

/* ── FILTER BAR ── */
.filters{{display:flex;gap:.6rem;flex-wrap:wrap;margin-bottom:1rem}}
.fbtn{{
  padding:.35rem 1.1rem;border-radius:20px;
  border:1px solid var(--border);
  background:rgba(4,12,30,0.5);
  color:var(--dim);font-family:var(--font-mono);font-size:.68rem;
  cursor:pointer;letter-spacing:.06em;
  transition:all .25s cubic-bezier(.34,1.56,.64,1);
}}
.fbtn:hover{{border-color:var(--b3);color:var(--b3);background:rgba(0,207,255,0.07);transform:translateY(-1px)}}
.fbtn.active{{
  background:linear-gradient(135deg,var(--b1),var(--b2));
  color:#fff;border-color:transparent;
  box-shadow:0 4px 20px rgba(0,144,255,0.35);
  transform:translateY(-1px);
}}

/* ── HINT ── */
.hint{{
  display:flex;align-items:center;gap:.75rem;
  background:rgba(0,207,255,0.05);
  border:1px solid rgba(0,207,255,0.15);
  border-radius:8px;padding:.55rem 1rem;
  font-size:.7rem;color:var(--dim);
  font-family:var(--font-mono);margin-bottom:1rem;
}}
.hint b{{color:var(--b3)}}

/* ── TABLE ── */
.table-wrap{{overflow-x:auto;border-radius:12px;border:1px solid var(--border)}}
table{{width:100%;border-collapse:collapse;font-family:var(--font-mono);font-size:.73rem}}
thead tr{{background:rgba(4,14,40,0.9);border-bottom:1px solid var(--border2)}}
thead th{{padding:.7rem 1rem;text-align:left;font-size:.6rem;letter-spacing:.18em;text-transform:uppercase;color:var(--b3)}}
tbody tr{{border-bottom:1px solid rgba(0,144,255,0.07);transition:background .15s}}
tbody tr:not(.drow):hover{{background:rgba(0,100,255,0.05)}}
td{{padding:.5rem 1rem;vertical-align:top}}
.ts{{color:var(--dim);white-space:nowrap;width:68px}}
.row-err td{{background:rgba(255,59,59,0.04)}}
.row-warn td{{background:rgba(255,179,0,0.04)}}
.row-ok td{{background:rgba(0,230,118,0.03)}}
.badge{{
  display:inline-block;padding:.1rem .38rem;border-radius:4px;
  font-size:.6rem;letter-spacing:.04em;margin-right:.4rem;
  color:#000;font-weight:700;vertical-align:middle;
}}
.clickable{{cursor:pointer}}
.clickable:hover td{{background:rgba(0,150,255,0.08) !important}}
.ei{{opacity:.3;font-size:.62rem;margin-left:.4rem;transition:transform .25s cubic-bezier(.34,1.56,.64,1)}}
.clickable.open .ei{{transform:rotate(90deg);opacity:.8;color:var(--b3)}}
.drow{{display:none}}
.drow.open{{display:table-row;animation:slideIn .2s ease-out}}
.drow td{{padding:0}}
.dpanel{{
  margin:.3rem 1rem .85rem;
  background:rgba(0,20,60,0.7);backdrop-filter:blur(14px);
  border:1px solid var(--border2);border-left:2px solid var(--b3);
  border-radius:10px;padding:1.2rem 1.5rem;
}}
.dtitle{{font-family:var(--font-head);font-size:.8rem;font-weight:700;color:var(--b3);margin-bottom:.9rem;letter-spacing:.05em}}
.dgrid{{display:grid;grid-template-columns:1fr 1fr;gap:.9rem}}
.dfull{{grid-column:1/-1}}
.di{{display:flex;flex-direction:column;gap:.25rem}}
.dlbl{{font-size:.58rem;letter-spacing:.14em;text-transform:uppercase;color:var(--dim)}}
.dval{{font-size:.72rem;color:var(--text);line-height:1.65}}

/* ── RESOLVE ── */
.resolve-grid{{display:flex;flex-direction:column;gap:.45rem}}
.ri{{
  display:flex;align-items:center;gap:.9rem;
  background:rgba(4,12,30,0.6);
  border:1px solid var(--border);border-left:2px solid;
  border-radius:10px;padding:.7rem 1.1rem;
  font-family:var(--font-mono);font-size:.75rem;
  transition:background .2s,transform .2s;
}}
.ri:hover{{background:rgba(6,18,50,0.8);transform:translateX(4px)}}
.ri-ok{{border-left-color:var(--green)}} .ri-warn{{border-left-color:var(--yellow)}} .ri-err{{border-left-color:var(--red)}}
.ri-icon{{font-size:1.1rem;flex-shrink:0}}
.ri-cat{{font-size:.6rem;color:var(--dim);letter-spacing:.12em;text-transform:uppercase}}
.ri-act{{color:var(--text);font-size:.75rem;margin-top:.1rem}}

/* ── FOOTER ── */
footer{{
  text-align:center;padding:2.5rem;color:var(--dim);
  font-family:var(--font-mono);font-size:.65rem;
  border-top:1px solid var(--border);margin-top:2rem;
  position:relative;
}}
footer::before{{
  content:'';position:absolute;top:0;left:20%;right:20%;height:1px;
  background:linear-gradient(90deg,transparent,var(--b2),transparent);
  animation:glowPulse 4s ease-in-out infinite;
}}
.footer-logo{{
  font-family:var(--font-head);
  font-size:.75rem;letter-spacing:.2em;
  background:linear-gradient(90deg,var(--b2),var(--b3));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  margin-bottom:.5rem;display:block;
}}

/* ── SCROLLBAR ── */
::-webkit-scrollbar{{width:5px;height:5px}}
::-webkit-scrollbar-track{{background:var(--bg0)}}
::-webkit-scrollbar-thumb{{background:rgba(0,144,255,0.3);border-radius:3px}}
::-webkit-scrollbar-thumb:hover{{background:rgba(0,207,255,0.5)}}

@media(max-width:640px){{
  .cards{{grid-template-columns:1fr}}
  header,.glass-section{{padding:1.5rem}}
  .dgrid{{grid-template-columns:1fr}}
  .header-meta{{gap:1rem}}
}}
</style>
</head>
<body>

<div class="bg-wrap">
  <div class="bg-orb orb1"></div>
  <div class="bg-orb orb2"></div>
  <div class="bg-orb orb3"></div>
</div>
<div class="bg-grid"></div>
<div class="bg-scan"></div>

<header>
  <div class="header-line"></div>
  <div class="logo-group">
    <img class="logo-img" src="{LOGO_URL}" alt="BIOMESH" onerror="this.style.display='none'">
    <div>
      <div class="logo-text">BIOMESH</div>
      <div class="logo-version">{VERSION} &nbsp;—&nbsp; Rapport de Diagnostic</div>
      <div class="creator-tag"><span class="creator-dot"></span> by {CREATOR}</div>
    </div>
  </div>
  <div class="header-meta">
    <div class="meta-item"><span class="meta-label">Machine</span><span class="meta-value">{machine}</span></div>
    <div class="meta-item"><span class="meta-label">Système</span><span class="meta-value">{os_info}</span></div>
    <div class="meta-item"><span class="meta-label">Généré le</span><span class="meta-value">{now_str}</span></div>
  </div>
</header>

<div class="wrap">

<div class="cards">
  <div class="card card-ok"><span class="card-icon">✔</span><div class="card-num">{len(oks)}</div><div class="card-lbl">Checks OK</div><div class="card-bar"></div></div>
  <div class="card card-warn"><span class="card-icon">⚠</span><div class="card-num">{len(warnings)}</div><div class="card-lbl">Avertissements</div><div class="card-bar"></div></div>
  <div class="card card-err"><span class="card-icon">✘</span><div class="card-num">{len(errors)}</div><div class="card-lbl">Erreurs critiques</div><div class="card-bar"></div></div>
</div>

{rs}

<div class="glass-section anim-up" style="animation-delay:.4s">
  <div class="section-title">Problèmes détectés — cliquez pour le détail</div>
  <div class="issue-list">{ih}</div>
</div>

<div class="glass-section anim-up" style="animation-delay:.5s">
  <div class="section-title">Journal complet — lignes ERR/WARN cliquables</div>
  <div class="hint"><span>💡</span> Cliquez sur une ligne <b>ERR</b> ou <b>WARN</b> pour afficher l'analyse détaillée.</div>
  <div class="filters">
    <button class="fbtn active" onclick="filterLog(this,'ALL')">TOUT</button>
    <button class="fbtn" onclick="filterLog(this,'ERR')">ERREURS</button>
    <button class="fbtn" onclick="filterLog(this,'WARN')">WARNINGS</button>
    <button class="fbtn" onclick="filterLog(this,'OK')">OK</button>
    <button class="fbtn" onclick="filterLog(this,'INFO')">INFO</button>
  </div>
  <div class="table-wrap">
    <table id="logTable">
      <thead><tr><th>Heure</th><th>Entrée</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</div>

</div>

<footer>
  <span class="footer-logo">BIOMESH {VERSION}</span>
  by {CREATOR} &nbsp;·&nbsp; {now_str} &nbsp;·&nbsp; {machine}
</footer>

<script>
function toggleRow(id){{
  const dr=document.getElementById(id),tr=dr.previousElementSibling;
  if(!dr)return;
  const open=dr.classList.contains('open');
  dr.classList.toggle('open',!open);tr.classList.toggle('open',!open);
  const ei=document.getElementById('ei-'+id);
  if(ei)ei.style.transform=open?'':'rotate(90deg)';
}}
function toggleIssue(el,id){{
  const d=document.getElementById(id);if(!d)return;
  const open=d.classList.contains('open');
  d.classList.toggle('open',!open);el.classList.toggle('exp',!open);
}}
function filterLog(btn,level){{
  document.querySelectorAll('.fbtn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  const rows=document.querySelectorAll('#logTable tbody tr');
  rows.forEach(row=>{{
    if(row.classList.contains('drow'))return;
    if(level==='ALL'){{row.style.display='';return;}}
    const badge=row.querySelector('.badge');
    const match=badge&&badge.textContent.trim()===level;
    row.style.display=match?'':'none';
    const next=row.nextElementSibling;
    if(!match&&next&&next.classList.contains('drow'))next.style.display='none';
  }});
}}
// Stagger animation observer
const obs=new IntersectionObserver(entries=>{{
  entries.forEach(e=>{{if(e.isIntersecting)e.target.style.animationPlayState='running'}});
}},{{threshold:.1}});
document.querySelectorAll('.anim-up').forEach(el=>{{el.style.animationPlayState='paused';obs.observe(el)}});
</script>
</body>
</html>"""

    with open(HTML_REPORT,"w",encoding="utf-8") as f: f.write(html)
    print(c(f"  🌐  Rapport HTML : {os.path.abspath(HTML_REPORT)}","teal"))

# ══════════════════════════════════════════════════════════════════════════════
# SYNTHESE
# ══════════════════════════════════════════════════════════════════════════════

def print_summary():
    section(f"SYNTHESE FINALE — BIOMESH {VERSION}")
    errors=[l for l in log_lines if "[ERR]" in l]
    warnings=[l for l in log_lines if "[WARN]" in l]
    oks=[l for l in log_lines if "[OK]" in l]
    print()
    print(c(f"  ┌{'─'*64}┐","lb"))
    print(c(f"  │  ✔  Checks OK         : {len(oks):<5}{'':37}│","green"))
    print(c(f"  │  ⚠  Avertissements    : {len(warnings):<5}{'':37}│","yellow"))
    print(c(f"  │  ✘  Erreurs critiques : {len(errors):<5}{'':37}│","red"))
    print(c(f"  └{'─'*64}┘","lb"))
    print()
    if errors:
        print(c("  PROBLÈMES CRITIQUES :","red"))
        for e in errors: print(c(f"    ✘ {re.sub(r'\\[\\d+:\\d+:\\d+\\] \\[ERR\\] ','',e)}","red"))
        print()
    if warnings:
        print(c("  AVERTISSEMENTS :","yellow"))
        for w in warnings[:8]: print(c(f"    ⚠ {re.sub(r'\\[\\d+:\\d+:\\d+\\] \\[WARN\\] ','',w)}","yellow"))
        print()
    if not errors and not warnings: print(c("  ✔  Aucun problème majeur détecté.","green"))
    elif errors: print(c("  → Lancez le Mode 2 pour résoudre automatiquement.","lb"))
    log(f"Résumé : {len(oks)} OK | {len(warnings)} WARN | {len(errors)} ERR","INFO",print_also=False)

# ══════════════════════════════════════════════════════════════════════════════
# MENU PRINCIPAL — RELEASE
# ══════════════════════════════════════════════════════════════════════════════

def main_menu():
    banner()
    log_exists=os.path.exists(LOG_FILE)
    G=GRAD
    print(c(f"  ╔{'═'*60}╗","lb"))
    print(c(f"  ║{'MENU PRINCIPAL':^60}║","lb"))
    print(c(f"  ╠{'═'*60}╣","lb"))
    print(c(f"  ║{'':60}║","lb"))
    print(f"  {G[0]}║{C['reset']}  {G[1]}[ 1 ]{C['reset']}  {G[3]}🔍  Diagnostic Windows{C['reset']}{'Analyse complète':>32}  {G[0]}║{C['reset']}")
    print(c(f"  ║{'':60}║","lb"))
    if log_exists:
        print(f"  {G[0]}║{C['reset']}  {G[1]}[ 2 ]{C['reset']}  {G[3]}⚙   Résolution Windows{C['reset']}{'Correction automatique':>32}  {G[0]}║{C['reset']}")
    else:
        print(c(f"  ║  [ 2 ]  ⚙   Résolution Windows{'Diagnostic requis':>37}  ║","dim"))
    print(c(f"  ║{'':60}║","lb"))
    print(c(f"  ║  [ Q ]  🚪  Quitter{'':42}║","dim"))
    print(c(f"  ║{'':60}║","lb"))
    print(c(f"  ╚{'═'*60}╝","lb"))
    print()
    if log_exists:
        try:
            mtime=os.path.getmtime(LOG_FILE)
            dt=datetime.datetime.fromtimestamp(mtime).strftime('%d/%m/%Y à %H:%M')
            print(c(f"  📄  Dernier diagnostic : {dt}","green"))
            with open(LOG_FILE,encoding="utf-8",errors="replace") as f: fc=f.read()
            ec=fc.count("[ERR]"); wc=fc.count("[WARN]")
            if ec: print(c(f"  ⚠   {ec} erreur(s) · {wc} avertissement(s) détecté(s)","yellow"))
            else:  print(c("  ✔   Aucune erreur dans le dernier diagnostic","green"))
        except: pass
        print()
    print(c(f"  by {CREATOR}  ·  BIOMESH {VERSION}","dim")); print()
    print(c("  Votre choix : ","lb"),end="")
    try: return input().strip().upper()
    except (KeyboardInterrupt,EOFError): return "Q"

# ══════════════════════════════════════════════════════════════════════════════
# DIAGNOSTIC COMPLET
# ══════════════════════════════════════════════════════════════════════════════

def run_diagnostic():
    global log_lines
    log_lines=[]
    banner(f"DIAGNOSTIC COMPLET — MODE 1")
    print(c(f"  Machine : {platform.node()}  ·  {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}","dim"))
    print(c("  Démarrage...","lb")); print()
    log(f"BIOMESH {VERSION} — Diagnostic sur {platform.node()}","INFO",print_also=False)
    steps=[
        ("Informations système",check_system_info),
        ("Indice de stabilité",check_system_stability),
        ("Processeur",check_cpu),
        ("Mémoire RAM",check_ram),
        ("Disques",check_disks),
        ("Intégrité Fichiers",check_filesystem_integrity),
        ("Réseau",check_network),
        ("Alimentation",check_power),
        ("GPU",check_gpu),
        ("Processus & Services",check_processes),
        ("Navigateurs Web",check_browsers),
        ("MAJ & Sécurité",check_updates),
        ("Fichiers système (SFC & DISM)",check_system_files),
        ("Journaux d'événements",check_event_logs),
        ("BSOD",check_bsod),
        ("Pilotes",check_drivers),
        ("Mémoire virtuelle",check_virtual_memory),
        ("Démarrage",check_startup),
    ]
    total=len(steps)
    for i,(label,func) in enumerate(steps,1):
        print()
        filled=int((i/total)*30); bar="█"*filled+"░"*(30-filled)
        print(c(f"  [{i:02d}/{total}] {C['reset']}{GRAD[min(i//4,5)]}{bar}{C['reset']} {c(label,'white')}","lb"))
        try: func()
        except Exception as e:
            log(f"Erreur dans '{label}' : {e}","ERR")
            log(traceback.format_exc(),"ERR",print_also=False)
    print_summary(); save_log(); save_html_report()
    errors=[l for l in log_lines if "[ERR]" in l]
    if errors:
        print(); print(c(f"  {'─'*58}","dim"))
        print(c(f"  💡  {len(errors)} erreur(s) — Lancez le Mode 2 pour résoudre.","yellow"))
        print(c(f"  {'─'*58}","dim"))
    print(); print(c(f"  📄  Rapport texte : {os.path.abspath(LOG_FILE)}","teal"))
    print(c(f"  🌐  Rapport HTML  : {os.path.abspath(HTML_REPORT)}","teal"))
    print(); input(c("  Entrée pour revenir au menu...","dim"))

# ══════════════════════════════════════════════════════════════════════════════
# INSTALL DEPS
# ══════════════════════════════════════════════════════════════════════════════

def install_dependencies():
    pkgs=["psutil","wmi","requests","pywin32"]
    if os.path.exists("requirements.txt"):
        subprocess.run([sys.executable,"-m","pip","install","-r","requirements.txt","-q","--disable-pip-version-check"],check=False)
        return
    for pkg in pkgs:
        try: __import__("win32api" if pkg=="pywin32" else pkg)
        except ImportError:
            print(c(f"  Installation de {pkg}...","yellow"))
            subprocess.run([sys.executable,"-m","pip","install",pkg,"-q","--disable-pip-version-check"],check=False)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    os.system("color")
    if sys.platform=="win32":
        try: ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11),7)
        except: pass
    install_dependencies()
    global psutil,wmi,winreg
    import psutil
    try: import wmi
    except: wmi=None
    import winreg
    while True:
        choice=main_menu()
        if choice=="1": run_diagnostic()
        elif choice=="2": run_resolve_mode()
        elif choice in ("Q","0","EXIT","QUITTER"):
            cls(); banner("AU REVOIR")
            print(c(f"  Merci d'utiliser BIOMESH {VERSION}","lb"))
            print(c(f"  by {CREATOR}","dim")); print()
            time.sleep(1); sys.exit(0)
        else:
            print(c("  Choix invalide.","red"),end=" "); input()

if __name__=="__main__":
    main()
