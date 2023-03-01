import argparse
import re


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to iBug 300-W data split XML file")
ap.add_argument("-t", "--output", required=True,
	help="path output data split XML file")
ap.add_argument('-f')
args = vars(ap.parse_args())

LANDMARKS = set(list(range(36, 48)))


PART = re.compile("part name='[0-9]+'")
#mở tệp đầu vào để đọc và viết ra tệp cần ghi
print("[INFO] parsing data split XML file...")
rows = open(args["input"]).read().strip().split("\n")
output = open(args["output"], "w")

# lặp qua file đầu vào
for row in rows:
	
	#kiểm tra tọa độ (x,y) có phải của mắt không
	parts = re.findall(PART, row)
	
	#nếu không có ghi dòng hiện tại
	if len(parts) == 0:
		output.write("{}\n".format(row))
	else:
		# chuyển tên của thuộc tính trên từng hàng
		attr = "name='"
		i = row.find(attr)
		j = row.find("'", i + len(attr) + 1)
		name = int(row[i + len(attr):j])
		
		#nếu tên tồn tại trong chỉ mục ghi nó ra file output
		if name in LANDMARKS:
			output.write("{}\n".format(row))
output.close()