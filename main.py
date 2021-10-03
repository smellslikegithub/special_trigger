import re
from pathlib import Path


class MdFileHeadingExtractor:
    def __init__(self):
        self.legal_chapter_names = [
            "## Contributing", "## History", "## Configuration Management", "## Contributing"
        ]
        self._md_file_text = []
        self._extracted_chapter = []

    def read_md(self, path: Path):
        try:
            with open(path) as file:
                self._md_file_text = file.readlines()
        except FileNotFoundError:
            print("File Not Found")

    def print_md_file_content(self):
        print(self._md_file_text)

    # Finds index for chapters having neither or leading Hashtags
    def find_chapter_name_and_index_start(self, chapter_name: str):
        result = []

        if "#" not in chapter_name.split(" ")[0]:
            reg_ex_chapter_name_finder = rf"(#+? {chapter_name}\s+)"
        else:
            print("In Else")
            reg_ex_chapter_name_finder = rf"({chapter_name}\s+)"

        for index, line in enumerate(self._md_file_text):
            re_output = re.findall(reg_ex_chapter_name_finder, line, re.MULTILINE)
            if len(re_output) != 0:
                hash_tag_len = len(re_output[0].split(" ")[0])
                result.append((index, re_output, hash_tag_len))
        print(result)

        self.find_chapter_name_and_index_end(result)

    def find_chapter_name_and_index_end(self, data_set: list):
        print("===================================================")
        if len(data_set) != 0:
            print(data_set[0][0])
            for index_data_set, tuple_data in enumerate(data_set):
                print(tuple_data)
                for index_md_file_text, _ in enumerate(self._md_file_text, start=tuple_data[0] + 1):
                    # split_hashtag_in_line = re.findall(rf"#+? ", line, re.MULTILINE)
                    # print(f"Index = {index_md_file_text}, Line = {self._md_file_text[index_data_set]}")

                    if index_md_file_text < len(self._md_file_text) and "#" in self._md_file_text[index_md_file_text].split(" ")[0]:
                        split_hashtag_in_line = self._md_file_text[index_md_file_text].split(" ")[0]

                        # If same len of hashtag found, get that end index
                        if len(split_hashtag_in_line) == tuple_data[2]:
                            print(f"Found ending = {index_md_file_text} at line  = {self._md_file_text[index_md_file_text]}")
                            break
                        # If len of hashtag is less that source but greater than 1, get that index/
                        elif len(split_hashtag_in_line) < tuple_data[2] and len(split_hashtag_in_line) >= 1:
                            print(
                                f"Found ending = {index_md_file_text} at line  = {self._md_file_text[index_md_file_text]}")
                            break

        else:
            print("Empty Data Set")

    def extract_chapter_when_only_name_given(self, chapter_name: str):

        # We want to extract ## Contributing
        self.find_chapter_name_and_index_start(chapter_name)

    def extract_chapter_from_settings_file(self, chapter_name: str):

        # We want to extract ## Contributing
        self.find_chapter_name_and_index_start(chapter_name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_extract = MdFileHeadingExtractor()
    file_extract.read_md(Path("test.md"))
    # file_extract.print_md_file_content()
    file_extract.extract_chapter_when_only_name_given("#### Contributing")

    # l = ["a", "b", "c", "d"]
    #
    # for i, e in enumerate(l, start=2):
    #     if(i<len(l)):
    #         print (f"Index = {i}, element = {l[i]}")
