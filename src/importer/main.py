import os
import time
import uuid

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from utils.to_xml_converter import CSVtoXMLConverter
from utils.database import Database

CSV_INPUT_PATH = "/csv"
XML_OUTPUT_PATH = "/shared/output"


def get_converted_files():
    list = []
    db = Database()
    for file in db.selectAll("SELECT src FROM converted_documents WHERE deleted_on IS NULL"):
        list.append(file[0])

    return list


def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']


def generate_unique_file_name():
    return f"{XML_OUTPUT_PATH}/{str(uuid.uuid4())}.xml"


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
        except:
            self._observer.stop()
        self._observer.join()

        print("\nWatcher terminated\n")


class CSVHandler(FileSystemEventHandler):
    def __init__(self):
        self._converted_files = get_converted_files()

    def convert_csv(self, csv_path):
        # here we avoid converting the same file again
        if csv_path in self._converted_files:
            return

        print(f"new file to convert: '{csv_path}'")

        # we generate an unique file name for the XML file
        xml_path = generate_unique_file_name()

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

        # append the file to memory
        self._converted_files.append(csv_path)

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            self.convert_csv(event.src_path)

    def on_any_event(self, event):
        print(event)


if __name__ == "__main__":
    handler = CSVHandler()

    csv_files = get_csv_files_in_input_folder()

    for csv_path in csv_files:
        handler.convert_csv(csv_path)

    w = Watcher(CSV_INPUT_PATH, CSVHandler())
    w.run()
