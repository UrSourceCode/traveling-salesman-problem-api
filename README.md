# Travelling Salesman Problem dengan Genetic Algorithm

## Anggota Kelompok
| NRP        | Nama                            |
|------------|---------------------------------|
| 5025201013 | Adifa Widyadhani Chanda D'layla |
| 5025201050 | Elshe Erviana Angely            |
| 5025201248 | Fajar Zuhri Hadiyanto           |

## MockUp Aplikasi
![mockup](https://media.discordapp.net/attachments/940989743657795594/979921237843263538/unknown.png) <br />
Aplikasi ini dibuat dengan menggunakan framework frontend `React.js`. Data dari frontend akan diterima oleh backend menggunakan framework `Flask`. Deployment menggunakan Heroku (API) dan Vercel (front). Aplikasi dapat diakses melalui [Link Berikut](https://traveling-salesman-problem-eta.vercel.app/).

## Genetic Algorithm
Metode yang digunakan adalah dengan Genetic Algorithm. Langkah-langkah dari Travelling Salesman Problem ini adalah sebagai berikut: <br />
1. Membuat class City untuk setiap kota dengan paremeter latitude, longitude, dan id dari city
    ```py
    class City:
    def __init__(self, lon, lat, id):
        self.lon = lon # longitude
        self.lat = lat # latitude
        self.id = id

    def distance(self, city):
        distance = haversine(self.lon, self.lat, city.lon, city.lat)
        return distance # metode penghitungan dengan haversine

    def __repr__(self):
        return "(" + str(self.lon) + "," + str(self.lat) + ")"
    ```
2. Membuat population dalam `cityList` dan route yang mungkin menggunakan `random.sample`
    ```py
    def create_route(city_list):
        route = random.sample(city_list, len(city_list))
        return route
    def initial_population(pop_size, city_list):
        population = []

        for i in range(0, pop_size):
            population.append(create_route(city_list))
        return population
    ```
3. Menghitung route distance dan membuat fitness, yaitu mencari seberapa bagus rute. Rute akan diurutkan dengan `rank_routes`
    ```py
    class Fitness:
        def route_fitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.route_distance())
        return self.fitness
    ```
    Dari hal diatas dapat disimpulkan, semakin jauh jarak dari kedua titik maka nilai fitness akan semakin kecil. <br />
    ```py
    def rank_routes(population):
        fitness_results = {}
        for i in range(0, len(population)):
            fitness_results[i] = Fitness(population[i])
        return sorted(fitness_results.items(), key=lambda x: x[1].route_fitness(), reverse=True)
    ```
4. Membuat mating pool dari selection result dan population sebagai parent untuk memilih populasi berikutnya
    ```py
    def mating_pool(population, selection_results):
        matingpool = []
        for i in range(0, len(selection_results)):
            index = selection_results[i]
            matingpool.append(population[index])
        return matingpool
    ```
5. Membuat breed yaitu keturunan selanjutnya dengan crossover kemudian mengumpulkannya ke dalam populasi
    ```py
    def breed_population(matingpool, elite_size):
        children = []
        length = len(matingpool) - elite_size
        pool = random.sample(matingpool, len(matingpool))

        for i in range(0, elite_size):
            children.append(matingpool[i])

        for i in range(0, length):
            child = breed(pool[i], pool[len(matingpool) - i - 1])
            children.append(child)
        return children
    ```
6. Melakukan mutasi pada populasi untuk menjelajah rute yang baru
    ```py
    def mutate_population(population, mutation_rate):
        mutated_pop = []

        for ind in range(0, len(population)):
            mutated_ind = mutate(population[ind], mutation_rate)
            mutated_pop.append(mutated_ind)
        return mutated_pop
    ```
7. Mengulangi proses hingga menemukan rute dengan jarak paling pendek

## Penghitungan Jarak pada Map Menggunakan Haversine Formula
Haversine Formula merupakan sebuah persamaan dalam navigasi dengan cara memberikan jarak radius (lingkaran besar) antara dua titik pada permukaan bola (bumi) berdasarkan latitude dan longitude. (Sumber: [Movable](https://www.movable-type.co.uk/scripts/latlong.html)). <br />
Formula yang digunakan dalam project ini adalah sebagai berikut:
```py
from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r
```

## Pembuatan Aplikasi
Aplikasi ini dibuat menggunakan framework `Python` yaitu `Flask` dan `React.js`. Komunikasi antara frontend dengan backend dilakukan dengan API. Web depan akan mengirimkan data dalam bentuk `json` kemudian akan dikomputasi oleh backend. Data yang diterima oleh backend adalah id dan koordinat. <br />
```py
from flask import Flask, request, jsonify
from flask_cors import CORS
from genetics_algorithm import ga, City

app = Flask(__name__)

CORS(app)


@app.route('/tsp', methods=["POST"])
```
Method `POST` akan mengirimkan data yang telah dikomputasi backend kepada frontend sehingga dapat menampilkan rute secara sirkular. Output yang dikirimkan adalah:
```py
output = {
    "distances": distances,
    "total_distance": distance,
    "id_list": id_list
}
print(output)
return jsonify(output)
```