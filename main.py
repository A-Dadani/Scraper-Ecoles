import requests
from bs4 import BeautifulSoup
import time
import random
import csv

def main():
    curr_classement = 0
    master_array = [["classement", "nom", "note", "spécialités", "nombre_eleves_bac", "nombre_eleves_cpge", "nombre_eleves_adm_paralleles", "nombre_entreprises_forum", "reputation_internationale", "salaire_a_sortie", "insertion_deux_mois", "dimplomés_en_postes_internationaux"]]
    for i in range(1, 10):
        URL = "https://www.letudiant.fr/classements/classement-des-ecoles-d-ingenieurs.html?page=" + str(i)
        print("\n\nRequesting from " + URL)
        page = requests.get(URL)
        sleep_time = 5 + random.random()
        print("Sleeping for " + str(sleep_time) + "...")
        time.sleep(sleep_time)
        soup = BeautifulSoup(page.content, "html.parser")
        ecole_row_elements = soup.find_all('tr', attrs={'data-toggle-group': 'laureate-details'})
        for ecole_row in ecole_row_elements:
            curr_classement += 1
            name_ecole = ecole_row.find_all('a')[0].text
            note_ecole = ecole_row.find_all('td')[2].text.strip()
            specialites_ecole = None
            nb_bac_ecole = None
            nb_cpge_ecole = None
            nb_admission_parallele = None
            nb_forums = None
            reputation_internationale_ecole = None
            salaire_ecole = None
            insertion_ecole = None
            diplomes_international_ecole = None
            
            ecole_URL = ecole_row.find_all('a')[0]['href']
            ecole_page = requests.get(ecole_URL)
            print("\nRequesting child", curr_classement, "from:", ecole_URL)
            sleep_time = 5 + random.random()
            print("Sleeping for " + str(sleep_time) + "...")
            time.sleep(sleep_time)
            ecole_soup = BeautifulSoup(ecole_page.content, "html.parser")

            criteria_elements = ecole_soup.find_all('div', class_='criterion-row')
            
            for criterion_element in criteria_elements:
                row_title = criterion_element.find('span').text.strip()
                row_content = criterion_element.find_all('div')[3].text.strip()
                match row_title:
                    case "Spécialités proposées":
                        specialites_ecole = row_content
                    case "Cycle prépa intégrée - Nombre d'intégrés à bac":
                        nb_bac_ecole = row_content
                    case "Cycle ingénieur - Nombre d'intégrés issus de CPGE":
                        nb_cpge_ecole = row_content
                    case "Cycle ingénieur - Nombre d'intégrés issus d'admissions parallèles":
                        nb_admission_parallele = row_content
                    case "Forums entreprises":
                        nb_forums = f"{criterion_element.find_all('div')[4].text.strip()} [{row_content}]"
                    case "Réputation internationale":
                        reputation_internationale_ecole = f"{criterion_element.find_all('div')[4].text.strip()} [{row_content}]"
                    case "Salaire à la sortie":
                        salaire_ecole = f"{criterion_element.find_all('div')[4].text.strip()} [{row_content}]"
                    case "Insertion à deux mois":
                        insertion_ecole = row_content
                    case "Diplômés en poste à l'international":
                        diplomes_international_ecole = f"{criterion_element.find_all('div')[4].text.strip()} [{row_content}]"
            master_array.append([str(curr_classement), name_ecole, note_ecole, specialites_ecole, nb_bac_ecole, nb_cpge_ecole, nb_admission_parallele, nb_forums, reputation_internationale_ecole, salaire_ecole, insertion_ecole, diplomes_international_ecole])
    with open('ecoles_detailed.csv', 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        # write arrays as rows to CSV file
        for row in master_array:
            writer.writerow(row)
    print("\nResults written to file ecoles_detailed.csv")

if __name__ == '__main__':
    main()