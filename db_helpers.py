from pymongo import MongoClient
import const_helper

def manager_connection_to_db (db_quary):
    def connect():
        try:
            client = MongoClient(const_helper.MONGO_URI)  
            db = client['admin']   
            
            not_been_answered_clients = db_quary(db)

            client.close()
            return not_been_answered_clients
        
        except:
            print('Ошибка при запросе к базе')
    return connect

@manager_connection_to_db
def get_clients(db):
    clients = db['clients']
    products = db['products']
    categories_product = db['categoriesproducts']

    data_for_message = []
    not_been_answered_clients = list(clients.find({'products.isBeenAnswered': False}))
    for client in not_been_answered_clients:
        client_data_for_message = {
            '_id': str(client['_id']),
            'name': client['name'],
            'contact': client['contact'],
            'products': []
        }
        for product in client['products']:
            product_id = product['product']
            client_product = products.find_one({'_id': product_id})

            category_id = client_product['category']
            category = categories_product.find_one({'_id': category_id})

            client_data_for_message['products'].append({
                'price': client_product['price'],
                'category_name': category['name']
            })

        data_for_message.append(client_data_for_message)
        

    return data_for_message

@manager_connection_to_db
def answer_client(db, client_contact):
    # запросс в базу для изменения поля isAnswer
    # поле назодится в коллекции clients чтобы ее достать нужно написать db['clients']
    # Найти клиента нужно по полю contact, оно для каждого клиента уникально
    # как сделать запросс в базу данных mongoDb для изменения одного поля у конкретного документапри помощи py спроси у chatGpt или поищи в интернете
    clients = db['clients']