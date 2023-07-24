import MySQLdb
from flask import Flask, render_template,request,jsonify
from weather import main as get_weather
import mysql.connector
# import streamlit as st

app = Flask(__name__, template_folder='template')


def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='sys'
    )


@app.route('/',methods =['GET','POST'])
def index():
    data =None
    if request.method == 'POST':
        city=request.form['cityName']
        state=request.form['cityName']
        country=request.form['cityName']
        data =get_weather(city,state,country)
    return render_template('index1.html',data=data)

@app.route('/weather', methods=['GET','DELETE'])
def get_all_details():
    city=request.form['cityName']
    state=request.form['stateName']
    country=request.form['countryName']
    try:
        data =get_weather(city,state,country)
        if request.method == 'DELETE':
            try:
                query="Delete from sys.practice_python where cityName=%s and stateName=%s and countryName=%s"
                conn=create_connection()
                cursor=conn.cursor()
                cursor.execute(query,(city,state,country))
                conn.commit()
                return jsonify({'message':'Successfully deleted the weather details'}),201
            except MySQLdb.Error as e:
                return jsonify({'message':'DB Connection is not Successful'}),500
            finally:
                cursor.close()
                conn.close()
        else:
            return jsonify(data)
    except IndexError:
        return "No Data Available for selected Combination"

@app.route('/weather/api', methods=['GET','POST'])
def get_all_details1():
    args = request.args
    city=args.get('cityName')
    state=args.get('stateName')
    country=args.get('countryName')
    try:
        data =get_weather(city,state,country)
        if request.method == 'POST':
            try:
                query = "Insert into sys.practice_python(cityName,stateName,countryName,description,humidity,main,temperature,pressure) " \
                        "values(%s,%s,%s,%s,%s,%s,%s,%s)"
                conn=create_connection()
                cursor=conn.cursor()
                cursor.execute(query,(city,state,country,data.description,data.humidity,data.main,data.temperature,data.pressure))
                conn.commit()
                return jsonify({'message': 'weather details added successfully'}), 201
            except MySQLdb.Error as e:
                return jsonify({'error': 'Failed to insert data into the database.'}), 500
            finally:
                cursor.close()
                conn.close()
        else:
            return jsonify(data)
    except IndexError:
        return "No Data Available for selected Combination"



@app.route('/weather/api1/<cityName>/<stateName>/<countryName>', methods=['GET','PUT','POST'])
def get_all_details2(cityName,stateName,countryName):
    try:
        data =get_weather(cityName,stateName,countryName)
        if request.method == 'PUT':
            try:
                query = "update sys.practice_python SET description=%s , humidity=%s , main=%s , " \
                        "temperature=%s , pressure=%s where trim(cityName)=%s and trim(stateName)=%s and trim(countryName)=%s "
                conn=create_connection()
                cursor=conn.cursor()
                cursor.execute(query,(data.description,data.humidity,data.main,data.temperature,data.pressure,cityName,stateName,countryName))
                conn.commit()
                return jsonify({'message': 'weather details updated successfully'}), 201
            except MySQLdb.Error as e:
                return jsonify({'error': 'Failed to update the weather details .'}), 500
            finally:
                cursor.close()
                conn.close()
        elif request.method == 'POST':
            try:
                query1 = "Insert into sys.practice_python(cityName,stateName,countryName) " \
                        "values(%s,%s,%s)"
                conn=create_connection()
                cursor=conn.cursor()
                cursor.execute(query1,(cityName,stateName,countryName))
                conn.commit()
                return jsonify({'message':'Loaded Data Successfully'}),201
            except MySQLdb.Error as e:
                return jsonify({'message':'Failed to Load Data'}),500
            finally:
                cursor.close()
                conn.close()
        else:
            return jsonify(data)
    except IndexError:
        return "No Data Available for selected Combination"

@app.route("/getdetails",methods=['GET'])
def get_details_from_table():
    try:
        resp=request.get_json()
        if not resp:
            return jsonify({'message': 'JSON data not found in the request.'}), 400

        if not isinstance(resp, list):
            return jsonify({'message': 'JSON data must be a list of dictionaries.'}), 400
        data=[]
        for i in range(len(resp)):
            query="select * from sys.practice_python where cityName=%s and stateName=%s and countryName=%s"
            conn=create_connection()
            cursor=conn.cursor()
            cursor.execute(query,(resp[i].get('cityName'),resp[i].get('stateName'),resp[i].get('countryName')))
            result = cursor.fetchall()
            data.extend([{'id':wd[0],'cityName':wd[1],'stateName':wd[2],'countryName':wd[3],'humidity':wd[5],'main':wd[6],'temperature':wd[7],'pressure':wd[8]} for wd in result])
            # for wd in result:
            #     data.append({'id':wd[0],'cityName':wd[1],'stateName':wd[2],'countryName':wd[3],'humidity':wd[5],'main':wd[6],'temperature':wd[7],'pressure':wd[8]})
            conn.commit()
        return jsonify(data),200
    except Exception as e:
        return jsonify({'message':str(e)}),500
    finally:
        cursor.close()
        conn.close()
if __name__ == '__main__':
    app.run(debug=True)
