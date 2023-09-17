import httpx
import csv
import asyncio

def go_through_list(data_items: list) -> dict:
    for item in data_items:
        yield item

def read_structure() -> dict:
    url = 'http://5.159.103.105:4000/api/v1/structure'
    response = httpx.get(url)
    response_json = response.json()
    yield from go_through_list(response_json['items'])

def read_data():
    url = 'http://5.159.103.105:4000/api/v1/logs'
    page = 1
    print(f"Process page {page}...")
    response = httpx.get(url, params={"page": page})
    response_json = response.json()
    yield from go_through_list(response_json['items'])
    while response_json['items'] != []:
        if response.status_code != 200:
            continue
        page += 1
        print(f"Process page {page}...")
        response = httpx.get(url, params={"page": page})
        yield from go_through_list(response_json['items'])

async def write_csv_file(header, filename):
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file, delimiter="\t")
        await write_row(writer, header.keys())
        for data in read_data():
            row = []
            for field_header, field_type in header.items():
                if field_type == "numeric":
                    row.append(float(data[field_header]))
                else:
                    row.append(str(data[field_header]))

            await write_row(writer, row)

async def write_row(writer, row):
    writer.writerow(row)


def run():
    header = dict()
    for field in read_structure():
        header[field["field_name"]] = field["format"]

    filename = "customs_data.csv"
    asyncio.run(write_csv_file(header, filename))


if __name__ == "__main__":
    run()