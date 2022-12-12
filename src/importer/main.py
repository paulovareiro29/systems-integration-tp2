import os
import time
import uuid

from utils.to_xml_converter import CSVtoXMLConverter

CSV_INPUT_PATH = "/csv"
XML_OUTPUT_PATH = "/shared/output"


def get_converted_files():
    #!TODO: you should retrieve from the database the files that were already converted before
    return []


def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']


def generate_unique_file_name():
    return f"/shared/output/{str(uuid.uuid4())}.xml"


def convert_csv_to_xml(in_path, out_path):
    converter = CSVtoXMLConverter(in_path)
    file = open(out_path, "w")
    file.write(converter.to_xml_str())


if __name__ == "__main__":
    converted_files = get_converted_files()

    while True:
        print("looking for new files...")
        csv_files = get_csv_files_in_input_folder()

        for csv_path in csv_files:

            # here we avoid converting the same file again
            if csv_path in converted_files:
                continue

            print(f"new file to convert: '{csv_path}'")

            # we generate an unique file name for the XML file
            xml_path = generate_unique_file_name()

            # we do the conversion
            convert_csv_to_xml(csv_path, xml_path)

            print(f"new xml file generated: '{xml_path}'")

            #!TODO: we store the XML into the imported_documents table

            #!FIXME: instead of updating the local cache for converted files, we should reload them from the database
            #!FIXME: in the next iteration
            converted_files.append(csv_path)

        # hold execution for 60 seconds
        time.sleep(60)
