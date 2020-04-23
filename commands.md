Commands to get everything up and running

List all IPs on Mac
arp -a

Run rmate on laptop
ssh -R 52698:localhost:52698 pi@192.168.0.100

Open file from Pi on laptop
rmate ./<filename>

Run build_faces_dataset.py example run
python3 ./build_faces_dataset.py -n="Zaid" -o="./"

Run compute_face_encodings.py example run
python3 ./compute_face_encodings.py -o="./build"