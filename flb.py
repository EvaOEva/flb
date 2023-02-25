# -*- coding: utf-8 -*-
# Author: TLLB
# Place: Gaoxin Chengdu
# Time: 2023/2/15 15:49
# File : main.py
# Project : new_app
import re
import json
import flet as ft
import time
import random
from flet_core import Page
from requests_html import HTMLSession
from lxml import etree


class FuLiBa_Photo(object):

    def __init__(self, page: ft.Page):#, page: ft.Page

        self.page = page
        self.cyd_url = "http://ciyuandao.com/photo/list/0-0-{}"
        self.vmgirls_url = "http://www.cnu.cc/discoveryPage/hot-111?page={}"
        self.flhz_url = "https://fuliba23.net/flhz/page/{}"
        self.tikwm_url = "https://www.tikwm.com/api/user/posts"

        def on_dialog_result(e: ft.FilePickerResultEvent):
            print("Selected files:", e.files)
            print("Selected file or directory:", e.path)

        self.file_picker = ft.FilePicker(on_result=self.on_dialog_result)
        self.page.overlay.append(self.file_picker)


        self.headers = {
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

        self.img_list = []
        self.page_middle = ''
        self.gallery_title = ''
        self.avgirls = "asuka.kirara"
        self.cursor = 0
        self.epath = ''


        self.cyd_images = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=220,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,

        )

        self.vmgirls_images = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=300,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,

        )

        self.tikwm_images = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=320,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,

        )

        self.flhz_images = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=300,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,

        )

        self.cyd_page = 0
        self.cnu_page = 0
        self.flhz_page = 0
        self.tiktok_page = 0

        self.page.views.clear()
        self.page.views.append(

            ft.Column(
                [ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(),
                 ft.Text(), ft.ProgressRing(), ft.Text("资源加载中..."), ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),

        )
        self.page.update()

        home_page_data = self.get_cyd_page(1)
        self.cyd = self.cyd_Module_Page(home_page_data)
        home_page_data = self.get_vmgirls_page(1)
        self.vmgirls = self.vmgirls_Module_Page(home_page_data)
        home_page_data = self.get_tikwm_page(self.cursor,self.avgirls)
        self.tikwm = self.tikwm_Module_Page(home_page_data)
        home_page_data = self.get_flhz_page(1)
        self.flhz = self.flhz_Module_Page(home_page_data)

        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.page.go(self.page.route)

    def on_click(self, e):
        self.page.views.append(

            ft.Column(
                [ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(),
                 ft.Text(), ft.ProgressRing(), ft.Text("资源加载中..."), ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),

        )
        self.page.update()
        self.img_list = self.get_info_img(e.control.data)
        self.page.views.pop()
        self.page_middle = ""
        self.page_middle = ft.Image(src=self.img_list[0], width=500, height=620, data=0)
        self.gallery_title = e.control.tooltip
        if "ciyuandao" in e.control.image_src:
            self.page.go("/gallery")
        elif 'cnu' in e.control.image_src:
            self.page.go("/cnu/gallery")
        elif 'fuliba' in e.control.image_src:
            self.page.go("/flhz/gallery")
        else:
            pass


    def on_hover(self,e):
        e.control.image_opacity = 0.7 if e.data == "true" else 1
        e.control.update()

    def download_video(self,e):
        url = e.control.data
        self.file_picker.save_file()
        while True:
            if self.epath  == "":
                continue
            else:
                break
        session = HTMLSession()
        self.page.views.append(

            ft.Column(
                [ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(),
                 ft.Text(), ft.ProgressRing(), ft.Text("视频下载中..."), ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),

        )
        self.page.update()
        r = session.get(url)
        with open(f'{self.epath}', 'wb') as f:
            f.write(r.content)
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("视频下载完成"),
            action="确定",
        )
        self.page.snack_bar.open = True
        self.page.views.pop()
        self.epath = ""
        self.page.update()

    def on_dialog_result(self,e: ft.FilePickerResultEvent):
        self.epath = e.path


    def save_file_result(self,e: ft.FilePickerResultEvent):
        url = "https://www.tikwm.com//video/media/play/7174690953121385730.mp4"
        session = HTMLSession()
        r = session.get(url)
        aa = e.path if e.path else "Cancelled!"
        with open(f'{aa}','wb') as f:
            f.write(r.content)



    def cyd_Module_Page(self,home_page_data):
        img_title = home_page_data[2]
        img_src = home_page_data[0]
        img_url = home_page_data[1]
        for i in range(0, len(img_title)):
            self.cyd_images.controls.append(
                ft.Container(
                    bgcolor=ft.colors.BLUE_GREY_50,
                    border_radius=ft.border_radius.all(10),
                    margin=1,
                    padding=1,
                    tooltip=f'{img_title[i]}',
                    on_hover = self.on_hover,
                    on_click=self.on_click,
                    ink=True,
                    image_src=img_src[i],
                    data=f"http://ciyuandao.com{img_url[i]}",
                    image_opacity = 1,

                )
            )

        return self.cyd_images

    def vmgirls_Module_Page(self,home_page_data):
        img_title = home_page_data[2]
        img_src = home_page_data[0]
        img_url = home_page_data[1]
        for i in range(0, len(img_title)):
            self.vmgirls_images.controls.append(
                ft.Container(
                    bgcolor=ft.colors.BLUE_GREY_50,
                    border_radius=ft.border_radius.all(10),
                    margin=1,
                    padding=1,
                    tooltip=f'{img_title[i]}',
                    on_hover=self.on_hover,
                    on_click=self.on_click,
                    ink=True,
                    image_src=img_src[i],
                    data=f"{img_url[i]}",
                    image_opacity=1,

                )
            )
        return self.vmgirls_images


    def tikwm_Module_Page(self,home_page_data):
        # print(home_page_data)
        img_title = home_page_data[2]
        img_src = home_page_data[0]
        img_url = home_page_data[1]
        for i in range(0, len(img_title)):
            self.tikwm_images.controls.append(
                ft.Container(
                    bgcolor=ft.colors.BLUE_GREY_50,
                    border_radius=ft.border_radius.all(10),
                    margin=1,
                    padding=1,
                    tooltip=f'{img_title[i]}',
                    on_hover=self.on_hover,
                    on_click=self.download_video,
                    ink=True,
                    image_src=img_src[i],
                    data=f"{img_url[i]}",
                    image_opacity=1,

                )
            )
        return self.tikwm_images


    def flhz_Module_Page(self,home_page_data):
        img_title = home_page_data[2]
        img_src = home_page_data[0]
        img_url = home_page_data[1]
        for i in range(0, len(img_title)):
            self.flhz_images.controls.append(
                ft.Container(
                    bgcolor=ft.colors.BLUE_GREY_50,
                    border_radius=ft.border_radius.all(10),
                    margin=1,
                    padding=1,
                    tooltip=f'{img_title[i][0:-4]}',
                    on_hover=self.on_hover,
                    on_click=self.on_click,
                    ink=True,
                    image_src=img_src[i],
                    data=f"{img_url[i]}",
                    image_opacity=1,

                )
            )
        return self.flhz_images



    def get_cyd_page(self,page):
        session = HTMLSession()
        r = session.get(self.cyd_url.format(page),headers = self.headers)
        img_src = r.html.xpath('.//li[@class="font12 fleft"]/a/img/@src')
        img_url = r.html.xpath('.//li[@class="font12 fleft"]/a/@href')
        img_title = r.html.xpath('.//li[@class="font12 fleft"]/p[1]/a/text()')
        return img_src,img_url,img_title

    def get_vmgirls_page(self,page):
        session = HTMLSession()
        r = session.get(self.vmgirls_url.format(page),headers = self.headers)
        img_src = r.html.xpath('.//div[@class="grid-item work-thumbnail"]/a/img/@src')
        img_title = r.html.xpath('.//div[@class="grid-item work-thumbnail"]/a/img/@alt')
        img_url = r.html.xpath('.//div[@class="grid-item work-thumbnail"]/a/@href')
        return img_src,img_url,img_title

    def get_tikwm_page(self,cursor,name):
        session = HTMLSession()
        data = {"unique_id":name,"count":12,"cursor":cursor,"web":1,"hd":1}
        r = session.post(self.tikwm_url,headers = self.headers,data = data)
        r_dict = json.loads(r.html.text)
        videos_list = r_dict["data"]["videos"]
        self.cursor = r_dict["data"]["cursor"]
        img_src = []
        img_title = []
        img_url = []
        for video in videos_list:
            src = "https://www.tikwm.com/" + video["cover"]
            title = video["title"]
            url = "https://www.tikwm.com/" + video["play"]
            img_src.append(src)
            img_title.append(title)
            img_url.append(url)

        return img_src,img_url,img_title


    def get_flhz_page(self,page):
        session = HTMLSession()
        r = session.get(self.flhz_url.format(page),headers = self.headers)
        img_src = r.html.xpath('.//img[@class="thumb"]/@data-src')
        img_title = r.html.xpath('.//img[@class="thumb"]/@alt')
        img_url = r.html.xpath('.//a[@class="focus"]/@href')
        return img_src, img_url, img_title


    def get_info_img(self,img_url):
        session = HTMLSession()
        r = session.get(img_url,headers = self.headers)
        if "ciyuandao" in img_url:
            img_src = r.html.xpath('.//p[@class="mbottom10"]/a/img/@src')
        elif "cnu" in img_url:
            ll = []
            img_src = r.html.xpath('.//div[@id="imgs_json"]/text()')[0]
            for img in json.loads(img_src):
                ll.append(f'http://imgoss.cnu.cc/{img["img"]}?x-oss-process=style/content')
            img_src = ll
        elif "fuliba" in img_url:
            last_page = r.html.xpath('.//div[@class="article-paging"]/a')
            r = session.get(f"{img_url}{'/'}{len(last_page) + 1}",headers = self.headers)
            img_src = r.html.xpath('.//img[@decoding="async"]/@src')
        return img_src

    def next_click(self, e):
        self.page_middle.data += 1
        if self.page_middle.data >= len(self.img_list):
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("到底啦福娃,后面没有内容了"),
                action="确定",
            )
            self.page.snack_bar.open = True
            self.page.update()
        else:
            if "[" in self.img_list[0]:
                self.page_middle.src = f'http://imgoss.cnu.cc/{json.loads(self.img_list)[self.page_middle.data]["img"]}?x-oss-process=style/content'
            else:
                self.page_middle.src = self.img_list[self.page_middle.data]
            self.page.update()

    def before_click(self, e):
        if self.page_middle.data == 0:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("已经是第一张啦!"),
                action="确定",
            )
            self.page.snack_bar.open = True
            self.page.update()
        else:
            self.page_middle.data -= 1
            if "[" in self.img_list[0]:
                self.page_middle.src = f'http://imgoss.cnu.cc/{json.loads(self.img_list)[self.page_middle.data]["img"]}?x-oss-process=style/content'
            else:
                self.page_middle.src = self.img_list[self.page_middle.data]
            self.page.update()

    def cyd_refresh_click(self,e):
        self.cyd_images.clean()
        self.cyd_page  += 1
        if self.cyd_page > 450:
            self.cyd_page = 1
        home_page_data = self.get_cyd_page(self.cyd_page)
        self.cyd = self.cyd_Module_Page(home_page_data)
        self.page.go(self.page.route)

    def vmgirls_refresh_click(self,e):
        self.vmgirls_images.clean()
        self.cnu_page += 1
        if self.cnu_page > 320:
            self.cnu_page = 1
        home_page_data = self.get_vmgirls_page(self.cnu_page)
        self.vmgirls = self.vmgirls_Module_Page(home_page_data)
        self.page.go('/cnu')


    def flhz_refresh_click(self,e):
        self.flhz_images.clean()
        self.flhz_page += 1
        if self.flhz_page > 13:
            self.flhz_page = 1
        home_page_data = self.get_vmgirls_page(self.flhz_page)
        self.flhz = self.flhz_Module_Page(home_page_data)
        self.page.go('/flhz')


    def tiktok_refresh_click(self,e):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("每10秒请求一次,请耐心等待"),
            action="确定",
        )
        self.page.snack_bar.open = True
        if e.control.data == 0:
            self.tikwm_images.clean()
            # self.page.update()
            self.page.views.append(
                ft.Column(
                    [ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(),
                     ft.Text(), ft.ProgressRing(), ft.Text("资源加载中..."), ], alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),

            )
            self.page.update()
            home_page_data = self.get_tikwm_page(self.cursor, self.avgirls)
            self.tikwm = self.tikwm_Module_Page(home_page_data)
            time.sleep(10)
            self.page.views.pop()
            self.page.go('/tikwm')
        try:
            if e.control.value == self.avgirls:
                pass
            else:
                self.tikwm_images.clean()
                self.avgirls = e.control.value
                self.cursor = 0
                self.page.views.append(
                    ft.Column(
                        [ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(), ft.Text(),
                         ft.Text(), ft.ProgressRing(), ft.Text("资源加载中..."), ], alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                )
                self.page.update()
                home_page_data = self.get_tikwm_page(self.cursor,self.avgirls)
                self.tikwm = self.tikwm_Module_Page(home_page_data)
                time.sleep(10)
                self.page.views.pop()
                self.page.go('/tikwm')
        except:
            pass

    def wm_click(self, e):
        text = e.control.text
        if text == '次元岛':
            self.page.go('./')
        elif text == "CNU":
            self.page.go('/cnu')
        elif text == "福利汇总":
            self.page.go('/flhz')
        else:
            self.page.go('/tikwm')


    def route_change(self,route):
        self.page.views.clear()
        self.page.views.append(
            ft.View(
                "/",
                [
                    ft.FloatingActionButton(
                        content=ft.Row([ft.Icon(ft.icons.REFRESH), ft.Text("更多")], alignment="center", spacing=5),
                        bgcolor=ft.colors.AMBER_300,
                        shape=ft.RoundedRectangleBorder(radius=5),
                        width=100,
                        mini=True,
                        on_click=self.cyd_refresh_click,),
                    self.cyd,
                    ft.AppBar(
                        leading=ft.Icon(ft.icons.PALETTE),
                        leading_width=40,
                        toolbar_height=50,
                        title=ft.Text("次元岛"),
                        center_title=False,
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        actions=[
                            ft.PopupMenuButton(
                                items=[
                                    ft.PopupMenuItem(text="次元岛", checked=True, on_click=''),
                                    ft.PopupMenuItem(),
                                    ft.PopupMenuItem(text="CNU", checked=False, on_click=self.wm_click),
                                    ft.PopupMenuItem(text="福利汇总", checked=False, on_click=self.wm_click),
                                    ft.PopupMenuItem(text="TikTok", checked=False, on_click=self.wm_click),
                                ]
                            ),
                        ],
                    )
                    # ft.NavigationBar(destinations=[
                    # ft.NavigationDestination(icon=ft.icons.ACCESSIBLE_FORWARD, label="次元岛",selected_icon_content=ft.Icon(ft.icons.ACCESS_ALARM_OUTLINED)),
                    # ft.NavigationDestination(icon=ft.icons.COMMUTE, label="唯美女生",selected_icon_content=ft.Icon(ft.icons.CABIN_OUTLINED)),
                    # ft.NavigationDestination(icon=ft.icons.COMMUTE, label="爱美女",selected_icon_content=ft.Icon(ft.icons.CABIN_OUTLINED))],
                    # on_change=self.wm_click)
                ]
            )
        )

        if self.page.route == "/cnu" or self.page.route == "/cnu/gallery":
            # self.page.views.clear()
            self.page.views.append(
                ft.View(
                    "/cnu",
                    [
                        ft.FloatingActionButton(
                            content=ft.Row([ft.Icon(ft.icons.MORE_HORIZ_ROUNDED), ft.Text("更多")], alignment="center",spacing=5),
                            bgcolor=ft.colors.AMBER_300,
                            shape=ft.RoundedRectangleBorder(radius=5),
                            width=100,
                            mini=True,
                            on_click=self.vmgirls_refresh_click),
                        self.vmgirls,
                        ft.AppBar(
                            leading=ft.Icon(ft.icons.PALETTE),
                            leading_width=40,
                            toolbar_height=50,
                            title=ft.Text("CNU"),
                            center_title=False,
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            actions=[
                                ft.PopupMenuButton(
                                    items=[
                                        ft.PopupMenuItem(text="CNU", checked=True, on_click=''),
                                        ft.PopupMenuItem(),
                                        ft.PopupMenuItem(text="次元岛", checked=False, on_click=self.wm_click),
                                        ft.PopupMenuItem(text="福利汇总", checked=False, on_click=self.wm_click),
                                        ft.PopupMenuItem(text="TikTok", checked=False, on_click=self.wm_click),
                                    ]
                                ),
                            ],
                        )
                        # ft.NavigationBar(destinations=[
                        #     ft.NavigationDestination(icon=ft.icons.ACCESSIBLE_FORWARD, label="次元岛"),
                        #     ft.NavigationDestination(icon=ft.icons.COMMUTE, label="唯美女生"),
                        #     ft.NavigationDestination(icon=ft.icons.COMMUTE, label="爱美女"), ],
                        #     on_change=self.wm_click)

                    ]
                )
            )

        if self.page.route == "/cnu/gallery":
            # self.page.views.append(
            #     ft.Column(
            #         [ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.ProgressRing(),ft.Text(),], alignment=ft.MainAxisAlignment.CENTER,
            #         horizontal_alignment=ft.CrossAxisAlignment.CENTER
            #     ),
            # )
            # self.page.update()
            # time.sleep(2)
            # self.page.views.pop()
            self.page.views.append(
                ft.View(
                    "/cnu/gallery",
                    [
                        ft.AppBar(title=ft.Text(self.gallery_title), bgcolor=ft.colors.SURFACE_VARIANT,leading_width=40,
                        toolbar_height=50,),
                        ft.Row([ft.IconButton(ft.icons.NAVIGATE_BEFORE,on_click=self.before_click),self.page_middle,ft.IconButton(ft.icons.NAVIGATE_NEXT,on_click=self.next_click)],alignment=ft.MainAxisAlignment.CENTER,),
                    ],

                )
            )

        if self.page.route == "/gallery":
            # self.page.views.append(
            #     ft.Column(
            #         [ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.ProgressRing(),ft.Text(),], alignment=ft.MainAxisAlignment.CENTER,
            #         horizontal_alignment=ft.CrossAxisAlignment.CENTER
            #     ),
            # )
            # self.page.update()
            # time.sleep(2)
            # self.page.views.pop()
            self.page.views.append(
                ft.View(
                    "/gallery",
                    [
                        ft.AppBar(title=ft.Text(self.gallery_title), bgcolor=ft.colors.SURFACE_VARIANT,leading_width=40,
                        toolbar_height=50,),
                        ft.Row([ft.IconButton(ft.icons.NAVIGATE_BEFORE,on_click=self.before_click),self.page_middle,ft.IconButton(ft.icons.NAVIGATE_NEXT,on_click=self.next_click)],alignment=ft.MainAxisAlignment.CENTER,),
                    ],

                )
            )


        if self.page.route == "/tikwm" or self.page.route == "/tikwm/gallery":
            # self.page.views.clear()
            self.page.views.append(
                ft.View(
                    "/tikwm",
                    [
                        ft.FloatingActionButton(
                            content=ft.Row([ft.Icon(ft.icons.REFRESH), ft.Text("更多")], alignment="center",spacing=5),
                            bgcolor=ft.colors.AMBER_300,
                            shape=ft.RoundedRectangleBorder(radius=5),
                            width=100,
                            mini=True,
                            data = 0,
                            on_click=self.tiktok_refresh_click),
                        self.tikwm,
                        ft.AppBar(
                            leading=ft.Icon(ft.icons.PALETTE),
                            leading_width=40,
                            toolbar_height=50,
                            title=ft.Text("TikTok"),
                            center_title=False,
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            actions=[
                                ft.RadioGroup(content=ft.Row([
                                    ft.Radio(value="fukada0318", label="深田咏美"),
                                    ft.Radio(value="asuka.kirara", label="明日花绮罗"),
                                    ft.Radio(value="yua_nikami", label="三上悠亚")],alignment=ft.MainAxisAlignment.CENTER), on_change=self.tiktok_refresh_click),
                                ft.Text("             "),
                                ft.PopupMenuButton(
                                    items=[
                                        ft.PopupMenuItem(text="TikTok", checked=True, on_click=''),
                                        ft.PopupMenuItem(),
                                        ft.PopupMenuItem(text="次元岛", checked=False, on_click=self.wm_click),
                                        ft.PopupMenuItem(text="CNU", checked=False, on_click=self.wm_click),
                                        ft.PopupMenuItem(text="福利汇总", checked=False, on_click=self.wm_click),
                                    ]
                                ),

                            ],
                        ),

                        # ft.NavigationBar(destinations=[
                        #     ft.NavigationDestination(icon=ft.icons.ACCESSIBLE_FORWARD, label="次元岛"),
                        #     ft.NavigationDestination(icon=ft.icons.COMMUTE, label="唯美女生"),
                        #     ft.NavigationDestination(icon=ft.icons.COMMUTE, label="爱美女"), ],
                        #     on_change=self.wm_click)

                    ]
                )
            )

        if self.page.route == "/tikwm/gallery":
            # self.page.views.append(
            #     ft.Column(
            #         [ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.ProgressRing(),ft.Text(),], alignment=ft.MainAxisAlignment.CENTER,
            #         horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            # )
            # self.page.update()
            # time.sleep(3)
            # self.page.views.pop()
            self.page.views.append(
                ft.View(
                    "/tikwm/gallery",
                    [
                        ft.AppBar(title=ft.Text(self.gallery_title), bgcolor=ft.colors.SURFACE_VARIANT,leading_width=40,
                        toolbar_height=50,),
                        ft.Row([ft.IconButton(ft.icons.NAVIGATE_BEFORE,on_click=self.before_click),self.page_middle,ft.IconButton(ft.icons.NAVIGATE_NEXT,on_click=self.next_click),],alignment=ft.MainAxisAlignment.CENTER,),
                    ],

                )
            )


        if self.page.route == "/flhz" or self.page.route == "/flhz/gallery":
            # self.page.views.clear()
            self.page.views.append(
                ft.View(
                    "/flhz",
                    [
                        ft.FloatingActionButton(
                            content=ft.Row([ft.Icon(ft.icons.REFRESH), ft.Text("更多")], alignment="center",spacing=5),
                            bgcolor=ft.colors.AMBER_300,
                            shape=ft.RoundedRectangleBorder(radius=5),
                            width=100,
                            mini=True,
                            on_click=self.vmgirls_refresh_click),
                        self.flhz,
                        ft.AppBar(
                            leading=ft.Icon(ft.icons.PALETTE),
                            leading_width=40,
                            toolbar_height=50,
                            title=ft.Text("福利汇总"),
                            center_title=False,
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            actions=[
                                ft.PopupMenuButton(
                                    items=[
                                        ft.PopupMenuItem(text="福利汇总", checked=True, on_click=''),
                                        ft.PopupMenuItem(),
                                        ft.PopupMenuItem(text="次元岛", checked=False, on_click=self.wm_click),
                                        ft.PopupMenuItem(text="CNU", checked=False, on_click=self.wm_click),
                                        ft.PopupMenuItem(text="TikTok", checked=False, on_click=self.wm_click),
                                    ]
                                ),
                            ],
                        )
                        # ft.NavigationBar(destinations=[
                        #     ft.NavigationDestination(icon=ft.icons.ACCESSIBLE_FORWARD, label="次元岛"),
                        #     ft.NavigationDestination(icon=ft.icons.COMMUTE, label="唯美女生"),
                        #     ft.NavigationDestination(icon=ft.icons.COMMUTE, label="爱美女"), ],
                        #     on_change=self.wm_click)

                    ]
                )
            )

        if self.page.route == "/flhz/gallery":
            # self.page.views.append(
            #     ft.Column(
            #         [ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.Text(),ft.ProgressRing(),ft.Text(),], alignment=ft.MainAxisAlignment.CENTER,
            #         horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            # )
            # self.page.update()
            # time.sleep(3)
            # self.page.views.pop()
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("随缘观看，挂图也是因为太大了，不用反馈,等待超过10秒就是挂了"),
                action="确定",
            )
            self.page.snack_bar.open = True
            self.page.views.append(
                ft.View(
                    "/flhz/gallery",
                    [
                        ft.AppBar(title=ft.Text(self.gallery_title), bgcolor=ft.colors.SURFACE_VARIANT,leading_width=40,
                        toolbar_height=50,),
                        ft.Row([ft.IconButton(ft.icons.NAVIGATE_BEFORE,on_click=self.before_click),self.page_middle,ft.IconButton(ft.icons.NAVIGATE_NEXT,on_click=self.next_click)],alignment=ft.MainAxisAlignment.CENTER,),
                    ],
                self.page.snack_bar
                )
            )

        self.page.update()



    def view_pop(self,view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)



def main(page: ft.Page):
    page.window_height = 727
    page.window_width = 635
    page.window_max_height = 727
    page.window_min_height = 727
    page.window_max_width = 635
    page.window_min_width = 635
    page.title = "wnflb2023 - Designed by 兔小小 in Chengdu "
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER



    page.add(ft.Text(""))
    c = FuLiBa_Photo(page)
    # page.add(c)
    # page.update()

ft.app(target=main)


