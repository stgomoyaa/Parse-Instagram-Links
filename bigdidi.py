from selenium import webdriver
import time

# Función para número de líneas
def lineas(filename):
    with open(filename) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1

# Solicitando datos
print("======================================================")
print("|👑A R M A D O R  D E  P A C K S                     |\n")
print("|🧠Versión: 1.4                                      |")
print("|🚀By Ceo de PF                                      |\n")
print("|💕5763 -> $0.04 per 1.000 (HQ LIKES) - BAJAN        |\n")
print("|💕3012 -> $0.072 per 1.000 (UHQ LIKES) - ESTABLES   |\n")
print("|👀5857 -> $0.072 per 1.000 (HQ R/VIEWS) - NODROP    |")
print("======================================================\n")

# Solitando username y si es post-reel
respuesta = input("🚚¿Posts(1) o Reels(2)? =>")
user = input("✍Ingresa el nombre de usuario =>")

# Solicitando ID
if respuesta == "1":
    ids = input("✍Ingresa el id que quieres usar para los likes =>")
elif respuesta == "2":
    ids = input("✍Ingresa el id que quieres usar para las views =>")

# Solicitando Cantidad
if respuesta == "1":
    quantity = input("✍Ingresa cuántos likes quieres por post =>")
elif respuesta == "2":
    quantity = input("✍Ingresa cuántas views quieres por reel =>")
howMuch = int(input("📌Cuántos son?=>"))

# Obteniendo el usuario de chromedriver
options = webdriver.ChromeOptions() 
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('log-level=3')
options.add_argument(r"user-data-dir=C:\Users\stgom\AppData\Local\Google\Chrome\User Data")
PATH = r"C:\Users\stgom\Desktop\rsdt\chromedriver.exe"
driver = webdriver.Chrome(PATH,options=options)

# Ingresando a Instagram
if respuesta == "1":
    driver.get("https://www.instagram.com/"+user)
elif respuesta == "2":
    driver.get(f"https://www.instagram.com/{user}/reels/")

time.sleep(5)

# Scrolleando y copiando links
links = []
elements = driver.find_elements_by_xpath("//a[@href]")
for i in elements:
    if '/p/' in i:
        while(links.count < )
        links.append(i.get_attribute('href'))
    
scrolldown = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
match=False

# Usando un While para llegar hasta el final del perfil
while(match==False):
    last_count = scrolldown
    time.sleep(1.8)
    elements = driver.find_elements_by_xpath("//a[@href]")
    for i in elements:
        links.append(i.get_attribute('href'))
    scrolldown = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    if last_count==scrolldown:
        match=True

# Ingresando los datos a un txt
for l in links:
    with open(f"{''.join(user.split('.'))}.txt", "w") as f:
        for l in links:
            f.write(f"{ids}|{l}|{quantity}")
            f.write("\n")

# Eliminando los repetidos
uniqlines = set(open(f"{''.join(user.split('.'))}.txt").readlines())
bar = open(f"{''.join(user.split('.'))}.txt", 'w').writelines(uniqlines)

# Se pasan los links requeridos a un txt
with open(f"{''.join(user.split('.'))}.txt", "w") as f:
    for link in links_to_keep:
        f.write(link)

nLineas = lineas(f"{''.join(user.split('.'))}.txt")
print("")
print("==============================")
print("🔥T O D O  R E A D Y🔥\n")
print(f"")
print(f"🤙Añadidos {nLineas} Enlaces")
print(f"📌A {''.join(user.split('.'))}.txt")
print("==============================\n")
