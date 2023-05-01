import re
import csv
import os


def papper_not_found(line):
    patron = r'"([^"]*)"'
    match = re.search(patron, line)
    if match:
        name = match.group(1)
        return name
    return None


def parse_line(line):
    line = line.strip()
    if line.startswith("Título:"):
        return ('titulo', line.split("Título: ")[1])
    elif line.startswith("Resumen:"):
        return ('resumen', line.split("Resumen: ")[1])
    elif line.startswith("Citas:"):
        return ('citas', line.split("Citas: ")[1])
    else:
        return None


def read_data_from_file(file_name):
    data = []
    with open(file_name, "r", encoding='utf-8') as file:
        registro = {}
        for line in file:
            parsed = parse_line(line)
            if parsed:
                key, value = parsed
                registro[key] = value
            elif parsed == None and "-" not in line:
                title_paper = papper_not_found(line)
                if title_paper:
                    data.append({
                        'titulo': title_paper,
                        'resumen': '-',
                        'citas': '-'
                    })
            elif registro:
                data.append(registro)
                registro = {}
        if registro:
            data.append(registro)
    return data


def write_csv(name, data):
    with open("csv/"+name+'.csv', mode='w', newline='', encoding='utf-8') as archivo_csv:
        # creamos el objeto writer
        writer = csv.writer(archivo_csv)

        # escribimos una fila de datos
        writer.writerow(['título', 'autor', 'citas', 'observación'])
        for reg in data:
            # escribimos otra fila de datos
            title = reg.get('titulo')
            summary = reg.get('resumen')
            nro_city = reg.get('citas')
            observation = '-'
            if summary != '-':
                summary = (summary.split('-'))[0]
                observation = 'no encontrado'
            writer.writerow([title, summary, nro_city, observation])


nombre_carpeta = "csv"
ruta_carpeta = os.path.join(os.getcwd(), nombre_carpeta)
if os.path.exists(ruta_carpeta):
    print("La carpeta existe")
else:
    os.mkdir(ruta_carpeta)

# Uso de las funciones
conferences_years = ['WER22', 'WER21', 'WER20', 'WER19', 'WER18', 'WER17', 'WER16', 'WER15', 'WER14', 'WER13', 'WER12',
                     'WER11', 'WER10', 'WER09', 'WER08', 'WER07', 'WER06', 'WER05', 'WER04', 'WER03', 'WER02', 'WER01', 'WER00', 'WER99', 'WER98']
for name in conferences_years:
    # name = 'WER22'
    data = read_data_from_file(name+".txt")
    write_csv(name, data)
