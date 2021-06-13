import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://postgres:#########@localhost:5432/base_test1')
connection = engine.connect()

# Название и год выхода альбомов, вышедших в 2018 году;
print('\n1.Название и год выхода альбомов, вышедших в 2018 году:')
sel = connection.execute("""
    SELECT name 
    FROM albums 
    WHERE extract( year from date ) = 2018
    """).fetchall()
print(sel)

print('\n2.Название и продолжительность самого длительного трека:')
track = connection.execute("""
    SELECT name, duration
    FROM track_list
    ORDER BY duration DESC
    LIMIT 1
    """).fetchall()
print(track)

print('\n3.Название треков, продолжительность которых не менее 3,5 минуты:')
track_limit_duration = connection.execute("""
    SELECT name, duration
    FROM track_list
    WHERE duration > '00:03:30'
    ORDER BY duration DESC
    """).fetchall()
print(track_limit_duration)

print('\n4.Названия сборников, вышедших в период с 2018 по 2020 год включительно:')

name_collections_18_20 = connection.execute("""
    SELECT name
    FROM collections
    WHERE (extract( year from date ) >= 2018) AND (extract( year from date ) <= 2020)    
    """).fetchall()
print(name_collections_18_20)

print('\n5.Исполнители, чье имя состоит из 1 слова:')
name_groups = connection.execute("""
    SELECT name
    FROM groups
    where not name like '%% %%'
    """).fetchall()
print(name_groups)

print('\n6.Название треков, которые содержат слово "мой"/"my":')
name_tracks_my = connection.execute("""
    SELECT name
    FROM track_list
    where name like '%%мой%%'
    """).fetchall()
print(name_tracks_my)




