import requests
from bs4 import BeautifulSoup

def scrape_resort_data(resort_name):
    # Base URL for the resort's snow report page
    url = f"https://infonieve.es/estacion-esqui/{resort_name}/parte-de-nieve/"

    # Initialize dictionary to store resort data in the desired format
    resort_data = {
        "estado": 0,
        "calidad": "N/A",
        "espesor_maximo": "N/A",
        "espesor_minimo": "N/A",
        "peligro_de_aludes": "N/A",
        "kilometros": "N/A",
        "pistas": {
            "totales": "N/A",
            "verdes": "N/A",
            "azules": "N/A",
            "rojas": "N/A",
            "negras": "N/A",
            "itinerarios": "N/A"
        }
    }

    try:
        # Fetch and parse the page
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Scrape 'Estado' (open/closed status)
        estado_div = soup.select_one(".box_est_parteestado_estado")
        if estado_div:
            if estado_div.text.strip() != "CERRADA":
                resort_data["estado"] = 1

        # Scrape 'Calidad' (quality of snow)
        calidad_div = soup.select_one(".box_est_partedet_nieve")
        if calidad_div:
            resort_data["calidad"] = calidad_div.text.strip()

        # Scrape 'Espesor Mínimo' and 'Espesor Máximo' (snow depths)
        espesor_divs = soup.select(".box_est_partedet_datosnieve .box_est_partedet_dato")
        
        if len(espesor_divs) >= 2:
            # Remove "cm" and strip whitespace
            espesor_minimo = espesor_divs[0].text.strip().replace("cm", "")
            espesor_maximo = espesor_divs[1].text.strip().replace("cm", "")
            
            # Use conditional expressions for cleaner assignment
            resort_data["espesor_minimo"] = "N/A" if espesor_minimo == "-" else espesor_minimo
            resort_data["espesor_maximo"] = "N/A" if espesor_maximo == "-" else espesor_maximo


        # Scrape 'Peligro de Aludes' (avalanche danger level)
        peligro_div = soup.select_one(".box_est_partedet_aludes .box_est_partedet_aludesno")
        if peligro_div:
            if (peligro_div.text.strip() != "sin información"):
                resort_data["peligro_de_aludes"] = peligro_div.text.strip()

        # Scrape 'Kilómetros'
        kilometros_div = soup.select_one(".box_est_partedet_datosgeneral > div:nth-of-type(3) .dato_circulo_leyenda")
        if kilometros_div:
            kilometros_data = kilometros_div.text.strip().replace("/", "")
            resort_data["kilometros"] = kilometros_data  # Stores the value '50,5' without the '/' character

        # Scrape 'Pistas Totales' (total pistes count)
        pistas_div = soup.select(".box_est_partedet_datosgeneral .dato_circulo")[1]
        if pistas_div:
            # TODO - handle pistas & totals, i need the second with that tag, the first dont correspond to pistas but to
            pistas = pistas_div.select_one(".dato_circulo_dato").text.strip()
            totals = pistas_div.select_one(".dato_circulo_leyenda").text.strip()
            resort_data["pistas"]["totales"] = f"{pistas}{totals}"  # Format as "pistas /totals"

        # Scrape breakdown of pistes by type
        trail_breakdown_divs = soup.select(".box_est_partedet_datospistas .dato_circulo")
        trail_types = ["verdes", "azules", "rojas", "negras", "itinerarios"]
        for i, type_ in enumerate(trail_types):
            try:
                count = trail_breakdown_divs[i].select_one(".dato_circulo_dato").text.strip()
                total = trail_breakdown_divs[i].select_one(".dato_circulo_leyenda").text.strip()
                resort_data["pistas"][type_] = f"{count}{total}"  # Format as "count/total"
            except (IndexError, AttributeError):
                resort_data["pistas"][type_] = "N/A"  # Handle missing data

    except Exception as e:
        print(f"Error scraping from Infonieve for {resort_name}: {e}")
    
    return resort_data

def scrape_resorts_names():
    url = "https://infonieve.es/sitemap.xml"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        return []

    # Split the content by lines
    lines = response.text.splitlines()
    resorts = set()

    # Iterate through each line to find resort URLs
    for line in lines:
        line = line.strip()  # Remove extra whitespace

        # Match URLs in the format /estacion-esqui/<resort_name>/
        if "/estacion-esqui/" in line and line.count("/") == 5:
            resort_name = line.split("/")[4]
            resorts.add(resort_name)

    # Return resort names as a list
    return list(resorts)
