# -*- coding: utf-8 -*-
import os
import zipfile


def get_fb_content(zip_file, extract_file, where_store):
    with zipfile.ZipFile(zip_file) as my_zip:
        result = my_zip.extract(extract_file, where_store)
    return result


def get_archive_file(path, id_book):
    for archive in os.listdir(path):
        if archive.endswith('.zip'):
            fb, start, end = archive[:-4].split('-')
            pos = end.find('_')
            if pos > -1:
                end = end[:pos]
            start_num = int(start)
            end_num = int(end)
            if (id_book >= start_num) and (id_book <= end_num):
                return archive
