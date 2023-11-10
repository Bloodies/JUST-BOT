from datetime import datetime

asd = "CALENDAR;" + ";".join(["IGNORE", str(datetime.now().year), str(datetime.now().month), str(datetime.now().day)])
print(asd)