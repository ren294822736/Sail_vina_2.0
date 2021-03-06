from tkinter import *
from tkinter.ttk import *
import configer, genbox, help_text, s_combobox, s_checkbox, s_button, s_label, s_entry, tooltip
from tkinter import messagebox
import os
import shutil
import time
import check
import requests
from contextlib import closing
from receptor_processor import *
from s_toplevel import *
import webbrowser

pdbqt_to_pdb_path = os.path.realpath(__file__) + "/../res/pdbqt_to_pdb.py"
pdb_to_pdbqt_path = os.path.realpath(__file__) + "/../res/prepare_ligand4.py"
prepare_receptor4_path = os.path.realpath(__file__) + "/../res/prepare_receptor4.py"


class Tab1(object):  # 配置config.txt

    def __init__(self, tab: Frame, config: configer.Configer) -> object:
        """
        创建一个选项卡,需要父窗口和用来保存配置的配置器

        :param tab: 选项卡
        :param config:  配置器
        """
        # 变量
        self.root = tab
        self.config = config

        # 创建分块内容
        self._create_main_frame()
        self._create_option_frame()
        self._create_tools_frame()
        self._create_output_frame()

        # 帮助按钮
        self.help_button = s_button.HelpButton(root=self.root, help_text=help_text.TAB1_TEXT, x=410, y=300, width=80)
        tooltip.create_tooltip(self.help_button.help_button, "获取帮助")

    def _create_main_frame(self):
        self.main_label_frame = LabelFrame(self.root, text="主要参数")
        self.main_label_frame.place(x=10, y=10, width=320, height=120)

        # center_x
        s_label.SLabel(self.main_label_frame, text="center_x = ",
                       x=10, y=5)
        self.center_x = s_entry.SEntry(self.main_label_frame, textvariable=StringVar(),
                                       text=configer.Configer.get_para("center_x"),
                                       x=95, y=5, width=60)
        tooltip.create_tooltip(self.center_x.entry, "对接位点的x坐标")

        # center_y
        s_label.SLabel(self.main_label_frame, text="center_y = ",
                       x=10, y=35)
        self.center_y = s_entry.SEntry(self.main_label_frame, textvariable=StringVar(),
                                       text=configer.Configer.get_para("center_y"),
                                       x=95, y=35, width=60)
        tooltip.create_tooltip(self.center_y.entry, "对接位点的y坐标")

        # center_z
        s_label.SLabel(self.main_label_frame, text="center_z = ", x=10, y=65)
        self.center_z = s_entry.SEntry(self.main_label_frame, textvariable=StringVar(),
                                       text=configer.Configer.get_para("center_z"),
                                       x=95, y=65, width=60)
        tooltip.create_tooltip(self.center_z.entry, "对接位点的z坐标")

        # size_x
        s_label.SLabel(self.main_label_frame, text="size_x = ",
                       x=175, y=5)
        self.size_x = s_entry.SEntry(self.main_label_frame, textvariable=StringVar(),
                                     text=configer.Configer.get_para("size_x"),
                                     x=245, y=5, width=60)
        tooltip.create_tooltip(self.size_x.entry, "对接位点的x方向大小")

        # size_y
        s_label.SLabel(self.main_label_frame, text="size_y = ",
                       x=175, y=35)
        self.size_y = s_entry.SEntry(self.main_label_frame, textvariable=StringVar(),
                                     text=configer.Configer.get_para("size_y"),
                                     x=245, y=35, width=60)
        tooltip.create_tooltip(self.size_y.entry, "对接位点的y方向大小")

        # size_z
        s_label.SLabel(self.main_label_frame, text="size_z = ",
                       x=175, y=65)
        self.size_z = s_entry.SEntry(self.main_label_frame, textvariable=StringVar(),
                                     text=configer.Configer.get_para("size_z"),
                                     x=245, y=65, width=60)
        tooltip.create_tooltip(self.size_z.entry, "对接位点的z方向大小")

    def _create_option_frame(self):
        self.option_label_frame = LabelFrame(self.root, text="可选")
        self.option_label_frame.place(x=340, y=10, width=240, height=120)

        # exhaustiveness
        s_label.SLabel(self.option_label_frame, text="exhaustiveness = ",
                       x=10, y=5)
        self.exhaustiveness = s_entry.SEntry(self.option_label_frame, textvariable=StringVar(),
                                             text=configer.Configer.get_para("exhaustiveness"),
                                             x=140, y=5, width=20)
        tooltip.create_tooltip(self.exhaustiveness.entry, "搜索度，越大耗时越长，建议保持默认")

        # num_modes
        s_label.SLabel(self.option_label_frame, text="num_modes = ",
                       x=10, y=35)
        self.num_modes = s_entry.SEntry(self.option_label_frame, textvariable=StringVar(),
                                        text=configer.Configer.get_para("num_modes"),
                                        x=140, y=35, width=20)
        tooltip.create_tooltip(self.num_modes.entry, "最多生成多少种结合模式")

        # energy_range
        s_label.SLabel(self.option_label_frame, text="energy_range = ",
                       x=10, y=65)
        self.energy_range = s_entry.SEntry(self.option_label_frame, textvariable=StringVar(),
                                           text=configer.Configer.get_para("energy_range"),
                                           x=140, y=65, width=20)

        tooltip.create_tooltip(self.energy_range.entry, "最大最小结合模式能量差")

        # 恢复默认值
        default_button = Button(self.option_label_frame, text="默认", command=self._change_default)
        default_button.place(x=170, y=62, width=60)
        tooltip.create_tooltip(default_button, "恢复默认值")

    def _change_default(self):
        self.exhaustiveness.textvariable.set(8)
        self.num_modes.textvariable.set(9)
        self.energy_range.textvariable.set(3)

    def _create_tools_frame(self):
        self.tools_frame = LabelFrame(self.root, text="工具")
        self.tools_frame.place(x=10, y=140, width=570, height=100)

        # 读取配置文件
        self.read_config_button = s_button.SButton(self.tools_frame, "读取配置文件", 10, 10)
        tooltip.create_tooltip(self.read_config_button.button, "必须选择config.txt文件！")
        self.read_config_entry = s_entry.SEntry(root=self.tools_frame, textvariable=StringVar(),
                                                text=configer.Configer.get_para("read_config"),
                                                x=100, y=14, width=360)
        tooltip.create_tooltip(self.read_config_entry.entry, "你选择的config.txt文件位置")
        self.read_config_button.bind_open_file(entry_text=self.read_config_entry.textvariable,
                                               title="请选择config.txt文件",
                                               file_type="txt")
        self.read_button = s_button.SButton(self.tools_frame, "读取到参数", 470, 10)
        tooltip.create_tooltip(self.read_button.button, "读取到上方")
        self.read_button.button.bind("<Button-1>", self.read_config)

        # 自动生成盒子
        self.choose_raw_ligand_button = s_button.SButton(self.tools_frame, "读取共晶配体", 10, 40)
        tooltip.create_tooltip(self.choose_raw_ligand_button.button, "必须选择共晶配体pdbqt文件！")
        self.choose_raw_ligand_entry = s_entry.SEntry(root=self.tools_frame, textvariable=StringVar(),
                                                      text=configer.Configer.get_para("choose_raw_ligand"),
                                                      x=100, y=44, width=360)
        self.choose_raw_ligand_button.bind_open_file(entry_text=self.choose_raw_ligand_entry.textvariable,
                                                     title="请选择“共晶配体”PDBQT文件！",
                                                     file_type="pdbqt")
        tooltip.create_tooltip(self.choose_raw_ligand_entry.entry, "你选择的共晶配体pdbqt文件位置")
        self.gen_box_button = s_button.SButton(self.tools_frame, "计算对接位点", 470, 40)
        tooltip.create_tooltip(self.gen_box_button.button, "自动计算对接位点，该对接位点为共晶配体的"
                                                           "最小外切正方体，结果仅供参考。")
        self.gen_box_button.button.bind("<Button-1>", self.gen_box)

    def _create_output_frame(self):
        self.output_frame = LabelFrame(self.root, text="输出配置文件")
        self.output_frame.place(x=10, y=250, width=570, height=50)

        # 输出配置文件
        self.output_config_button = s_button.SButton(self.output_frame, "选择输出目录", 10, 0)
        tooltip.create_tooltip(self.output_config_button.button, "选择config.txt输出的目录")
        self.output_config_entry = s_entry.SEntry(root=self.output_frame, textvariable=StringVar(),
                                                  text=configer.Configer.get_para("output_config"),
                                                  x=100, y=4, width=360)
        tooltip.create_tooltip(self.output_config_entry.entry, "输出config.txt文件的位置")
        self.output_config_button.bind_open_dir(self.output_config_entry.textvariable, title="选择输出目录")
        self.gen_config_button = s_button.SButton(self.output_frame, "输出", 470, 0)
        tooltip.create_tooltip(self.gen_config_button.button, "开始输出")
        self.gen_config_button.button.bind("<Button-1>", self.output_config)

    def read_config(self, event):
        if not self.read_config_entry.textvariable.get().endswith("config.txt"):  # 判断是否是config.txt
            messagebox.showerror(title="错误", message="请选择config.txt文件！")
            return

        with open(self.read_config_entry.textvariable.get(), "r") as f:
            for line in f.readlines():
                para_name, para = configer.ConfigReader.get_config_para(line)
                if para_name == "center_x":
                    self.center_x.textvariable.set(para)
                elif para_name == "center_y":
                    self.center_y.textvariable.set(para)
                elif para_name == "center_z":
                    self.center_z.textvariable.set(para)
                elif para_name == "size_x":
                    self.size_x.textvariable.set(para)
                elif para_name == "size_y":
                    self.size_y.textvariable.set(para)
                elif para_name == "size_z":
                    self.size_z.textvariable.set(para)
                elif para_name == "exhaustiveness":
                    self.exhaustiveness.textvariable.set(para)
                elif para_name == "num_modes":
                    self.num_modes.textvariable.set(para)
                elif para_name == "energy_range":
                    self.energy_range.textvariable.set(para)
                elif para_name == "":
                    continue
                else:
                    messagebox.showwarning("未知参数！", "包含未知参数\"%s\"" % para_name)
                    continue

    def output_config(self, event):

        # 判断盒子大小
        size_x = float(self.size_x.textvariable.get())
        size_y = float(self.size_y.textvariable.get())
        size_z = float(self.size_z.textvariable.get())

        box_size = size_x * size_y * size_z
        if box_size >= 27000:
            messagebox.showerror("错误！", "盒子总大小应小于27000，当前%.2f，请减小盒子大小！" % box_size)
            return

        if self.output_config_entry.textvariable.get() == "":
            messagebox.showerror("错误！", "请选择输出路径！")
            return

        config_dict = {"center_x = ": self.center_x.textvariable.get(),
                       "center_y = ": self.center_y.textvariable.get(),
                       "center_z = ": self.center_z.textvariable.get(),
                       "size_x = ": size_x,
                       "size_y = ": size_y,
                       "size_z = ": size_z,
                       "exhaustiveness = ": self.exhaustiveness.textvariable.get(),
                       "num_modes = ": self.num_modes.textvariable.get(),
                       "energy_range = ": self.energy_range.textvariable.get()
                       }
        output_path = self.output_config_entry.textvariable.get()
        configer.ConfigWriter.write_config(config_dict, output_path)
        messagebox.showinfo("导出配置文件成功！", "配置文件已经导出到：\n%s/config.txt" % output_path)

    def gen_box(self, event):
        if not self.choose_raw_ligand_entry.textvariable.get().endswith(".pdbqt"):
            messagebox.showerror("错误！", "请选择pdbqt文件！")
            return

        box = genbox.Box(self.choose_raw_ligand_entry.textvariable.get())
        try:
            center_x, center_y, center_z, box_size = box.get_box()
        except ZeroDivisionError:
            messagebox.showerror("错误！", "请确保选择的是共晶的pdbqt配体！")
        else:
            self.center_x.textvariable.set(center_x)
            self.center_y.textvariable.set(center_y)
            self.center_z.textvariable.set(center_z)
            self.size_x.textvariable.set(box_size)
            self.size_y.textvariable.set(box_size)
            self.size_z.textvariable.set(box_size)
            messagebox.showinfo("成功！", "已自动计算位点，仅供参考！")

    def save_para(self):
        self.config.para_dict["center_x"] = self.center_x.textvariable.get()
        self.config.para_dict["center_y"] = self.center_y.textvariable.get()
        self.config.para_dict["center_z"] = self.center_z.textvariable.get()
        self.config.para_dict["size_x"] = self.size_x.textvariable.get()
        self.config.para_dict["size_y"] = self.size_y.textvariable.get()
        self.config.para_dict["size_z"] = self.size_z.textvariable.get()

        self.config.para_dict["exhaustiveness"] = self.exhaustiveness.textvariable.get()
        self.config.para_dict["num_modes"] = self.num_modes.textvariable.get()
        self.config.para_dict["energy_range"] = self.energy_range.textvariable.get()

        self.config.para_dict["read_config"] = self.read_config_entry.textvariable.get()
        self.config.para_dict["choose_raw_ligand"] = self.choose_raw_ligand_entry.textvariable.get()
        self.config.para_dict["output_config"] = self.output_config_entry.textvariable.get()


class Tab2(object):  # 准备配体

    def __init__(self, tab, config):
        self.root = tab
        self.config = config

        self._create_choose_ligand_frame()
        self._create_output_ligand_frame()

        # 开始转换
        self._create_convert()

        # 帮助按钮
        self.help_button = s_button.HelpButton(root=self.root, help_text=help_text.TAB2_TEXT, x=410, y=300, width=80)
        tooltip.create_tooltip(self.help_button.help_button, "获取帮助")

    def _create_choose_ligand_frame(self):
        self.choose_ligand_labelframe = LabelFrame(self.root, text="输入选项")
        self.choose_ligand_labelframe.place(x=10, y=10, width=570, height=85)

        # 选择输入配体的格式
        s_label.SLabel(root=self.choose_ligand_labelframe, text="输入格式：",
                       x=10, y=0)
        input_format_text = ("mol", "smi", "sdf", "mol2", "pdb", "pdbqt")
        self.input_format = s_combobox.SCombbox(root=self.choose_ligand_labelframe, textvariable=StringVar(),
                                                values=input_format_text,
                                                default_value=configer.Configer.get_para("input_format"),
                                                x=80, y=0, width=60)
        tooltip.create_tooltip(self.input_format.combobox, "导入配体的格式")

        self.choose_ligands_button = s_button.SButton(self.choose_ligand_labelframe, text="选择单/多个配体", x=10, y=30)
        tooltip.create_tooltip(self.choose_ligands_button.button, "选择一个或者多个所选格式的配体")
        self.choose_ligand_dir_button = s_button.SButton(self.choose_ligand_labelframe, text="选择文件夹", x=110, y=30)
        tooltip.create_tooltip(self.choose_ligand_dir_button.button, "选择包含配体的文件夹，匹配其中所选格式的文件")
        self.choose_ligands_entry = s_entry.SEntry(root=self.choose_ligand_labelframe, textvariable=StringVar(),
                                                   text=configer.Configer.get_para("choose_ligands"),
                                                   x=200, y=34, width=360)
        tooltip.create_tooltip(self.choose_ligands_entry.entry, "所选的配体或者包含配体的目录")
        self.choose_ligands_button.bind_open_files(entry_text=self.choose_ligands_entry.textvariable,
                                                   title="选择单/多个配体",
                                                   file_type=self.input_format.textvariable)
        self.choose_ligand_dir_button.bind_open_dir(entry_text=self.choose_ligands_entry.textvariable,
                                                    title="选择包含配体文件的文件夹")

    def _create_output_ligand_frame(self):
        self.choose_output_ligand_labelframe = LabelFrame(self.root, text="输出选项")
        self.choose_output_ligand_labelframe.place(x=10, y=100, width=570, height=115)

        # 第一排
        first_y = 0
        s_label.SLabel(root=self.choose_output_ligand_labelframe, text="输出格式：", x=10, y=first_y)
        output_format_text = ("pdbqt", "pdb", "sdf", "mol2")
        self.output_format = s_combobox.SCombbox(root=self.choose_output_ligand_labelframe, textvariable=StringVar(),
                                                 values=output_format_text,
                                                 default_value=configer.Configer.get_para("output_format"),
                                                 x=80, y=0, width=60)
        tooltip.create_tooltip(self.output_format.combobox, "导出配体的格式")

        # 第二排
        second_y = 30
        # 生成3d
        s_label.SLabel(root=self.choose_output_ligand_labelframe, text="选      项：", x=10, y=second_y)
        self.gen3d = s_checkbox.SCheckbutton(root=self.choose_output_ligand_labelframe, text="3d", variable=StringVar(),
                                             value=configer.Configer.get_para("gen3d"), x=150, y=second_y)
        tooltip.create_tooltip(self.gen3d.checkbutton, "是否生成三维坐标。\n"
                                                       "输入配体是平面结构时，请勾选。\n"
                                                       "输入配体时立体结构时，不建议勾选。")

        # pH
        s_label.SLabel(root=self.choose_output_ligand_labelframe, text="pH", x=80, y=second_y)
        self.ph = s_entry.SEntry(root=self.choose_output_ligand_labelframe, textvariable=StringVar(),
                                 text=configer.Configer.get_para("pH"), x=110, y=second_y + 2, width=30)
        tooltip.create_tooltip(self.ph.entry, "按照一定的规则在指定pH生成质子化状态。为obabel内置"
                                              "方法，对某些氨基酸可能会发生变化，结果不一定可靠。")

        # 能量最小化
        self.is_minimize = s_checkbox.SCheckbutton(self.choose_output_ligand_labelframe, text="能量最小化",
                                                   variable=StringVar(),
                                                   value=configer.Configer.get_para("is_minimize"),
                                                   x=200, y=second_y)
        tooltip.create_tooltip(self.is_minimize.checkbutton, "是否对分子进行能量最小化")
        self.is_minimize.checkbutton.bind("<Button-1>", self._disable_minimize)
        s_label.SLabel(root=self.choose_output_ligand_labelframe, text="力场", x=290, y=second_y)
        minimize_value = ("MMFF94", "MMFF94s", "GAFF", "Chemical", "UFF")
        self.minimize = s_combobox.SCombbox(root=self.choose_output_ligand_labelframe,
                                            textvariable=StringVar(), values=minimize_value,
                                            default_value=configer.Configer.get_para("minimize"),
                                            x=325, y=second_y, width=100)
        tooltip.create_tooltip(self.minimize.combobox, "能量最小化使用的力场，推荐MMFF94")

        # 默认
        self.default_button = s_button.SButton(root=self.choose_output_ligand_labelframe, text="默认",
                                               x=450, y=second_y - 2)
        self.default_button.button.bind("<Button-1>", self._default)
        tooltip.create_tooltip(self.default_button.button, "恢复默认值")

        # 初始化状态
        if self.is_minimize.variable.get() == "0" or self.is_minimize.variable.get() == "":
            self.minimize.combobox.configure(state="disable")

        # 第三排
        third_y = 60
        self.choose_output_dir_button = s_button.SButton(self.choose_output_ligand_labelframe, text="选择输出文件夹",
                                                         x=10, y=third_y)
        tooltip.create_tooltip(self.choose_output_dir_button.button, "选择配体输出的文件夹")
        self.choose_output_dir_entry = s_entry.SEntry(root=self.choose_output_ligand_labelframe,
                                                      textvariable=StringVar(),
                                                      text=configer.Configer.get_para("ligand_output_dir"),
                                                      x=110, y=third_y + 4, width=450)
        tooltip.create_tooltip(self.choose_output_dir_entry.entry, "所选的输出目录")
        self.choose_output_dir_button.bind_open_dir(entry_text=self.choose_output_dir_entry.textvariable,
                                                    title="选择要输出配体的文件夹")

    def _disable_minimize(self, event):
        state = self.is_minimize.variable.get()
        if state == "1":
            self.minimize.combobox.configure(state="disable")
        elif state == "0" or state == "":
            self.minimize.combobox.configure(state="readonly")

    def _default(self, event):
        self.ph.textvariable.set("7.4")
        self.gen3d.variable.set("1")
        self.is_minimize.variable.set("1")
        self.minimize.textvariable.set("MMFF94")
        self.is_minimize.checkbutton.configure(state="normal")
        self.minimize.combobox.configure(state="readonly")

    def save_para(self):
        self.config.para_dict["input_format"] = self.input_format.textvariable.get()
        self.config.para_dict["choose_ligands"] = self.choose_ligands_entry.textvariable.get()
        self.config.para_dict["output_format"] = self.output_format.textvariable.get()
        self.config.para_dict["gen3d"] = self.gen3d.variable.get()
        self.config.para_dict["pH"] = self.ph.textvariable.get()
        self.config.para_dict["is_minimize"] = self.is_minimize.variable.get()
        self.config.para_dict["minimize"] = self.minimize.textvariable.get()
        self.config.para_dict["ligand_output_dir"] = self.choose_output_dir_entry.textvariable.get()

    def _create_convert(self):
        y = 230
        self.convert_button = s_button.SButton(root=self.root, x=10, y=y, text="开始转换")
        tooltip.create_tooltip(self.convert_button.button, "开始转换")
        self.progress = Progressbar(self.root, mode="determinate")
        self.progress.place(x=100, y=y + 2, width=400)
        tooltip.create_tooltip(self.progress, "转换进度")
        self.progress_label = s_label.SLabel(self.root, text="没有任务", x=510, y=y)
        self.convert_button.button.bind("<Button-1>", self._start_convert)

    def _start_convert(self, event):
        obabel_path = configer.Configer.get_para("obabel_path")
        if not check.Check.check_obabel(obabel_path):
            return

        input_files = self.choose_ligands_entry.textvariable.get()

        # 判断输入内容不能包含空格
        if check.Check.has_space(input_files):
            messagebox.showerror("输入错误！", "输入路径不能包含空格！")
            return

        input_format = self.input_format.textvariable.get()
        input_ligands = []

        # 判断输入的内容
        if input_files.endswith(";"):
            if input_files.split(".")[-1][0:-1] != input_format:
                messagebox.showerror("错误！", "选择的配体和输入的配体不符合！")
                return
            input_ligands.extend(input_files.split(";")[0:-1])
        elif os.path.isdir(input_files):
            list_file = os.listdir(input_files)
            for file in list_file:
                if file.endswith(input_format):
                    input_ligands.append(input_files + "/" + file)
            if len(input_ligands) == 0:
                messagebox.showerror("错误！", "所选文件夹中不包含选择格式的配体！")
                return
        else:
            messagebox.showerror("错误！", "请检查输入的配体！")
            return

        ph = self.ph.textvariable.get()
        # ph不能为空
        if ph == "":
            messagebox.showerror("错误！", "请输入pH！")
            return

        gen3d = self.gen3d.variable.get()
        is_minimize = self.is_minimize.variable.get()
        minimize = self.minimize.textvariable.get()
        output_format = self.output_format.textvariable.get()
        output_path = self.choose_output_dir_entry.textvariable.get()

        # 输出目录不能为空
        if output_path == "" or output_path.count(" ") > 0:
            messagebox.showerror("输入错误！", "输出路径不能包含空格！")
            return
        if not os.path.exists(output_path):
            messagebox.showerror("输入错误！", "输出路径不存在！")
            return

        python_path = configer.Configer.get_para("python_path")
        # 检查python路径是否正确
        if not check.Check.check_python(python_path):
            return

        output_ligands = []

        for ligand in input_ligands:
            ligand_name = ligand.split("/")[-1].split(".")[0] + "." + output_format
            output_ligands.append(output_path + "/" + ligand_name)

        if input_format == output_format:
            messagebox.showerror("错误！", "输入和输出格式不应相等！")
            return

        self.progress["maximum"] = len(input_ligands)

        # 进行格式转换
        if input_format == "pdbqt":  # pdbqt->other
            # pdbqt->pdb
            if output_format == "pdb":
                # adt执行pdbqt转pdb
                i = 0
                while i < len(input_ligands):
                    command = "%s %s -f %s -o %s" % (python_path, pdbqt_to_pdb_path,
                                                     input_ligands[i], output_ligands[i])

                    # 更改标签文字
                    label_text = "%i/%i" % (i + 1, len(input_ligands))
                    self.progress_label.label.configure(text=label_text)
                    self.progress_label.label.update()

                    # 更新进度条
                    self.progress["value"] = i + 1
                    self.progress.update()

                    os.system(command)
                    i += 1
                messagebox.showinfo("转换完成！", "成功将pdbqt转换成pdb！")
                self.progress["value"] = 0
                self.progress_label.label.configure(text="没有任务")
                return

            else:
                # obabel转换成输出格式，先转成pdb
                pdb_ligands = []
                for ligand in input_ligands:
                    ligand_name = ligand.split("/")[-1].split(".")[0] + ".pdb"
                    pdb_ligands.append(output_path + "/tmp/" + ligand_name)

                self.progress["maximum"] = len(input_ligands) * 2

                os.mkdir(output_path + "/tmp")  # 创建临时文件夹

                i = 0
                while i < len(input_ligands):
                    command = "%s %s -f %s -o %s" % (python_path, pdbqt_to_pdb_path,
                                                     input_ligands[i], pdb_ligands[i])

                    label_text = "%i/%i" % (i + 1, len(input_ligands))
                    self.progress_label.label.configure(text=label_text)
                    self.progress_label.label.update()

                    self.progress["value"] = i + 1
                    self.progress.update()

                    os.system(command)
                    i += 1

                i = 0
                while i < len(input_ligands):
                    command = "%s %s -O %s" % (obabel_path, pdb_ligands[i], output_ligands[i])

                    # 更改标签文字
                    label_text = "%i/%i" % (i + 1, len(input_ligands))
                    self.progress_label.label.configure(text=label_text)
                    self.progress_label.label.update()

                    # 更新进度条
                    self.progress["value"] = i + 1 + len(input_ligands)
                    self.progress.update()

                    os.system(command)
                    i += 1
                shutil.rmtree(output_path + "/tmp")
                messagebox.showinfo("转换完成！", "成功将pdbqt转换%s！" % output_format)
                self.progress["value"] = 0
                self.progress_label.label.configure(text="没有任务")
                return

        elif input_format == "pdb" or input_format == "mol2" and output_format == "pdbqt":  # pdb->pdbqt
            print("使用ADT脚本将pdb转换成pdbqt")
            i = 0
            while i < len(input_ligands):
                command = "%s %s -l %s -o %s" % (python_path, pdb_to_pdbqt_path,
                                                 input_ligands[i], output_ligands[i])

                # 更改标签文字
                label_text = "%i/%i" % (i + 1, len(input_ligands))
                self.progress_label.label.configure(text=label_text)
                self.progress_label.label.update()

                # 更新进度条
                self.progress["value"] = i + 1 + len(input_ligands)
                self.progress.update()

                os.system(command)
                i += 1
            messagebox.showinfo("转换完成！", "成功将%s转换pdbqt！" % input_format)
            self.progress["value"] = 0
            self.progress_label.label.configure(text="没有任务")
            return

        else:  # 输入不是pdbqt
            if output_format == "pdbqt":
                # obabel转换成输出格式，先转成pdb
                pdb_ligands = []
                for ligand in input_ligands:
                    ligand_name = ligand.split("/")[-1].split(".")[0] + ".pdb"
                    pdb_ligands.append(output_path + "/tmp/" + ligand_name)

                self.progress["maximum"] = len(input_ligands) * 2

                os.mkdir(output_path + "/tmp")  # 创建临时文件夹

                i = 0
                while i < len(input_ligands):
                    command = "%s %s -O %s -p %s --gen3d --minimize --ff %s" % (obabel_path, input_ligands[i],
                                                                                pdb_ligands[i],
                                                                                ph, minimize)

                    label_text = "%i/%i" % (i + 1, len(input_ligands))
                    self.progress_label.label.configure(text=label_text)
                    self.progress_label.label.update()

                    self.progress["value"] = i + 1
                    self.progress.update()

                    os.system(command)
                    i += 1

                i = 0
                while i < len(input_ligands):
                    command = "%s %s -l %s -o %s" % (python_path, pdb_to_pdbqt_path,
                                                     pdb_ligands[i], output_ligands[i])

                    # 更改标签文字
                    label_text = "%i/%i" % (i + 1, len(input_ligands))
                    self.progress_label.label.configure(text=label_text)
                    self.progress_label.label.update()

                    # 更新进度条
                    self.progress["value"] = i + 1 + len(input_ligands)
                    self.progress.update()

                    os.system(command)
                    i += 1
                shutil.rmtree(output_path + "/tmp")
                messagebox.showinfo("转换完成！", "成功将%s转换pdbqt！" % input_format)
                self.progress["value"] = 0
                self.progress_label.label.configure(text="没有任务")
                return
            else:
                if gen3d == "1":
                    if is_minimize == "1":
                        i = 0
                        while i < len(input_ligands):
                            command = "%s %s -O %s -p %s --gen3d --minimize --ff %s" % (obabel_path, input_ligands[i],
                                                                                        output_ligands[i],
                                                                                        ph, minimize)

                            label_text = "%s/%s" % (i + 1, len(input_ligands))
                            self.progress_label.label.configure(text=label_text)
                            self.progress_label.label.update()

                            self.progress["value"] = i + 1
                            self.progress.update()

                            os.system(command)
                            i += 1
                        messagebox.showinfo("成功！", "成功将%s转换成%s！" % (input_format, output_format))
                        self.progress["value"] = 0
                        self.progress_label.label.configure(text="没有任务")
                    else:
                        i = 0
                        while i < len(input_ligands):
                            command = "%s %s -O %s -p %s --gen3d" % (obabel_path, input_ligands[i],
                                                                     output_ligands[i],
                                                                     ph)

                            label_text = "%s/%s" % (i + 1, len(input_ligands))
                            self.progress_label.label.configure(text=label_text)
                            self.progress_label.label.update()

                            self.progress["value"] = i + 1
                            self.progress.update()

                            os.system(command)
                            i += 1
                        messagebox.showinfo("成功！", "成功将%s转换成%s！" % (input_format, output_format))
                        self.progress["value"] = 0
                        self.progress_label.label.configure(text="没有任务")
                else:
                    if is_minimize == "1":
                        i = 0
                        while i < len(input_ligands):
                            command = "%s %s -O %s -p %s --minimize --ff %s" % (obabel_path, input_ligands[i],
                                                                                output_ligands[i],
                                                                                ph, minimize)

                            label_text = "%s/%s" % (i + 1, len(input_ligands))
                            self.progress_label.label.configure(text=label_text)
                            self.progress_label.label.update()

                            self.progress["value"] = i + 1
                            self.progress.update()

                            os.system(command)
                            i += 1
                        messagebox.showinfo("成功！", "成功将%s转换成%s！" % (input_format, output_format))
                        self.progress["value"] = 0
                        self.progress_label.label.configure(text="没有任务")
                    else:
                        i = 0
                        while i < len(input_ligands):
                            command = "%s %s -O %s -p %s" % (obabel_path, input_ligands[i],
                                                             output_ligands[i],
                                                             ph)

                            label_text = "%s/%s" % (i + 1, len(input_ligands))
                            self.progress_label.label.configure(text=label_text)
                            self.progress_label.label.update()

                            self.progress["value"] = i + 1
                            self.progress.update()

                            os.system(command)
                            i += 1
                        messagebox.showinfo("成功！", "成功将%s转换成%s！" % (input_format, output_format))
                        self.progress["value"] = 0
                        self.progress_label.label.configure(text="没有任务")


class Tab4(object):  # 分子对接

    def __init__(self, tab, config):
        self.root = tab
        self.config = config

        self._choose_ligand_frame()
        self._choose_protein_frame()
        self._choose_output_frame()
        self._choose_docking_config()

        self._start_docking()

        # 帮助按钮
        self.help_button = s_button.HelpButton(root=self.root, help_text=help_text.TAB4_TEXT, x=410, y=300, width=80)
        tooltip.create_tooltip(self.help_button.help_button, "获取帮助")

    def _choose_ligand_frame(self):
        self.choose_ligand_labelframe = LabelFrame(self.root, text="选择配体")
        self.choose_ligand_labelframe.place(x=10, y=10, width=570, height=50)

        self.choose_ligands = s_button.SButton(root=self.choose_ligand_labelframe, text="选择单/多个配体", x=10, y=0)
        tooltip.create_tooltip(self.choose_ligands.button, "选择单/多个配体，配体格式必须是pdbqt！")
        self.choose_ligand_dir = s_button.SButton(root=self.choose_ligand_labelframe, text="选择文件夹", x=110, y=0)
        tooltip.create_tooltip(self.choose_ligand_dir.button, "选择包含pdbqt格式配体的文件夹。")
        self.choose_ligand_entry = s_entry.SEntry(root=self.choose_ligand_labelframe, textvariable=StringVar(),
                                                  text=configer.Configer.get_para("choose_docking_ligands"),
                                                  x=200, y=4, width=360)
        tooltip.create_tooltip(self.choose_ligand_entry.entry, "选择的配体或者包含配体的文件夹")
        self.choose_ligands.bind_open_files(entry_text=self.choose_ligand_entry.textvariable,
                                            title="选择单/多个配体",
                                            file_type="pdbqt")
        self.choose_ligand_dir.bind_open_dir(entry_text=self.choose_ligand_entry.textvariable,
                                             title="选择包含pdbqt配体的文件夹")

    def _choose_protein_frame(self):
        self.choose_protein_labelframe = LabelFrame(self.root, text="选择受体")
        self.choose_protein_labelframe.place(x=10, y=70, width=570, height=50)

        self.choose_proteins = s_button.SButton(root=self.choose_protein_labelframe, text="选择受体文件夹", x=10, y=0)
        tooltip.create_tooltip(self.choose_proteins.button, "选择受体文件夹。受体必须命名为preped.pdbqt\n"
                                                            "单个受体请选择包含这个受体的文件夹\n"
                                                            "多个受体请选择包含多个受体文件夹的文件夹\n"
                                                            "详情见帮助及教程")
        self.choose_proteins_entry = s_entry.SEntry(root=self.choose_protein_labelframe, textvariable=StringVar(),
                                                    text=configer.Configer.get_para("choose_docking_proteins"),
                                                    x=110, y=4, width=450)
        tooltip.create_tooltip(self.choose_proteins_entry.entry, "包含受体的文件夹")
        self.choose_proteins.bind_open_dir(entry_text=self.choose_proteins_entry.textvariable,
                                           title="选择包含pdbqt受体的文件夹")

    def _choose_output_frame(self):
        self.choose_output_labelframe = LabelFrame(self.root, text="结果输出")
        self.choose_output_labelframe.place(x=10, y=130, width=570, height=50)

        self.choose_output = s_button.SButton(root=self.choose_output_labelframe, text="选择输出文件夹", x=10, y=0)
        tooltip.create_tooltip(self.choose_output.button, "选择对接结果输出目录")
        self.choose_output_entry = s_entry.SEntry(root=self.choose_output_labelframe, textvariable=StringVar(),
                                                  text=configer.Configer.get_para("choose_docking_output"),
                                                  x=110, y=4, width=450)
        tooltip.create_tooltip(self.choose_output_entry.entry, "所选的对接结果输出目录")
        self.choose_output.bind_open_dir(entry_text=self.choose_output_entry.textvariable,
                                         title="选择对接输出的文件夹")

    def _choose_docking_config(self):
        self.choose_config_labelframe = LabelFrame(self.root, text="对接配置")
        self.choose_config_labelframe.place(x=10, y=190, width=570, height=50)

        self.docking_time_label = s_label.SLabel(root=self.choose_config_labelframe, text="对接次数：", x=10, y=0)

        self.times_entry = s_entry.SEntry(root=self.choose_config_labelframe,
                                          textvariable=StringVar(),
                                          text=configer.Configer.get_para("docking_times"),
                                          x=80, y=0, width=20)
        tooltip.create_tooltip(self.times_entry.entry, "每个配体需要对接的次数")

    def _start_docking(self):
        y = 250
        self.docking_button = s_button.SButton(root=self.root, text="开始对接", x=10, y=y)
        tooltip.create_tooltip(self.docking_button.button, "使用Vina进行对接")

        self.progress = Progressbar(self.root, mode="determinate")
        self.progress.place(x=100, y=y + 2, width=400)
        tooltip.create_tooltip(self.progress, "对接进度")

        self.progress_label = s_label.SLabel(self.root, text="没有任务", x=510, y=y)
        self.docking_button.button.bind("<Button-1>", self._docking)

        text_y = 276
        self.current_protein_frame = Frame(self.root, width=200, height=40)
        self.current_protein_frame.place(x=10, y=text_y)
        self.current_protein = s_label.SLabel(root=self.current_protein_frame, text="", x=0, y=0)
        self.current_ligand_frame = Frame(self.root, width=200, height=50)
        self.current_ligand_frame.place(x=220, y=text_y)
        self.current_ligand = s_label.SLabel(root=self.current_ligand_frame, text="", x=0, y=0)
        self.current_time_frame = Frame(self.root, width=150, height=50)
        self.current_time_frame.place(x=430, y=text_y)
        self.current_time = s_label.SLabel(root=self.current_time_frame, text="", x=0, y=0)

    def _docking(self, event):
        input_ligands_full = self.choose_ligand_entry.entry.get()
        receptor_dir = self.choose_proteins_entry.entry.get()
        output_dir = self.choose_output_entry.entry.get()
        docking_times = self.times_entry.entry.get()

        # 所有选择的路径和文件都不能为空。
        if input_ligands_full == "" or receptor_dir == "" or output_dir == "" or docking_times == "":
            messagebox.showerror("错误！", "输入不能为空！")
            return

        # 不能包括空格
        if input_ligands_full.count(" ") > 0:
            messagebox.showerror("错误！", "配体路径不能包含空格！")
            return
        if receptor_dir.count(" ") > 0:
            messagebox.showerror("错误！", "受体路径不能包含空格！")
            return
        if output_dir.count(" ") > 0:
            messagebox.showerror("错误！", "输出路径不能包含空格！")
            return
        if docking_times.count(" ") > 0:
            messagebox.showerror("错误！", "请输入每个配体要对接的次数！")
            return

        try:
            times = int(docking_times)
        except ValueError:
            messagebox.showerror("错误！", "对接次数必须是数字！")
            return

        if not os.path.exists(output_dir):
            messagebox.showerror("错误！", "输出的路径不存在！")
            return

        input_ligands = []

        # 输入的配体
        if input_ligands_full.endswith(";"):  # 如果是单个或者多个配体
            if input_ligands_full.split(".")[-1][0:-1] != "pdbqt":  # 必须是pdbqt文件
                messagebox.showerror("错误！", "配体必须是pdbqt格式！")
                return
            input_ligands.extend(input_ligands_full.split(";")[0:-1])
        elif os.path.isdir(input_ligands_full):  # 如果选择的是目录
            list_file = os.listdir(input_ligands_full)
            for file in list_file:
                if file.endswith("pdbqt"):
                    input_ligands.append(input_ligands_full + "/" + file)
            if len(input_ligands) == 0:
                messagebox.showerror("错误！", "所选文件夹中不包含pdbqt格式的配体！")
                return
        else:
            messagebox.showerror("错误！", "请检查输入的配体！")
            return

        # 输入的受体
        receptors = []
        configs = []
        if os.path.exists("%s/preped.pdbqt" % receptor_dir):  # 选择了一个受体
            if not os.path.exists("%s/config.txt" % receptor_dir):
                messagebox.showerror("错误！", "受体中没有config.txt文件！")
                return
            receptors.append("%s/preped.pdbqt" % receptor_dir)
            configs.append("%s/config.txt" % receptor_dir)
        else:  # 可能选择了多个受体
            if not os.path.exists(receptor_dir):
                messagebox.showerror("错误！", "所选受体目录不存在！")
                return
            child_receptor = os.listdir(receptor_dir)
            for receptor in child_receptor:
                if os.path.exists("%s/%s/preped.pdbqt" % (receptor_dir, receptor)):
                    if not os.path.exists("%s/%s/config.txt" % (receptor_dir, receptor)):
                        messagebox.showwarning("警告！", "受体%s中没有config.txt文件，将不进行对接！" % receptor)
                        continue
                    receptors.append("%s/%s/preped.pdbqt" % (receptor_dir, receptor))
                    configs.append("%s/%s/config.txt" % (receptor_dir, receptor))
        if len(receptors) == 0:
            messagebox.showerror("错误！", "没有受体，请检查选择的文件夹或者子文件夹中是否"
                                        "包含preped.pdbqt文件!")
            return

        self.progress["maximum"] = len(receptors) * len(input_ligands)
        for receptor in receptors:
            # 在输出目录创建受体的文件夹
            output_dir_r = "%s/%s" % (output_dir, receptor.split("/")[-2])
            if not os.path.exists(output_dir_r):
                os.mkdir(output_dir_r)

            for ligand in input_ligands:
                # 初始化循环次数
                i = 0

                # 更新进度条和标签
                current_num = receptors.index(receptor) * len(input_ligands) + input_ligands.index(ligand) + 1
                max_num = len(receptors) * len(input_ligands)
                label_text = "%s/%s" % (current_num, max_num)

                self.progress_label.label.configure(text=label_text)
                self.progress_label.label.update()

                self.progress["value"] = current_num
                self.progress.update()

                current_protein = "当前受体：%s" % receptor.split("/")[-2]
                self.current_protein.label.configure(text=current_protein)
                self.current_protein.label.update()

                current_ligand = "当前配体：%s" % ligand.split("/")[-1].split(".")[0]
                self.current_ligand.label.configure(text=current_ligand)
                self.current_ligand.label.update()

                current_time = "当前次数：%i" % (i + 1)
                self.current_time.label.configure(text=current_time)
                self.current_time.label.update()

                time.sleep(0.5)
                # 开始对接
                while i < times:
                    ligand_basename = ligand.split("/")[-1].split(".")[0]
                    output = "%s/%s_out%s.pdbqt" % (output_dir_r, ligand_basename, i + 1)
                    vina_path = os.path.realpath(__file__) + "/../res/vina.exe"
                    command = "%s --ligand %s --receptor %s --config %s --out %s" % (vina_path,
                                                                                     ligand,
                                                                                     receptor,
                                                                                     configs[receptors.index(receptor)],
                                                                                     output)
                    os.system(command)
                    i += 1
        messagebox.showinfo("成功！", "对接完成！")
        self.progress_label.label.configure(text="没有任务")
        self.progress_label.label.update()

        self.progress["value"] = 0
        self.progress.update()

        self.current_protein.label.configure(text="")
        self.current_protein.label.update()

        self.current_ligand.label.configure(text="")
        self.current_ligand.label.update()

        self.current_time.label.configure(text="")
        self.current_time.label.update()

    def save_para(self):
        self.config.para_dict["choose_docking_ligands"] = self.choose_ligand_entry.textvariable.get()
        self.config.para_dict["choose_docking_proteins"] = self.choose_proteins_entry.textvariable.get()
        self.config.para_dict["choose_docking_output"] = self.choose_output_entry.textvariable.get()
        self.config.para_dict["docking_times"] = self.times_entry.textvariable.get()


class Tab3(object):  # 准备受体

    chains = None

    def __init__(self, tab, config):
        self.root = tab
        self.config = config

        # 结构对象
        self.structure = None
        self.model_name = None
        self.chain_name = None
        self.ligand_name = None

        # listbox控件
        self.model_list = None
        self.chain_list = None
        self.ligand_list = None

        self.output_path = None

        self.create_download_receptor()
        self.create_prepared_receptor()

        # 帮助按钮
        self.help_button = s_button.HelpButton(root=self.root, help_text=help_text.TAB3_TEXT, x=410, y=300, width=80)
        tooltip.create_tooltip(self.help_button.help_button, "获取帮助")

    def create_download_receptor(self):
        download_receptor_labelframe = LabelFrame(self.root, text="下载受体")
        download_receptor_labelframe.place(x=10, y=10, width=570, height=115)

        s_label.SLabel(download_receptor_labelframe, "PDBID：", x=10, y=0)
        self.pdbid_entry = s_entry.SEntry(download_receptor_labelframe, textvariable=StringVar(),
                                          text=configer.Configer.get_para("pdbid"),
                                          x=70, y=0, width=50)
        tooltip.create_tooltip(self.pdbid_entry.entry, "请输入四位PDB的ID")

        pdb_save_path_button = s_button.SButton(download_receptor_labelframe,
                                                text="选择保存的路径", x=10, y=30)
        tooltip.create_tooltip(pdb_save_path_button.button, "选择下载受体要保存的位置")
        self.pdb_save_path_entry = s_entry.SEntry(download_receptor_labelframe,
                                                  textvariable=StringVar(),
                                                  text=configer.Configer.get_para("pdb_path"),
                                                  x=110, y=35, width=440)
        tooltip.create_tooltip(self.pdb_save_path_entry.entry, "文件将要保存的目录，不存在将创建文件夹")
        pdb_save_path_button.bind_open_dir(entry_text=self.pdb_save_path_entry.textvariable, title="选择要保存的路径")

        download_pdb_button = s_button.SButton(download_receptor_labelframe,
                                               text="开始下载", x=10, y=60)
        tooltip.create_tooltip(download_pdb_button.button, "从Protein Data Bank下载受体")
        download_pdb_button.button.bind("<Button-1>", self.downloadpdb)
        self.download_progressbar = Progressbar(download_receptor_labelframe, mode="determinate")
        self.download_progressbar.place(x=100, y=62, width=380)
        tooltip.create_tooltip(self.download_progressbar, "下载进度")

        self.download_state_label = s_label.SLabel(download_receptor_labelframe,
                                                   text="没有下载", x=490, y=60)

    def create_prepared_receptor(self):
        prepared_receptor_labelframe = LabelFrame(self.root, text="准备受体")
        prepared_receptor_labelframe.place(x=10, y=130, width=570, height=110)

        choose_raw_receptor_button = s_button.SButton(prepared_receptor_labelframe,
                                                      text="选择受体", x=10, y=0)
        tooltip.create_tooltip(choose_raw_receptor_button.button, "选择要进行准备的pdb受体")
        self.choose_raw_receptor_entry = s_entry.SEntry(prepared_receptor_labelframe,
                                                        textvariable=StringVar(),
                                                        text=configer.Configer.get_para("raw_receptor_path"),
                                                        x=100, y=3, width=360)
        tooltip.create_tooltip(self.choose_raw_receptor_entry.entry, "选择的受体")
        choose_raw_receptor_button.bind_open_file(entry_text=self.choose_raw_receptor_entry.textvariable,
                                                  title="选择受体pdb文件", file_type="pdb")
        get_info_button = s_button.SButton(prepared_receptor_labelframe, text="受体信息",
                                           x=470, y=0)
        get_info_button.button.bind("<Button-1>", self.getinfo)
        tooltip.create_tooltip(get_info_button.button, "查看受体信息")

        # 提取配体
        ligand_save_path_button = s_button.SButton(prepared_receptor_labelframe,
                                                   text="配体输出路径", x=10, y=30)
        tooltip.create_tooltip(ligand_save_path_button.button, "选择提取的配体要保存的位置")
        self.ligand_save_path_entry = s_entry.SEntry(prepared_receptor_labelframe,
                                                     textvariable=StringVar(),
                                                     text=configer.Configer.get_para("extract_ligand_path"),
                                                     x=100, y=33, width=360)
        tooltip.create_tooltip(self.ligand_save_path_entry.entry, "提取的配体保存的目录，不存在将创建文件夹")
        ligand_save_path_button.bind_open_dir(entry_text=self.ligand_save_path_entry.textvariable, title="选择要保存的路径")

        save_ligand_button = s_button.SButton(prepared_receptor_labelframe, text="提取配体",
                                              x=470, y=30)
        save_ligand_button.button.bind("<Button-1>", self.extract_ligand)
        tooltip.create_tooltip(save_ligand_button.button, "提取受体中的配体")

        # 准备受体
        save_prepared_receptor_button = s_button.SButton(prepared_receptor_labelframe,
                                                         text="受体输出路径", x=10, y=60)
        tooltip.create_tooltip(save_prepared_receptor_button.button, "选择准备后的受体保存路径")
        self.choose_prepare_output_path = s_entry.SEntry(prepared_receptor_labelframe,
                                                         textvariable=StringVar(),
                                                         text=configer.Configer.get_para("preped_path"),
                                                         x=100, y=63, width=360)
        tooltip.create_tooltip(self.choose_prepare_output_path.entry, "准备受体后的输出目录")
        save_prepared_receptor_button.bind_open_dir(self.choose_prepare_output_path.textvariable,
                                                    title="选择输出目录")

        prepare_receptor_button = s_button.SButton(prepared_receptor_labelframe, text="准备受体",
                                                   x=470, y=60)
        prepare_receptor_button.button.bind("<Button-1>", self.prepared_receptor)
        tooltip.create_tooltip(prepare_receptor_button.button, "开始准备受体")

    def getinfo(self, event):
        receptor = self.choose_raw_receptor_entry.textvariable.get()  # 获取受体
        self.output_path = self.ligand_save_path_entry.textvariable.get()  # 配体输出路径

        if not receptor.endswith("pdb"):
            messagebox.showerror("错误！", "受体只支持pdb格式！")
            return
        if check.Check.check_path(receptor):
            messagebox.showerror("错误", "受体路径不能包含空格！")
            return

        structure = ReceptorProcessor.get_structure(receptor)

        window = STopLevel(self.root, 500, 400, "PDB信息").toplevel
        wraplength = 480

        s_name = structure.header["name"]
        s_label.SLabel(window, "受体名称:\n" + s_name, 10, 10).label.configure(wraplength=wraplength)

        s_redate = structure.header["release_date"]
        s_label.SLabel(window, "发布时间:\n" + s_redate, 10, 70).label.configure(wraplength=wraplength)

        s_method = structure.header["structure_method"]
        s_label.SLabel(window, "方法:\n" + s_method, 10, 130).label.configure(wraplength=wraplength)

        s_resolution = str(structure.header["resolution"])
        s_label.SLabel(window, "分辨率:\n" + s_resolution + "埃", 10, 190).label.configure(wraplength=wraplength)

        s_refe = structure.header["journal_reference"]
        reference = s_label.SLabel(window, "参考文献:\n" + s_refe, 10, 250).label
        reference.configure(wraplength=wraplength)
        doi_url = "http://www.doi.org/" + s_refe.strip().split(" ")[-1]
        open_url_button = s_button.SButton(window, "打开文献网页", 75, 245)
        open_url_button.button.configure(command=lambda: webbrowser.open(doi_url))
        tooltip.create_tooltip(open_url_button.button, "使用默认浏览器打开文献链接")

    def downloadpdb(self, event):
        pdbid = self.pdbid_entry.textvariable.get()
        filepath = self.pdb_save_path_entry.textvariable.get()
        if len(pdbid) != 4:
            messagebox.showerror("错误！", "请输入四位pdb代码！")
            return
        state, current_entry = check_pdb_status(pdbid)
        if state == "CURRENT":
            self._downloadpdb(current_entry, filepath)
        elif state == "OBSOLETE":
            messagebox.showwarning("当前pdb已经过时！", "将下载%s" % current_entry)
            self._downloadpdb(current_entry, filepath)
        else:
            messagebox.showerror("错误！", "当前pdb不存在，请检查id是否正确！")
            return

    def _downloadpdb(self, pdbid, filepath):
        url = 'http://www.rcsb.org/pdb/files/%s.pdb' % pdbid

        # 末尾如果含有斜杠，去掉斜杠
        if filepath.endswith("/"):
            filepath = filepath[0:-1]

        if not os.path.exists(filepath):
            os.mkdir(filepath)

        filename = filepath + "/%s.pdb" % pdbid

        try:
            file_size = len(requests.get(url).content)
        except requests.HTTPError:
            messagebox.showerror("下载错误", "请求失败，请重试")
            return
        except:
            messagebox.showerror("下载错误", "请求失败，请重试")
            return

        self.download_progressbar["maximum"] = file_size

        with closing(requests.get(url, stream=True)) as response:
            chunk_size = 1024  # 单次请求最大值
            data_length = 0
            with open(filename, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    data_length += len(data)
                    # 更新进度条
                    self.download_progressbar["value"] = data_length
                    self.download_progressbar.update()

                    # 更新标签
                    percent = int(data_length / file_size * 100)
                    self.download_state_label.label.configure(text="%i/100" % percent)
                    self.download_state_label.label.update()

        # 文件下载结束
        messagebox.showinfo("下载成功！", "成功下载%s" % pdbid)

        # 更新进度条
        self.download_progressbar["value"] = 0
        self.download_progressbar.update()

        # 更新标签
        self.download_state_label.label.configure(text="没有任务")
        self.download_state_label.label.update()

    def extract_ligand(self, event):
        receptor = self.choose_raw_receptor_entry.textvariable.get()  # 获取受体
        self.output_path = self.ligand_save_path_entry.textvariable.get()  # 配体输出路径

        if not receptor.endswith("pdb"):
            messagebox.showerror("错误！", "受体只支持pdb格式！")
            return
        if check.Check.check_path(receptor):
            messagebox.showerror("错误", "受体路径不能包含空格！")
            return
        if check.Check.check_path(self.output_path):
            messagebox.showerror("错误", "配体输出路径不能包含空格！")
            return
        self._extract_ligand(receptor)

    def _extract_ligand(self, pdb):
        self.structure = ReceptorProcessor.get_structure(pdb)

        top = STopLevel(self.root, 300, 250, "提取配体").toplevel

        # 创建切换卡
        self.notebook = Notebook(top)

        # 创建每个选项卡
        self.choose_model_tab = Frame(self.notebook)
        self.choose_chain_tab = Frame(self.notebook)
        self.choose_ligand_tab = Frame(self.notebook)

        # 添加选项卡
        self.notebook.add(self.choose_model_tab, text="model")
        self.notebook.add(self.choose_chain_tab, text="chain")
        self.notebook.add(self.choose_ligand_tab, text="ligand")

        # 选项卡创建内容
        self.choose_model()
        self.choose_chain()
        self.choose_ligand()

        self.notebook.place(x=10, y=10, width=290, height=230)

    def jump_model(self, event):

        # 禁用后两个
        self.notebook.tab(1, state="disable")
        self.notebook.tab(0, state="normal")
        self.notebook.tab(2, state="disable")

        self.notebook.select(tab_id=0)

    def choose_model(self):
        # 禁用后两个
        self.notebook.tab(1, state="disable")
        self.notebook.tab(2, state="disable")

        self.model_list = Listbox(self.choose_model_tab, width=30, height=10)

        model_ids = ReceptorProcessor.get_model_ids(self.structure)
        Tab3.refresh_listbox(model_ids, self.model_list)

        self.model_list.place(x=10, y=10, width=255, height=150)
        scroll = Scrollbar(self.model_list)
        scroll.pack(side=RIGHT, fill=Y)
        self.model_list.configure(yscrollcommand=scroll.set)
        scroll.config(command=self.model_list.yview)

        next_button = s_button.SButton(self.choose_model_tab, "下一步", 165, 170)
        next_button.button.bind("<Button-1>", self.jump_chain)

    def jump_chain(self, event):
        self.model_name = self.model_list.get(ACTIVE)
        model = self.structure[self.model_name]
        chain_names = ReceptorProcessor.get_chain_ids(model)
        Tab3.refresh_listbox(chain_names, self.chain_list)

        # 禁用后两个
        self.notebook.tab(0, state="disable")
        self.notebook.tab(1, state="normal")
        self.notebook.tab(2, state="disable")

        self.notebook.select(tab_id=1)

    def choose_chain(self):
        self.chain_list = Listbox(self.choose_chain_tab, width=30, height=10)
        self.chain_list.place(x=10, y=10, width=255, height=150)
        scroll = Scrollbar(self.chain_list)
        scroll.pack(side=RIGHT, fill=Y)
        self.chain_list.configure(yscrollcommand=scroll.set)
        scroll.config(command=self.chain_list.yview)

        pre_button = s_button.SButton(self.choose_chain_tab, "上一步", 10, 170)
        pre_button.button.bind("<Button-1>", self.jump_model)

        next_button = s_button.SButton(self.choose_chain_tab, "下一步", 165, 170)
        next_button.button.bind("<Button-1>", self.jump_ligand)

    def jump_ligand(self, event):
        self.chain_name = self.chain_list.get(ACTIVE)
        chain = self.structure[self.model_name][self.chain_name]
        het_names = ReceptorProcessor.get_het_ids(chain)
        Tab3.refresh_listbox(het_names, self.ligand_list)

        # 禁用两个
        self.notebook.tab(0, state="disable")
        self.notebook.tab(2, state="normal")
        self.notebook.tab(1, state="disable")

        self.notebook.select(tab_id=2)

    def choose_ligand(self):
        self.ligand_list = Listbox(self.choose_ligand_tab, width=30, height=10)
        self.ligand_list.place(x=10, y=10, width=255, height=150)
        scroll = Scrollbar(self.ligand_list)
        scroll.pack(side=RIGHT, fill=Y)
        self.ligand_list.configure(yscrollcommand=scroll.set)
        scroll.config(command=self.ligand_list.yview)

        pre_button = s_button.SButton(self.choose_ligand_tab, "上一步", 10, 170)
        pre_button.button.bind("<Button-1>", self.jump_chain)

        next_button = s_button.SButton(self.choose_ligand_tab, "提取配体", 165, 170)
        tooltip.create_tooltip(next_button.button, "提取选中的配体为pdbqt格式")
        next_button.button.bind("<Button-1>", self.save_ligand)

    def save_ligand(self, event):
        self.ligand_name = self.ligand_list.get(ACTIVE)

        python_path = configer.Configer.get_para("python_path")
        if not check.Check.check_python(python_path):
            return

        LigandExtractor(self.structure, self.model_name,
                        self.chain_name, self.ligand_name).extract_ligand(self.output_path)

        input_ligand = self.output_path + "/%s_%s.pdb" % (self.chain_name, self.ligand_name)
        output_ligand = self.output_path + "/%s_%s.pdbqt" % (self.chain_name, self.ligand_name)
        command = "%s %s -l %s -o %s" % (python_path, pdb_to_pdbqt_path,
                                         input_ligand, output_ligand)
        os.system(command)
        os.remove(input_ligand)
        messagebox.showinfo("提取成功！", "成功提取配体！")

    @staticmethod
    def refresh_listbox(content_list: list, list_box: Listbox):
        list_box.delete(0, END)
        for content in content_list:
            list_box.insert(END, content)

    def prepared_receptor(self, event):
        input_file = self.choose_raw_receptor_entry.textvariable.get()
        output_path = self.choose_prepare_output_path.textvariable.get()
        output_file = output_path + "/preped.pdbqt"
        python_path = configer.Configer.get_para("python_path")

        if not check.Check.check_python(python_path):
            return

        if check.Check.check_path(input_file) or check.Check.check_path(output_path):
            messagebox.showinfo("错误！", "输入文件不能包含空格")
            return

        if not input_file.endswith(".pdb"):
            messagebox.showinfo("错误!", "只支持输入pdb文件！")
            return

        message = ChainExtractor.judge_homo(input_file)
        if message:
            warning = ""
            for content in message:
                warning += content + "\n"
            if messagebox.askyesno("检测到同源链", "是否保留只保留特定链？（可多选）\n" + warning):
                structure = ReceptorProcessor.get_structure(input_file)
                chains_ids = ReceptorProcessor.get_chain_ids(structure[0])

                top = STopLevel(self.root, 275, 205, "选择要保存的链").toplevel

                chains_list = Listbox(top, width=30, height=10, selectmode=EXTENDED)
                chains_list.place(x=10, y=10, width=255, height=150)
                self.refresh_listbox(chains_ids, chains_list)
                scroll = Scrollbar(chains_list)
                scroll.pack(side=RIGHT, fill=Y)
                chains_list.configure(yscrollcommand=scroll.set)
                scroll.config(command=chains_list.yview)

                def extract_chains():
                    Tab3.chains = []
                    selections = chains_list.curselection()
                    for select in selections:
                        Tab3.chains.append(chains_list.get(select))
                    top.destroy()

                save_button = s_button.SButton(top, "提取链", 10, 170)
                save_button.button.configure(command=extract_chains)

                def cancel():
                    Tab3.chains = None
                    top.destroy()

                cancel_button = s_button.SButton(top, "取消", 165, 170)
                cancel_button.button.configure(command=cancel)

                top.protocol("WM_DELETE_WINDOW", cancel)

                self.root.wait_window(top)
            else:
                Tab3.chains = []
        else:
            messagebox.showinfo("没有检测到同源链", "受体将自动保存为preped.pdbqt文件")
            Tab3.chains = []

        if Tab3.chains is None:
            return

        structure = ReceptorProcessor.get_structure(input_file)
        ChainExtractor.extract_chain(structure, Tab3.chains, output_path)

        pdb_input = output_path + "/preped.pdb"
        cmd = "%s %s -r %s -o %s -e" % (python_path, prepare_receptor4_path, pdb_input, output_file)
        os.system(cmd)
        messagebox.showinfo("成功", "成功准备受体！\n注意：自动准备会删除DNA等非标准残基，结果仅供参考。")

    def save_para(self):
        self.config.para_dict["pdbid"] = self.pdbid_entry.textvariable.get()
        self.config.para_dict["pdb_path"] = self.pdb_save_path_entry.textvariable.get()
        self.config.para_dict["extract_ligand_path"] = self.ligand_save_path_entry.textvariable.get()
        self.config.para_dict["raw_receptor_path"] = self.choose_raw_receptor_entry.textvariable.get()
        self.config.para_dict["preped_path"] = self.choose_prepare_output_path.textvariable.get()


class Tab5(object):  # 复合

    def __init__(self, tab, config):
        self.root = tab
        self.config = config

        self._choose_ligand_frame()
        self._choose_protein_frame()
        self._choose_output_frame()
        self._start_join()

        # 帮助按钮
        self.help_button = s_button.HelpButton(root=self.root, help_text=help_text.TAB5_TEXT, x=410, y=300, width=80)
        tooltip.create_tooltip(self.help_button.help_button, "获取帮助")

    def _choose_ligand_frame(self):
        self.choose_ligand_labelframe = LabelFrame(self.root, text="选择配体")
        self.choose_ligand_labelframe.place(x=10, y=10, width=570, height=85)

        # 选择输入配体的格式
        s_label.SLabel(root=self.choose_ligand_labelframe, text="输入格式：",
                       x=10, y=0)
        input_format_text = ("pdbqt", "sdf", "mol2", "pdb")
        self.input_format = s_combobox.SCombbox(root=self.choose_ligand_labelframe, textvariable=StringVar(),
                                                values=input_format_text,
                                                default_value=configer.Configer.get_para("complex_ligand_format"),
                                                x=80, y=0, width=60)
        tooltip.create_tooltip(self.input_format.combobox, "导入配体的格式")

        # 选择第几个配体
        s_label.SLabel(root=self.choose_ligand_labelframe, text="选择第",
                       x=160, y=0)
        self.complex_ligand_num_entry = s_entry.SEntry(self.choose_ligand_labelframe, textvariable=StringVar(),
                                                       text=configer.Configer.get_para("complex_ligand_num"),
                                                       x=205, y=2, width=20)
        tooltip.create_tooltip(self.complex_ligand_num_entry.entry, "只针对多构象pdbqt文件。输入"
                                                                    "要进行复合的构象")
        s_label.SLabel(root=self.choose_ligand_labelframe, text="个构象",
                       x=230, y=0)

        # 是否保留提取配体
        self.remain_ligand = s_checkbox.SCheckbutton(self.choose_ligand_labelframe,
                                                     text="保留提取构象", variable=StringVar(),
                                                     value=configer.Configer.get_para("remain_ligand"),
                                                     x=280, y=0)
        tooltip.create_tooltip(self.remain_ligand.checkbutton, "只针对多构象pdbqt文件。"
                                                               "保留提取的构象。")

        # 选择配体
        self.choose_ligands_button = s_button.SButton(self.choose_ligand_labelframe, text="选择单/多个配体", x=10, y=30)
        tooltip.create_tooltip(self.choose_ligands_button.button, "选择一个或者多个所选格式的配体")
        self.choose_ligand_dir_button = s_button.SButton(self.choose_ligand_labelframe, text="选择文件夹", x=110, y=30)
        tooltip.create_tooltip(self.choose_ligand_dir_button.button, "选择包含配体的文件夹，匹配其中所选格式的文件")
        self.choose_ligands_entry = s_entry.SEntry(root=self.choose_ligand_labelframe, textvariable=StringVar(),
                                                   text=configer.Configer.get_para("choose_complex_ligands"),
                                                   x=200, y=34, width=360)
        tooltip.create_tooltip(self.choose_ligands_entry.entry, "所选的配体或者包含配体的目录")
        self.choose_ligands_button.bind_open_files(entry_text=self.choose_ligands_entry.textvariable,
                                                   title="选择单/多个配体",
                                                   file_type=self.input_format.textvariable)
        self.choose_ligand_dir_button.bind_open_dir(entry_text=self.choose_ligands_entry.textvariable,
                                                    title="选择包含配体文件的文件夹")

    def _choose_protein_frame(self):
        self.choose_protein_labelframe = LabelFrame(self.root, text="选择受体")
        self.choose_protein_labelframe.place(x=10, y=100, width=570, height=50)

        self.choose_proteins = s_button.SButton(root=self.choose_protein_labelframe, text="选择受体", x=10, y=0)
        tooltip.create_tooltip(self.choose_proteins.button, "选择pdbqt格式的受体")
        self.choose_proteins_entry = s_entry.SEntry(root=self.choose_protein_labelframe, textvariable=StringVar(),
                                                    text=configer.Configer.get_para("choose_complex_proteins"),
                                                    x=110, y=4, width=450)
        tooltip.create_tooltip(self.choose_proteins_entry.entry, "受体文件")
        self.choose_proteins.bind_open_file(entry_text=self.choose_proteins_entry.textvariable,
                                            title="选择蛋白受体", file_type="pdbqt")

    def _choose_output_frame(self):
        self.choose_output_labelframe = LabelFrame(self.root, text="复合物输出")
        self.choose_output_labelframe.place(x=10, y=155, width=570, height=50)

        self.choose_output = s_button.SButton(root=self.choose_output_labelframe, text="选择输出文件夹", x=10, y=0)
        tooltip.create_tooltip(self.choose_output.button, "选择复合物输出目录")
        self.choose_output_entry = s_entry.SEntry(root=self.choose_output_labelframe, textvariable=StringVar(),
                                                  text=configer.Configer.get_para("choose_complex_output"),
                                                  x=110, y=4, width=450)
        tooltip.create_tooltip(self.choose_output_entry.entry, "所选的复合物输出目录")
        self.choose_output.bind_open_dir(entry_text=self.choose_output_entry.textvariable,
                                         title="选择复合物输出的文件夹")

    def _start_join(self):
        y = 220
        self.docking_button = s_button.SButton(root=self.root, text="结合", x=10, y=y)
        tooltip.create_tooltip(self.docking_button.button, "将配体和受体结合成一个文件")
        self.docking_button.button.bind("<Button-1>", self._join)

        self.progress = Progressbar(self.root, mode="determinate")
        self.progress.place(x=100, y=y + 2, width=400)
        tooltip.create_tooltip(self.progress, "结合进度")

        self.progress_label = s_label.SLabel(self.root, text="没有任务", x=510, y=y)

        text_y = 256
        self.current_ligand_frame = Frame(self.root, width=400, height=40)
        self.current_ligand_frame.place(x=10, y=text_y)
        self.current_ligand = s_label.SLabel(root=self.current_ligand_frame, text="", x=0, y=0)

    def _join(self, event):
        input_format = self.input_format.textvariable.get()
        input_ligands_full = self.choose_ligands_entry.entry.get()
        input_receptor = self.choose_proteins_entry.entry.get()
        output_dir = self.choose_output_entry.entry.get()
        choose_num = self.complex_ligand_num_entry.entry.get()
        remain = self.remain_ligand.variable.get()

        # 所有选择的路径和文件都不能为空。
        if input_ligands_full == "" or input_receptor == "" or output_dir == "":
            messagebox.showerror("错误！", "输入不能为空！")
            return

        # 不能包括空格
        if check.Check.has_space(input_ligands_full):
            messagebox.showerror("错误！", "配体路径不能包含空格！")
            return
        if check.Check.has_space(input_receptor):
            messagebox.showerror("错误！", "受体路径不能包含空格！")
            return
        if check.Check.has_space(output_dir):
            messagebox.showerror("错误！", "输出路径不能包含空格！")
            return

        # 选择构象要是数字
        try:
            num = int(choose_num)
        except ValueError:
            messagebox.showerror("错误！", "提取的构象必须是数字！")
            return

        # 输出路径必须存在
        if not os.path.exists(output_dir):
            messagebox.showerror("错误！", "输出的路径不存在！")
            return

        # 受体格式必须是pdbqt
        if not input_receptor.endswith(".pdbqt"):
            messagebox.showerror("错误！", "输入的受体必须是pdbqt格式。")
            return

        input_ligands = []

        # 输入的配体
        if input_ligands_full.endswith(";"):  # 如果是单个或者多个配体
            if input_ligands_full.split(".")[-1][0:-1] != input_format:  # 格式不匹配
                messagebox.showerror("错误！", "配体格式不是所选格式！")
                return
            input_ligands.extend(input_ligands_full.split(";")[0:-1])
        elif os.path.isdir(input_ligands_full):  # 如果选择的是目录
            list_file = os.listdir(input_ligands_full)
            for file in list_file:
                if file.endswith(input_format):
                    input_ligands.append(input_ligands_full + "/" + file)
            if len(input_ligands) == 0:
                messagebox.showerror("错误！", "所选文件夹中不包含%s格式的配体！" % input_format)
                return
        else:
            messagebox.showerror("错误！", "请检查输入的配体！")
            return

        python_path = configer.Configer.get_para("python_path")

        # 检查路径是否正确
        if not check.Check.check_python(python_path):
            return
        obabel_path = configer.Configer.get_para("obabel_path")
        if not check.Check.check_obabel(obabel_path):
            return

        self.progress_label.label.configure(text="准备受体")
        self.progress_label.label.update()

        # 将受体pdbqt转成pdb
        input_pdb = output_dir + "/" + input_receptor.split(".")[0].split("/")[-1] + ".pdb"
        command = "%s %s -f %s -o %s" % (python_path, pdbqt_to_pdb_path,
                                         input_receptor, input_pdb)
        os.system(command)

        ligands = []

        self.progress_label.label.configure(text="准备配体")
        self.progress_label.label.update()

        if input_format == "pdbqt":
            for ligand in input_ligands:
                # 是否是单个配体:
                with open(ligand, "r") as f:
                    line = f.readline()
                    if "MODEL" not in line:
                        # 只有一个，直接转换成pdb
                        pdb_ligand = output_dir + "/" + ligand.split(".")[0].split("/")[-1] + ".pdb"
                        command = "%s %s -f %s -o %s" % (python_path, pdbqt_to_pdb_path,
                                                         ligand, pdb_ligand)
                        os.system(command)
                        ligands.append(pdb_ligand)
                    else:
                        # 指针归位
                        f.seek(0)
                        # 有多个，提取之后转pdb
                        first_lines = []
                        last_lines = []
                        for (line_num, line_value) in enumerate(f):
                            if line_value.startswith("MODEL"):
                                first_lines.append(line_num)
                            if line_value == "ENDMDL\n":
                                last_lines.append(line_num)

                        # 如果选择构象大于实际构象
                        try:
                            first_line = first_lines[num - 1]
                            last_line = last_lines[num - 1] + 1
                            max_num = choose_num
                        except IndexError:
                            first_line = first_lines[-1]
                            last_line = last_lines[-1] + 1
                            max_num = str(len(first_lines))

                        f.seek(0)
                        splited_molecule = f.readlines()[first_line:last_line]
                        output_pdbqt = output_dir + "/" + ligand.split(".")[0].split("/")[
                            -1] + "_" + max_num + ".pdbqt"
                        with open(output_pdbqt, "w") as writer:
                            writer.writelines(splited_molecule)
                        output_pdb = output_dir + "/" + ligand.split(".")[0].split("/")[
                            -1] + "_" + max_num + ".pdb"
                        command = "%s %s -f %s -o %s" % (python_path, pdbqt_to_pdb_path,
                                                         output_pdbqt, output_pdb)
                        os.system(command)
                        os.remove(output_pdbqt)
                        ligands.append(output_pdb)
        else:
            ligands = input_ligands

        # 进行复合
        self.progress["maximum"] = len(ligands)
        for ligand in ligands:
            # 更新进度条
            label_text = str(ligands.index(ligand) + 1) + "/" + str(len(ligands))
            self.progress_label.label.configure(text=label_text)
            self.progress_label.label.update()

            self.progress["value"] = ligands.index(ligand) + 1
            self.progress.update()

            current_ligand = "当前配体：%s" % ligand.split("/")[-1].split(".")[0]
            self.current_ligand.label.configure(text=current_ligand)
            self.current_ligand.label.update()

            output_name = ligand.split("/")[-1].split(".")[0] + "_" + input_receptor.split("/")[-1].split(".")[
                0] + ".pdb"
            output = output_dir + "/" + output_name
            command = "%s %s %s -j -O %s" % (obabel_path, ligand, input_pdb, output)
            os.system(command)

        # 如果不保留提取配体，删除提取配体
        if input_format == "pdbqt" and remain == "0":
            for ligand in ligands:
                os.remove(ligand)

        # 删除受体
        os.remove(input_pdb)

        messagebox.showinfo("成功！", "生成复合物成功！")
        self.progress_label.label.configure(text="没有任务")
        self.progress_label.label.update()

        self.progress["value"] = 0
        self.progress.update()

        self.current_ligand.label.configure(text="")
        self.current_ligand.label.update()

    def save_para(self):
        self.config.para_dict["complex_ligand_format"] = self.input_format.textvariable.get()
        self.config.para_dict["complex_ligand_num"] = self.complex_ligand_num_entry.textvariable.get()
        self.config.para_dict["choose_complex_ligands"] = self.choose_ligands_entry.textvariable.get()
        self.config.para_dict["remain_ligand"] = self.remain_ligand.variable.get()
        self.config.para_dict["choose_complex_proteins"] = self.choose_proteins_entry.textvariable.get()
        self.config.para_dict["choose_complex_output"] = self.choose_output_entry.textvariable.get()


class Tab6(object):

    def __init__(self, tab):
        self.label1 = Label(tab, text=help_text.TAB6_TEXT, wraplength=565)
        self.label1.place(x=10, y=10)


class Tab7(object):

    def __init__(self, tab, config):
        self.config = config
        self.label1 = Label(tab, text="作用力分析，开发中")
        self.label1.grid()


class Tab8(object):

    def __init__(self, tab, config):
        self.config = config
        self.label1 = Label(tab, text="工具，开发中……")
        self.label1.grid()
