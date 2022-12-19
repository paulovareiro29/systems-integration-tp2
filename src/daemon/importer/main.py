import asyncio
import time
import uuid

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from utils.to_xml_converter import CSVtoXMLConverter
from utils.database import Database


def get_csv_files_in_directory(directory):
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames if
            os.path.splitext(f)[1] == '.csv']


def generate_unique_file_name(directory):
    return f"{directory}/{str(uuid.uuid4())}.xml"


def convert_csv_to_xml(in_path, out_path):
    converter = CSVtoXMLConverter(in_path)
    xml = converter.to_xml_str()
    file = open(out_path, "w")
    file.write(converter.to_xml_str())
    return xml


def insert_imported_doc(file_name, xml):
    db = Database()
    try:
        db.insert(
            "INSERT INTO imported_documents (file_name, xml) VALUES (%s,%s)", (file_name, xml))
    except Exception as error:
        print(error)
        raise error


def insert_converted_doc(src, dst, filesize):
    db = Database()
    try:
        db.insert(
            "INSERT INTO converted_documents(src, dst, file_size) VALUES (%s,%s,%s)", (src, dst, filesize))
    except Exception as error:
        print(error)
        raise error


class Watcher:
    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self._observer = Observer()
        self._handler = handler
        self._directory = directory

    def run(self):
        self._observer.schedule(self._handler, self._directory, recursive=True)
        self._observer.start()
        print(f"\nWatcher Running in {self._directory}/\n")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self._observer.stop()
            self._observer.join()

        print("\nWatcher terminated\n")


class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self._output_path = output_path
        self._input_path = input_path

    async def convert_csv(self, csv_path):
        # here we avoid converting the same file again
        if csv_path in await self.get_converted_files():
            return

        print(f"new file to convert: '{csv_path}'")

        # we generate an unique file name for the XML file
        xml_path = generate_unique_file_name(self._output_path)

        # we do the conversion
        xml = convert_csv_to_xml(csv_path, xml_path)

        try:
            # insert converted doc
            insert_converted_doc(src=csv_path,
                                 dst=xml_path,
                                 filesize=os.stat(xml_path).st_size)

            # insert imported doc
            insert_imported_doc(file_name=csv_path,
                                xml=xml)

            print(f"new xml file generated: '{xml_path}'")
        except:
            os.remove(xml_path)

    async def get_converted_files(self):
        list = []
        db = Database()
        for file in db.selectAll("SELECT src FROM converted_documents WHERE deleted_on IS NULL"):
            list.append(file[0])

        return list

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            asyncio.run(self.convert_csv(event.src_path))


if __name__ == "__main__":
    CSV_INPUT_PATH = "/csv"
    XML_OUTPUT_PATH = "/shared/output"

    handler = CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH)

    csv_files = get_csv_files_in_directory(CSV_INPUT_PATH)

    for csv_path in csv_files:
        asyncio.run(handler.convert_csv(csv_path))

    w = Watcher(CSV_INPUT_PATH, handler=handler)
    w.run()
