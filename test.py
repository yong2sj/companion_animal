import re

print("hello world")
matches = ["익명", "집사"]
keyword = "익명의 집사"
if any(re.findall(r"|".join(matches), keyword, re.IGNORECASE)):
    print("True")
