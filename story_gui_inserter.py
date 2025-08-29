#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
故事可视化插入工具 - Story Visual Insertion Tool
基于tkinter的图形界面工具，用于批量插入故事到数据库
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pymysql
import os
import shutil
from datetime import datetime
from PIL import Image, ImageTk
from config import Config
from create_demo_user import get_demo_user_id

class StoryInserterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI故事平台 - 批量故事插入工具")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # 变量
        self.selected_image_path = tk.StringVar()
        self.story_count = 0
        self.demo_user_id = None
        
        # 初始化admin用户
        self.init_admin_user()
        
        # 创建界面
        self.create_widgets()
        
    def init_admin_user(self):
        """初始化admin用户"""
        try:
            self.demo_user_id = get_demo_user_id()
            if not self.demo_user_id:
                messagebox.showerror("错误", "无法创建或获取admin用户！")
                self.root.quit()
        except Exception as e:
            messagebox.showerror("错误", f"初始化admin用户失败: {e}")
            self.root.quit()
    
    def create_widgets(self):
        """创建GUI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="🌟 AI故事平台 - 故事插入工具", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 故事计数
        self.count_label = ttk.Label(main_frame, text=f"已插入故事数量: {self.story_count}", 
                                    font=("Arial", 10))
        self.count_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        # 故事标题
        ttk.Label(main_frame, text="故事标题 (Title):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(main_frame, width=50)
        self.title_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 故事简介
        ttk.Label(main_frame, text="故事简介 (Description):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.description_entry = ttk.Entry(main_frame, width=50)
        self.description_entry.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 故事内容
        ttk.Label(main_frame, text="故事内容 (Content):").grid(row=4, column=0, sticky=(tk.W, tk.N), pady=5)
        self.content_text = scrolledtext.ScrolledText(main_frame, width=50, height=10, wrap=tk.WORD)
        self.content_text.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 图片选择
        ttk.Label(main_frame, text="封面图片:").grid(row=5, column=0, sticky=tk.W, pady=5)
        
        image_frame = ttk.Frame(main_frame)
        image_frame.grid(row=5, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.select_image_btn = ttk.Button(image_frame, text="选择图片", command=self.select_image)
        self.select_image_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.image_label = ttk.Label(image_frame, text="未选择图片")
        self.image_label.grid(row=0, column=1, sticky=tk.W)
        
        # 图片预览
        self.image_preview = ttk.Label(main_frame, text="图片预览")
        self.image_preview.grid(row=6, column=1, columnspan=2, pady=10)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=20)
        
        # 插入按钮
        self.insert_btn = ttk.Button(button_frame, text="✅ 插入故事", 
                                   command=self.insert_story, style="Accent.TButton")
        self.insert_btn.grid(row=0, column=0, padx=10)
        
        # 清空按钮
        self.clear_btn = ttk.Button(button_frame, text="🗑️ 清空表单", 
                                  command=self.clear_form)
        self.clear_btn.grid(row=0, column=1, padx=10)
        
        # 批量插入按钮
        self.batch_btn = ttk.Button(button_frame, text="📁 批量插入示例", 
                                  command=self.batch_insert)
        self.batch_btn.grid(row=0, column=2, padx=10)
        
        # 状态栏
        self.status_label = ttk.Label(main_frame, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 配置grid权重
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def select_image(self):
        """选择图片文件"""
        filetypes = [
            ('图片文件', '*.jpg *.jpeg *.png *.webp'),
            ('所有文件', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title="选择封面图片",
            filetypes=filetypes
        )
        
        if filename:
            self.selected_image_path.set(filename)
            self.image_label.config(text=os.path.basename(filename))
            self.show_image_preview(filename)
            self.update_status(f"已选择图片: {os.path.basename(filename)}")
    
    def show_image_preview(self, image_path):
        """显示图片预览"""
        try:
            # 打开并调整图片大小
            image = Image.open(image_path)
            image.thumbnail((200, 150), Image.Resampling.LANCZOS)
            
            # 转换为tkinter可用格式
            photo = ImageTk.PhotoImage(image)
            
            # 更新预览标签
            self.image_preview.config(image=photo, text="")
            self.image_preview.image = photo  # 保持引用
            
        except Exception as e:
            self.image_preview.config(image="", text=f"预览失败: {str(e)}")
    
    def calculate_reading_time(self, content):
        """计算阅读时间"""
        word_count = len(content.split())
        reading_time = max(1, round(word_count / 250))  # 英文250词/分钟
        return reading_time, len(content)
    
    def copy_image_to_uploads(self, image_path, story_id):
        """复制图片到uploads目录"""
        if not image_path or not os.path.exists(image_path):
            return None, None
        
        try:
            # 获取文件扩展名
            file_ext = os.path.splitext(image_path)[1]
            new_filename = f"admin_story_{story_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_ext}"
            
            # uploads目录路径
            script_dir = os.path.dirname(os.path.abspath(__file__))
            uploads_dir = os.path.join(script_dir, 'static', 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            
            dest_path = os.path.join(uploads_dir, new_filename)
            
            # 复制文件
            shutil.copy2(image_path, dest_path)
            
            return f"/static/uploads/{new_filename}", os.path.basename(image_path)
            
        except Exception as e:
            self.update_status(f"图片复制失败: {e}")
            return None, None
    
    def insert_story(self):
        """插入单个故事"""
        # 验证输入
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        
        if not title:
            messagebox.showerror("错误", "请输入故事标题！")
            return
        
        if not content:
            messagebox.showerror("错误", "请输入故事内容！")
            return
        
        try:
            self.update_status("正在插入故事...")
            
            # 连接数据库
            connection = pymysql.connect(**Config.DB_CONFIG)
            cursor = connection.cursor()
            
            # 计算阅读时间和字数
            reading_time, word_count = self.calculate_reading_time(content)
            
            # 插入故事
            story_query = """
                INSERT INTO stories (user_id, title, content, language, language_name, description, 
                                   image_path, image_original_name, reading_time, word_count, status, published_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            published_at = datetime.now()
            
            cursor.execute(story_query, (
                self.demo_user_id,
                title,
                content,
                'en-US',  # 固定为英文
                'English',
                description,
                None,  # 先插入，后更新图片
                None,
                reading_time,
                word_count,
                'published',
                published_at
            ))
            
            story_id = cursor.lastrowid
            
            # 处理图片
            if self.selected_image_path.get():
                image_path, original_name = self.copy_image_to_uploads(
                    self.selected_image_path.get(), story_id)
                if image_path:
                    cursor.execute("""
                        UPDATE stories 
                        SET image_path = %s, image_original_name = %s 
                        WHERE id = %s
                    """, (image_path, original_name, story_id))
            
            connection.commit()
            connection.close()
            
            # 更新计数
            self.story_count += 1
            self.count_label.config(text=f"已插入故事数量: {self.story_count}")
            
            self.update_status(f"✅ 故事插入成功！ID: {story_id}")
            messagebox.showinfo("成功", f"故事 '{title}' 插入成功！\nID: {story_id}")
            
            # 清空表单
            self.clear_form()
            
        except Exception as e:
            self.update_status(f"❌ 插入失败: {e}")
            messagebox.showerror("错误", f"插入故事失败: {e}")
    
    def batch_insert(self):
        """批量插入示例故事"""
        sample_stories = [
            {
                'title': 'The Enchanted Forest Adventure',
                'content': 'Once upon a time, in a mystical forest where ancient trees whispered secrets to the wind, a young explorer named Emma discovered a hidden path covered in luminescent moss. As she ventured deeper into the woods, magical creatures began to appear: tiny pixies dancing around her shoulders, wise old owls offering cryptic advice, and gentle deer guiding her way. The forest seemed alive with wonder and mystery, each step revealing new enchantments that would change Emma\'s life forever.',
                'description': 'A magical journey through an enchanted forest full of wonder and discovery',
            },
            {
                'title': 'The Time Traveler\'s Dilemma',
                'content': 'Dr. Sarah Chen had spent decades perfecting her time machine, but she never anticipated the moral complexity of her first journey. Standing in her laboratory in 2024, she held the power to change history in her hands. Should she prevent disasters, save lives, or preserve the natural flow of time? As she stepped into the swirling vortex of temporal energy, Sarah realized that every choice would ripple through the centuries, affecting countless lives in ways she could never fully comprehend.',
                'description': 'A scientist grapples with the ethical implications of time travel',
            },
            {
                'title': 'The Last Library on Mars',
                'content': 'In the year 2157, when digital consciousness had replaced physical books on Earth, Maya Rodriguez maintained the last physical library on Mars Colony Seven. Surrounded by thousands of paper books in a climate-controlled dome, she served as the guardian of humanity\'s written heritage. When corporate executives arrived to digitize and destroy the collection, Maya had to choose between following orders and preserving the irreplaceable connection between human hands and the written word.',
                'description': 'A librarian\'s fight to preserve physical books in a digital future',
            }
        ]
        
        if messagebox.askyesno("确认", f"将插入 {len(sample_stories)} 个示例故事，确定继续吗？"):
            success_count = 0
            
            for i, story_data in enumerate(sample_stories):
                try:
                    # 填充表单
                    self.title_entry.delete(0, tk.END)
                    self.title_entry.insert(0, story_data['title'])
                    
                    self.description_entry.delete(0, tk.END)
                    self.description_entry.insert(0, story_data['description'])
                    
                    self.content_text.delete(1.0, tk.END)
                    self.content_text.insert(1.0, story_data['content'])
                    
                    # 插入故事
                    self.insert_story()
                    success_count += 1
                    
                    self.update_status(f"批量插入进度: {i+1}/{len(sample_stories)}")
                    self.root.update()  # 更新界面
                    
                except Exception as e:
                    self.update_status(f"批量插入第{i+1}个故事失败: {e}")
                    continue
            
            messagebox.showinfo("完成", f"批量插入完成！成功插入 {success_count}/{len(sample_stories)} 个故事")
    
    def clear_form(self):
        """清空表单"""
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.content_text.delete(1.0, tk.END)
        self.selected_image_path.set("")
        self.image_label.config(text="未选择图片")
        self.image_preview.config(image="", text="图片预览")
        if hasattr(self.image_preview, 'image'):
            self.image_preview.image = None
        self.update_status("表单已清空")
    
    def update_status(self, message):
        """更新状态栏"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

def main():
    """主函数"""
    root = tk.Tk()
    
    # 设置主题样式
    style = ttk.Style()
    style.theme_use('clam')  # 使用现代主题
    
    app = StoryInserterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()