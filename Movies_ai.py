import pandas as pd

# Veri setini okuma
column_names = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv("reading_data/users.data", sep="\t", names=column_names)

# Film başlıklarını okuma
movie_titles = pd.read_csv("reading_data/movie_id_titles.csv")

# Veri setlerini birleştirme
df = pd.merge(df, movie_titles, on='item_id')

# Pivot tablo oluşturma
moviemat = df.pivot_table(index='user_id', columns='title', values='rating')

film_ismi=str(input("Film ismi söyleyin size benzerlerini önerelim: "))
film_sayisi=int(input("Kaç tane film önermemi istersin: "))
# Star Wars filmine verilen puanlar
film_user_ratings = moviemat[film_ismi]

# Star Wars filmiyle benzerlik hesaplama
similar_to_film = moviemat.corrwith(film_user_ratings)

# Benzerlik skorlarını DataFrame'e dönüştürme
corr_film = pd.DataFrame(similar_to_film, columns=['Correlation'])
corr_film.dropna(inplace=True)

# En çok benzeyen 10 filmi sıralama
top_similar_movies = corr_film.sort_values('Correlation', ascending=False).head(10)

# Timestamp sütununu kaldırma
df.drop(['timestamp'], axis=1, inplace=True)

# Filmlerin ortalama puanlarını hesaplama
ratings = pd.DataFrame(df.groupby('title')['rating'].mean())

# Puanları ekrana yazdırma
top_rated_movies = ratings.sort_values('rating', ascending=False).head()
#print(top_rated_movies)

#oy sayısını satır olarak ekle
ratings['rating_oy_sayisi']=pd.DataFrame(df.groupby('title')['rating'].count())
#ratings.head()
#oy sayısına göre sırala
ratings.sort_values('rating_oy_sayisi',ascending=False).head()

#en son rating oy sayısı  ekleme
corr_film=corr_film.join(ratings['rating_oy_sayisi'])
#corr_starwars.head()

en_cok_benzeyenler=corr_film[corr_film['rating_oy_sayisi']>100].sort_values('Correlation',ascending=False)

benzeyenlerin_title = '\n'.join(en_cok_benzeyenler.index[1:film_sayisi+1])
print("\n=================================\n\n")
print(benzeyenlerin_title)
print("\n\n=================================\n\n\n\n\n")
