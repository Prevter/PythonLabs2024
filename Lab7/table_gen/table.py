from typing import List

def find_max_len(data: List[List[str]]) -> List[int]:
    max_len = [0] * len(data[0])
    for row in data:
        for i in range(len(row)):
            l = len(str(row[i]))
            if l > max_len[i]:
                max_len[i] = l
    return max_len


def from_list(data: List[List[str]]) -> str:
    if len(data) == 0:
        return "Empty list"
    max_len = find_max_len(data)
    table = []
    
    # Header
    header = []
    for i in range(len(data[0])):
        header.append(str(data[0][i]).ljust(max_len[i]))
    table.append("  ".join(header))

    # Separator
    separator = []
    for i in range(len(data[0])):
        separator.append("-" * max_len[i])
    table.append("--".join(separator))

    # Data
    for i in range(1, len(data)):
        row = []
        for j in range(len(data[i])):
            row.append(str(data[i][j]).ljust(max_len[j]))
        table.append("  ".join(row))
    return "\n".join(table)