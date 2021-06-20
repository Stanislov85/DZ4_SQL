import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://postgres:3sU34#Rr!@localhost:5432/base_test1')
connection = engine.connect()

# Название и год выхода альбомов, вышедших в 2018 году;
# print('\n1.Название и год выхода альбомов, вышедших в 2018 году:')
# sel = connection.execute("""
#     SELECT name
#     FROM albums
#     WHERE extract( year FROM date ) = 2018
#     """).fetchall()
# print(sel)
#
# print('\n2.Название и продолжительность самого длительного трека:')
# track = connection.execute("""
#     SELECT name, duration
#     FROM track_list
#     ORDER BY duration DESC
#     LIMIT 1
#     """).fetchall()
# print(track)
#
# print('\n3.Название треков, продолжительность которых не менее 3,5 минуты:')
# track_limit_duration = connection.execute("""
#     SELECT name, duration
#     FROM track_list
#     WHERE duration > '00:03:30'
#     ORDER BY duration DESC
#     """).fetchall()
# print(track_limit_duration)
#
# print('\n4.Названия сборников, вышедших в период с 2018 по 2020 год включительно:')
#
# name_collections_18_20 = connection.execute("""
#     SELECT name
#     FROM collections
#     WHERE (extract( year FROM date ) >= 2018) AND (extract( year FROM date ) <= 2020)
#     """).fetchall()
# print(name_collections_18_20)
#
# print('\n5.Исполнители, чье имя состоит из 1 слова:')
# name_groups = connection.execute("""
#     SELECT name
#     FROM groups
#     WHERE not name like '%% %%'
#     """).fetchall()
# print(name_groups)
#
# print('\n6.Название треков, которые содержат слово "мой"/"my":')
# name_tracks_my = connection.execute("""
#     SELECT name
#     FROM track_list
#     WHERE name like '%%мой%%'
#     """).fetchall()
# print(name_tracks_my)


#DZ_5


print('\n7.Количество исполнителей в каждом жанре:')
count_groups_genre = connection.execute("""
    SELECT gm.name, count(gr.name)
    FROM genre_music as gm
    LEFT JOIN groups_genre as gg on gm.id = gg.id_genre
    LEFT JOIN groups as gr on gg.id_group = gr.id
    GROUP BY gm.name
    ORDER BY count(gr.id) DESC
    """).fetchall()
print(count_groups_genre)


print('\n8.Количество треков, вошедших в альбомы 2019-2020 годов:')
count_tracks = connection.execute("""
    SELECT tl.name, a.date
    FROM albums as a
    LEFT JOIN track_list as tl on tl.id_album = a.id
    WHERE (extract(year FROM a.date) >= 2019) and (extract(year FROM a.date) <= 2020)
    """).fetchall()
print(count_tracks)


print('\n9.Средняя продолжительность треков по каждому альбому:')
midle_duration_tracks = connection.execute("""
    SELECT a.name, AVG(tl.duration)
    FROM albums as a
    LEFT JOIN track_list as tl on tl.id_album = a.id
    GROUP BY a.name
    ORDER BY AVG(tl.duration)
  """).fetchall()
print(midle_duration_tracks)


print('\n10.Все исполнители, которые не выпустили альбомы в 2020 году:')
all_groups_year2020 = connection.execute("""
    SELECT distinct gr.name
    FROM groups as gr
    WHERE gr.name not in (
        SELECT distinct gr.name
        FROM groups as gr
        LEFT JOIN groups_albums as ga on gr.id = ga.id_group
        LEFT JOIN albums as a on a.id = ga.id_album
        WHERE extract(year FROM a.date) = 2020
    )
    ORDER BY gr.name
    """).fetchall()
print(all_groups_year2020)


print('\n11.Названия сборников, в которых присутствует конкретный исполнитель (Баста):')
name_collections = connection.execute("""
    SELECT distinct cl.name
    FROM collections as cl
    LEFT JOIN track_collections as tc on cl.id = tc.id_collections
    LEFT JOIN track_list as tl on tl.id = tc.id_track
    LEFT JOIN albums as a on a.id = tl.id_album
    LEFT JOIN groups_albums as ga on ga.id_album = a.id
    LEFT JOIN groups as gr on gr.id = ga.id_group
    WHERE gr.name like '%%Баста%%'
    ORDER BY cl.name
  """).fetchall()
print(name_collections)


print('\n12.Название альбомов, в которых присутствуют исполнители более 1 жанра:')
name_albums = connection.execute("""
    SELECT a.name
    FROM albums as a
    LEFT JOIN groups_albums as ga on a.id = ga.id_album
    LEFT JOIN groups as gr on gr.id = ga.id_group
    LEFT JOIN groups_genre as gg on gr.id = gg.id_group
    LEFT JOIN genre_music as gm on gm.id = gg.id_genre
    GROUP BY a.name
    HAVING count(distinct gm.name) > 1
    ORDER BY a.name
  """).fetchall()
print(name_albums)


print('\n13.Наименование треков, которые не входят в сборники:')
name_tracks_join_collections = connection.execute("""
    SELECT tl.name
    FROM track_list as tl
    LEFT JOIN track_collections as tc on tl.id = tc.id_track
    WHERE tc.id_track is null
  """).fetchall()
print(name_tracks_join_collections)


print('\n14.Исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько):')
group_short_track = connection.execute("""
    SELECT gr.name, tl.duration
    FROM track_list as tl
    LEFT JOIN albums as a on a.id = tl.id_album
    LEFT JOIN groups_albums as ga on ga.id_album = a.id
    LEFT JOIN groups as gr on gr.id = ga.id_group
    GROUP BY gr.name, tl.duration
    HAVING tl.duration = (SELECT min(duration) FROM track_list)
    ORDER BY gr.name
  """).fetchall()
print(group_short_track)


print('\n15.Название альбомов, содержащих наименьшее количество треков:')
name_album_mintrack = connection.execute("""
    SELECT distinct a.name
    FROM albums as a
    LEFT JOIN track_list as tl on tl.id_album = a.id
    WHERE tl.id_album in (
        SELECT id_album
        FROM track_list
        GROUP BY id_album
        HAVING count(id) = (
            SELECT count(id)
            FROM track_list
            GROUP BY id_album
            ORDER BY count
            limit 1
        )
    )
    ORDER BY a.name
   """).fetchall()
print(name_album_mintrack)