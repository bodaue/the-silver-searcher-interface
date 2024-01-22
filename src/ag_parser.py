import re
from collections import defaultdict


class AgParser:
    def __init__(self, result_string):
        self.result_string: str = result_string

    def format_text(self, flag_c: bool = False) -> str:
        if flag_c:
            lines = sorted(self.result_string.split('\n'))
            text = '\n'.join(map(lambda x: x.lstrip(':'), lines))
            return text

        data_dict = self._parse()
        text = ''
        for filename in data_dict:
            text += filename + '\n'
            for match in data_dict[filename]:
                line_number, match_line = match
                text += f'{line_number}: {match_line}\n'

            text += '\n'
        return text

    def _parse(self) -> dict:
        lines = self.result_string.split('\n')
        lines = [line.strip() for line in lines if line.strip()]
        match_dict = defaultdict(list)
        name = ''
        for line in lines:
            if line.startswith(':'):
                name = line[1:]
            else:
                line_number, indexes, match_line = re.split(r'[:;]', line, maxsplit=2)
                match_dict[name].append((int(line_number), match_line.strip()))
        match_dict = dict(sorted(match_dict.items()))
        return match_dict
