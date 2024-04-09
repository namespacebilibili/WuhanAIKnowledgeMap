import csv
import json


def read_company_list(file_path):
    company_list = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            company_list.add(row[0])
    return company_list

def filter_csv_files(csv_files, company_list_file, output_file):
    company_list = read_company_list(company_list_file)
    gathered_lines = []

    for csv_file in csv_files:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('主申请人名称') in company_list:
                    filtered_row = {
                        "主申请人名称": row.get("主申请人名称"),
                        "专利号": row.get("专利号"),
                        "专利名称": row.get("专利名称"),
                        "其他申请人名称": row.get("其他申请人名称")
                    }
                    gathered_lines.append(filtered_row)
    gathered_lines.sort(key=lambda x: x["主申请人名称"])

    # Write gathered lines to output file
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ["主申请人名称", "专利号", "专利名称", "其他申请人名称"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(gathered_lines)

def extract_patent():
    csv_files = ["发明专利2015年.csv", "发明专利2016年.csv", "发明专利2017年.csv", "发明专利2018年.csv", "发明专利2019年.csv", "发明专利2020年.csv"]
    company_list_file = "武汉市AI相关企业.csv"
    output_file = "patent_results.csv"
    filter_csv_files(csv_files, company_list_file, output_file)

def generate_patent_json():
    with open("武汉市AI相关企业专利.csv", 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        json_data = []
        for row in csv_reader:
            row_dict = {}
            row = row[0].split(',')
            row_dict['name'] = row[2]
            row_dict['company'] = row[0]
            if row[3] != 'NA':
                row_dict['collaborator'] = row[3]
            json_data.append(row_dict)
            print(row_dict)
        
    with open("patent_nodes.json", 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

def count_patents():
    counts = {}
    with open('武汉市AI相关企业专利.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            company_name = row['主申请人名称']
            counts[company_name] = counts.get(company_name, 0) + 1
    json_data = []
    for company, count in counts.items():
        level = ""
        if count < 10:
            level = "潜力型"
        elif count >= 10 and count < 50:
            level = "优势型"
        elif count >= 50 and count < 100:
            level = "领先型"
        elif count > 100:
            level = "巅峰型"
        json_data.append({"company": company, "patent_numbers": count, "innovation level": level})
    with open('patent_numbers.json', 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

def collaborators():
    collaborator = []
    with open('武汉市AI相关企业专利.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['其他申请人名称'] != 'NA':
                new_dict = {'name': row['其他申请人名称']}
                if new_dict not in collaborator:
                    collaborator.append(new_dict)
    with open('collaborator_nodes.json', 'w', encoding='utf-8') as file:
        json.dump(collaborator, file, ensure_ascii=False, indent=4)

def create_evaluation():
    levels = [{"name": "潜力型"}, {"name": "优势型"}, {"name": "领先型"}, {"name": "巅峰型"}]
    with open('innovation_level_nodes.json', 'w', encoding='utf-8') as file:
        json.dump(levels, file, ensure_ascii=False, indent=4)

def evaluate():
    with open('patent_numbers.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    innovation_counts = {}
    for item in data:
        innovation_level = item['innovation level']
        innovation_counts[innovation_level] = innovation_counts.get(innovation_level, 0) + 1
    print(innovation_counts)
