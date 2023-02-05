from flask import Flask, jsonify, request, render_template

# Antiga DB -> 
carros = []

app = Flask(__name__)


# http://127.0.0.1:5000
# Rotas ---------------------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

@app.route('/cadastro', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')

@app.route('/update/<string:modelo>/<string:ano>', methods=['GET'])
def update(modelo, ano):
    for carro in carros:
        if modelo == carro['modelo'] and ano == carro['ano']:
            print(carro['status'])
            return render_template('update.html', data=carro)        
    return render_template('update.html', data={})

# GET request to retrieve all carros
@app.route('/carros', methods=['GET'])
def get_carros():
    if not carros:
        return jsonify({'message':'No cars founded in server'}), 404
    return jsonify({'carros': carros}), 200

# GET request to retrieve one car
@app.route('/carros/<string:modelo>/<string:ano>', methods=['GET'])
def get_carro(modelo, ano):
    for carro in carros:
        if modelo == carro['modelo'] and ano == carro['ano']:
            return render_template('car.html', data=carro)
    return jsonify({'message':'carro not found'}), 404

# POST request to add a new carro with data of the new carro on a json file
@app.route('/carros', methods=['POST'])
def add_carro():
    if not request.is_json:
        return jsonify({'message':'body is not a json'}), 415
    
    data = request.get_json()

    if not data or not all(key in data for key in ('modelo','marca', 'ano', 'observacoes', 'valor', 'status')):
        return jsonify({'message':'bad request'}), 400
    
    id = 1
    
    if len(carros) > 0:
        id = carros[-1]['id'] + 1

    c = {'id':id, 'image':'https://autoentusiastas.com.br/ae/wp-content/uploads/2016/01/Novo-Jetta-Highline-9-1140x720.jpg'}

    c.update(data)

    carros.append(c) 

    return jsonify({'carro': c}), 201

# PUT request to update a carro
@app.route('/carros/<int:id>', methods=['PUT'])
def update_carro(id):
    if not request.is_json:
        return jsonify({'message':'body is not a json'}), 415

    data = request.get_json()

    if not data or not all(key in data for key in ('modelo','marca', 'ano', 'observacoes', 'valor', 'status')):
        return jsonify({'message':'bad request'}), 400

    for i,carro in enumerate(carros):
        if carro['id'] == id:
            c = {'id':id, 'image':'https://autoentusiastas.com.br/ae/wp-content/uploads/2016/01/Novo-Jetta-Highline-9-1140x720.jpg'}
            c.update(data)
            carros[i] = c
            return jsonify({'carro': carros[i]}),200
            
    return jsonify({'message':'carro not found'}), 404

# DELETE request to delete a carro
@app.route('/carros/<int:id>', methods=['DELETE'])
def delete_carro(id):
    for i,carro in enumerate(carros):
        if carro['id'] == id:
            del carros[i]   
            return jsonify({'message': 'carro deleted'}),200
    return jsonify({'message':'carro not found'}), 404

# ---------------------------------------------------------------------------------------------------------

app.run(debug=True)