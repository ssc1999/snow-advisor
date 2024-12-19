import requests
from bs4 import BeautifulSoup

class InfonieveScraper:
    def __init__(self, resort_name):
        self.resort_name = resort_name
        self.base_url = f"https://infonieve.es/estacion-esqui/{resort_name}/parte-de-nieve/"
        
    def scrape_resort_data(self):
        """Scrape the snow report data for a specific resort from Infonieve."""
        resort_data = {
            "status": "Closed",
            "quality": "-",
            "maximum_thickness": "-",
            "minimum_thickness": "-",
            "avalanche_risk": "-",
            "kilometers": "-",
            "slopes": {
                "total": "-",
                "green": "-",
                "blue": "-",
                "red": "-",
                "black": "-",
                "itineraries": "-"
            }
        }

        try:
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Scrape each field, with logging for missing data
            estado_div = soup.select_one(".box_est_parteestado_estado")
            resort_data["status"] = "Open" if estado_div and estado_div.text.strip() != "CERRADA" else "Closed"

            calidad_div = soup.select_one(".box_est_partedet_nieve")
            resort_data["quality"] = calidad_div.text.strip() if calidad_div else "-"

            espesor_divs = soup.select(".box_est_partedet_datosnieve .box_est_partedet_dato")
            if len(espesor_divs) >= 2:
                resort_data["minimum_thickness"] = espesor_divs[0].text.strip().replace("cm", "") or "-"
                resort_data["maximum_thickness"] = espesor_divs[1].text.strip().replace("cm", "") or "-"

            peligro_div = soup.select_one(".box_est_partedet_aludes .box_est_partedet_aludesno")
            if peligro_div and peligro_div.text.strip() != "sin información":
                resort_data["avalanche_risk"] = peligro_div.text.strip()

            kilometros_div = soup.select_one(".box_est_partedet_datosgeneral > div:nth-of-type(3) .dato_circulo")
            if kilometros_div:
                dato = kilometros_div.select_one(".dato_circulo_dato")
                leyenda = kilometros_div.select_one(".dato_circulo_leyenda")
                
                dato_text = dato.text.strip() if dato and dato.text.strip() else "-"
                leyenda_text = leyenda.text.strip().lstrip("/") if leyenda and leyenda.text.strip() else "-"
                
                # Combine both parts into the desired format
                resort_data["kilometers"] = f"{dato_text}/{leyenda_text}"
    
            pistas_div = soup.select(".box_est_partedet_datosgeneral .dato_circulo")
            if len(pistas_div) > 1:
                # Safely extract text from dato_circulo_dato and dato_circulo_leyenda
                dato = pistas_div[1].select_one(".dato_circulo_dato")
                leyenda = pistas_div[1].select_one(".dato_circulo_leyenda")
                
                dato_text = dato.text.strip() if dato and dato.text.strip() else "-"
                leyenda_text = leyenda.text.strip().lstrip("/") if leyenda and leyenda.text.strip() else "-"
                
                # Combine into the desired format
                resort_data["slopes"]["total"] = f"{dato_text}/{leyenda_text}"

            # Extract individual piste types (verdes, azules, etc.)
            trail_breakdown_divs = soup.select(".box_est_partedet_datospistas .dato_circulo")
            trail_types = ["verdes", "azules", "rojas", "negras", "itinerarios"]
            
            # Mapping of Spanish trail types to English
            trail_type_translation = {
                "verdes": "green",
                "azules": "blue",
                "rojas": "red",
                "negras": "black",
                "itinerarios": "itineraries"
            }

            for i, type_ in enumerate(trail_types):
                try:
                    count = trail_breakdown_divs[i].select_one(".dato_circulo_dato")
                    total = trail_breakdown_divs[i].select_one(".dato_circulo_leyenda")
                    
                    count_text = count.text.strip() if count and count.text.strip() else "-"
                    total_text = total.text.strip().lstrip("/") if total and total.text.strip() else "-"
                    
                    resort_data["slopes"][trail_type_translation[type_]] = f"{count_text}/{total_text}"
                except (IndexError, AttributeError):
                    resort_data["slopes"][trail_type_translation[type_]] = "-"
                    
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