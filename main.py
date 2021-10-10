import re
from pathlib import Path


class ChapterExtract:
    def __init__(self, starting_index: int, ending_index: int, chapter_name: str, num_of_hashtag: int):
        """
        The name of this class symbolizes an extracted layer from a chapter.
        :param starting_index: The starting index for extracting the chapter content
        :param ending_index: The ending index for extracting the chapter content
        :param chapter_name: The name of the chapter being extracted along with hashtags
        :param num_of_hashtag: Number of hashtags signifying which type of header
        """
        self.starting_index = starting_index
        self.ending_index = ending_index
        self.chapter_name = chapter_name
        self.num_of_hashtag = num_of_hashtag
        self.chapter_extract = None


class MdFileHeadingExtractor:
    def __init__(self):
        self._md_file_text = []
        self._chapter_details = []

    def _read_md(self, path: Path):
        try:
            with open(path) as file:
                self._md_file_text = file.readlines()
        except FileNotFoundError:
            print("File Not Found")
        return self

    def _slice_chapter(self):
        if len(self._chapter_details) != 0 and self._chapter_details[0].starting_index is not None:
            for chapter_item in self._chapter_details:
                chapter_slice_startpos = chapter_item.starting_index
                chapter_slice_endpos = chapter_item.ending_index
                sliced_chapter_content = self._md_file_text[chapter_slice_startpos:chapter_slice_endpos]
                chapter_item.chapter_extract = sliced_chapter_content
                # print(item.chapter_extract)
            return self

    # Finds index for chapters having neither or leading Hashtags
    def _find_chapter_name_and_index(self, chapter_name: str):

        if "#" not in chapter_name.split(" ")[0]:
            reg_ex_chapter_name_finder = rf"(#+? {chapter_name}\s+)"

        else:
            reg_ex_chapter_name_finder = rf"({chapter_name}\s+)"

        for index, line in enumerate(self._md_file_text):
            re_chapter_name_grabber = re.findall(reg_ex_chapter_name_finder, line, re.MULTILINE)
            if len(re_chapter_name_grabber) != 0:
                # print(f" re_chapter_name_grabber RESULT = {reg_ex_chapter_name_finder}")
                hash_tag_len = len(re_chapter_name_grabber[0].split(" ")[0])

                # Find the ending index till where we need to capture
                end_index = self._find_end_index_of_chapter([(index, re_chapter_name_grabber, hash_tag_len)])

                chapter_extract = ChapterExtract(index, end_index, re_chapter_name_grabber[0], hash_tag_len)
                self._chapter_details.append(chapter_extract)

        return self

    def _find_end_index_of_chapter(self, data_set: list):
        end_index = None
        if len(data_set) != 0:
            for index_md_file_text, _ in enumerate(self._md_file_text, start=data_set[0][0] + 1):
                if index_md_file_text < len(self._md_file_text) and "#" in \
                        self._md_file_text[index_md_file_text].split(" ")[0]:
                    split_hashtag_in_line = self._md_file_text[index_md_file_text].split(" ")[0]

                    # If same len of hashtag found, get that end index
                    if len(split_hashtag_in_line) == data_set[0][2]:
                        end_index = index_md_file_text
                        break
                    # If len of hashtag is less that source but greater than 1, get that index/
                    elif data_set[0][2] > len(split_hashtag_in_line) >= 1:
                        end_index = index_md_file_text
                        break
            return end_index
        else:
            print("Empty Data Set")

    def extract_chapter_from_file(self, chapter_name: str, file_name: Path):

        self._read_md(file_name)._find_chapter_name_and_index(chapter_name)._slice_chapter()

        return self._chapter_details


    # def find_chapter_name_and_content(self, chapter_name: str, file_name: Path):
    #     """
    #     :return: Returns a List of Chapter Objects that contains the chapter starting index, chapter name, ending
    #     index for the contents and the number of hashtags in the chapter name. This method is a standalone method
    #     and should be used to trace if a file contains a specific chapter and it's contents.
    #     """
    #
    #     self._find_chapter_name_and_index()


if __name__ == '__main__':
    file_extract = MdFileHeadingExtractor()
    result = file_extract.extract_chapter_from_file("#### Contributing", Path("test.md"))
    for item in result:
        print(item.__dict__)

