# 🦾 BYM412 - Ödev 2  
### **Kendi Robotunu İnşa Et (Diff Drive + Kamera + TF/URDF + Ball Chaser)**  
**Ders:** BYM412 Robotik (Güz Dönemi)  
**Üniversite:** İstanbul Sağlık ve Teknoloji Üniversitesi  
**Öğrenci:** Ali Üre  
**Numara:** 220609040  
**Dil:** 🐍 Python  
**Teslim Tarihi:** 27.10.2025  

---

## 🎯 **1. Projenin Amacı**
Bu projenin amacı, Gazebo Harmonic ortamında **ROS 2 Humble** kullanarak sıfırdan bir diferansiyel tahrikli mobil robot modeli oluşturmak,  
robota bir **kamera sensörü** eklemek, robotun **TF yapısını (URDF)** tanımlamak,  
ve kamera görüntüsündeki **beyaz küreyi (ball)** takip eden bir **Ball Chaser düğümü** geliştirmektir.

---

## ⚙️ **2. Sistem Bilgisi**

| Bileşen | Versiyon / Açıklama |
|----------|----------------------|
| İşletim Sistemi | Ubuntu 22.04.5 LTS |
| Kernel | 6.8.0-85-generic |
| ROS2 Dağıtımı | Humble Hawksbill |
| Gazebo | Harmonic (Gazebo Classic 11.10.2) |
| Python | 3.10 |
| Donanım | 8 GB RAM / Intel i5 İşlemci |

---

## 🤖 **3. Proje Yapısı**

```
robot_ws/
├── ball_chaser/
│   ├── package.xml
│   ├── setup.py
│   ├── ball_chaser/
│   │   ├── __init__.py
│   │   └── ball_chaser_node.py
│
├── my_robot_description/
│   └── urdf/
│       └── my_robot.urdf.xacro
│
├── my_robot_bringup/
│   └── launch/
│       └── bringup.launch.py
│
├── my_robot_control/
│   └── diff_drive_controller.yaml
│
├── worlds/
│   └── white_ball.sdf
│
└── SSF_HASH.txt
```

---

## 🔩 **4. Çalıştırma Adımları**

### 1️⃣ Workspace’i Derle
```bash
cd ~/robot_ws
colcon build --symlink-install
source install/setup.bash
```

### 2️⃣ Simülasyonu Başlat
```bash
ros2 launch my_robot_bringup bringup.launch.py
```
Bu adım **Gazebo**, **RViz**, **TF yapısı** ve **kamera sensörünü** aynı anda başlatır.

### 3️⃣ Nesneleri Spawn Et
```bash
ros2 run gazebo_ros spawn_entity.py -topic /robot_description -entity my_robot -x 0 -y 0 -z 0.05
ros2 run gazebo_ros spawn_entity.py -file ~/robot_ws/worlds/white_ball.sdf -entity white_ball -x 1.0 -y 0.0 -z 0.05
```

### 4️⃣ Kamerayı Aç
```bash
ros2 run rqt_image_view rqt_image_view
```

### 5️⃣ Robotu Manuel Hareket Ettir
```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.2}, angular: {z: 0.0}}" -r 10
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.0}}" -1
```

### 6️⃣ Ball Chaser Düğümünü Çalıştır
```bash
ros2 run ball_chaser ball_chaser_node
```
Bu düğüm, `/camera_sensor/image_raw` üzerinden beyaz topu algılayıp `/cmd_vel` çıktısı üretir.

---

## 🧠 **5. Ball Chaser Davranışı**
- Robot, topu algıladığında sürekli “🎯 Top görüldü: (x, y)” mesajı üretmektedir.  
- Mevcut versiyonda robot ileri yönde hareket etmektedir.  
- HSV renk aralığının iyileştirilmesiyle top takibi daha kararlı hale getirilebilir.  
- `ball_chaser_node.py` dosyası Python ile yazılmıştır.

---

## 🧭 **6. TF ve RViz Doğrulaması**
TF zinciri:  
```
world → odom → base_link → (left/right/caster)_link → camera_link
```
RViz ekranında hem robot modeli hem de `/camera/image_raw` görüntüsü başarıyla gösterilmektedir.  
TF yapısı `ros2 run tf2_tools view_frames` komutuyla **PDF olarak** kaydedilmiştir.

---

## 📸 **7. Görseller**
- Gazebo ortamında robot + top görüntüsü
  images/Ekran Görüntüsü - 2025-10-27 17-15-01.png
- RViz ekranı (model + TF + kamera görüntüsü)  
- Ball Chaser terminal logları  

*(Ekran görüntüleri rapor dosyasında bulunmaktadır.)*

---

## 🔗 **8. Bağlantılar**
**🎥 YouTube (Unlisted):** [https://youtu.be/_________](#)  
**💾 GitHub (Public):** [https://github.com/aliure/BYM412_BallChaser_Robot](#)

---

## 🧾 **9. Lisans ve Bilgilendirme**
Bu proje, **BYM412 Robotik Dersi - Ödev 2** kapsamında hazırlanmıştır.  
Kod ve modeller bireysel olarak geliştirilmiş, üçüncü taraf kaynak kullanılmamıştır.
