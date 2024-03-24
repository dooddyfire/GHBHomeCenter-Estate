1. ติดตั้ง library ที่ต้องใช้

pip install -r requirements.txt 

2. ไฟล์หลักในการรันมี 2 ไฟล์

- ไฟล์สำหรับรันแบบไม่ตั้งเวลา sam.py ( เอาไปตั้ง crontab ได้) 
- ไฟล์สำหรับรันแบบตั้งเวลาได้ timeapp.py 

3. วิธีการรัน ใช้คำสั่ง

python ชื่อไฟล์ที่จะรัน.py

- รันแบบไม่ตั้งเวลา 
python sam.py 

- รันไฟล์ตัวที่ตั้งเวลาได้ 
python timeapp.py
