import tkinter as tk
from tkinter import messagebox
import random
import os
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Import Pillow modules

# Character pool and competitive teams
characters = [
    "Raiden", "Argenti", "Aventurine", "Bailu", "Black Swan", "Blade", "Boothill", 
    "Bronya", "Clara", "Dan Heng - Imbibitor Lunae", "Dr Ratio", "Feixiao", 
    "Firefly", "Fu Xuan", "Gepard", "Himeko", "Huohuo", "Jade", "Jiaoqiu", 
    "Jing Yuan", "Jingliu", "Kafka", "Lingsha", "Luocha", "Rappa", "Robin", 
    "Ruan Mei", "Seele", "Silver Wolf", "Sparkle", "Topaz", 
    "Trailblazer Fire", "Trailblazer Imaginary", "Trailblazer Physical", 
    "Welt", "Yanqing", "Yunli", "Arlan", "Asta", "Dan Heng", "Gallagher", 
    "Guinaifen", "Hanya", "Herta", "Hook", "Luka", "Lynx", "March 7th", 
    "March 7th Imaginary", "Misha", "Moze", "Natasha", "Pela", "Qingque", 
    "Sampo", "Serval", "Sushang", "Tingyun", "Xueyi", "Yukong", "Sunday"
]


competitive_teams = [
    #Raiden Teams
    ["Raiden", "Jiaoqiu", "Sparkle", "Aventurine"],
    ["Raiden", "Jiaoqiu", "Sparkle", "Fu Xuan"],
    ["Raiden", "Kafka", "Black Swan", "Aventurine"],
    ["Raiden", "Kafka", "Black Swan", "Huohuo"],
    ["Raiden", "Pela", "Sparkle", "Fu Xuan"],
    ["Raiden", "Jiaoqiu", "Pela", "Aventurine"],
    ["Raiden", "Kafka", "Black Swan", "Fu Xuan"],
    ["Raiden", "Jiaoqiu", "Pela", "Fu Xuan"],
    ["Raiden", "Pela", "Silver Wolf", "Fu Xuan"],
    ["Raiden", "Silver Wolf", "Sparkle", "Fu Xuan"],

    #Argenti
    ["Argenti", "Robin", "Tingyun", "Gallagher"],
    ["Jade", "Argenti", "Tingyun", "Aventurine"],
    ["Argenti", "Robin", "Sparkle", "Huohuo"],
    
    #Arlan has no teams lol
    ["Arlan", "Aventurine", "Robin", "Sunday"],
    
    #Asta
    ["Kafka", "Black Swan", "Asta", "Huohuo"],
    ["Firefly", "Asta", "Trailblazer Imaginary", "Lingsha"],
    ["Kafka", "Black Swan", "Asta", "Luocha"],
    ["Rappa", "Asta", "Ruan Mei", "Gallagher"],
    ["Himiko", "Asta", "Ruan Mei", "Aventurine"],
    ["Rappa", "Asta", "Trailblazer Imaginary", "Gallagher"],
    ["Firefly", "Asta", "Trailblazer Imaginary", "Gallagher"],
    ["Firefly", "Asta", "Trailblazer Imaginary", "Ruan Mei"],
    ["Kafka", "Black Swan", "Asta", "Bailu"],
    ["Rappa", "Asta", "Trailblazer Imaginary", "Lingsha"],
    
    #Aventurine
    ["Feixiao", "Topaz", "Robin", "Aventurine"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Aventurine"],
    ["Feixiao", "Moze", "Robin", "Aventurine"],
    ["Raiden", "Jiaoqiu", "Sparkle", "Aventurine"],
    ["Raiden", "Jiaoqiu", "Pela", "Aventurine"],
    ["Raiden", "Kafka", "Black Swan", "Aventurine"],
    ["Dr Ratio", "Topaz", "Robin", "Aventurine"],
    ["Raiden", "Pela", "Silver Wolf", "Aventurine"],
    ["Raiden", "Pela", "Sparkle", "Aventurine"],
    ["Raiden", "Black Swan", "Jiaoqiu", "Aventurine"],
    
    #Bailu
    ["Raiden", "Kafka", "Black Swan", "Bailu"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Bailu"],
    ["Kafka", "Black Swan", "Robin", "Bailu"],
    ["Kafka", "Black Swan", "Ruan Mei", "Bailu"],
    ["Firefly", "Trailblazer Imaginary", "Ruan Mei", "Bailu"],
    ["Feixiao", "Bronya", "Robin", "Bailu"],
    ["Raiden", "Jiaoqiu", "Pela", "Bailu"],
    ["Raiden", "Bronya", "Jiaoqiu", "Bailu"],
    ["Feixiao", "Topaz", "Robin", "Bailu"],
    ["Raiden", "Silver Wolf", "Sparkle", "Bailu"],
    
    #Black Swan
    ["Kafka", "Black Swan", "Robin", "Huohuo"],
    ["Raiden", "Kafka", "Black Swan", "Fu Xuan"],
    ["Raiden", "Kafka", "Black Swan", "Aventurine"],
    ["Raiden", "Kafka", "Black Swan", "Huohuo"],
    ["Kafka", "Black Swan", "Ruan Mei", "Huohuo"],
    ["Raiden", "Black Swan", "Jiaoqiu", "Aventurine"],
    ["Kafka", "Black Swan", "Robin", "Aventurine"],
    ["Raiden", "Black Swan", "Jiaoqui", "Fu Xuan"],
    ["Raiden", "Black Swan", "Pela", "Aventurine"],
    ["Raiden", "Black Swan", "Sparkle", "Aventurine"],
    
    #Blade
    ["Blade", "Bronya", "Sparkle", "Luocha"],
    ["Blade", "Bronya", "Sparkle", "Huohuo"],
    ["Blade", "Bronya", "Robin", "Luocha"],
    ["Blade", "March 7th Imaginary", "Robin", "Huohuo"],
    ["Jade", "Blade", "Bronya", "Luocha"],
    ["Blade", "Bronya", "Sparkle", "Fu Xuan"],
    ["Jade", "Blade", "Robin", "Luocha"],
    ["Jade", "Blade", "Bronya", "Fu Xuan"],
    ["Blade", "Robin", "Sparkle", "Huohuo"],
    ["Blade", "Bronya", "Robin", "Huohuo"],
    
    #Boothill
    ["Boothill", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Boothill", "Trailblazer Imaginary", "Ruan Mei", "Lingsha"],
    ["Boothill", "Bronya", "Ruan Mei", "Gallagher"],
    ["Boothill", "Bronya", "Trailblazer Imaginary", "Ruan Mei"],
    ["Boothill", "Trailblazer Imaginary", "Ruan Mei", "Advneturine"],
    ["Boothill", "Bronya", "Pela", "Ruan Mei"],
    ["Rappa", "Boothill", "Trailblazer Imaginary", "Gallagher"],
    ["Boothill", "Bronya", "Ruan Mei", "Lingsha"],
    ["Boothill", "Raiden", "Bronya", "Ruan Mei"],
    ["Boothill", "Bronya", "Ruan Mei", "Aventurine"],
    ["Boothill", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    
    #Bronya
    ["Feixiao", "March 7th Imaginary", "Bronya", "Robin"],
    ["Raiden", "Bronya", "Jiaoqiu", "Aventurine"],
    ["Firefly", "Bronya", "Trailblazer Imaginary", "Ruan Mei"],
    ["Raiden", "Bronya", "Pela", "Fu Xuan"],
    ["Raiden", "Bronya", "Pela", "Aventurine"],
    ["Raiden", "Bronya", "Jiaoqiu", "Fu Xuan"],
    ["Feixiao", "March 7th Imaginary", "Bronya", "Aventurine"],
    ["Feixiao", "Topaz", "Bronya", "Aventurine"],
    ["Raiden", "Bronya", "Jiaoqiu", "Gallagher"],
    ["Feixiao", "Bronya", "Robin", "Aventurine"],
    
    #Clara
    ["Clara", "March 7th Imaginary", "Robin", "Fu Xuan"],
    ["Clara", "Topaz", "Robin", "Fu Xuan"],
    ["Clara", "Robin", "Sparkle", "Fu Xuan"],
    ["Clara", "Sparkle", "Tingyun", "Fu Xuan"],
    ["Clara", "March 7th Imaginary", "Robin", "Aventurine"],
    ["Feixiao", "Clara", "Robin", "Huohuo"],
    ["Feixiao", "Clara", "Topaz", "Aventurine"],
    ["Clara", "Topaz", "Robin", "Aventurine"],
    ["Clara", "March 7th Imaginary", "Robin", "Huohuo"],
    ["Clara", "Robin", "Sparkle", "Aventurine"],
    
    #Dan Heng
    ["Dan Heng", "Bronya", "Ruan Mei", "Fu Xuan"],
    ["Feixiao", "Dan Heng", "Topaz", "Robin"],
    ["Dan Heng", "March 7th Imaginary", "Robin", "Aventurine"],

    #Imbibitor Lunae
    ["Dan Heng - Imbibitor Lunae", "Sparkle", "Tingyun", "Luocha"],
    ["Dan Heng - Imbibitor Lunae", "Robin", "Sparkle", "Huohuo"],
    ["Dan Heng - Imbibitor Lunae", "Robin", "Sparkle", "Aventurine"],
    ["Dan Heng - Imbibitor Lunae", "Robin", "Sparkle", "Gallagher"],
    ["Dan Heng - Imbibitor Lunae", "Jiaoqiu", "Sparkle", "Luocha"],
    ["Dan Heng - Imbibitor Lunae", "Ruan Mei", "Sparkle", "Huohuo"],
    ["Dan Heng - Imbibitor Lunae", "Sparkle", "Tingyun", "Aventurine"],
    ["Dan Heng - Imbibitor Lunae", "Ruan Mei", "Sparkle", "Gallagher"],
    ["Dan Heng - Imbibitor Lunae", "Ruan Mei", "Sparkle", "Luocha"],
    ["Dan Heng - Imbibitor Lunae", "Ruan Mei", "Sparkle", "Aventurine"],
    
    #Dr Ratio
    ["Dr Ratio", "Topaz", "Robin", "Aventurine"],
    ["Dr Ratio", "Moze", "Robin", "Aventurine"],
    ["Dr Ratio", "March 7th Imaginary", "Robin", "Aventurine"],
    ["Dr Ratio", "Jiaoqiu", "Robin", "Aventurine"],
    ["Dr Ratio", "Robin", "Silver Wolf", "Aventurine"],
    ["Feixiao", "Dr Ratio", "Robin", "Aventurine"],
    ["Dr Ratio", "Moze", "Jiaoqiu", "Aventurine"],
    ["Dr Ratio", "March 7th Imaginary", "Ruan Mei", "Aventurine"],
    ["Dr Ratio", "Topaz", "Bronya", "Huohuo"],
    ["Dr Ratio", "Topaz", "Silver Wolf", "Aventurine"],
    
    #Feixiao
    ["Feixiao", "Topaz", "Robin", "Aventurine"],
    ["Feixiao", "Moze", "Robin", "Aventurine"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Aventurine"],
    ["Feixiao", "Moze", "Robin", "Gallagher"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Gallagher"],
    ["Feixiao", "Topaz", "Bronya", "Aventurine"],
    ["Feixiao", "March 7th Imaginary", "Sparkle", "Gallagher"],
    ["Feixiao", "Topaz", "Sparkle", "Gallagher"],
    ["Feixiao", "March 7th Imaginary", "Bronya", "Aventurine"],
    ["Feixiao", "Topaz", "Moze", "Aventurine"],
    ["Feixiao", "Moze", "March 7th Imaginary", "Aventurine"],
    ["Feixiao", "Topaz", "March 7th Imaginary", "Gallagher"],
    ["Feixiao", "Topaz", "Robin", "Aventurine"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Aventurine"],
    ["Feixiao", "Moze", "Robin", "Aventurine"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Fu Xuan"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Huohuo"],
    ["Feixiao", "Topaz", "Robin", "Fu Xuan"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Gallagher"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Luocha"],
    ["Feixiao", "Topaz", "Robin", "Lingxia"],
    ["Feixiao", "Topaz", "Robin", "Huohuo"],

    #FireFly <3
    ["Firefly", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Firefly", "Trailblazer Imaginary", "Ruan Mei", "Lingxia"],
    ["Firefly", "Trailblazer Imaginary", "Ruan Mei", "Luocha"],
    ["Firefly", "Trailblazer Imaginary", "Ruan Mei", "Aventurine"],
    ["Rappa", "Firefly", "Trailblazer Imaginary", "Ruan Mei"],
    ["Firefly", "Trailblazer Imaginary", "Ruan Mei", "Huohuo"],
    ["Firefly", "Bronya", "Trailblazer Imaginary", "Ruan Mei"],
    ["Rappa", "Firefly", "Trailblazer Imaginary", "Lingxia"],
    ["Rappa", "Firefly", "Trailblazer Imaginary", "Gallagher"],
    ["Firefly", "Himeko", "Trailblazer Imaginary", "Ruan Mei"],
    
    #Fu Xuan
    ["Raiden", "Jiaoqiu", "Sparkle", "Fu Xuan"],
    ["Raiden", "Kafka", "Silver Wolf", "Fu Xuan"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Fu Xuan"],
    ["Raiden", "Jiaoqiu", "Pela", "Fu Xuan"],
    ["Raiden", "Pela", "Silver Wolf", "Fu Xuan"],
    ["Raiden", "Pela", "Sparkle", "Fu Xuan"],
    ["Raiden", "Silver Wolf", "Sparkle", "Fu Xuan"],
    ["Feixiao", "Topaz", "Robin", "Fu Xuan"],
    ["Raiden", "Black Swan", "Jiaoqiu", "Fu Xuan"],
    ["Raiden", "Jiaoqiu", "Silver Wolf", "Fu Xuan"],

    #Gallagher
    ["Firefly", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Rappa", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Himeko", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Raiden", "Jiaoqiu", "Pela", "Gallagher"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Gallagher"],
    ["Raiden", "Jiaoqiu", "Sparkle", "Gallagher"],
    ["Boothill", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Kafka", "Black Swan", "Ruan Mei", "Gallagher"],
    ["Raiden", "Kafka", "Black Swan", "Gallagher"],
    ["Feixiao", "Topaz", "Robin", "Gallagher"],

    #Gepard
    ["Raiden", "Kafka", "Black Swan", "Gepard"],
    ["Raiden", "Pela", "Silver Wolf", "Gepard"],
    ["Raiden", "Silver Wolf", "Sparkle", "Gepard"],
    ["Raiden", "Bronya", "Pela", "Gepard"],
    ["Kafka", "Black Swan", "Ruan Mei", "Gepard"],
    ["Raiden", "Pela", "Sparkle", "Gepard"],
    ["Raiden", "Jiaoqiu", "Pela", "Gepard"],
    ["Raiden", "Black Swan", "Pela", "Gepard"],
    ["Raiden", "Jiaoqiu", "Sparkle", "Gepard"],
    ["Kafka", "Black Swan", "Robin", "Gepard"],


    #Lil Guin
    ["Raiden", "Guinaifen", "Pela", "Aventurine"],
    ["Kafka", "Black Swan", "Guinaifen", "Huohuo"],
    ["Raiden", "Guinaifen", "Pela", "Fu Xuan"],
    ["Raiden", "Guinaifen", "Jiaoshui", "Gallagher"],
    ["Kafka", "Black Swan", "Guinaifen", "Luocha"],
    ["Raiden", "Guinaifen", "Pela", "Gallagher"],
    ["Guinaifen", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Raiden", "Black Swan", "Guinaifen", "Aventurine"],
    ["Raiden", "Guinaifen", "Jiaoshui", "Aventurine"],
    ["Raiden", "Guinaifen", "Ruan Mei", "Fu Xuan"],
    
    #Hanya
    ["Dan Heng - Imbibitor Lunae", "Hanya", "Ruan Mei", "Gallagher"],
    ["Raiden", "Black Swan", "Hanya", "Aventurine"],
    ["Yunli", "Hanya", "Tingyun", "Huohuo"],
    ["Raiden", "Hanya", "Pela", "Gepard"],
    ["Dan Heng - Imbibitor Lunae", "Hanya", "Tingyun", "Aventurine"],
    ["Jing Yuan", "Hanya", "Tingyun", "Huohuo"],
    ["Kafka", "Black Swan", "Hanya", "Lynx"],
    ["Dan Heng - Imbibitor Lunae", "Hanya", "Sparkle", "Luocha"],
    ["Yunli", "Hanya", "Tingyun", "Aventurine"],

    #Herta
    ["Herta", "Pela", "Robin", "Sparkle"],
    ["Jade", "Herta", "Robin", "Gallagher"],
    ["Clara", "Herta", "Robin", "Aventurine"],
    ["Jade", "Herta", "Ruan Mei", "Aventurine"],
    ["Herta", "Topaz", "Ruan Mei", "Aventurine"],
    ["Herta", "Ruan Mei", "Sparkle", "Lingsha"],
    ["Raiden", "Herta", "Jiaoqiu", "Aventurine"],
    ["Jade", "Herta", "Robin", "Aventurine"],
    ["Himeko", "Herta", "Robin", "Aventurine"],
    
    #Himiko
    
    #Hook
    ["Hook", "Raiden", "Jiaoqiu", "Aventurine"],
    ["Hook", "Robin", "Sparkle", "Lingxia"],
    
    #Huohuo
    ["Kafka", "Black Swan", "Robin", "Huohuo"],
    ["Kafka", "Black Swan", "Ruan Mei", "Huohuo"],
    ["Feixiao", "Topaz", "Robin", "Huohuo"],
    ["Kafka", "Black Swan", "Jiaoqiu", "Huohuo"],
    ["Raiden", "Jiaoqiu", "Sparkle", "Huohuo"],
    ["Raiden", "Kafka", "Black Swan", "Huohuo"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Huohuo"],
    ["Yunli", "Robin", "Tingyun", "Huohuo"],
    ["Raiden", "Jiaoqiu", "Pela", "Huohuo"],
    ["Firefly", "Trailblazer Imaginary", "Ruan Mei", "Huohuo"],

    #Jade
    ["Jade", "Feixiao", "Robin", "Aventurine"],
    ["Jade", "Himeko", "Robin", "Aventurine"],
    ["Jade", "Bronya", "Robin", "Lingsha"],
    ["Jade", "Blade", "Bronya", "Luocha"],
    ["Jade", "Feixiao", "Topaz", "Aventurine"],
    ["Jade", "Trailblazer Imaginary", "Ruan Mei", "Lingsha"],
    ["Jade", "Robin", "Ruan Mei", "Lingxia"],
    ["Jade", "Topaz", "Robin", "Aventurine"],
    ["Jade", "Feixiao", "Robin", "Fu Xuan"],
    ["Jade", "Blade", "Robin", "Luocha"],

    #Jiaoqiu
    ["Raiden", "Jiaoqiu", "Sparkle", "Aventurine"],
    ["Raiden", "Jiaoqiu", "Sparkle", "Fu Xuan"],
    ["Raiden", "Jiaoqiu", "Pela", "Gallagher"],
    ["Raiden", "Jiaoqiu", "Robin", "Aventurine"],
    ["Raiden", "Jiaoqiu", "Silverwolf", "Aventurine"],
    ["Raiden", "Jiaoqiu", "Pela", "Aventurine"],
    ["Raiden", "Jiaoqiu", "Pela", "Fu Xuan"],
    ["Raiden", "Black Swan", "Jiaoqiu", "Aventurine"],
    ["Raiden", "Jiaoqiu", "Sparkle", "Gallagher"],
    ["Raiden", "Bronya", "Jiaoqiu", "Aventurine"],

    #Jing Yuan
    ["Jing Yuan", "Sparkle", "Tingyun", "Fu Xuan"],
    ["Jing Yuan", "Robin", "Tingyun", "Aventurine"],
    ["Jing Yuan", "Sparkle", "Tingyun", "Aventurine"],
    ["Jing Yuan", "Robin", "Sparkle", "Fu Xuan"],
    ["Jing Yuan", "Topaz", "Robin", "Aventurine"],
    ["Jing Yuan", "Sparkle", "Tingyun", "Huohuo"],
    ["Jing Yuan", "Robin", "Sparkle", "Aventurine"],
    ["Jing Yuan", "Robin", "Tingyun", "Huohuo"],
    ["Jing Yuan", "Robin", "Sparkle", "Huohuo"],
    ["Jing Yuan", "Trailblazer Imaginary", "Ruan Mei", "Lingxia"],

    #Jingliu
    ["Jingliu", "Bronya", "Ruan Mei", "Huohuo"],
    ["Jingliu", "Bronya", "Robin", "Gallagher"],
    ["Jingliu", "Robin", "Sparkle", "Huohuo"],
    ["Feixiao", "Jingliu", "Yunli", "Luocha"],
    ["Jingliu", "Silverwolf", "Sparkle", "Fu Xuan"],
    ["Jingliu", "Bronya", "Robin", "Huohuo"],
    ["Jingliu", "Blade", "Ruan Mei", "Fu Xuan"],
    ["Rappa", "Jingliu", "Ruan Mei", "Luocha"],
    ["Jingliu", "Ruan Mei", "Tingyun", "Gallagher"],
    ["Jingliu", "Ruan Mei", "Sparkle", "Huohuo"],

    #Kafka
    ["Kafka", "Black Swan", "Robin", "Huohuo"],
    ["Raiden", "Kafka", "Black Swan", "Aventurine"],
    ["Kafka", "Black Swan", "Ruan Mei", "Huohuo"],
    ["Kafka", "Black Swan", "Ruan Mei", "Gallagher"],
    ["Raiden", "Kafka", "Black Swan", "Gallagher"],
    ["Raiden", "Kafka", "Black Swan", "Fu Xuan"],
    ["Raiden", "Kafka", "Black Swan", "Huohuo"],
    ["Kafka", "Black Swan", "Robin", "Aventurine"],
    ["Raiden", "Kafka", "Black Swan", "Luocha"],
    ["Kafka", "Black Swan", "Ruan Mei", "Luocha"],

    #Lingsha
    ["Firefly", "Trailblazer Imaginary", "Ruan mei", "Lingsha"],
    ["Himiko", "Trailblazer Imaginary", "Ruan mei", "Lingsha"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Lingsha"],
    ["Raiden", "Jiaoqiu", "Pela", "Lingsha"],
    ["Boothill", "Trailblazer Imaginary", "Ruan mei", "Lingsha"],
    ["Rapa", "Trailblazer Imaginary", "Ruan mei", "Lingsha"],
    ["Feixiao", "Topaz", "Robin", "Lingsha"],
    ["Rapa", "Firefly", "Trailblazer Imaginary", "Lingsha"],
    ["Raiden", "Jiaoqiu", "Sparkle", "Lingsha"],
    ["March 7th Imaginary", "Trailblazer Imaginary", "Ruan mei", "Lingsha"],
    ["Firefly", "Trailblazer Imaginary", "Ruan mei", "Lingsha"],
    ["Feixiao", "Topaz", "Robin", "Lingsha"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Lingsha"],
    ["Dr Ratio", "Topaz", "Robin", "Lingsha"],
    ["Dr Ratio", "Mose", "Tingyun", "Lingsha"],
    ["Dr Ratio", "Topaz", "Tingyun", "Lingsha"],
    ["Dr Ratio", "Mose", "Robin", ""],



    #Luka has no teams lol
    
    #Luocha
    ["Feixiao", "March 7th Imaginary", "Robin", "Luocha"],
    ["Raiden", "Kafka", "Black Swan", "Luocha"],
    ["Kafka", "Black Swan", "Ruan Mei", "Luocha"],
    ["Kafka", "Black Swan", "Robin", "Luocha"],
    ["Raiden", "Jiaoqiu", "Sparkle", "Luocha"],
    ["Firefly", "Trailblazer Imaginary", "Ruanmei", "Luocha"],
    ["Rapa", "Trailblazer Imaginary", "Ruanmei", "Luocha"],
    ["Feixiao", "Topaz", "Robin", "Luocha"],
    ["Feixiao", "Mose", "Robin", "Luocha"],
    ["Danhong and Baibiter Lunay", "Ruan Mei", "Sparkle", "Luocha"],

    
    #Lynx
    ["Rappa", "Trailblazer Imaginary", "Ruan Mei", "Lynx"],
    ["Firefly", "Trailblazer Imaginary", "Ruan Mei", "Lynx"],
    ["Bleed", "Bronya", "Sparkle", "Lynx"],
    ["Raiden", "Silverwolf", "Sparkle", "Lynx"],
    ["Yunli", "Sparkle", "Tingyun", "Lynx"],
    ["Yunli", "Robin", "Sparkle", "Lynx"],
    ["Kafka", "Black Swan", "Robin", "Lynx"],
    ["Dr Ratio", "Silverwolf", "Sparkle", "Lynx"],
    ["Blade", "Bronya", "Jiaoqiu", "Lynx"],
    ["Kafka", "BlackSwan", "Hanya", "Lynx"],

    #March 7th
    ["Feixiao", "Mose", "Robin", "March 7th"],
    ["Raiden", "Baranya", "Pela", "March 7th"],
    ["Raiden", "Jiaochui", "Sparkle", "March 7th"],
    ["Yunli", "Topaz", "Robin", "March 7th"],
    ["BlackSwan", "Serval", "Tingyun", "March 7th"],

    #March 7th Imaginary
    ["Feixiao", "March 7th Imaginary", "Robin", "Aventurine"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Huohuo"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Luocha"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Lingsha"],
    ["Feixiao", "March 7th Imaginary", "Sparkle", "Aventurine"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Fu Xuan"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Gallagher"],
    ["Feixiao", "March 7th Imaginary", "Bronya", "Robin"],
    ["Feixiao", "March 7th Imaginary", "Bronya", "Aventurine"],
    ["March 7th Imaginary", "Trailblazer Imaginary", "Ruan Mei", "Lingsha"],

    #Misha
    ["Misha", "Trailblazer Imaginary", "Sparkle", "Lingxia"],
    
    #Moze
    ["Feixiao", "Moze", "Robin", "Aventurine"],
    ["Dr Ratio", "Moze", "Robin", "Aventurine"],
    ["Dr Ratio", "Moze", "Tingyun", "Aventurine"],
    ["Dr Ratio", "Moze", "Robin", "Gallagher"],
    ["Dr Ratio", "Moze", "Tingyun", "Gallagher"],
    ["Feixiao", "Moze", "Topaz", "Aventurine"],
    ["Feixiao", "Moze", "March 7th Imaginary", "Aventurine"],

    #Natasha
    ["Firefly", "Trailblazer Imaginary", "Ruan Mei", "Natasha"],
    ["Kafka", "Pela", "Ruan Mei", "Natasha"],
    ["Yunli", "Bronya", "Tingyun", "Natasha"],

    #Pela
    ["Raiden", "Jiaoqiu", "Pela", "Aventurine"],
    ["Raiden", "Pela", "Silver Wolf", "Fu Xuan"],
    ["Raiden", "Pela", "Silver Wolf", "Aventurine"],
    ["Raiden", "Jiaoqiu", "Pela", "Gallagher"],
    ["Raiden", "Black Swan", "Pela", "Fu Xuan"],
    ["Raiden", "Jiaoqiu", "Pela", "Fu Xuan"],
    ["Raiden", "Pela", "Sparkle", "Fu Xuan"],
    ["Raiden", "Pela", "Sparkle", "Aventurine"],
    ["Raiden", "Black Swan", "Pela", "Aventurine"],
    ["Raiden", "Jiaoqiu", "Pela", "Huohuo"],

    #Qinque
    ["Qingque", "Silver Wolf", "Sparkle", "Fu Xuan"],
    ["Qingque", "Robin", "Sparkle", "Huohuo"],
    ["Qingque", "Ruan Mei", "Sparkle", "Fu Xuan"],
    ["Qingque", "Sparkle", "Tingyun", "Fu Xuan"],
    ["Qingque", "Robin", "Sparkle", "Fu Xuan"],
    ["Qingque", "Bronya", "Sparkle", "Fu Xuan"],

    #Rappa
    ["Rappa", "Trailblazer Imaginary", "Ruan Mei", "Lingsha"],
    ["Rappa", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Rappa", "Trailblazer Imaginary", "Asta", "Gallagher"],
    ["Rappa", "Trailblazer Imaginary", "Pela", "Gallagher"],
    ["Rappa", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Rappa", "Firefly", "Trailblazer Imaginary", "Ruan Mei"],
    ["Rappa", "Trailblazer Harmony", "Ruan Mei", "Aventurine"],
    ["Rappa", "Firefly", "Trailblazer Imaginary", "Lingsha"],
    ["Rappa", "Himeko", "Trailblazer Imaginary", "Gallagher"],
    ["Rappa", "Trailblazer Imaginary", "Ruan Mei", "Lingsha"],
    ["Rappa", "Trailblazer Imaginary", "Ruan Mei", "Luocha"],
    ["Rappa", "Trailblazer Imaginary", "Ruan Mei", "Huohuo"],
    ["Rappa", "Firefly", "Trailblazer Imaginary", "Gallagher"],
    ["Rappa", "Trailblazer Imaginary", "Pela", "Gallagher"],

    #Robin
    ["Feixiao", "Topaz", "Robin", "Aventurine"],
    ["Feixiao", "Moze", "Robin", "Aventurine"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Fu Xuan"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Huohuo"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Gallagher"],
    ["Feixiao", "March 7th Imaginary", "Robin", "Aventurine"],
    ["Kafka", "Black Swan", "Robin", "Huohuo"],
    ["Dr Ratio", "Topaz", "Robin", "Aventurine"],
    ["Feixiao", "Topaz", "Robin", "Fu Xuan"],
    ["Raiden", "Jiaoqiu", "Robin", "Aventurine"],

    #Ruan Mei
    ["Firefly", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Rappa", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Himeko", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Himeko", "Trailblazer Imaginary", "Ruan Mei", "Lingsha"],
    ["Boothill", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Firefly", "Trailblazer Imaginary", "Ruan Mei", "Lingsha"],
    ["Rappa", "Trailblazer Imaginary", "Ruan Mei", "Lingsha"],
    ["Kafka", "Black Swan", "Ruan Mei", "Huohuo"],
    ["Firefly", "Trailblazer Imaginary", "Ruan Mei", "Luocha"],
    ["Firefly", "Trailblazer Imaginary", "Ruan Mei", "Aventurine"],

    #Sampo
    ["Kafka", "Black Swan", "Sampo", "Huohuo"],
    ["Raiden", "Kafka", "Sampo", "Fu Xuan"],
    ["Kafka", "Black Swan", "Sampo", "Luocha"],
    ["Raiden", "Black Swan", "Sampo", "Aventurine"],
    ["Kafka", "Sampo", "Ruan Mei", "Huohuo"],
    ["Kafka", "Sampo", "Robin", "Huohuo"],
    ["Raiden", "Sampo", "Jiaoqiu", "Aventurine"],
    ["Kafka", "Black Swan", "Sampo", "Fu Xuan"],
    ["Raiden", "Kafka", "Sampo", "Aventurine"],
    ["Kafka", "Sampo", "Ruan Mei", "Fu Xuan"],

    #Seele
    ["Seele", "Silver Wolf", "Sparkle", "Fu Xuan"],
    ["Seele", "Bronya", "Robin", "Silver Wolf"],
    ["Seele", "Silver Wolf", "Tingyun", "Fu Xuan"],
    ["Seele", "Lynx", "Sparkle", "Aventurine"],
    ["Seele", "Sparkle", "Tingyun", "Fu Xuan"],
    ["Robin", "Sparkle", "Fu Xuan", "Seele"],
    ["Robin", "Sparkle", "Gallagher", "Seele"],
    ["Bronya", "Silver Wolf", "Fu Xuan", "Seele"],
    ["Seele", "Robin", "Silver Wolf", "Sparkle"],
    ["Seele", "Robin", "Sparkle", "Luocha"],

    #Serval
    ["Serval", "Robin", "Sparkle", "Fu Xuan"],
    ["Serval", "Sparkle", "Tingyun", "Huohuo"],
    ["Serval", "Robin", "Tingyun", "Gallagher"],
    ["Serval", "Robin", "Silver Wolf", "Fu Xuan"],
    ["Black Swan", "Serval", "Tingyun", "March 7th"],
    ["Serval", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Serval", "Sparkle", "Tingyun", "Luocha"],
    ["Serval", "Sparkle", "Tingyun", "Fu Xuan"],
    ["Kafka", "Serval", "Silver Wolf", "Fu Xuan"],

    #Silver Wolf
    ["Raiden", "Pela", "Silver Wolf", "Fu Xuan"],
    ["Raiden", "Pela", "Silver Wolf", "Aventurine"],
    ["Raiden", "Silver Wolf", "Sparkle", "Aventurine"],
    ["Qingque", "Silver Wolf", "Sparkle", "Fu Xuan"],
    ["Raiden", "Pela", "Silver Wolf", "Gallagher"],
    ["Raiden", "Silver Wolf", "Sparkle", "Fu Xuan"],
    ["Raiden", "Jiaoqiu", "Silver Wolf", "Aventurine"],
    ["Raiden", "Jiaoqiu", "Silver Wolf", "Fu Xuan"],
    ["Seele", "Silver Wolf", "Sparkle", "Fu Xuan"],
    ["Raiden", "Black Swan", "Silver Wolf", "Fu Xuan"],

    #Sparkle
    ["Raiden", "Jiaoqiu", "Sparkle", "Aventurine"],
    ["Raiden", "Pela", "Sparkle", "Fu Xuan"],
    ["Raiden", "Pela", "Sparkle", "Aventurine"],
    ["Raiden", "Silver Wolf", "Sparkle", "Aventurine"],
    ["Raiden", "Jiaoqiu", "Sparkle", "Huohuo"],
    ["Raiden", "Jiaoqiu", "Sparkle", "Fu Xuan"],
    ["Raiden", "Silver Wolf", "Sparkle", "Fu Xuan"],
    ["Raiden", "Jiaoqiu", "Sparkle", "Gallagher"],
    ["Raiden", "Black Swan", "Sparkle", "Aventurine"],
    ["Raiden", "Jiaoqiu", "Ruan Mei", "Sparkle"],

    #Sunday
    ["Jing Yuan", "Sunday", "Robin", "Huohuo"],
    ["Jing Yuan", "Sunday", "Tingyun", "Huohuo"],
    ["Jing Yuan", "Sunday", "Ruan Mei", "Huohuo"],
    ["Jing Yuan", "Sunday", "Robin", "Aventurine"],
    ["Jing Yuan", "Sunday", "Tingyun", "Aventurine"],
    ["Jing Yuan", "Sunday", "Ruan Mei", "Aventurine"],
    ["Dan Heng - Imbibitor Lunae", "Sunday", "Robin", "Luocha"],
    ["Dan Heng - Imbibitor Lunae", "Sunday", "Tingyun", "Luocha"],
    ["Dan Heng - Imbibitor Lunae", "Sunday", "Ruan Mei", "Luocha"],

    #Sushang
    ["Sushang", "Robin", "Silver Wolf", "Lingsha"],
    #THE Herta <3
    
    #Tingyun
    ["Yunli", "Robin", "Tingyun", "Huohuo"],
    ["Yunli", "Sparkle", "Tingyun", "Huohuo"],
    ["Jing Yuan", "Sparkle", "Tingyun", "Huohuo"],
    ["Kafka", "Black Swan", "Tingyun", "Huohuo"],
    ["Yunli", "Robin", "Tingyun", "Aventurine"],
    ["Dan Heng - Imbibitor Lunae", "Sparkle", "Tingyun", "Aventurine"],
    ["Jing Yuan", "Sparkle", "Tingyun", "Fu Xuan"],
    ["Jing Yuan", "Robin", "Tingyun", "Aventurine"],
    ["Dan Heng - Imbibitor Lunae", "Sparkle", "Tingyun", "Luocha"],
    ["Jing Yuan", "Sparkle", "Tingyun", "Aventurine"],
    
    #Tingyun - Fugue
    
    #Topaz
    ["Feixiao", "Topaz", "Robin", "Aventurine"],
    ["Feixiao", "Topaz", "Robin", "Fu Xuan"],
    ["Feixiao", "Topaz", "Robin", "Huohuo"],
    ["Feixiao", "Topaz", "Robin", "Gallagher"],
    ["Yunli", "Topaz", "Robin", "Aventurine"],
    ["Dr Ratio", "Topaz", "Robin", "Aventurine"],
    ["Feixiao", "Topaz", "Robin", "Lingsha"],
    ["Feixiao", "Topaz", "Robin", "Luocha"],
    ["Feixiao", "Topaz", "Sparkle", "Aventurine"],
    ["Feixiao", "Topaz", "Robin", "Aventurine"],

    #Trailblazer - Imaginary
    
    #Trailblazer - Ice
    
    #Welt
    ["Raiden", "Welt", "Pela", "Sparkle"],
    ["Welt", "Trailblazer Imaginary", "Ruan Mei", "Gallagher"],
    ["Raiden", "Welt", "Spparkle", "Aventurine"],
    ["Raiden", "Welt", "Jiaoqiu", "Gallagher"],
    ["Raiden", "Welt", "Bronya", "Sparkle"],
    ["Raiden", "Welt", "Pela", "Fu Xuan"],
    ["Raiden", "Welt", "Pela", "Ruan Mei"],
    ["Raiden", "Welt", "Sparkle", "Fu Xuan"],
    ["Raiden", "Welt", "Jiaoqiu", "Sparkle"],
    ["Feixiao", "Welt", "Robin", "Aventurine"],
    
    #Xueyi
    ["Xueyi", "Silver Wolf", "Sparkle", "Fu Xuan"],
    ["Firefly", "Xueyi", "Trailblazer Imaginary", "Ruan Mei"],
    
    #Yanqing
    ["Yanqing", "Kafka", "Black Swan", "Aventurine"],
    
    #Yukong
    ["Feixiao", "Tingyun", "Yukong", "Huohuo"],
    ["Dan Heng - Imbibitor Lunae", "Tingyun", "Yukong", "Luocha"],
    ["Feixiao", "Robin", "Yukong", "Lingsha"],
    ["Yunli", "Tingyun", "Yukong", "Huohuo"],
    
    #Yunli
    ["Yunli", "Robin", "Tingyun", "Huohuo"],
    ["Yunli", "Topaz", "Robin", "Aventurine"],
    ["Feixiao", "Yunli", "Robin", "Aventurine"],
    ["Yunli", "March 7th Imaginary", "Robin", "Huohuo"],
    ["Yunli", "Topaz", "Robin", "Huohuo"],
    ["Yunli", "Robin", "Sparkle", "Huohuo"],
    ["Yunli", "Sparkle", "Tingyun", "Huohuo"],
    ["Feixiao", "Yunli", "Tingyun", "Huohuo"],
    ["Yunli", "Robin", "Tingyun", "Aventurine"],
    ["Yunli", "Robin", "Tingyun", "Fu Xuan"],






]

# Randomizer functions
def true_random():
    return random.sample(characters, 4)

def competitive_random():
    return random.choice(competitive_teams)

def character_select(character):
    valid_teams = [team for team in competitive_teams if character in team]
    if not valid_teams:
        return None
    return random.choice(valid_teams)

# GUI Application
class StarRailRandomizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Honkai: Star Rail Randomizer")
        self.geometry("600x400")  # Increased size to accommodate icons
        self.resizable(False, False)
        self.frames = {}
        self.icon_dir = "icons"  # Directory for character icons
        self.character_images = self.load_character_images()
        self.setup_frames()

    def setup_frames(self):
        for F in (MainMenu, TrueRandomPage, CompRandomPage, MainSelectPage):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainMenu)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def load_character_images(self):
        """Load and resize character images from the icon directory."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_dir = os.path.join(script_dir, "icons")
        
        images = {}
        for char in characters:
            filename = os.path.join(icon_dir, f"{char.lower().replace(' ', '_')}.png")
            if os.path.exists(filename):
                # Open the image using Pillow and resize it
                pil_image = Image.open(filename).resize((64, 64), Image.Resampling.LANCZOS)  # Resize to 64x64
                images[char] = ImageTk.PhotoImage(pil_image)  # Convert to Tkinter-compatible format
            else:
                print(f"Warning: Missing icon for {char} ({filename})")
                images[char] = None
        return images



class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Honkai: Star Rail Randomizer", font=("Arial", 18)).pack(pady=20)
        tk.Button(self, text="True Random", command=lambda: master.show_frame(TrueRandomPage), width=20).pack(pady=10)
        tk.Button(self, text="Competitive Random", command=lambda: master.show_frame(CompRandomPage), width=20).pack(pady=10)
        tk.Button(self, text="Main Select", command=lambda: master.show_frame(MainSelectPage), width=20).pack(pady=10)

class TrueRandomPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="True Random Mode", font=("Arial", 18)).pack(pady=20)
        
        # Frame for displaying team icons and names
        self.team_frame = tk.Frame(self)
        self.team_frame.pack(pady=10)
        
        tk.Button(self, text="Generate Team", command=self.generate_team, width=20).pack(pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: master.show_frame(MainMenu), width=20).pack(pady=10)

    def generate_team(self):
        for widget in self.team_frame.winfo_children():
            widget.destroy()  # Clear previous team display
        
        team = true_random()
        for char in team:
            self.display_character(char)

    def display_character(self, char):
        """Display a character's icon and name."""
        frame = tk.Frame(self.team_frame)
        frame.pack(side="left", padx=10)
        
        icon = self.master.character_images.get(char)
        if icon:
            tk.Label(frame, image=icon).pack()  # Display icon
        tk.Label(frame, text=char, font=("Arial", 12)).pack()  # Display name

class CompRandomPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Competitive Random Mode", font=("Arial", 18)).pack(pady=20)
        
        # Frame for displaying team icons and names
        self.team_frame = tk.Frame(self)
        self.team_frame.pack(pady=10)
        
        tk.Button(self, text="Generate Team", command=self.generate_team, width=20).pack(pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: master.show_frame(MainMenu), width=20).pack(pady=10)

    def generate_team(self):
        for widget in self.team_frame.winfo_children():
            widget.destroy()  # Clear previous team display
        
        team = competitive_random()
        for char in team:
            self.display_character(char)

    def display_character(self, char):
        """Display a character's icon and name."""
        frame = tk.Frame(self.team_frame)
        frame.pack(side="left", padx=10)
        
        icon = self.master.character_images.get(char)
        if icon:
            tk.Label(frame, image=icon).pack()  # Display icon
        tk.Label(frame, text=char, font=("Arial", 12)).pack()  # Display name

class MainSelectPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Main Select Mode", font=("Arial", 18)).pack(pady=20)
        
        tk.Label(self, text="Select a character:", font=("Arial", 14)).pack(pady=5)
        self.selected_char = tk.StringVar(value=characters[0])  # Default to the first character
        self.char_dropdown = tk.OptionMenu(self, self.selected_char, *characters)
        self.char_dropdown.config(font=("Arial", 14), width=15)
        self.char_dropdown.pack(pady=5)
        
        # Frame for displaying team icons and names
        self.team_frame = tk.Frame(self)
        self.team_frame.pack(pady=10)
        
        tk.Button(self, text="Generate Team", command=self.generate_team, width=20).pack(pady=10)
        tk.Button(self, text="Back to Main Menu", command=lambda: master.show_frame(MainMenu), width=20).pack(pady=10)

    def generate_team(self):
        # Clear any existing team display
        for widget in self.team_frame.winfo_children():
            widget.destroy()

        # Get the selected character
        character = self.selected_char.get()
        team = character_select(character)
        
        if team:
            # Display each team member's icon and name
            for char in team:
                self.display_character(char)
        else:
            tk.Label(self.team_frame, text=f"No valid teams for {character}.", font=("Arial", 14)).pack()

    def display_character(self, char):
        """Display a character's icon and name."""
        frame = tk.Frame(self.team_frame)
        frame.pack(side="left", padx=10)
        
        icon = self.master.character_images.get(char)
        if icon:
            tk.Label(frame, image=icon).pack()  # Display icon
        tk.Label(frame, text=char, font=("Arial", 12)).pack()  # Display name


# Run the application
if __name__ == "__main__":
    app = StarRailRandomizer()
    app.mainloop()
