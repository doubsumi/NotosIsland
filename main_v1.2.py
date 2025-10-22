import subprocess
import sys
import GPUtil
import psutil
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFileDialog)
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import (QPainter, QBrush, QColor, QPen, QPixmap,
                         QFont, QCursor, QPainterPath)


class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化配置
        self.expanded = False
        self.settings_open = False
        self.bg_image = None
        self.dragging = False
        self.drag_position = None
        self.bg_color = QColor(20, 20, 20, 160)  # 初始背景颜色

        # V1.2：记录原始位置和当前位置
        self.original_position = None  # 原始顶部居中位置
        self.current_position = None  # 当前窗口位置
        # V1.2：手动展开标记
        self.manual_expanded = False  # 标记是否通过双击手动展开

        # 设置窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(450, 50)

        # 创建UI
        self.init_ui()

        # 设置初始位置（屏幕顶部居中）
        self.center_on_top()

        # V1.2：记录初始位置
        self.original_position = self.pos()
        self.current_position = self.pos()

        # 创建定时器更新数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # 每秒更新一次

        # 初始化数据
        self.prev_net_io = psutil.net_io_counters()
        self.prev_disk_io = psutil.disk_io_counters()
        self.net_speed = "▼ 0B/s ▲ 0B/s "
        self.cpu_usage = "0%"
        self.gpu_usage = "0%"
        self.mem_usage = "0%"
        self.cpu_temp = "N/A"
        self.gpu_temp = "N/A"
        self.disk_speed = "0B/s R 0B/s W"

        # 尝试初始化WMI用于获取温度
        # self.ohm_available = False
        # try:
        #     self.w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        #     # 测试连接是否成功
        #     if len(self.w.Sensor()) > 0:
        #         self.ohm_available = True
        #         print("Open Hardware Monitor 已连接")
        #     else:
        #         print("警告: Open Hardware Monitor 未返回任何传感器数据")
        # except Exception as e:
        #     print(f"警告: 无法连接到Open Hardware Monitor: {str(e)}")
        #     print("温度监控功能不可用，请安装Open Hardware Monitor")
        #     self.w = None

        self.update_data()

    def center_on_top(self):
        """将窗口定位在屏幕顶部居中"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        self.move(x, 10)  # 距离顶部10像素
        # 更新位置记录
        self.original_position = self.pos()
        self.current_position = self.pos()

    # 简约现代风格的按钮样式
    button_style_modern = """
        QPushButton {
            background-color: rgba(45, 55, 72, 0.9);
            color: white;
            border: 1px solid rgba(74, 85, 104, 0.8);
            border-radius: 16px;  /* 减小圆角 */
            font-size: 14px;      /* 减小字体 */
            letter-spacing: 0.3px;
            min-height: 30px;     /* 减小最小高度 */
            min-width: 86px;      /* 减小最小宽度 */
        }
        QPushButton:hover {
            background-color: rgba(56, 66, 83, 0.95);
            border: 1px solid rgba(100, 130, 240, 0.8);
        }
        QPushButton:pressed {
            background-color: rgba(35, 45, 62, 0.9);
        }
    """

    def create_buttons(self):
        """创建所有按钮并添加到布局"""
        # 更换背景按钮
        self.bg_btn = QPushButton("更换背景")

        self.bg_btn.setStyleSheet(self.button_style_modern)
        self.bg_btn.clicked.connect(self.change_background)
        self.bg_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # 清除背景按钮
        self.clear_bg_btn = QPushButton("清除背景")

        self.clear_bg_btn.setStyleSheet(self.button_style_modern.replace("45, 55, 72", "65, 45, 102"))
        self.clear_bg_btn.clicked.connect(self.clear_background)
        self.clear_bg_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # 关闭程序按钮
        self.close_btn = QPushButton("关闭程序")

        self.close_btn.setStyleSheet(self.button_style_modern.replace("45, 55, 72", "102, 45, 45"))
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # 将按钮添加到布局
        self.row3.addWidget(self.bg_btn)
        self.row3.addWidget(self.clear_bg_btn)
        self.row3.addWidget(self.close_btn)

    def init_ui(self):
        """初始化UI组件"""
        # 主布局
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 第一行 - 主要指标
        self.row1 = QHBoxLayout()
        self.row1.setSpacing(10)
        self.row1.setContentsMargins(15, 5, 15, 5)  # V1.2：左右边距15px，上下边距5px

        self.net_label = self.create_label("0B/s")
        self.cpu_label = self.create_label("CPU: 0%")
        self.gpu_label = self.create_label("GPU: 0%")
        self.mem_label = self.create_label("RAM: 0%")

        self.row1.addWidget(self.net_label)
        self.row1.addWidget(self.cpu_label)
        self.row1.addWidget(self.gpu_label)
        self.row1.addWidget(self.mem_label)

        # 第二行 - 扩展信息
        self.row2 = QHBoxLayout()
        self.row2.setSpacing(10)
        self.row2.setContentsMargins(25, 5, 15, 5)  # V1.2：左右边距15px，上下边距5px

        self.cpu_temp_label = self.create_label("CPU: N/A")
        self.gpu_temp_label = self.create_label("GPU: N/A")
        self.disk_label = self.create_label(": 0B/s")

        # 添加弹性空间使内容居中
        self.row2.addWidget(self.disk_label)
        self.row2.addWidget(self.cpu_temp_label)
        self.row2.addWidget(self.gpu_temp_label)

        # 第三行 - 设置面板
        self.row3 = QHBoxLayout()
        self.row3.setSpacing(50)  # 按钮间距增加到50px
        self.row3.setAlignment(Qt.AlignCenter)  # 按钮居中对齐

        # 先创建所有按钮，然后再添加到布局
        self.create_buttons()

        # 创建可隐藏部件
        self.row1_widget = QWidget()
        self.row1_widget.setLayout(self.row1)

        self.row2_widget = QWidget()
        self.row2_widget.setLayout(self.row2)
        self.row2_widget.hide()

        self.row3_widget = QWidget()
        self.row3_widget.setLayout(self.row3)
        self.row3_widget.hide()

        # 添加到主布局
        self.main_layout.addWidget(self.row1_widget)
        self.main_layout.addWidget(self.row2_widget)
        self.main_layout.addWidget(self.row3_widget)

        # 设置主布局
        self.setLayout(self.main_layout)

        # 设置样式
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
            QLabel {
                color: white;
                font-family: Arial;
                font-size: 13px;
            }
        """)

    def create_label(self, text, font_size=10, min_width=70):
        """创建样式化的标签"""
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setMinimumWidth(min_width)
        font = QFont("Arial", font_size)
        label.setFont(font)
        return label

    def update_data(self):
        """更新所有监控数据"""
        # 更新网速
        self.update_network_speed()

        # 更新CPU使用率
        self.cpu_usage = f"{psutil.cpu_percent()}%"
        self.cpu_label.setText(f"CPU: {self.cpu_usage}")

        # 更新内存使用率
        mem = psutil.virtual_memory()
        self.mem_usage = f"{mem.percent}%"
        self.mem_label.setText(f"RAM: {self.mem_usage}")

        # 更新GPU使用率
        self.update_gpu_usage()

        # 更新温度
        self.update_temperatures()

        # 更新磁盘速度
        self.update_disk_speed()

    def update_network_speed(self):
        """计算并更新网络速度"""
        try:
            current_net_io = psutil.net_io_counters()
            bytes_sent = current_net_io.bytes_sent - self.prev_net_io.bytes_sent
            bytes_recv = current_net_io.bytes_recv - self.prev_net_io.bytes_recv

            # 转换为合适的单位
            sent_speed = self.format_speed(bytes_sent)
            recv_speed = self.format_speed(bytes_recv)

            self.net_speed = f"▼{recv_speed}/s ▲{sent_speed}/s"
            self.net_label.setText(f"{self.net_speed}")

            self.prev_net_io = current_net_io
        except Exception as e:
            # print(f"更新网络速度时出错: {str(e)}")
            pass

    def update_gpu_usage(self):
        """使用隐藏窗口的方式获取GPU使用率"""
        try:
            # 首先尝试使用 nvidia-smi 隐藏窗口获取
            try:
                result = subprocess.run([
                    'nvidia-smi',
                    '--query-gpu=utilization.gpu',
                    '--format=csv,noheader,nounits'
                ], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

                if result.returncode == 0 and result.stdout.strip():
                    usage_values = result.stdout.strip().split('\n')
                    if usage_values:
                        # 取第一个GPU的使用率或计算平均值
                        if len(usage_values) == 1:
                            usage = float(usage_values[0].strip())
                        else:
                            usage = sum(float(u.strip()) for u in usage_values if u.strip()) / len(usage_values)

                        self.gpu_usage = f"{usage:.0f}%"
                        self.gpu_label.setText(f"GPU: {self.gpu_usage}")
                        return
            except (subprocess.SubprocessError, FileNotFoundError, ValueError):
                # 如果 nvidia-smi 失败，回退到 GPUtil
                pass

            # 回退到 GPUtil 获取
            gpus = GPUtil.getGPUs()
            if gpus:
                if len(gpus) == 1:
                    # 单个GPU
                    gpu = gpus[0]
                    self.gpu_usage = f"{gpu.load * 100:.0f}%"
                else:
                    # 多个GPU，显示平均使用率
                    total_usage = sum(gpu.load for gpu in gpus)
                    avg_usage = total_usage / len(gpus)
                    self.gpu_usage = f"{avg_usage * 100:.0f}%"
            else:
                self.gpu_usage = "N/A"

        except Exception as e:
            # print(f"获取GPU使用率时出错: {str(e)}")
            self.gpu_usage = "Err"
        self.gpu_label.setText(f"GPU: {self.gpu_usage}")

    def update_temperatures(self):
        """使用隐藏窗口的方式获取GPU温度"""
        try:
            # 使用 nvidia-smi 隐藏窗口获取温度
            try:
                result = subprocess.run([
                    'nvidia-smi',
                    '--query-gpu=temperature.gpu',
                    '--format=csv,noheader,nounits'
                ], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

                if result.returncode == 0 and result.stdout.strip():
                    temp_values = result.stdout.strip().split('\n')
                    if temp_values and temp_values[0].strip():
                        if len(temp_values) == 1:
                            temp = float(temp_values[0].strip())
                        else:
                            temp = sum(float(t.strip()) for t in temp_values if t.strip()) / len(temp_values)

                        self.gpu_temp = f"{temp:.0f}°C"
                        self.gpu_temp_label.setText(f"GPU: {self.gpu_temp}")
                        return
            except (subprocess.SubprocessError, FileNotFoundError, ValueError):
                # 如果 nvidia-smi 失败，回退到 GPUtil
                pass

            # 回退到 GPUtil 获取温度
            gpus = GPUtil.getGPUs()
            if gpus:
                if len(gpus) == 1:
                    # 单个GPU
                    gpu = gpus[0]
                    if hasattr(gpu, 'temperature') and gpu.temperature is not None:
                        self.gpu_temp = f"{gpu.temperature:.0f}°C"
                    else:
                        self.gpu_temp = "N/A"
                else:
                    # 多个GPU，显示平均温度
                    valid_temps = [gpu.temperature for gpu in gpus
                                   if hasattr(gpu, 'temperature') and gpu.temperature is not None]
                    if valid_temps:
                        avg_temp = sum(valid_temps) / len(valid_temps)
                        self.gpu_temp = f"{avg_temp:.0f}°C"
                    else:
                        self.gpu_temp = "N/A"
            else:
                self.gpu_temp = "N/A"

        except Exception as e:
            # print(f"获取GPU温度时出错: {str(e)}")
            self.gpu_temp = "Err"
        self.gpu_temp_label.setText(f"GPU: {self.gpu_temp}")

    def update_disk_speed(self):
        """计算并更新磁盘读写速度"""
        try:
            current_disk_io = psutil.disk_io_counters()

            # 计算读写字节差值
            read_bytes = current_disk_io.read_bytes - self.prev_disk_io.read_bytes
            write_bytes = current_disk_io.write_bytes - self.prev_disk_io.write_bytes

            # 格式化速度
            read_speed = self.format_speed(read_bytes)
            write_speed = self.format_speed(write_bytes)

            self.disk_speed = f"R {read_speed}/s W {write_speed}/s"
            self.disk_label.setText(f"DSK: R {read_speed}/s W {write_speed}/s")

            # 更新前值
            self.prev_disk_io = current_disk_io
        except Exception as e:
            # print(f"更新磁盘速度时出错: {str(e)}")
            pass

    def format_speed(self, bytes):
        """格式化速度显示"""
        if bytes < 1024:
            return f"{bytes}B"
        elif bytes < 1024 * 1024:
            return f"{bytes / 1024:.1f}KB"
        elif bytes < 1024 * 1024 * 1024:
            return f"{bytes / (1024 * 1024):.1f}MB"
        else:
            return f"{bytes / (1024 * 1024 * 1024):.1f}GB"

    def update_display(self):
        """根据状态更新UI显示"""
        # 鼠标移出时强制关闭设置面板
        if not self.expanded:
            self.settings_open = False

        if self.settings_open and self.expanded:
            self.row3_widget.show()
        else:
            self.row3_widget.hide()

        # 第二行显示取决于是否展开
        if self.expanded:
            self.row2_widget.show()
        else:
            self.row2_widget.hide()

        # 调整窗口大小
        self.adjust_size()

    def adjust_size(self):
        """根据状态调整窗口大小"""
        base_width = 450
        if self.settings_open:
            # 三行显示
            self.setFixedSize(base_width, 150)
        elif self.expanded:
            # 两行显示
            self.setFixedSize(base_width, 100)
        else:
            # 只显示第一行
            self.setFixedSize(base_width, 50)

        # 重新居中（只有在原始位置时才居中）
        if self.current_position == self.original_position:
            self.center_on_top()
        else:
            # 如果用户拖动过窗口，保持当前位置，只更新大小
            self.move(self.current_position)

        # 更新背景（如果有）
        if hasattr(self, 'bg_image') and self.bg_image:
            # 重新缩放背景
            self.bg_image = QPixmap(self.bg_image).scaled(
                self.size(),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            )
        self.update()

    def change_background(self):
        """更换背景图片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择背景图片", "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_path:
            # 加载图片并调整大小
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.bg_image = pixmap.scaled(
                    self.size(),
                    Qt.IgnoreAspectRatio,
                    Qt.SmoothTransformation
                )
                # 重置图片透明度为默认值
                self.image_alpha = 230
                # 重置背景颜色设置
                if hasattr(self, 'bg_color'):
                    self.bg_color = QColor(20, 20, 20, 230)
                self.update()

    def clear_background(self):
        """清除背景图片，恢复颜色背景"""
        self.bg_image = None
        # 重置背景颜色为默认值
        self.bg_color = QColor(20, 20, 20, 230)
        self.update()

    def close(self):
        """重写close函数"""
        sys.exit(0)

    def enterEvent(self, event):
        """鼠标进入事件 - 展开窗口"""
        if not self.expanded:
            self.expanded = True
            self.update_display()

    def leaveEvent(self, event):
        """鼠标离开事件 - 只有在非手动展开状态时才收起窗口"""
        # 只有在不是手动展开状态时，鼠标离开才收起窗口
        if not self.manual_expanded:
            self.expanded = False
            self.settings_open = False  # 设置面板也关闭
            self.update_display()

    def mousePressEvent(self, event):
        """鼠标按下事件 - 开始拖动"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """鼠标移动事件 - 处理拖动"""
        if self.dragging and event.buttons() == Qt.LeftButton:
            new_position = event.globalPos() - self.drag_position
            self.move(new_position)
            # V1.2：更新当前位置记录
            self.current_position = new_position
            event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件 - 停止拖动"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            # V1.2：更新当前位置记录
            self.current_position = self.pos()

    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件 - 恢复原始位置或完全切换展开状态"""
        if event.button() == Qt.LeftButton:
            try:
                # 如果当前不在原始位置，则恢复原始位置
                if self.current_position != self.original_position:
                    self.move(self.original_position)
                    self.current_position = self.original_position
                    self.animate_move(self.original_position)
                else:
                    # 如果已经在原始位置，在完全收起和完全展开之间切换
                    if not self.expanded or not self.settings_open:
                        # 切换到完全展开状态（三行）
                        self.expanded = True
                        self.settings_open = True
                        # V1.2：标记为手动展开状态，鼠标移出不自动收起
                        self.manual_expanded = True
                    else:
                        # 切换到完全收起状态（一行）
                        self.expanded = False
                        self.settings_open = False
                        self.manual_expanded = False

                    self.update_display()

                event.accept()
            except Exception as e:
                # print(f"双击事件处理出错: {str(e)}")
                pass

    def animate_move(self, target_position):
        """QPropertyAnimation移动到目标位置"""
        try:
            from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

            animation = QPropertyAnimation(self, b"pos")
            animation.setDuration(300)  # 300毫秒动画
            animation.setStartValue(self.pos())
            animation.setEndValue(target_position)
            animation.setEasingCurve(QEasingCurve.OutCubic)  # 缓动曲线
            animation.start()

        except ImportError:
            # 如果动画不可用，直接移动
            self.move(target_position)
        except Exception as e:
            # print(f"动画移动失败: {str(e)}")
            self.move(target_position)

    def adjust_image_alpha(self, delta):
        """调节背景图片的透明度"""
        try:
            # 初始化或获取当前的图片透明度
            if not hasattr(self, 'image_alpha'):
                self.image_alpha = 230  # 默认透明度（0-255）

            # 根据滚轮方向调整透明度
            if delta > 0:
                # 向上滚动 - 增加透明度（变得更不透明）
                self.image_alpha = min(self.image_alpha + 15, 255)
            else:
                # 向下滚动 - 减少透明度（变得更透明）
                self.image_alpha = max(self.image_alpha - 15, 30)  # 最小透明度为30

        except Exception as e:
            # print(f"调节图片透明度时出错: {str(e)}")
            pass

    def adjust_color_alpha(self, delta):
        """调节背景颜色的透明度"""
        try:
            # 初始化或获取当前的背景颜色
            if not hasattr(self, 'bg_color'):
                # 初始背景颜色（深灰色，透明度230）
                self.bg_color = QColor(20, 20, 20, 230)

            # 根据滚轮方向调整透明度
            if delta > 0:
                # 向上滚动 - 增加透明度（变得更不透明）
                new_alpha = min(self.bg_color.alpha() + 15, 255)
            else:
                # 向下滚动 - 减少透明度（变得更透明）
                new_alpha = max(self.bg_color.alpha() - 15, 0)  # 允许全透明

            # 更新背景颜色
            self.bg_color.setAlpha(new_alpha)

        except Exception as e:
            # print(f"调节颜色透明度时出错: {str(e)}")
            pass

    def wheelEvent(self, event):
        """鼠标滚轮事件 - 改变背景透明度（支持颜色背景和图片背景）"""
        try:
            # 获取当前角度增量（滚轮滚动量）
            delta = event.angleDelta().y()

            # 根据是否有背景图片选择不同的透明度调节方式
            if hasattr(self, 'bg_image') and self.bg_image and not self.bg_image.isNull():
                # 有背景图片时，调节图片透明度
                self.adjust_image_alpha(delta)
            else:
                # 无背景图片时，调节颜色透明度
                self.adjust_color_alpha(delta)

            # 重绘窗口
            self.update()

            # 接受事件，防止事件继续传播
            event.accept()

        except Exception as e:
            # print(f"处理滚轮事件时出错: {str(e)}")
            pass

    def paintEvent(self, event):
        """绘制窗口背景和边框 - 使用圆角裁剪"""
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            radius = min(self.height() // 2, 25)

            # 创建圆角矩形路径
            path = QPainterPath()
            rect = QRectF(0, 0, self.width(), self.height())
            path.addRoundedRect(rect, radius, radius)

            # 设置裁剪区域
            painter.setClipPath(path)

            # 绘制背景
            if hasattr(self, 'bg_image') and self.bg_image and not self.bg_image.isNull():
                # 绘制背景图片并应用透明度
                painter.setOpacity(getattr(self, 'image_alpha', 230) / 255.0)
                painter.drawPixmap(0, 0, self.bg_image)
                painter.setOpacity(1.0)  # 恢复不透明度
            else:
                # 使用可调节的背景颜色
                if hasattr(self, 'bg_color'):
                    # 使用滚轮调节的颜色
                    painter.setBrush(QBrush(self.bg_color))
                else:
                    # 默认黑色半透明背景
                    painter.setBrush(QBrush(QColor(20, 20, 20, 230)))
                painter.drawRect(self.rect())

            # 绘制边框
            painter.setPen(QPen(QColor(80, 80, 80), 1))
            border_rect = QRectF(self.rect().adjusted(0, 0, -1, -1))
            painter.drawRoundedRect(border_rect, radius, radius)
        except Exception as e:
            # print(f"绘制错误: {str(e)}")
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 不再检查是否已经有实例在运行，允许运行多个程序
    window_title = "NotosIsland"
    monitor = SystemMonitor()
    monitor.setWindowTitle(window_title)
    monitor.show()
    sys.exit(app.exec_())
