import requests
from bs4 import BeautifulSoup

class InfonieveScraper:
    def __init__(self, resort_name):
        self.resort_name = resort_name
        self.base_url = f"https://infonieve.es/estacion-esqui/{resort_name}/parte-de-nieve/"
        
    def scrape_resort_data(self):
        """Scrape the snow report data for a specific resort from Infonieve."""
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
            response = requests.get(self.base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 'Estado' (open/closed status)
            estado_div = soup.select_one(".box_est_parteestado_estado")
            if estado_div and estado_div.text.strip() != "CERRADA":
                resort_data["estado"] = 1

            # 'Calidad' (snow quality)
            calidad_div = soup.select_one(".box_est_partedet_nieve")
            if calidad_div:
                resort_data["calidad"] = calidad_div.text.strip()

            # 'Espesor Mínimo' and 'Espesor Máximo' (snow depths)
            espesor_divs = soup.select(".box_est_partedet_datosnieve .box_est_partedet_dato")
            if len(espesor_divs) >= 2:
                resort_data["espesor_minimo"] = espesor_divs[0].text.strip().replace("cm", "") or "N/A"
                resort_data["espesor_maximo"] = espesor_divs[1].text.strip().replace("cm", "") or "N/A"

            # 'Peligro de Aludes' (avalanche danger level)
            peligro_div = soup.select_one(".box_est_partedet_aludes .box_est_partedet_aludesno")
            if peligro_div and peligro_div.text.strip() != "sin información":
                resort_data["peligro_de_aludes"] = peligro_div.text.strip()

            # 'Kilómetros' (total kilometers)
            kilometros_div = soup.select_one(".box_est_partedet_datosgeneral > div:nth-of-type(3) .dato_circulo_leyenda")
            if kilometros_div:
                resort_data["kilometros"] = kilometros_div.text.strip().replace("/", "")

            # 'Pistas Totales' (total pistes count)
            pistas_div = soup.select(".box_est_partedet_datosgeneral .dato_circulo")[1]
            if pistas_div:
                resort_data["pistas"]["totales"] = f"{pistas_div.select_one('.dato_circulo_dato').text.strip()}{pistas_div.select_one('.dato_circulo_leyenda').text.strip()}"

            # Breakdown of pistes by type
            trail_breakdown_divs = soup.select(".box_est_partedet_datospistas .dato_circulo")
            trail_types = ["verdes", "azules", "rojas", "negras", "itinerarios"]
            for i, type_ in enumerate(trail_types):
                try:
                    count = trail_breakdown_divs[i].select_one(".dato_circulo_dato").text.strip()
                    total = trail_breakdown_divs[i].select_one(".dato_circulo_leyenda").text.strip()
                    resort_data["pistas"][type_] = f"{count}{total}"
                except (IndexError, AttributeError):
                    resort_data["pistas"][type_] = "N/A"  # Handle missing data

        except requests.RequestException as e:
            print(f"Error scraping from Infonieve for {self.resort_name}: {e}")
        
        return resort_data

    @staticmethod
    def scrape_resorts_names():
        """Scrape resort names from the Infonieve sitemap."""
        url = "https://infonieve.es/sitemap.xml"
        response = requests.get(url)

        if response.status_code != 200:
            return []

        lines = response.text.splitlines()
        resorts = set()

        for line in lines:
            line = line.strip()
            if "/estacion-esqui/" in line and line.count("/") == 5:
                resort_name = line.split("/")[4]
                resorts.add(resort_name)

        return list(resorts)