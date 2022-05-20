import requests
import csv

file = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQr_Pz7arcPoimNTbyAZ4cCXDUDAO5AjMwbGtZ4aA6YnmeukK7GBohWvhaxQW0FtixJSWtW_F2i32ty/pub?gid=373560562&single=true&output=csv';


def get_online_csv(url):
  """
  Cette fonction permet de récupérer le contenu d'un csv en ligne.
  Pour les google spreadsheets: fichier > publier sur le web > format csv > copier le lien
  """
  results = []
  with requests.Session() as s:
      download = s.get(url)
      decoded_content = download.content.decode('utf-8')
      reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
      for row in reader:
        results.append(row)
  return results

csv_content = get_online_csv(file)

partners = {}

for flow in csv_content:
  partner = flow['partner_clean']
  flow_type = flow['terre_mer']
  value = flow['value']
  if partner not in partners: 
    partners[partner] = {
      "terre": 0,
      "mer": 0
    }
  partners[partner][flow_type] += float(value)

output = []

for partner, values in partners.items():
  ratio = values["mer"] / (values["mer"] + values["terre"])
  output.append({
    "partner": partner,
    "ratio_terre_mer": ratio,
    "somme_mer": values["mer"],
    "somme_terre": values["terre"]
  })

with open("terre_mer.csv", "w") as f:
  writer = csv.DictWriter(f, fieldnames=["partner", "ratio_terre_mer", "somme_mer", "somme_terre"])
  writer.writeheader()
  for row in output:
    writer.writerow(row)
  f.close()