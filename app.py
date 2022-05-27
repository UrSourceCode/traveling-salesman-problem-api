from flask import Flask, request, jsonify
from flask_cors import CORS
from genetics_algorithm import ga, City

app = Flask(__name__)

CORS(app)


@app.route('/tsp', methods=["POST"])
def do_tsp():
    input_json = request.get_json(force=True)
    print(input_json)

    city_list = []

    for i in range(0, len(input_json)):
        city_list.append(
            City.City(id=input_json[i]["id"], lon=input_json[i]["coordinate"][0], lat=input_json[i]["coordinate"][1]))

    iteration_map = {
        0: 50,
        4: 100,
        8: 170,
        12: 400,
        25: 900
    }

    num_of_generation = iteration_map[max([i for i in iteration_map.keys() if i < len(input_json)])]

    [id_list, distance] = ga.genetic_algorithm(population=city_list, pop_size=100, elite_size=20, mutation_rate=0.01,
                                               generations=num_of_generation)

    distances = []
    for i in range(len(id_list)):
        distances.append({
            'from': id_list[i].id,
            'to': id_list[(i + 1) % len(id_list)].id,
            'distance': id_list[i].distance(id_list[(i + 1) % len(id_list)])
        })

    id_list = list(map(lambda x: x.id, id_list))

    output = {
        "distances": distances,
        "total_distance": distance,
        "id_list": id_list
    }
    print(output)
    return jsonify(output)


if __name__ == "__main__":
    app.run()
