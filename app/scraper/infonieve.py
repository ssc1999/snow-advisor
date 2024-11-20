import requests
from bs4 import BeautifulSoup

class InfonieveScraper:
    def __init__(self, resort_name):
        self.resort_name = resort_name
        self.base_url = f"https://infonieve.es/estacion-esqui/{resort_name}/parte-de-nieve/"
        
    def scrape_resort_data(self):
        """Scrape the snow report data for a specific resort from Infonieve."""
        resort_data = {
            "estado": "Closed",
            "calidad": "-",
            "espesor_maximo": "-",
            "espesor_minimo": "-",
            "peligro_de_aludes": "-",
            "kilometros": "-",
            "pistas": {
                "totales": "-",
                "verdes": "-",
                "azules": "-",
                "rojas": "-",
                "negras": "-",
                "itinerarios": "-"
            }
        }

        try:
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Scrape each field, with logging for missing data
            estado_div = soup.select_one(".box_est_parteestado_estado")
            resort_data["estado"] = "Open" if estado_div and estado_div.text.strip() != "CERRADA" else "Closed"

            calidad_div = soup.select_one(".box_est_partedet_nieve")
            resort_data["calidad"] = calidad_div.text.strip() if calidad_div else "-"

            espesor_divs = soup.select(".box_est_partedet_datosnieve .box_est_partedet_dato")
            if len(espesor_divs) >= 2:
                resort_data["espesor_minimo"] = espesor_divs[0].text.strip().replace("cm", "") or "-"
                resort_data["espesor_maximo"] = espesor_divs[1].text.strip().replace("cm", "") or "-"

            peligro_div = soup.select_one(".box_est_partedet_aludes .box_est_partedet_aludesno")
            if peligro_div and peligro_div.text.strip() != "sin información":
                resort_data["peligro_de_aludes"] = peligro_div.text.strip()

            kilometros_div = soup.select_one(".box_est_partedet_datosgeneral > div:nth-of-type(3) .dato_circulo_leyenda")
            if kilometros_div:
                resort_data["kilometros"] = kilometros_div.text.strip().replace("/", "")

            pistas_div = soup.select(".box_est_partedet_datosgeneral .dato_circulo")
            if len(pistas_div) > 1:
                resort_data["pistas"]["totales"] = f"{pistas_div[1].select_one('.dato_circulo_dato').text.strip()} / {pistas_div[1].select_one('.dato_circulo_leyenda').text.strip()}"

            trail_breakdown_divs = soup.select(".box_est_partedet_datospistas .dato_circulo")
            trail_types = ["verdes", "azules", "rojas", "negras", "itinerarios"]
            for i, type_ in enumerate(trail_types):
                try:
                    resort_data["pistas"][type_] = f"{trail_breakdown_divs[i].select_one('.dato_circulo_dato').text.strip()} / {trail_breakdown_divs[i].select_one('.dato_circulo_leyenda').text.strip()}"
                except (IndexError, AttributeError):
                    resort_data["pistas"][type_] = "-"

        except requests.RequestException as e:
            print(f"Error fetching data for {self.resort_name}: {e}")

        return resort_data

    @staticmethod
    def scrape_resorts_names():
        """Scrape resort names from the Infonieve sitemap."""
        url = "https://infonieve.es/sitemap.xml"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error accessing sitemap: {e}")
            return []

        resorts = set()
        for line in response.text.splitlines():
            if "/estacion-esqui/" in line and line.count("/") == 5:
                resort_name = line.split("/")[4]
                resorts.add(resort_name)

        return list(resorts)